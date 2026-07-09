# ============================================================
# APP HRV - RECUPERACIÓN AUTONÓMICA POST CARGA COGNITIVA
# Streamlit App
# ============================================================

import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import joblib

from PIL import Image
from scipy.signal import butter, filtfilt, find_peaks
from scipy.stats import skew, kurtosis


# ============================================================
# RUTAS GENERALES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "07_modelo_local_MLP_recuperacion.joblib"
)

ICON_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "icono_app.jpeg"
)

WINDOW_SEC = 30
STEP_SEC = 15
RECOVERY_THRESHOLD_DEFAULT = 60


# ============================================================
# CONFIGURACIÓN VISUAL
# ============================================================

if os.path.exists(ICON_PATH):
    page_icon = Image.open(ICON_PATH)
else:
    page_icon = "❤️"

st.set_page_config(
    page_title="HRV Recovery App",
    page_icon=page_icon,
    layout="wide"
)


# ============================================================
# FUNCIONES DE LECTURA Y PROCESAMIENTO ECG
# ============================================================

def read_numeric_file(file, ecg_col_index=-1):
    """
    Lee archivo .txt, .csv o .tsv subido desde Streamlit.
    Acepta separadores por espacios, tabs, comas o punto y coma.
    """

    df = pd.read_csv(
        file,
        comment="#",
        header=None,
        sep=r"[\s,;]+",
        engine="python"
    )

    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.dropna(axis=1, how="all")

    if df.shape[1] == 0:
        raise ValueError("No se encontraron columnas numéricas en el archivo.")

    if ecg_col_index == -1:
        signal = df.iloc[:, -1].dropna().values
    else:
        signal = df.iloc[:, int(ecg_col_index)].dropna().values

    if len(signal) == 0:
        raise ValueError("La columna seleccionada no contiene datos válidos.")

    return signal.astype(float)


def bandpass_filter(x, fs, low=5, high=20, order=3):
    """
    Filtro pasa banda para resaltar el complejo QRS.
    """

    x = np.asarray(x, dtype=float)

    nyq = fs / 2
    high = min(high, nyq * 0.8)

    b, a = butter(order, [low / nyq, high / nyq], btype="band")
    y = filtfilt(b, a, x)

    return y


def zscore(x):
    return (x - np.nanmean(x)) / (np.nanstd(x) + 1e-8)


def detect_r_peaks(ecg, fs, prominence=0.8):
    """
    Detección robusta de picos R para ECG con posible polaridad invertida.

    Estrategia:
    1. Filtra ECG para resaltar QRS.
    2. Usa la envolvente absoluta para detectar latidos.
    3. Refina cada latido buscando el máximo absoluto local.
    4. Ajusta la polaridad solo para graficar los picos hacia arriba.
    """

    ecg = np.asarray(ecg, dtype=float)
    ecg = ecg - np.nanmedian(ecg)

    # Filtrado QRS
    filtered = bandpass_filter(ecg, fs, low=5, high=20, order=3)
    filtered_z = zscore(filtered)

    # Envolvente absoluta: útil aunque el QRS sea positivo o negativo
    envelope = np.abs(filtered_z)

    # Suavizado corto de la envolvente
    smooth_win = max(1, int(0.08 * fs))  # 80 ms
    kernel = np.ones(smooth_win) / smooth_win
    envelope_smooth = np.convolve(envelope, kernel, mode="same")

    # Distancia mínima más fisiológica
    # 0.45 s permite hasta aprox. 133 bpm
    min_distance = int(0.45 * fs)

    # Umbral robusto basado en mediana + MAD
    med = np.median(envelope_smooth)
    mad = np.median(np.abs(envelope_smooth - med)) + 1e-8
    height_threshold = med + 3.0 * mad

    candidate_peaks, _ = find_peaks(
        envelope_smooth,
        distance=min_distance,
        height=height_threshold
    )

    duration_sec = len(ecg) / fs
    min_expected_beats = duration_sec * 40 / 60

    # Si detecta muy pocos, relaja el criterio
    if len(candidate_peaks) < min_expected_beats:
        candidate_peaks, _ = find_peaks(
            envelope_smooth,
            distance=min_distance,
            prominence=prominence
        )

    # Refinamiento: buscar máximo absoluto cerca del candidato
    search_radius = int(0.08 * fs)  # ±80 ms
    refined_peaks = []

    for peak in candidate_peaks:
        start = max(0, peak - search_radius)
        end = min(len(filtered_z), peak + search_radius + 1)

        local_segment = filtered_z[start:end]

        if len(local_segment) == 0:
            continue

        local_idx = np.argmax(np.abs(local_segment))
        refined_peak = start + local_idx
        refined_peaks.append(refined_peak)

    refined_peaks = np.array(sorted(set(refined_peaks)), dtype=int)

    # Eliminar duplicados cercanos conservando el de mayor amplitud absoluta
    if len(refined_peaks) > 1:
        cleaned_peaks = []

        for peak in refined_peaks:
            if len(cleaned_peaks) == 0:
                cleaned_peaks.append(peak)
            else:
                last_peak = cleaned_peaks[-1]

                if peak - last_peak < min_distance:
                    if abs(filtered_z[peak]) > abs(filtered_z[last_peak]):
                        cleaned_peaks[-1] = peak
                else:
                    cleaned_peaks.append(peak)

        refined_peaks = np.array(cleaned_peaks, dtype=int)

    # Ajustar polaridad solo para visualización
    if len(refined_peaks) > 0:
        median_peak_value = np.median(filtered_z[refined_peaks])

        if median_peak_value < 0:
            filtered_for_plot = -filtered_z
        else:
            filtered_for_plot = filtered_z
    else:
        filtered_for_plot = filtered_z

    return refined_peaks, filtered_for_plot


def compute_window_features(ecg_filtered, peaks, fs, start_sec, end_sec):
    """
    Calcula features HRV y estadísticos por ventana.
    """

    peak_times = peaks / fs

    mask_peaks = (peak_times >= start_sec) & (peak_times < end_sec)
    peaks_win_sec = peak_times[mask_peaks]

    if len(peaks_win_sec) < 5:
        return None

    rr_ms = np.diff(peaks_win_sec) * 1000

    # Filtro fisiológico simple de intervalos RR
    rr_ms = rr_ms[(rr_ms >= 300) & (rr_ms <= 2000)]

    if len(rr_ms) < 4:
        return None

    diff_rr = np.diff(rr_ms)
    hr_inst = 60000 / rr_ms

    start_idx = int(start_sec * fs)
    end_idx = int(end_sec * fs)
    segment = ecg_filtered[start_idx:end_idx]

    if len(segment) == 0:
        return None

    features = {
        "HR_mean": np.mean(hr_inst),
        "HR_min": np.min(hr_inst),
        "HR_max": np.max(hr_inst),

        "RR_mean": np.mean(rr_ms),
        "RR_median": np.median(rr_ms),

        "SDNN": np.std(rr_ms, ddof=1),
        "RMSSD": np.sqrt(np.mean(diff_rr ** 2)),
        "pNN50": np.mean(np.abs(diff_rr) > 50) * 100,

        "NN_count": len(rr_ms),

        "ECG_mean": np.mean(segment),
        "ECG_std": np.std(segment),
        "ECG_rms": np.sqrt(np.mean(segment ** 2)),
        "ECG_ptp": np.ptp(segment),
        "ECG_energy": np.sum(segment ** 2) / len(segment),
        "ECG_skew": skew(segment),
        "ECG_kurtosis": kurtosis(segment)
    }

    return features


def extract_features_from_signal(
    ecg,
    participant,
    state,
    fs,
    window_sec=30,
    step_sec=15
):
    """
    Extrae features HRV por ventanas desde una señal ECG.
    """

    peaks, filtered = detect_r_peaks(ecg, fs)

    duration_sec = len(ecg) / fs
    rows = []
    window_id = 0

    for start_sec in np.arange(0, duration_sec - window_sec + 1, step_sec):

        end_sec = start_sec + window_sec
        window_id += 1

        feats = compute_window_features(
            ecg_filtered=filtered,
            peaks=peaks,
            fs=fs,
            start_sec=start_sec,
            end_sec=end_sec
        )

        if feats is None:
            continue

        row = {
            "participant": participant,
            "state": state,
            "window_id": window_id,
            "window_start_sec": start_sec,
            "window_end_sec": end_sec,
            "duration_file_sec": duration_sec,
            "n_peaks_total": len(peaks),
            "synthetic": False
        }

        row.update(feats)
        rows.append(row)

    return pd.DataFrame(rows), peaks, filtered


# ============================================================
# FUNCIONES DE RECUPERACIÓN
# ============================================================

def add_baseline_relative_features(df):
    """
    Agrega deltas y ratios respecto al basal promedio del participante.
    """

    df = df.copy()

    baseline_df = df[df["state"] == "basal"]

    if baseline_df.empty:
        return df

    baseline_features = [
        "HR_mean",
        "RR_mean",
        "SDNN",
        "RMSSD",
        "pNN50"
    ]

    baseline_means = baseline_df.groupby("participant")[baseline_features].mean()

    for feat in baseline_features:

        delta_values = []
        ratio_values = []

        for _, row in df.iterrows():

            participant = row["participant"]

            if participant in baseline_means.index:

                base_value = baseline_means.loc[participant, feat]
                current_value = row[feat]

                delta = current_value - base_value
                ratio = current_value / base_value if base_value != 0 else np.nan

            else:
                delta = np.nan
                ratio = np.nan

            delta_values.append(delta)
            ratio_values.append(ratio)

        df[f"{feat}_delta_basal"] = delta_values
        df[f"{feat}_ratio_basal"] = ratio_values

    return df


def safe_recovery_percent(value_rec, value_base, value_cog, direction="increase"):
    """
    Calcula porcentaje de recuperación hacia basal.
    """

    eps = 1e-8

    if direction == "increase":
        denom = value_base - value_cog

        if abs(denom) < eps:
            return np.nan

        return ((value_rec - value_cog) / denom) * 100

    if direction == "decrease":
        denom = value_cog - value_base

        if abs(denom) < eps:
            return np.nan

        return ((value_cog - value_rec) / denom) * 100

    raise ValueError("direction debe ser 'increase' o 'decrease'")


def create_recovery_dataset(features_df, threshold=60):
    """
    Usa basal y cognitivo como referencia.
    Etiqueta solo las ventanas de recuperación.
    """

    rows = []

    for participant, df_p in features_df.groupby("participant"):

        basal = df_p[df_p["state"] == "basal"]
        cog = df_p[df_p["state"] == "cognitivo"]
        rec = df_p[df_p["state"] == "recuperacion"]

        if basal.empty or cog.empty or rec.empty:
            continue

        base_mean = basal[["HR_mean", "RR_mean", "SDNN", "RMSSD", "pNN50"]].mean()
        cog_mean = cog[["HR_mean", "RR_mean", "SDNN", "RMSSD", "pNN50"]].mean()

        for _, row in rec.iterrows():

            hr_rec = safe_recovery_percent(
                row["HR_mean"],
                base_mean["HR_mean"],
                cog_mean["HR_mean"],
                direction="decrease"
            )

            rr_rec = safe_recovery_percent(
                row["RR_mean"],
                base_mean["RR_mean"],
                cog_mean["RR_mean"],
                direction="increase"
            )

            sdnn_rec = safe_recovery_percent(
                row["SDNN"],
                base_mean["SDNN"],
                cog_mean["SDNN"],
                direction="increase"
            )

            rmssd_rec = safe_recovery_percent(
                row["RMSSD"],
                base_mean["RMSSD"],
                cog_mean["RMSSD"],
                direction="increase"
            )

            pnn50_rec = safe_recovery_percent(
                row["pNN50"],
                base_mean["pNN50"],
                cog_mean["pNN50"],
                direction="increase"
            )

            rec_values = {
                "HR_recovery_pct": hr_rec,
                "RR_recovery_pct": rr_rec,
                "SDNN_recovery_pct": sdnn_rec,
                "RMSSD_recovery_pct": rmssd_rec,
                "pNN50_recovery_pct": pnn50_rec
            }

            for k, v in rec_values.items():
                if pd.notna(v):
                    rec_values[k] = np.clip(v, 0, 150)

            weights = {
                "RMSSD_recovery_pct": 0.40,
                "HR_recovery_pct": 0.25,
                "SDNN_recovery_pct": 0.20,
                "RR_recovery_pct": 0.15
            }

            weighted_sum = 0
            weight_total = 0

            for feat, w in weights.items():

                val = rec_values[feat]

                if pd.notna(val):
                    weighted_sum += w * val
                    weight_total += w

            recovery_score = weighted_sum / weight_total if weight_total > 0 else np.nan

            new_row = row.copy()

            for k, v in rec_values.items():
                new_row[k] = v

            new_row["recovery_score"] = recovery_score

            if pd.isna(recovery_score):
                new_row["recovery_label_rule"] = np.nan
            elif recovery_score >= threshold:
                new_row["recovery_label_rule"] = "recuperado"
            else:
                new_row["recovery_label_rule"] = "no_recuperado"

            rows.append(new_row)

    recovery_df = pd.DataFrame(rows)

    if recovery_df.empty:
        return recovery_df

    recovery_df = recovery_df.dropna(subset=["recovery_label_rule"])

    return recovery_df


# ============================================================
# FUNCIONES PSS
# ============================================================

def interpret_pss(score, version):
    """
    Interpretación descriptiva del PSS.
    No corresponde a diagnóstico clínico.
    """

    if score is None:
        return "Pendiente"

    if version == "PSS-10":

        if score <= 13:
            return "Estrés percibido bajo"

        if score <= 26:
            return "Estrés percibido moderado"

        return "Estrés percibido alto"

    if version == "PSS-14":

        if score <= 18:
            return "Estrés percibido bajo"

        if score <= 37:
            return "Estrés percibido moderado"

        return "Estrés percibido alto"

    return "No interpretable"


def get_pss_items(version):
    """
    Preguntas tipo PSS. Si tu curso usa una versión oficial específica,
    puedes reemplazar estos textos por los del formulario usado.
    """

    if version == "PSS-10":
        items = [
            "¿Con qué frecuencia te has sentido afectado/a por algo inesperado?",
            "¿Con qué frecuencia has sentido que no podías controlar cosas importantes?",
            "¿Con qué frecuencia te has sentido nervioso/a o estresado/a?",
            "¿Con qué frecuencia has sentido confianza para manejar problemas personales?",
            "¿Con qué frecuencia has sentido que las cosas iban bien?",
            "¿Con qué frecuencia has sentido que no podías afrontar tus pendientes?",
            "¿Con qué frecuencia has podido controlar dificultades de tu vida?",
            "¿Con qué frecuencia has sentido que tenías todo bajo control?",
            "¿Con qué frecuencia te has molestado por cosas fuera de tu control?",
            "¿Con qué frecuencia has sentido que las dificultades se acumulaban demasiado?"
        ]

        reverse_items = [3, 4, 6, 7]

    else:
        items = [
            "¿Con qué frecuencia te has sentido afectado/a por algo inesperado?",
            "¿Con qué frecuencia has sentido que no podías controlar cosas importantes?",
            "¿Con qué frecuencia te has sentido nervioso/a o estresado/a?",
            "¿Con qué frecuencia has manejado exitosamente problemas irritantes?",
            "¿Con qué frecuencia has sentido que afrontabas bien los cambios?",
            "¿Con qué frecuencia has sentido confianza para resolver problemas?",
            "¿Con qué frecuencia has sentido que las cosas iban bien?",
            "¿Con qué frecuencia has sentido que no podías afrontar tus pendientes?",
            "¿Con qué frecuencia has podido controlar dificultades de tu vida?",
            "¿Con qué frecuencia has sentido que tenías todo bajo control?",
            "¿Con qué frecuencia te has molestado por cosas fuera de tu control?",
            "¿Con qué frecuencia has pensado en cosas pendientes?",
            "¿Con qué frecuencia has podido controlar cómo usas tu tiempo?",
            "¿Con qué frecuencia has sentido que las dificultades se acumulaban demasiado?"
        ]

        reverse_items = [3, 4, 5, 6, 8, 9, 12]

    return items, reverse_items


def calculate_pss_score(responses, reverse_items):
    """
    Calcula puntaje PSS.
    Respuestas:
    0 = Nunca
    1 = Casi nunca
    2 = A veces
    3 = Bastante frecuente
    4 = Muy frecuente
    """

    score = 0

    for i, value in enumerate(responses):
        if i in reverse_items:
            score += 4 - value
        else:
            score += value

    return score


def render_pss_questionnaire(version):
    """
    Renderiza la encuesta PSS y devuelve score e interpretación.
    No deja respuestas por defecto.
    """

    items, reverse_items = get_pss_items(version)

    options = {
        "Nunca": 0,
        "Casi nunca": 1,
        "A veces": 2,
        "Bastante frecuente": 3,
        "Muy frecuente": 4
    }

    responses = []
    unanswered = 0

    st.subheader(f"Encuesta {version}")

    st.caption(
        "Responde considerando cómo te has sentido durante el último mes. "
        "El puntaje se usa solo como contexto del estrés percibido."
    )

    for i, question in enumerate(items, start=1):
        answer = st.radio(
            f"{i}. {question}",
            list(options.keys()),
            index=None,
            horizontal=True,
            key=f"{version}_q{i}"
        )

        if answer is None:
            unanswered += 1
            responses.append(None)
        else:
            responses.append(options[answer])

    if unanswered > 0:
        st.warning(f"Faltan {unanswered} pregunta(s) por responder.")
        return None, "Pendiente"

    score = calculate_pss_score(responses, reverse_items)
    interpretation = interpret_pss(score, version)

    return score, interpretation


# ============================================================
# MODELO MLP Y COMPATIBILIDAD
# ============================================================

def majority_vote(predictions):
    """
    Votación mayoritaria para predicciones por ventana.
    """

    if len(predictions) == 0:
        return "no_evaluable"

    counts = pd.Series(predictions).value_counts()

    return counts.idxmax()


def patch_sklearn_pipeline_for_prediction(model, X_new):
    """
    Corrige problemas de compatibilidad entre versiones de scikit-learn
    al cargar pipelines entrenados en otro entorno.
    """

    if not hasattr(model, "named_steps"):
        return model

    X_values = np.asarray(X_new, dtype=float)

    for step_name, step_obj in model.named_steps.items():

        class_name = step_obj.__class__.__name__

        if class_name == "SimpleImputer":

            if not hasattr(step_obj, "_fill_dtype"):
                step_obj._fill_dtype = X_values.dtype

            if not hasattr(step_obj, "_fit_dtype"):
                step_obj._fit_dtype = X_values.dtype

    return model


@st.cache_resource
def load_model():
    """
    Carga el modelo MLP local entrenado.
    """

    if not os.path.exists(MODEL_PATH):
        return None

    return joblib.load(MODEL_PATH)


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

if os.path.exists(ICON_PATH):
    st.image(ICON_PATH, width=110)

st.title("App HRV - Recuperación autonómica post carga cognitiva")

st.markdown(
    """
    Esta aplicación procesa señales ECG registradas en tres estados:
    **basal**, **cognitivo** y **recuperación**.

    A partir de la variabilidad de la frecuencia cardíaca, calcula un
    **recovery score** y aplica un modelo MLP exploratorio para clasificar la
    recuperación autonómica como **recuperado** o **no recuperado**.
    """
)

st.warning(
    "Esta herramienta corresponde a un estudio piloto académico. "
    "Los resultados no constituyen diagnóstico clínico."
)


# ============================================================
# PANEL LATERAL
# ============================================================

st.sidebar.header("Configuración")

participant = st.sidebar.text_input(
    "Código del participante",
    value="PX"
)

fs = st.sidebar.number_input(
    "Frecuencia de muestreo ECG (Hz)",
    min_value=50,
    max_value=5000,
    value=1000,
    step=50
)

ecg_col_index = st.sidebar.number_input(
    "Índice de columna ECG (-1 = última columna)",
    value=-1,
    step=1
)

recovery_threshold = st.sidebar.slider(
    "Umbral de recuperación (%)",
    min_value=40,
    max_value=80,
    value=RECOVERY_THRESHOLD_DEFAULT,
    step=5
)

st.sidebar.header("Encuesta de estrés")

pss_version = st.sidebar.selectbox(
    "Versión de encuesta",
    ["PSS-10", "PSS-14"]
)

use_questionnaire = st.sidebar.checkbox(
    "Responder encuesta en la app",
    value=True
)

if not use_questionnaire:
    max_pss = 40 if pss_version == "PSS-10" else 56

    pss_score = st.sidebar.number_input(
        f"Puntaje {pss_version}",
        min_value=0,
        max_value=max_pss,
        value=0,
        step=1
    )

    pss_interpretation = interpret_pss(pss_score, pss_version)

else:
    pss_score = None
    pss_interpretation = "Pendiente"


# ============================================================
# ENCUESTA PSS
# ============================================================

st.header("1. Encuesta de estrés percibido")

if use_questionnaire:
    with st.expander("Responder encuesta PSS", expanded=True):
        pss_score, pss_interpretation = render_pss_questionnaire(pss_version)

col_pss_1, col_pss_2 = st.columns(2)

col_pss_1.metric(
    f"Puntaje {pss_version}",
    "-" if pss_score is None else pss_score
)

col_pss_2.metric(
    "Interpretación",
    pss_interpretation
)


# ============================================================
# CARGA DE ARCHIVOS
# ============================================================

st.header("2. Carga de señales ECG")

col1, col2, col3 = st.columns(3)

with col1:
    basal_file = st.file_uploader(
        "Subir ECG basal",
        type=["txt", "csv", "tsv"],
        key="basal"
    )

with col2:
    cognitive_file = st.file_uploader(
        "Subir ECG cognitivo",
        type=["txt", "csv", "tsv"],
        key="cognitivo"
    )

with col3:
    recovery_file = st.file_uploader(
        "Subir ECG recuperación",
        type=["txt", "csv", "tsv"],
        key="recuperacion"
    )


# ============================================================
# PROCESAMIENTO
# ============================================================

if st.button("Procesar señales y predecir"):

    if basal_file is None or cognitive_file is None or recovery_file is None:

        st.error("Debes subir las tres señales: basal, cognitivo y recuperación.")

    elif pss_score is None:

        st.error("Debes completar la encuesta PSS antes de procesar las señales.")

    else:

        try:
            with st.spinner("Procesando señales ECG..."):

                ecg_basal = read_numeric_file(
                    basal_file,
                    ecg_col_index=int(ecg_col_index)
                )

                ecg_cog = read_numeric_file(
                    cognitive_file,
                    ecg_col_index=int(ecg_col_index)
                )

                ecg_rec = read_numeric_file(
                    recovery_file,
                    ecg_col_index=int(ecg_col_index)
                )

                df_basal, peaks_basal, filt_basal = extract_features_from_signal(
                    ecg_basal,
                    participant=participant,
                    state="basal",
                    fs=int(fs),
                    window_sec=WINDOW_SEC,
                    step_sec=STEP_SEC
                )

                df_cog, peaks_cog, filt_cog = extract_features_from_signal(
                    ecg_cog,
                    participant=participant,
                    state="cognitivo",
                    fs=int(fs),
                    window_sec=WINDOW_SEC,
                    step_sec=STEP_SEC
                )

                df_rec, peaks_rec, filt_rec = extract_features_from_signal(
                    ecg_rec,
                    participant=participant,
                    state="recuperacion",
                    fs=int(fs),
                    window_sec=WINDOW_SEC,
                    step_sec=STEP_SEC
                )

                if df_basal.empty or df_cog.empty or df_rec.empty:
                    st.error(
                        "No se pudieron extraer ventanas válidas de una o más señales. "
                        "Revisa la frecuencia de muestreo, la columna ECG o la calidad de la señal."
                    )
                    st.stop()

                all_features_df = pd.concat(
                    [df_basal, df_cog, df_rec],
                    ignore_index=True
                )

                all_features_df = add_baseline_relative_features(all_features_df)

                recovery_df = create_recovery_dataset(
                    all_features_df,
                    threshold=recovery_threshold
                )

            st.success("Procesamiento completado.")

            # ====================================================
            # RESUMEN DE PROCESAMIENTO
            # ====================================================

            st.header("3. Resumen de procesamiento")

            summary = (
                all_features_df
                .groupby("state")
                .agg(
                    n_ventanas=("window_id", "count"),
                    duracion_min=("duration_file_sec", lambda x: np.mean(x) / 60),
                    HR_mean=("HR_mean", "mean"),
                    RR_mean=("RR_mean", "mean"),
                    SDNN=("SDNN", "mean"),
                    RMSSD=("RMSSD", "mean"),
                    pNN50=("pNN50", "mean")
                )
                .reset_index()
            )

            st.dataframe(summary, use_container_width=True)

            # ====================================================
            # CONTROL VISUAL PICOS R
            # ====================================================

            st.subheader("Control visual de picos R en recuperación")

            fig, ax = plt.subplots(figsize=(12, 4))

            max_sec = min(10, len(filt_rec) / int(fs))
            t = np.arange(len(filt_rec)) / int(fs)
            mask = t <= max_sec
            peaks_plot = peaks_rec[(peaks_rec / int(fs)) <= max_sec]

            ax.plot(
                t[mask],
                filt_rec[mask],
                label="ECG recuperación filtrado"
            )

            ax.plot(
                peaks_plot / int(fs),
                filt_rec[peaks_plot],
                "o",
                label="Picos R"
            )

            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Amplitud normalizada")
            ax.set_title("Picos R detectados en la señal de recuperación")
            ax.grid(True)
            ax.legend()

            st.pyplot(fig)

            # ====================================================
            # RECOVERY SCORE
            # ====================================================

            st.header("4. Recovery score")

            if recovery_df.empty:

                st.error("No se pudieron calcular ventanas de recuperación válidas.")

            else:

                recovery_score_mean = recovery_df["recovery_score"].mean()
                recovery_score_median = recovery_df["recovery_score"].median()

                rule_label = (
                    "recuperado"
                    if recovery_score_mean >= recovery_threshold
                    else "no_recuperado"
                )

                col_a, col_b, col_c = st.columns(3)

                col_a.metric(
                    "Recovery score promedio",
                    f"{recovery_score_mean:.1f} %"
                )

                col_b.metric(
                    "Recovery score mediano",
                    f"{recovery_score_median:.1f} %"
                )

                col_c.metric(
                    "Clasificación por regla",
                    rule_label
                )

                cols_to_show = [
                    "window_id",
                    "window_start_sec",
                    "window_end_sec",
                    "HR_mean",
                    "RR_mean",
                    "SDNN",
                    "RMSSD",
                    "pNN50",
                    "HR_recovery_pct",
                    "RR_recovery_pct",
                    "SDNN_recovery_pct",
                    "RMSSD_recovery_pct",
                    "recovery_score",
                    "recovery_label_rule"
                ]

                st.dataframe(
                    recovery_df[cols_to_show],
                    use_container_width=True
                )

                # ====================================================
                # PREDICCIÓN MLP
                # ====================================================

                st.header("5. Predicción MLP")

                mlp_label = "modelo_no_disponible"
                recovery_df["MLP_prediction"] = "no_disponible"

                model_pack = load_model()

                if model_pack is None:

                    st.warning(
                        "No se encontró el modelo local MLP. "
                        "Coloca el archivo "
                        "`07_modelo_local_MLP_recuperacion.joblib` "
                        "en la carpeta `models/`."
                    )

                else:

                    model = model_pack["model"]
                    model_features = model_pack["features"]
                    label_encoder = model_pack.get("label_encoder", None)

                    missing_features = [
                        c for c in model_features
                        if c not in recovery_df.columns
                    ]

                    if len(missing_features) > 0:

                        st.error(f"Faltan features para el modelo: {missing_features}")
                        mlp_label = "no_evaluable"

                    else:

                        X_new = recovery_df[model_features].replace(
                            [np.inf, -np.inf],
                            np.nan
                        )

                        X_new = X_new.astype(float)

                        model = patch_sklearn_pipeline_for_prediction(model, X_new)

                        pred_encoded = model.predict(X_new)

                        if label_encoder is not None:
                            pred_text = label_encoder.inverse_transform(pred_encoded)
                        else:
                            pred_text = pred_encoded

                        recovery_df["MLP_prediction"] = pred_text

                        mlp_label = majority_vote(pred_text)

                        pred_counts_df = (
                            pd.Series(pred_text, name="clase")
                            .value_counts()
                            .reset_index()
                        )

                        pred_counts_df.columns = ["clase", "n"]

                        col_m1, col_m2 = st.columns(2)

                        col_m1.metric(
                            "Predicción global MLP",
                            mlp_label
                        )

                        col_m2.metric(
                            "Ventanas evaluadas",
                            len(pred_text)
                        )

                        st.write("Distribución de predicciones por ventana:")
                        st.dataframe(pred_counts_df, use_container_width=True)

                        st.dataframe(
                            recovery_df[
                                [
                                    "window_id",
                                    "recovery_score",
                                    "recovery_label_rule",
                                    "MLP_prediction"
                                ]
                            ],
                            use_container_width=True
                        )

                # ====================================================
                # PSS E INTERPRETACIÓN
                # ====================================================

                st.header("6. Estrés percibido e interpretación")

                col_p1, col_p2 = st.columns(2)

                col_p1.metric(
                    f"Puntaje {pss_version}",
                    pss_score
                )

                col_p2.metric(
                    "Interpretación PSS",
                    pss_interpretation
                )

                st.subheader("Interpretación integrada")

                if rule_label == "recuperado":

                    recovery_text = (
                        "El participante muestra una recuperación autonómica adecuada "
                        "según el recovery score calculado."
                    )

                else:

                    recovery_text = (
                        "El participante muestra una recuperación autonómica incompleta "
                        "según el recovery score calculado."
                    )

                if mlp_label in ["recuperado", "no_recuperado"]:

                    mlp_text = (
                        f"La MLP exploratoria predice globalmente: **{mlp_label}**."
                    )

                else:

                    mlp_text = (
                        "La predicción MLP no estuvo disponible o no pudo evaluarse."
                    )

                st.markdown(
                    f"""
                    **Resultado fisiológico:** {recovery_text}

                    **Modelo MLP:** {mlp_text}

                    **Estrés percibido:** El puntaje {pss_version} fue **{pss_score}**,
                    interpretado de forma descriptiva como **{pss_interpretation}**.

                    **Nota:** El PSS se usa como contexto del estado percibido de estrés,
                    no como entrada del modelo. La predicción se basa en features HRV extraídas
                    de las señales ECG.
                    """
                )

                # ====================================================
                # DESCARGA DE RESULTADOS
                # ====================================================

                st.header("7. Descargar resultados")

                csv_results = recovery_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="Descargar resultados por ventana",
                    data=csv_results,
                    file_name=f"resultados_HRV_{participant}.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Ocurrió un error durante el procesamiento: {e}")