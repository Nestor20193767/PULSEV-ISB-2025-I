
# Procesamiento de Señales Biomédicas y EMG Capacitivas: Filtros Digitales de Ultra Bajo Consumo

Este repositorio contiene la descripción e implementación de filtros digitales utilizados en señales biomédicas como EMG, ECG y EEG, incluyendo arquitecturas optimizadas para sensores electromiográficos capacitivos de ultra bajo consumo.

Además de los filtros clásicos utilizados en bioseñales, se incorpora una metodología basada en el paper:

> Roland, T., Amsuess, S., Russold, M. F., & Baumgartner, W. (2019). *Ultra-Low-Power Digital Filtering for Insulated EMG Sensing*. Sensors, 19(4), 959.

El documento diferencia claramente entre:

- **Filtros digitales clásicos**
- **Filtros IIR en punto fijo para microcontroladores**
- **Algoritmos de decisión STFT para detección de artefactos**

---

# 1. Filtro Pasa Altas (High-Pass Filter)

## Descripción

Se utiliza para eliminar la **deriva de línea de base (baseline wander)** y artefactos de movimiento de baja frecuencia.

En EMG capacitivos, el paper demuestra que los artefactos mecánicos son tan severos que la frecuencia de corte debe elevarse hasta **60 Hz** para garantizar estabilidad en prótesis mioeléctricas.

- **Frecuencias de ruido:**  
  - ECG/EEG: < 0.5–1 Hz  
  - EMG convencional: 10–20 Hz  
  - EMG capacitivo: 0–20 Hz (artefactos dinámicos)

## Sustento Científico

1. Akhbari, M., et al. (2013).  
   *A Hierarchical Method for Removal of Baseline Drift from Biomedical Signals.*

2. Roland, T., et al. (2019).  
   *Ultra-Low-Power Digital Filtering for Insulated EMG Sensing.*

---

## Implementación Normal (Punto Flotante)

```python
import numpy as np
from scipy import signal

def highpass_filter(data, cutoff=0.5, fs=1000, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high')
    return signal.filtfilt(b, a, data)
````

---

## Implementación del Paper (Punto Fijo IIR)

```python
def paper_fixed_point_highpass(data_in, a, b):
    """
    Implementación Fixed-Point basada en el paper.
    Coeficientes escalados en formato Q2.10
    """
    n = len(data_in)

    center = np.zeros(n, dtype=np.int32)
    data_out = np.zeros(n, dtype=np.int16)

    for k in range(2, n):
        center[k] = (
            a[0]*data_in[k]
            - a[1]*center[k-1]
            - a[2]*center[k-2]
        ) >> 10

        data_out[k] = (
            b[0]*center[k]
            + b[1]*center[k-1]
            + b[2]*center[k-2]
        ) >> 10

    return data_out
```

---

# 2. Filtro Pasa Bajos (Low-Pass Filter)

## Descripción

Atenúa ruido de alta frecuencia y también se utiliza como detector de envolvente tras la rectificación EMG.

En el paper aparecen dos configuraciones:

1. **531 Hz:** eliminación de ruido térmico/electromagnético
2. **3.1 Hz:** suavizado de la envolvente muscular

## Sustento Científico

1. Sharma, A., et al. (2016).
   *Modeling of EXG (ECG, EMG and EEG) non-idealities using MATLAB.*

2. Roland, T., et al. (2019).
   *Ultra-Low-Power Digital Filtering for Insulated EMG Sensing.*

---

## Implementación Normal (Punto Flotante)

```python
def lowpass_filter(data, cutoff=150, fs=1000, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq

    b, a = signal.butter(order, normal_cutoff, btype='low')

    return signal.filtfilt(b, a, data)
```

---

## Filtro de Suavizado del Paper (Punto Fijo)

```python
def paper_fixed_point_lowpass(data_in, c_scaled=1022):
    """
    c_scaled = 0.9981 * 1024 (Q1.10)
    """
    n = len(data_in)

    y = np.zeros(n, dtype=np.int32)
    out = np.zeros(n, dtype=np.int16)

    for k in range(1, n):

        y[k] = (
            (data_in[k] + y[k-1]) * c_scaled
        ) >> 10

        out[k] = y[k] >> 8

    return out
```

---

# 3. Filtro Notch / Comb (Rechaza Banda)

## Descripción

Elimina la interferencia de línea eléctrica (*Power-Line Interference*).

En Perú y muchos países americanos la frecuencia es:

* **60 Hz**
* Armónicos: 120 Hz, 180 Hz

El paper propone un filtro Butterworth de ancho 5 Hz para tolerar fluctuaciones de red eléctrica sin introducir inestabilidad.

## Sustento Científico

1. Piskorowski, J. (2012).
   *Powerline interference rejection from sEMG signal using notch filter with transient suppression.*

2. Roland, T., et al. (2019).
   *Ultra-Low-Power Digital Filtering for Insulated EMG Sensing.*

---

## Implementación Normal (Scipy)

```python
def notch_filter(data, f0=60.0, fs=1000, Q=30):

    b, a = signal.iirnotch(f0, Q, fs)

    return signal.filtfilt(b, a, data)
```

---

## Implementación Fixed-Point del Paper

```python
def paper_fixed_point_comb(data_in, a, b):

    n = len(data_in)

    center = np.zeros(n, dtype=np.int32)
    data_out = np.zeros(n, dtype=np.int16)

    for k in range(400, n):

        center_val = (
            a[0]*data_in[k]
            - a[200]*center[k-200]
            - a[400]*center[k-400]
        ) >> 10

        center[k] = center_val

        out_val = (
            b[0]*center[k]
            + b[200]*center[k-200]
            + b[400]*center[k-400]
        ) >> 10

        data_out[k] = np.clip(out_val, -32768, 32767)

    return data_out
```

---

# 4. Filtro Pasa Banda (Band-Pass Filter)

## Descripción

Permite aislar la banda fisiológica de interés eliminando simultáneamente componentes de baja y alta frecuencia.

Aplicaciones típicas:

* ECG: extracción QRS
* EEG: ritmos neuronales
* EMG: activación muscular

## Frecuencias de interés

* ECG: 0.5–100 Hz
* EEG: 0.5–40 Hz
* EMG: 20–500 Hz

## Sustento Científico

Jirapong, P., et al. (2025).
*High-Order Universal Filter for Bio-Signal Processing Applications.*

---

## Implementación en Python

```python
def bandpass_filter(data,
                    lowcut=0.5,
                    highcut=40.0,
                    fs=1000,
                    order=5):

    nyq = 0.5 * fs

    low = lowcut / nyq
    high = highcut / nyq

    b, a = signal.butter(
        order,
        [low, high],
        btype='band'
    )

    return signal.filtfilt(b, a, data)
```

---

# 5. Filtro Adaptativo (Adaptive Filter)

## Descripción

Los filtros adaptativos ajustan dinámicamente sus coeficientes para cancelar artefactos no estacionarios.

Son particularmente útiles cuando:

* El espectro del ruido se superpone con la señal
* Existen artefactos mecánicos variables
* El movimiento del usuario cambia continuamente

## Sustento Científico

Xu, L., et al. (2022).
*Motion-artifact reduction in capacitive heart-rate measurements by adaptive filtering.*

---

## Implementación LMS Simplificada

```python
def adaptive_lms_filter(signal_in,
                        noise_ref,
                        mu=0.01,
                        order=32):

    n = len(signal_in)

    w = np.zeros(order)

    output = np.zeros(n)

    for i in range(order, n):

        x = noise_ref[i-order:i][::-1]

        y = np.dot(w, x)

        e = signal_in[i] - y

        w = w + 2 * mu * e * x

        output[i] = e

    return output
```

---

# 6. Anexo: Algoritmo de Decisión STFT

## Descripción

El paper introduce un algoritmo basado en **Transformada de Fourier de Corto Tiempo (STFT)** para distinguir:

* Contracciones musculares reales
* Artefactos mecánicos violentos

La STFT NO forma parte de los filtros digitales principales.

Es un bloque independiente de decisión.

La lógica consiste en:

1. Calcular el espectro actual
2. Compararlo contra una contracción de referencia
3. Medir la diferencia espectral
4. Desactivar temporalmente la prótesis si la diferencia excede un umbral

---

## Implementación en Python

```python
from scipy.signal import stft

def stft_decision_algorithm(signal_window,
                            reference_spectrum,
                            fs=1000,
                            threshold=500):

    f, t, Zxx = stft(
        signal_window,
        fs,
        nperseg=128,
        noverlap=64
    )

    current_spectrum = np.mean(
        np.abs(Zxx),
        axis=1
    )

    difference_sum = np.sum(
        np.abs(current_spectrum - reference_spectrum)
    )

    if difference_sum > threshold:
        return "ARTEFACTO: Motor Desactivado"

    return "CONTRACCIÓN: Motor Activado"
```

---

# Bibliografía

1. Akhbari, M., et al. (2013).
   *A Hierarchical Method for Removal of Baseline Drift from Biomedical Signals.*

2. Sharma, A., et al. (2016).
   *Modeling of EXG (ECG, EMG and EEG) non-idealities using MATLAB.*

3. Piskorowski, J. (2012).
   *Powerline interference rejection from sEMG signal using notch filter with transient suppression.*

4. Jirapong, P., et al. (2025).
   *High-Order Universal Filter for Bio-Signal Processing Applications.*

5. Xu, L., et al. (2022).
   *Motion-artifact reduction in capacitive heart-rate measurements by adaptive filtering.*

6. Roland, T., Amsuess, S., Russold, M. F., & Baumgartner, W. (2019).
   *Ultra-Low-Power Digital Filtering for Insulated EMG Sensing. Sensors, 19(4), 959.*




