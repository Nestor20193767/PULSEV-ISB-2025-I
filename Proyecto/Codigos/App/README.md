# PulseV - Recuperación Autonómica Post Carga Cognitiva

Aplicación web desarrollada con **Streamlit** para visualizar métricas de variabilidad de la frecuencia cardíaca y clasificar de forma exploratoria la recuperación autonómica posterior a una tarea cognitiva.

## Descripción del proyecto

Este proyecto busca analizar la recuperación autonómica en estudiantes universitarios mediante el estudio de señales ECG registradas en tres fases experimentales:

1. **Basal:** registro en reposo antes de la tarea cognitiva.
2. **Tarea cognitiva:** registro durante una actividad mental demandante.
3. **Recuperación:** registro posterior a la tarea para observar el retorno fisiológico.

A partir del procesamiento offline de la señal ECG, se extraen métricas de variabilidad de la frecuencia cardíaca, conocidas como **HRV**, tales como:

- RMSSD
- SDNN
- Frecuencia cardíaca media
- Puntaje PSS-10

Estas métricas son utilizadas como entrada de la aplicación para visualizar el comportamiento fisiológico del participante y estimar su estado de recuperación autonómica.

## Objetivo de la aplicación

Desarrollar una interfaz web interactiva que permita:

- Cargar métricas HRV previamente calculadas.
- Visualizar la evolución de las métricas entre las fases basal, tarea cognitiva y recuperación.
- Calcular indicadores de recuperación fisiológica.
- Entregar una clasificación exploratoria del estado de recuperación autonómica.

## Flujo del sistema

```text
Adquisición ECG → Procesamiento HRV offline → CSV de features → App Streamlit → Clasificación
```

El procesamiento completo de la señal ECG no se realiza directamente dentro de la aplicación. En esta primera versión, la app recibe como entrada las características HRV previamente calculadas para facilitar la visualización, comparación y clasificación de los participantes.

## Input de la aplicación

La aplicación recibe un archivo CSV con las métricas HRV calculadas para cada participante y fase experimental.

### Formato esperado del archivo CSV

```csv
participante,fase,rmssd,sdnn,hr_mean,pss10_score
P01,Basal,42.1,55.3,72,18
P01,Tarea,25.4,36.2,91,18
P01,Recuperacion,39.8,50.7,76,18
P02,Basal,38.5,49.1,75,24
P02,Tarea,22.1,31.5,96,24
P02,Recuperacion,28.2,35.8,88,24
```

### Variables de entrada

| Variable | Descripción |
|---|---|
| participante | Código del participante evaluado |
| fase | Fase experimental: Basal, Tarea o Recuperacion |
| rmssd | Métrica HRV asociada a la actividad parasimpática |
| sdnn | Métrica HRV de variabilidad global |
| hr_mean | Frecuencia cardíaca media |
| pss10_score | Puntaje del cuestionario PSS-10 |

## Output de la aplicación

La aplicación entrega una clasificación exploratoria del estado de recuperación autonómica del participante.

### Clases de salida

- **Recuperación rápida**
- **Recuperación parcial**
- **Recuperación lenta**
- **No evaluable**

Además, la app muestra:

- Porcentaje de recuperación del RMSSD.
- Cambio de frecuencia cardíaca entre basal y recuperación.
- Gráficas de evolución por fase.
- Tabla de métricas por participante.
- Resumen general de clasificación.

## Arquitectura del algoritmo

La app está diseñada para representar el flujo del modelo PulseV. El modelo propuesto utiliza una arquitectura basada en redes neuronales para analizar patrones temporales en los datos fisiológicos.

La arquitectura considerada incluye:

```text
Input
↓
Reshape
↓
Conv1D
↓
Conv1D causal
↓
Attention
↓
Dense Softmax
↓
Clasificación
```

En esta versión de la aplicación, la clasificación se realiza mediante una regla exploratoria basada en la recuperación del RMSSD y el cambio de frecuencia cardíaca. En una etapa posterior, esta lógica puede ser reemplazada por el modelo entrenado exportado desde TensorFlow o Edge Impulse.

## Regla exploratoria usada

La aplicación evalúa principalmente:

```text
Recuperación RMSSD (%) = RMSSD recuperación / RMSSD basal × 100
```

También considera el cambio de frecuencia cardíaca:

```text
ΔHR = HR recuperación - HR basal
```

De forma exploratoria, se clasifica la recuperación según el grado de retorno del RMSSD hacia el valor basal y el comportamiento de la frecuencia cardíaca durante la recuperación.

## Estructura del proyecto

```text
Proyecto_HRV/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── features_hrv_demo.csv
│
└── assets/
    └── logo.png
```

## Ejecución local

Para ejecutar la aplicación en una computadora local, primero se deben instalar las dependencias:

```bash
pip install -r requirements.txt
```

Luego, se ejecuta la app con Streamlit:

```bash
streamlit run app.py
```

La aplicación se abrirá en el navegador, usualmente en la dirección:

```text
http://localhost:8501
```

## Dependencias principales

El proyecto utiliza las siguientes librerías:

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

## Consideraciones

Esta aplicación corresponde a una primera versión funcional del sistema. El procesamiento de la señal ECG se realiza de forma offline para asegurar una revisión adecuada de la calidad de señal, detección de picos R y extracción de métricas HRV.

La app se enfoca en la etapa final del flujo del proyecto:

```text
Input HRV → Visualización → Clasificación → Output
```

Por lo tanto, permite demostrar el funcionamiento general del algoritmo a partir de métricas fisiológicas ya procesadas.

## Estado actual

- App funcional en Streamlit.
- Visualización de métricas HRV.
- Carga de archivos CSV.
- Clasificación exploratoria del estado de recuperación.
- Preparada para integración futura con un modelo entrenado.