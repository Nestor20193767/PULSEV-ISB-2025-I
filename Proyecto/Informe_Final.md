# PULSEV — Informe Final del Proyecto  
### Curso: Introducción a Señales Biomédicas (ISB 2026-I)

> **Repositorio:** [PULSEV-ISB-2026-I](https://github.com/Nestor20193767/PULSEV-ISB-2026-I)  
> **Estado:** Informe final corregido con detección robusta de picos R, procesamiento local, modelo MLP exploratorio y exportación a Edge Impulse.

---

## Título

**Detección de recuperación autonómica post carga cognitiva mediante análisis de HRV en estudiantes universitarios**

---

## Resumen

La variabilidad de la frecuencia cardíaca (HRV, *Heart Rate Variability*) permite estimar de manera no invasiva la regulación del sistema nervioso autónomo a partir de los intervalos RR derivados de una señal ECG. En este proyecto se desarrolló un pipeline computacional para evaluar si un estudiante universitario recupera su estado autonómico basal después de una tarea cognitiva demandante. Para ello, se adquirieron señales ECG de tres participantes en tres condiciones secuenciales: reposo basal, carga cognitiva y recuperación. Las señales fueron procesadas en Python mediante filtrado pasa banda, detección robusta de picos R, segmentación en ventanas de 30 s con paso de 15 s y extracción de métricas HRV en el dominio temporal.

Durante el control de calidad se identificó que la detección inicial de picos R podía marcar picos secundarios en algunas señales, probablemente por la morfología bifásica o la polaridad del ECG. Por ello, se corrigió el algoritmo de detección utilizando la envolvente absoluta del complejo QRS, una distancia mínima fisiológica entre latidos y un refinamiento local por máximo absoluto. Luego de esta corrección, no se detectaron ventanas sospechosas en el control de calidad numérico.

A partir de las features HRV se calculó un **recovery score**, definido como un índice porcentual que compara el retorno de las métricas de recuperación hacia el basal individual de cada participante, tomando como referencia el cambio inducido durante la carga cognitiva. Con un umbral exploratorio de 60 %, las 55 ventanas reales de recuperación se distribuyeron en 33 ventanas recuperadas y 22 no recuperadas. Debido al tamaño reducido de la muestra, se generaron datos sintéticos únicamente en el espacio de características, no sobre la señal ECG cruda. El dataset aumentado alcanzó 220 muestras: 132 recuperadas y 88 no recuperadas.

Se entrenó una red neuronal MLP local sobre 15 features HRV y variables relativas al basal. La validación principal se realizó mediante *leave-one-subject-out* (LOSO), obteniendo un accuracy promedio de 0.528 y un F1 macro promedio de 0.412. Estos resultados evidencian una generalización limitada entre participantes, coherente con el carácter piloto del estudio y el tamaño muestral reducido (n = 3). Además, el dataset fue exportado a Edge Impulse para demostrar la viabilidad de implementación del modelo en una plataforma de aprendizaje automático embebido. En consecuencia, el resultado principal del sistema es el **recovery score fisiológico**, mientras que la predicción MLP se interpreta como apoyo exploratorio. El cuestionario PSS-14 se integra únicamente como contexto de estrés percibido y no como entrada del modelo.

---

## Palabras clave

`ECG` · `HRV` · `picos R` · `intervalos RR` · `carga cognitiva` · `recuperación autonómica` · `RMSSD` · `SDNN` · `PSS` · `MLP` · `Edge Impulse`

---

## Introducción

La carga cognitiva se relaciona con el esfuerzo mental requerido para ejecutar tareas de memoria de trabajo, atención sostenida o toma de decisiones. En estudiantes universitarios, este tipo de demanda puede generar cambios transitorios en la actividad autonómica, reflejados en el aumento de la frecuencia cardíaca y en la reducción de algunas métricas de HRV. La HRV es ampliamente utilizada como indicador indirecto del equilibrio entre la actividad simpática y parasimpática del sistema nervioso autónomo, y ha sido propuesta como una herramienta útil para estudiar estrés, recuperación fisiológica y carga mental [1]–[4].

En este contexto, una pregunta relevante no es únicamente si la carga cognitiva modifica la señal fisiológica durante la tarea, sino si el organismo logra retornar hacia su estado basal al finalizarla. Esta capacidad de recuperación puede interpretarse como un indicador de adaptabilidad autonómica. Por ello, este proyecto no se centra en clasificar las fases basal, cognitiva y recuperación, sino en estimar si la fase de recuperación evidencia un retorno fisiológico suficiente hacia el basal individual.

La solución propuesta consiste en procesar señales ECG adquiridas con BITalino, detectar los picos R, calcular intervalos RR y extraer métricas HRV por ventanas. A partir de estas métricas se construye un **recovery score**, que permite clasificar cada ventana de recuperación como `recuperado` o `no_recuperado`. Adicionalmente, se entrena una red neuronal MLP como clasificador exploratorio, y se exporta el dataset a Edge Impulse para evaluar su posible implementación en sistemas de aprendizaje automático en el borde (*edge AI*).

Dado que el estudio cuenta con solo tres participantes, sus resultados deben interpretarse como una **prueba de concepto metodológica**, no como una herramienta clínica validada. El objetivo principal es demostrar un flujo reproducible de procesamiento ECG-HRV y una forma interpretable de cuantificar recuperación autonómica post carga cognitiva.

---

## Planteamiento del problema

La evaluación del estrés académico y de la carga cognitiva suele apoyarse en cuestionarios subjetivos. Aunque estos instrumentos son útiles, no permiten observar directamente la respuesta fisiológica del sistema nervioso autónomo. Por otro lado, la señal ECG ofrece una vía objetiva y no invasiva para analizar la actividad cardiovascular y derivar métricas HRV asociadas al estrés y a la recuperación fisiológica [2], [3].

El problema abordado en este proyecto es el siguiente:

> **¿Es posible estimar, a partir de señales ECG y métricas HRV, si un estudiante universitario recupera su estado autonómico basal después de una tarea cognitiva demandante?**

Este problema presenta tres dificultades principales:

1. **Procesamiento de señal:** la detección de picos R debe ser confiable, ya que errores en los picos alteran los intervalos RR y, por tanto, todas las features HRV.
2. **Interpretación fisiológica:** las métricas HRV varían entre personas; por ello, no basta comparar valores absolutos entre participantes.
3. **Tamaño muestral reducido:** el estudio solo cuenta con tres participantes, lo que impide una validación estadística robusta y obliga a interpretar el modelo como exploratorio.

Por estas razones, se optó por una solución basada en comparación intra-sujeto: cada participante se evalúa respecto a su propio basal. Además, el puntaje PSS-14 se utiliza únicamente como contexto subjetivo del estrés percibido, sin incorporarse como entrada del modelo.

---

## Propuesta de solución

La solución implementada se organiza en etapas que van desde el protocolo de adquisición hasta el procesamiento, modelado, validación y despliegue exploratorio en Edge Impulse.

---

### 1. Protocolo de adquisición de datos

La adquisición se realizó en tres participantes: `P01`, `P02` y `P03`. El protocolo siguió una secuencia fija para reducir variaciones entre sujetos y mantener el mismo orden experimental en todos los registros.

Protocolo:

[Archivo del protocolo de adquisición](Archivos/Protocolo_Adquisicion.pdf)

#### 1.1 Encuesta PSS-14

Antes de registrar la señal ECG, cada participante respondió la encuesta **PSS-14** (*Perceived Stress Scale*), usada como medida subjetiva del estrés percibido. Este puntaje no se utilizó como entrada del modelo, sino como información contextual para interpretar el estado general del participante antes de la adquisición fisiológica.

[Formulario PSS-14 aplicado a los participantes](Archivos/PSS-14.pdf)

![Formulario PSS-14 aplicado a los participantes](Archivos/PSS14imagen.pdf)


El análisis de la encuesta se realizó mediante Python, convirtiendo las respuestas cualitativas a puntajes numéricos de 0 a 4. Los ítems positivos se invirtieron según la estructura de la PSS-14 y luego se calculó el puntaje total por participante.

```python
import pandas as pd

# Leer archivo
df = pd.read_excel("Formulario Proyecto.xlsx")

# Conversión de respuestas a puntajes
conversion = {
    "Nunca": 0,
    "Casi nunca": 1,
    "De vez en cuando": 2,
    "A menudo": 3,
    "Muy a menudo": 4,
    "Muy amenudo": 4   # por si Google Forms lo escribió así
}

# Ítems de la encuesta, todas las columnas excepto la marca temporal
items = list(df.columns[1:])

# Convertir texto a números
for col in items:
    df[col] = df[col].map(conversion)

# Ítems invertidos de la PSS-14
invertidos = [3, 4, 5, 6, 8, 9, 12]  # posiciones 4, 5, 6, 7, 9, 10 y 13

for i in invertidos:
    df[items[i]] = 4 - df[items[i]]

# Puntaje total
df["PSS_Total"] = df[items].sum(axis=1)

# Mostrar resultados
print(df[["Marca temporal", "PSS_Total"]])

# Guardar archivo con el puntaje
df.to_excel("Resultados_PSS14.xlsx", index=False)
```

El archivo generado con los puntajes fue:

```text
Resultados_PSS14.xlsx
```

**Imagen sugerida**

```markdown
![Resultados del análisis PSS-14](figures/resultados/resultados_pss14.png)
```

> Insertar una captura de la tabla generada por el código, o una tabla/resumen con el puntaje `PSS_Total` de cada participante.

#### 1.2 Configuración de electrodos ECG

La señal ECG fue registrada con BITalino y OpenSignals usando una configuración tipo **segunda derivación ECG** o **Lead II**, adecuada para resaltar el complejo QRS y facilitar la detección de picos R. Esta configuración fue seleccionada porque permite obtener una señal con morfología clara para el cálculo de intervalos RR y métricas HRV.

**Imagen sugerida**

```markdown
![Configuración de electrodos ECG en segunda derivación](figures/protocolo/configuracion_electrodos_2da_derivacion.png)
```

> Insertar la imagen de la configuración de electrodos. En el texto de la figura se puede indicar que corresponde a la segunda derivación ECG usada durante la adquisición.

#### 1.3 Toma de señales ECG

Cada participante fue evaluado en tres estados consecutivos:

| Orden | Estado | Descripción | Archivo esperado |
|---:|---|---|---|
| 1 | Basal | Registro en reposo previo a la tarea cognitiva | `PXX_basal_ECGv2.txt` |
| 2 | Cognitivo | Registro durante la prueba cognitiva 2-back | `PXX_cognitiva_ECGv2.txt` |
| 3 | Recuperación | Registro posterior a la tarea cognitiva | `PXX_recuperacion_ECGv2.txt` |

La frecuencia de muestreo utilizada fue de **1000 Hz**. Los registros se organizaron por participante y por estado para facilitar el procesamiento posterior.

#### 1.4 Prueba cognitiva 2-back

Durante la fase cognitiva, el participante realizó una tarea **2-back**, una prueba de memoria de trabajo en la que debe comparar el estímulo actual con el presentado dos posiciones antes. Esta tarea fue elegida porque incrementa la demanda atencional y de memoria de trabajo, generando una carga cognitiva controlada durante el registro ECG.

**Imagen sugerida**

```markdown
![Prueba cognitiva 2-back utilizada durante la adquisición](figures/protocolo/prueba_2back.png)
```

> Insertar una captura de la interfaz, presentación o ejemplo de la prueba 2-back usada durante la adquisición.

#### 1.5 Organización de archivos

```text
Proyecto_HRV/
├── data_raw/
│   ├── P01/
│   │   ├── P01_basal_ECGv2.txt
│   │   ├── P01_cognitiva_ECGv2.txt
│   │   └── P01_recuperacion_ECGv2.txt
│   ├── P02/
│   │   ├── P02_basal_ECGv2.h5.txt
│   │   ├── P02_cognitiva_ECGv2.h5.txt
│   │   └── P02_recuperacion_ECGv2.txt.txt
│   └── P03/
│       ├── P03_basal_ECGv2.txt
│       ├── P03_cognitiva_ECGv2.txt
│       └── P03_recuperacion_ECGv2.txt
├── figures/
│   ├── protocolo/
│   │   ├── formulario_pss14.png
│   │   ├── configuracion_electrodos_2da_derivacion.png
│   │   └── prueba_2back.png
│   └── resultados/
│       └── resultados_pss14.png
├── outputs/
├── models/
└── app.py
```

**Imagen sugerida**

```markdown
![Organización de archivos del proyecto](figures/estructura_directorios.png)
```

> Insertar una captura del explorador de archivos o del repositorio mostrando `data_raw/`, `figures/`, `outputs/`, `models/` y `app.py`.

---

### 2. Preprocesamiento ECG

El preprocesamiento incluyó:

1. Lectura flexible de archivos `.txt`, `.csv` o `.tsv`.
2. Selección de la columna ECG.
3. Filtrado pasa banda de 5–20 Hz para resaltar el complejo QRS.
4. Normalización tipo z-score.
5. Detección robusta de picos R.
6. Cálculo de intervalos RR.
7. Control de calidad visual y numérico.

Durante la revisión visual se observó que una detección basada solo en picos positivos/negativos podía seleccionar picos secundarios cercanos al QRS. Para corregirlo, se actualizó el algoritmo de detección:

- Se calculó la envolvente absoluta del ECG filtrado.
- Se suavizó la envolvente en una ventana corta.
- Se aplicó una distancia mínima entre latidos de 0.45 s.
- Se refinó cada detección buscando el máximo absoluto local en ±80 ms.
- La polaridad se ajustó solo para visualización.

Este ajuste permitió reducir falsas detecciones y estabilizar las métricas HRV.

**Imagen sugerida**

```markdown
![Control de calidad de picos R](outputs/qc_picos_R/QC_P01_recuperacion_picosR.png)
```

> Insertar una imagen de la carpeta `outputs/qc_picos_R/`, idealmente `QC_P01_recuperacion_picosR.png` o una donde se observe claramente un punto por cada complejo QRS.

---

### 3. Segmentación por ventanas

Las señales se dividieron en ventanas temporales de:

- **Tamaño de ventana:** 30 s
- **Paso:** 15 s
- **Solapamiento:** 50 %

Esta estrategia permitió aumentar el número de observaciones sin crear nuevos sujetos artificiales. Cada ventana sigue correspondiendo a una porción real de la señal ECG adquirida.

---

### 4. Extracción de features HRV

Por cada ventana se calcularon features HRV en el dominio temporal:

| Feature | Descripción |
|---|---|
| `HR_mean` | Frecuencia cardíaca media de la ventana |
| `RR_mean` | Promedio de intervalos RR |
| `SDNN` | Desviación estándar de intervalos NN |
| `RMSSD` | Raíz media cuadrática de diferencias sucesivas RR |
| `pNN50` | Porcentaje de diferencias RR sucesivas mayores a 50 ms |
| `NN_count` | Cantidad de intervalos NN válidos |

También se calcularon estadísticas de la señal ECG filtrada, como RMS, energía, desviación estándar, skewness y kurtosis. Sin embargo, para el modelo final se priorizaron las features HRV y sus variables relativas al basal, debido a su interpretación fisiológica directa.

---

### 5. Features relativas al basal

Para evitar comparaciones directas entre sujetos con basales distintos, se calcularon variables relativas al basal individual:

- `HR_mean_delta_basal`
- `RR_mean_delta_basal`
- `SDNN_delta_basal`
- `RMSSD_delta_basal`
- `pNN50_delta_basal`
- `HR_mean_ratio_basal`
- `RR_mean_ratio_basal`
- `SDNN_ratio_basal`
- `RMSSD_ratio_basal`
- `pNN50_ratio_basal`

Estas variables permiten analizar si una ventana se acerca o se aleja del estado basal propio de cada participante.

---

### 6. Recovery score

El **recovery score** fue diseñado como la salida principal del sistema. Para cada ventana de recuperación, se estimó el porcentaje de retorno hacia el basal usando como referencia el cambio entre el estado basal y el estado cognitivo.

Para features que deberían aumentar durante la recuperación, como `RMSSD`, `SDNN`, `RR_mean` y `pNN50`, se usó:

```text
recuperación (%) = (valor_recuperación - valor_cognitivo) / (valor_basal - valor_cognitivo) × 100
```

Para `HR_mean`, que normalmente debería disminuir al recuperarse, se usó la relación inversa:

```text
recuperación HR (%) = (valor_cognitivo - valor_recuperación) / (valor_cognitivo - valor_basal) × 100
```

El score final combinó las métricas con ponderaciones exploratorias:

| Métrica | Peso |
|---|---:|
| `RMSSD_recovery_pct` | 0.40 |
| `HR_recovery_pct` | 0.25 |
| `SDNN_recovery_pct` | 0.20 |
| `RR_recovery_pct` | 0.15 |

Se eligió un umbral exploratorio de 60 %:

```text
recovery_score ≥ 60 %  → recuperado
recovery_score < 60 %   → no_recuperado
```

Este umbral no representa un criterio clínico universal; fue seleccionado para este estudio piloto por su balance entre interpretación fisiológica y distribución de clases.

---

### 7. Modelo MLP local

Se entrenó una red neuronal MLP local usando `scikit-learn`. El modelo recibió 15 variables de entrada:

```text
HR_mean
RR_mean
SDNN
RMSSD
pNN50
HR_mean_delta_basal
RR_mean_delta_basal
SDNN_delta_basal
RMSSD_delta_basal
pNN50_delta_basal
HR_mean_ratio_basal
RR_mean_ratio_basal
SDNN_ratio_basal
RMSSD_ratio_basal
pNN50_ratio_basal
```

No se incluyó `recovery_score` como entrada para evitar *data leakage*, ya que esa variable se usa para definir la etiqueta. Tampoco se incluyó el puntaje PSS-14, porque se utiliza solo como contexto subjetivo.

La arquitectura local fue:

```text
SimpleImputer
↓
StandardScaler
↓
MLPClassifier
```

El modelo final fue guardado como:

```text
models/07_modelo_local_MLP_recuperacion.joblib
```

---

### 8. Aumento de datos sintéticos

Debido al número reducido de participantes, se generaron datos sintéticos únicamente en el espacio de features HRV. No se generaron señales ECG sintéticas.

La generación sintética se realizó mediante:

- bootstrap de ventanas reales,
- ruido gaussiano controlado,
- preservación de la etiqueta,
- clipping solo en datos sintéticos para evitar valores no plausibles.

Esto permitió aumentar el volumen de entrenamiento sin alterar los datos reales.

---

### 9. Validación local

La validación principal se realizó con **leave-one-subject-out** (LOSO):

```text
Fold 1: prueba con P01, entrenamiento con P02 + P03
Fold 2: prueba con P02, entrenamiento con P01 + P03
Fold 3: prueba con P03, entrenamiento con P01 + P02
```

En cada fold, los datos sintéticos se generaron únicamente a partir de los participantes de entrenamiento, nunca del participante de prueba. Esto evita fuga de información entre entrenamiento y evaluación.

---

### 10. Edge Impulse

El dataset final fue exportado a Edge Impulse con el archivo:

```text
outputs/05_dataset_edge_impulse_recuperacion.csv
```

El CSV contiene 15 features HRV y la columna `label`. En Edge Impulse se configuró:

| Configuración | Valor |
|---|---|
| Input | 15 features |
| Processing block | Flatten / Features |
| Learning block | Classification / Keras |
| Ciclos de entrenamiento | 50 |
| Learning rate | 0.0005 |
| Validación interna | 20 % |
| Clases | `recuperado`, `no_recuperado` |

Edge Impulse se utilizó principalmente para demostrar la viabilidad de implementación del clasificador en una plataforma de *edge machine learning*. La validación interna de Edge no se considera la validación principal del proyecto, porque proviene del mismo CSV y puede mezclar ventanas derivadas de los mismos participantes. Por ello, la validación principal reportada es la validación local LOSO.

**Imagen sugerida**

```markdown
![Diseño del impulse en Edge Impulse](figures/edge_impulse/impulse_design.png)
```

> Insertar captura del diseño del impulse: input de 15 features, bloque de procesamiento y clasificador.

```markdown
![Entrenamiento en Edge Impulse](figures/edge_impulse/training_output.png)
```

> Insertar captura del panel de entrenamiento con accuracy, loss, matriz de confusión, F1, RAM, Flash e inferencing time.

**Completar con los resultados finales de Edge Impulse**

```text
Accuracy interna Edge Impulse: [COMPLETAR]
Loss: [COMPLETAR]
F1 score: [COMPLETAR]
AUC: [COMPLETAR]
Inferencing time: [COMPLETAR]
RAM usage: [COMPLETAR]
Flash usage: [COMPLETAR]
```

---

### 11. Aplicación web

Se implementó una aplicación en Streamlit que permite:

1. Responder la encuesta PSS-14 dentro de la app.
2. Calcular automáticamente el puntaje PSS-14.
3. Subir las tres señales ECG.
4. Procesar la señal.
5. Visualizar picos R detectados.
6. Calcular el recovery score.
7. Mostrar la clasificación por regla.
8. Aplicar el modelo MLP local.
9. Descargar los resultados por ventana.

El PSS-14 se usa solo como contexto y no como feature del modelo.

**Imagen sugerida**

```markdown
![Interfaz de la aplicación Streamlit](figures/app/streamlit_app.png)
```

> Insertar captura general de la app funcionando.

```markdown
![Resultado recovery score y MLP](figures/app/resultados_app.png)
```

> Insertar captura donde se vea el recovery score, clasificación por regla y predicción MLP. Si hay discrepancia entre regla y MLP, indicar que el resultado principal es el recovery score y la MLP es exploratoria.

---

## Resultados

### 1. Resultados de la encuesta PSS-14

La encuesta PSS-14 permitió obtener un puntaje total de estrés percibido para cada participante antes de la adquisición ECG. Este resultado se reporta como contexto subjetivo y no se incorporó como variable de entrada al modelo MLP ni al cálculo del recovery score.

**Completar con los puntajes reales obtenidos:**

| Participante | PSS_Total | Interpretación contextual |
|---|---:|---|
| P01 | [COMPLETAR] | [Bajo / moderado / alto, según criterio usado] |
| P02 | [COMPLETAR] | [Bajo / moderado / alto, según criterio usado] |
| P03 | [COMPLETAR] | [Bajo / moderado / alto, según criterio usado] |

**Imagen sugerida**

```markdown
![Tabla de resultados PSS-14](figures/resultados/resultados_pss14.png)
```

> Insertar la captura de la tabla generada por el código o del archivo `Resultados_PSS14.xlsx`.

---

### 2. Ventanas extraídas

Luego de la corrección de picos R, se obtuvieron las siguientes ventanas válidas:

| Participante | Estado | Duración aproximada | Ventanas válidas |
|---|---|---:|---:|
| P01 | Basal | 5.04 min | 19 |
| P01 | Cognitivo | 5.08 min | 19 |
| P01 | Recuperación | 5.09 min | 19 |
| P02 | Basal | 5.10 min | 19 |
| P02 | Cognitivo | 4.39 min | 16 |
| P02 | Recuperación | 5.04 min | 19 |
| P03 | Basal | 3.71 min | 13 |
| P03 | Cognitivo | 3.93 min | 14 |
| P03 | Recuperación | 4.58 min | 17 |

En total se obtuvieron **55 ventanas reales de recuperación**.

---

### 3. Control de calidad

El control de calidad numérico no detectó ventanas sospechosas:

```text
Ventanas sospechosas: 0
```

Las frecuencias cardíacas promedio por estado se mantuvieron en rangos fisiológicos razonables:

| Participante | Basal HR_mean | Cognitivo HR_mean | Recuperación HR_mean |
|---|---:|---:|---:|
| P01 | 72.27 bpm | 75.04 bpm | 71.59 bpm |
| P02 | 78.51 bpm | 82.71 bpm | 77.18 bpm |
| P03 | 66.68 bpm | 72.81 bpm | 69.80 bpm |

Esto sugiere que la corrección en la detección de picos R permitió obtener intervalos RR más estables.

**Imagen sugerida**

```markdown
![Control de calidad de picos R corregido](outputs/qc_picos_R/QC_P01_recuperacion_picosR.png)
```

---

### 4. Distribución de clases reales

Con `RECOVERY_THRESHOLD = 60`, las 55 ventanas reales de recuperación quedaron distribuidas de la siguiente manera:

| Clase | Ventanas reales |
|---|---:|
| `recuperado` | 33 |
| `no_recuperado` | 22 |

La distribución por participante fue:

| Participante | `no_recuperado` | `recuperado` |
|---|---:|---:|
| P01 | 4 | 15 |
| P02 | 1 | 18 |
| P03 | 17 | 0 |

Esta distribución evidencia una diferencia marcada entre participantes, especialmente en P03, donde todas las ventanas de recuperación fueron clasificadas como `no_recuperado`.

---

### 5. Dataset aumentado

Se generaron tres muestras sintéticas por cada muestra real, únicamente en el espacio de características:

| Tipo de muestra | `no_recuperado` | `recuperado` |
|---|---:|---:|
| Real | 22 | 33 |
| Sintética | 66 | 99 |
| **Total** | **88** | **132** |

El dataset final para entrenamiento y Edge Impulse tuvo:

```text
220 muestras × 15 features + 1 etiqueta
```

---

### 6. Validación MLP local — LOSO

Los resultados de la validación leave-one-subject-out fueron:

| Fold | Participante de prueba | Accuracy | F1 macro | Muestras reales de prueba |
|---|---|---:|---:|---:|
| 1 | P01 | 0.789 | 0.756 | 19 |
| 2 | P02 | 0.737 | 0.424 | 19 |
| 3 | P03 | 0.059 | 0.056 | 17 |
| **Promedio** | — | **0.528** | **0.412** | — |

El modelo obtuvo buen desempeño relativo en P01 y accuracy aceptable en P02, pero falló al generalizar hacia P03. Esto se explica por la distribución de clases: P01 y P02 contienen mayoritariamente ventanas recuperadas, mientras que P03 contiene únicamente ventanas no recuperadas. Con solo tres participantes, el modelo no dispone de suficiente variabilidad interindividual para aprender patrones robustos.

**Imagen sugerida**

```markdown
![Matriz de confusión MLP LOSO](outputs/06_matriz_confusion_MLP_LOSO.png)
```

---

### 7. Interpretación de la app

En la app final, pueden aparecer casos donde el recovery score y la MLP no coinciden. Esto no debe presentarse como una falla del sistema, sino como una consecuencia esperable de trabajar con un modelo exploratorio entrenado con una muestra pequeña.

La interpretación jerárquica propuesta es:

1. **Salida principal:** recovery score y clasificación por regla.
2. **Salida secundaria:** predicción MLP exploratoria.
3. **Contexto:** puntaje PSS-14.

Cuando exista discordancia, debe priorizarse el recovery score, ya que es la métrica fisiológica definida explícitamente a partir del retorno hacia el basal.

---

## Conclusiones

- Se implementó un pipeline funcional para procesar ECG crudo, detectar picos R, extraer intervalos RR, calcular features HRV y estimar recuperación autonómica post carga cognitiva.

- La revisión visual del preprocesamiento permitió identificar errores en la detección inicial de picos R. La corrección mediante envolvente absoluta del QRS y refinamiento por máximo absoluto mejoró la estabilidad del procesamiento y eliminó ventanas sospechosas en el control de calidad numérico.

- El enfoque basado en **recovery score** fue más adecuado que una clasificación directa de estados, porque responde a la pregunta central del proyecto: si el participante recupera o no su estado autonómico tras la tarea cognitiva.

- Con el umbral exploratorio de 60 %, se obtuvo una distribución real de 33 ventanas recuperadas y 22 no recuperadas. Este umbral debe entenderse como una decisión metodológica del estudio piloto, no como un estándar clínico validado.

- El modelo MLP local alcanzó un accuracy promedio de 0.528 y un F1 macro de 0.412 en validación LOSO. Estos resultados muestran que el modelo no generaliza de forma estable entre participantes, principalmente por el tamaño muestral reducido y la distribución desigual de clases por sujeto.

- El aumento sintético se aplicó solo a features HRV y no a la señal ECG cruda, lo cual evita introducir morfologías cardíacas artificiales difíciles de validar.

- Edge Impulse permitió demostrar la viabilidad de trasladar el clasificador a una plataforma de aprendizaje automático en el borde. Sin embargo, la validación local LOSO se considera más confiable que la validación interna aleatoria de Edge para este estudio.

- El sistema final debe interpretarse como una **prueba de concepto académica y exploratoria**, no como una herramienta clínica. Para validar el enfoque sería necesario ampliar la muestra, incorporar más participantes con diferentes niveles de estrés, explorar métricas adicionales y evaluar la estabilidad del recovery score en protocolos repetidos.

---

## Limitaciones

- La muestra incluyó solo tres participantes, por lo que no es posible generalizar los resultados.
- Las ventanas solapadas aumentan observaciones, pero no equivalen a participantes independientes.
- El recovery score depende de un umbral exploratorio definido por el equipo.
- La MLP puede aprender patrones específicos de cada participante y no necesariamente patrones fisiológicos generales.
- No se incorporaron métricas HRV de frecuencia, como LF, HF o LF/HF, debido al tamaño de ventana y al alcance del proyecto.
- La app no debe ser utilizada con fines diagnósticos.

---

## Trabajo futuro

- Aumentar el número de participantes.
- Usar protocolos repetidos para evaluar confiabilidad intra-sujeto.
- Comparar distintos umbrales de recovery score.
- Incorporar análisis de frecuencia cuando existan registros más largos.
- Evaluar modelos más simples e interpretables, como regresión logística o Random Forest.
- Explorar validación externa con nuevos participantes no usados durante el desarrollo.
- Mejorar la interfaz de la app para mostrar consistencia o discordancia entre regla fisiológica y MLP.

---

## Referencias

[1] Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology. (1996). Heart rate variability: Standards of measurement, physiological interpretation and clinical use. *Circulation, 93*(5), 1043–1065. https://pubmed.ncbi.nlm.nih.gov/8598068/

[2] Shaffer, F., & Ginsberg, J. P. (2017). An overview of heart rate variability metrics and norms. *Frontiers in Public Health, 5*, 258. https://doi.org/10.3389/fpubh.2017.00258

[3] Kim, H. G., Cheon, E. J., Bai, D. S., Lee, Y. H., & Koo, B. H. (2018). Stress and heart rate variability: A meta-analysis and review of the literature. *Psychiatry Investigation, 15*(3), 235–245. https://doi.org/10.30773/pi.2017.08.17

[4] Delliaux, S., Delaforge, A., Deharo, J.-C., & Chaumet, G. (2019). Mental workload alters heart rate variability, lowering non-linear dynamics. *Frontiers in Physiology, 10*, 565. https://doi.org/10.3389/fphys.2019.00565

[5] Arutyunova, K. R., et al. (2024). Heart rate dynamics for cognitive load estimation in a realistic driving scenario. *Scientific Reports, 14*, 29090. https://doi.org/10.1038/s41598-024-79728-x

[6] Cohen, S., Kamarck, T., & Mermelstein, R. (1983). A global measure of perceived stress. *Journal of Health and Social Behavior, 24*(4), 385–396. https://www.jstor.org/stable/2136404

[7] PLUX Wireless Biosignals. (s. f.). *Getting started: BITalino electrocardiography (ECG) sensor*. https://support.pluxbiosignals.com/knowledge-base/getting-started-bitalino-electrocardiography-ecg-sensor/

[8] Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830. https://www.jmlr.org/papers/v12/pedregosa11a.html

[9] Edge Impulse. (s. f.). *Impulse design*. Edge Impulse Documentation. https://docs.edgeimpulse.com/studio/projects/impulse-design

---

## Bibliografía de autores

### Néstor Allende
Estudiante de Ingeniería Biomédica con interés en procesamiento de señales fisiológicas, análisis de datos biomédicos y aplicaciones de aprendizaje automático en salud digital. En este proyecto participó en el desarrollo del repositorio, organización del informe y procesamiento computacional.

### Ana Angulo
Estudiante de Ingeniería Biomédica con interés en instrumentación, adquisición de señales biomédicas y evaluación experimental. En este proyecto participó en el diseño del protocolo, adquisición de señales ECG y validación del procedimiento experimental.

### Luis/Bryan Loayza
Estudiante de Ingeniería Biomédica con interés en procesamiento de señales biomédicas, machine learning y desarrollo de aplicaciones interactivas. En este proyecto participó en el pipeline de HRV, cálculo del recovery score, entrenamiento MLP local, integración en Streamlit y análisis de resultados.

### Natalie Sante
Estudiante de Ingeniería Biomédica con interés en análisis fisiológico, bienestar académico y aplicaciones de biosensores. En este proyecto participó en la organización experimental, revisión de resultados y discusión de la interpretación fisiológica.

### Nataly Deledesma
Estudiante de Ingeniería Biomédica con interés en señales biomédicas, evaluación de estrés y tecnologías de monitoreo no invasivo. En este proyecto participó en la adquisición de datos, revisión del protocolo y apoyo en la documentación final.

> **Nota:** Reemplazar o ajustar estas biografías según la contribución real de cada integrante antes de entregar el informe final.
