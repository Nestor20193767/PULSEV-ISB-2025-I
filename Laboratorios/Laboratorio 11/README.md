
# Adquisición de ECG para análisis de recuperación autonómica post carga cognitiva

## Descripción del proyecto

Este repositorio contiene el avance del proyecto orientado al análisis de la recuperación autonómica posterior a una tarea de carga cognitiva en estudiantes universitarios, utilizando señales de electrocardiografía (ECG) y métricas de variabilidad de la frecuencia cardíaca (HRV).

En este avance se realizó una adquisición piloto con **3 participantes**. Cada participante fue evaluado en tres fases consecutivas:

1. **Reposo basal**
2. **Tarea cognitiva tipo 2-back**
3. **Recuperación fisiológica**

Además, antes del inicio del protocolo se aplicó la **Escala de Estrés Percibido PSS-10** como medida subjetiva del estrés percibido.

> **Nota:** Este avance se enfoca únicamente en la adquisición de datos y en la documentación del protocolo experimental. El procesamiento de señales, la detección de picos R, el cálculo de intervalos R-R y la extracción de métricas HRV serán desarrollados en una etapa posterior.

---

## Objetivo del avance

Realizar una primera adquisición piloto de señales ECG en estudiantes universitarios, siguiendo un protocolo experimental estructurado que permita registrar la actividad cardíaca durante reposo basal, carga cognitiva y recuperación fisiológica.

### Objetivos específicos

* Implementar el protocolo de adquisición de ECG.
* Registrar ECG continuo durante las tres fases experimentales.
* Aplicar la escala PSS-10 antes de la adquisición.
* Aplicar una tarea cognitiva tipo 2-back.
* Registrar el desempeño de la tarea cognitiva.
* Aplicar NASA-TLX al finalizar la tarea cognitiva.
* Verificar la calidad inicial de la señal ECG.
* Organizar los datos para su posterior procesamiento.

---

## Participantes

La adquisición piloto fue realizada en **3 estudiantes universitarios**.

### Criterios de inclusión

* Estudiantes universitarios entre 18 y 30 años.
* Ritmo cardíaco sinusal normal.
* Sin medicación que altere la frecuencia cardíaca.

### Criterios de exclusión

* Antecedentes de arritmias cardíacas.
* Uso de marcapasos.
* Tratamiento con psicofármacos.
* Trastornos activos de ansiedad o depresión.

### Registro de participantes

| Participante | Basal     | Tarea cognitiva | Recuperación | PSS-10   | NASA-TLX |
| ------------ | --------- | --------------- | ------------ | -------- | -------- |
| P01          | Realizado | Realizado       | Realizado    | Aplicado | Aplicado |
| P02          | Realizado | Realizado       | Realizado    | Aplicado | Aplicado |
| P03          | Realizado | Realizado       | Realizado    | Aplicado | Aplicado |

> Los participantes fueron identificados mediante códigos anónimos para proteger su identidad.

---

## Equipamiento utilizado

La adquisición de señales fisiológicas se realizó utilizando:

* Sistema **BITalino**.
* Sensor de **ECG de una derivación**.
* Electrodos desechables **Ag/AgCl**.
* Software **OpenSignals** para visualización y almacenamiento de datos.

---

## Configuración de electrodos

Los electrodos fueron colocados siguiendo una configuración de tres derivaciones:

| Electrodo        | Ubicación        |
| ---------------- | ---------------- |
| Positivo (+)     | Hombro izquierdo |
| Negativo (-)     | Hombro derecho   |
| Referencia / GND | Cresta ilíaca    |

### Imagen sugerida

Agregar aquí una imagen o esquema de la colocación de electrodos:

```markdown
![Colocación de electrodos](docs/images/electrode_placement.png)
```

Ruta sugerida del archivo:

```bash
docs/images/electrode_placement.png
```

---

## Protocolo experimental

El protocolo se desarrolló en una única sesión experimental con registro continuo de ECG durante tres fases consecutivas.

### Resumen del protocolo

| Fase   |                Condición | Duración | Descripción                                                                   |
| ------ | -----------------------: | -------: | ----------------------------------------------------------------------------- |
| Fase 1 |             Reposo basal |    5 min | El participante permanece sentado, en silencio y sin movimientos innecesarios |
| Fase 2 |          Carga cognitiva |    5 min | El participante realiza una tarea cognitiva tipo 2-back                       |
| Fase 3 | Recuperación fisiológica |    5 min | El participante permanece sentado en reposo pasivo después de la tarea        |

### Diagrama del protocolo

Agregar aquí una línea de tiempo del protocolo:

```markdown
![Línea de tiempo del protocolo](docs/images/protocol_timeline.png)
```

Ruta sugerida:

```bash
docs/images/protocol_timeline.png
```

Ejemplo de línea de tiempo:

```text
PSS-10 → ECG basal 5 min → ECG + tarea 2-back 5 min → NASA-TLX → ECG recuperación 5 min
```

---

## Fase 1: Reposo basal

Durante la fase basal, el participante permaneció sentado durante 5 minutos en un ambiente silencioso y controlado.

Indicaciones dadas al participante:

* Evitar movimientos innecesarios.
* No conversar durante el registro.
* No utilizar dispositivos electrónicos.
* Mantener una postura cómoda y estable.

El objetivo de esta fase fue obtener una línea base fisiológica para comparar los cambios producidos durante la tarea cognitiva y durante la recuperación.

### Señal sugerida para agregar

Agregar una imagen de ejemplo de la señal ECG basal:

```markdown
![ECG basal](figures/ecg_basal_example.png)
```

Ruta sugerida:

```bash
figures/ecg_basal_example.png
```

---

## Fase 2: Tarea cognitiva 2-back

Durante la segunda fase, el participante realizó una tarea cognitiva tipo **N-back**, específicamente una tarea **2-back**, durante 5 minutos.

En esta tarea, el participante debía identificar si el estímulo actual coincidía con el presentado dos posiciones antes en la secuencia.

Durante toda esta fase se mantuvo el registro continuo de ECG.

Al finalizar la tarea cognitiva, el participante completó el cuestionario **NASA-TLX**, utilizado para evaluar la carga cognitiva percibida durante la actividad.

### Variables asociadas a esta fase

* Señal ECG durante carga cognitiva.
* Accuracy de la tarea 2-back.
* Puntaje total NASA-TLX.

### Señales e imágenes sugeridas

Agregar una imagen de ejemplo de la señal ECG durante la tarea cognitiva:

```markdown
![ECG durante tarea cognitiva](figures/ecg_cognitive_task_example.png)
```

Agregar una captura o esquema de la tarea 2-back:

```markdown
![Tarea cognitiva 2-back](docs/images/nback_task_screenshot.png)
```

Rutas sugeridas:

```bash
figures/ecg_cognitive_task_example.png
docs/images/nback_task_screenshot.png
```

---

## Fase 3: Recuperación fisiológica

Después de finalizar la tarea cognitiva, el participante permaneció sentado en reposo pasivo durante 5 minutos.

Durante esta fase se continuó registrando ECG con el objetivo de analizar la recuperación autonómica posterior al esfuerzo cognitivo.

Esta etapa permitirá evaluar posteriormente si las métricas de HRV retornan hacia valores cercanos al estado basal.

### Señal sugerida para agregar

Agregar una imagen de ejemplo de la señal ECG durante recuperación:

```markdown
![ECG durante recuperación](figures/ecg_recovery_example.png)
```

Ruta sugerida:

```bash
figures/ecg_recovery_example.png
```

---

## Cuestionarios aplicados

### Escala de Estrés Percibido PSS-10

Antes de iniciar la adquisición, cada participante completó la **Escala de Estrés Percibido PSS-10**.

Este cuestionario fue aplicado para obtener una medida subjetiva del estrés percibido durante el último mes. El puntaje total podrá ser utilizado posteriormente como variable complementaria en el análisis de la recuperación autonómica.

### ¿Dónde colocar el formulario PSS-10?

Se recomienda guardar el formulario en la carpeta:

```bash
docs/forms/pss10_form.pdf
```

También se puede agregar el enlace al formulario digital:

```markdown
[PSS-10 - Formulario aplicado](PEGAR_AQUI_LINK_DEL_GOOGLE_FORMS)
```

### Recomendación para GitHub

Para el README se recomienda colocar únicamente:

* Nombre del instrumento.
* Objetivo del instrumento.
* Momento de aplicación.
* Link al formulario.
* Ruta al PDF del formulario.

No se recomienda colocar todas las preguntas directamente en el README, ya que lo haría demasiado extenso. Es mejor subir el PDF en la carpeta `docs/forms/` o colocar el link del Google Forms.

> **Importante:** Verificar que el formulario usado corresponda realmente a la versión PSS-10. Si se utiliza una escala de 14 ítems, se debe nombrar como PSS-14 y no como PSS-10.

### NASA-TLX

Después de la tarea cognitiva 2-back, cada participante completó el cuestionario **NASA-TLX**, utilizado para evaluar la carga cognitiva percibida.

Se recomienda guardar el formulario en:

```bash
docs/forms/nasa_tlx_form.pdf
```

Y enlazarlo en el README:

```markdown
[NASA-TLX - Formulario aplicado](docs/forms/nasa_tlx_form.pdf)
```

---

## Variables registradas

Para cada participante se registraron o se planea registrar las siguientes variables:

| Variable                      | Descripción                                                 |
| ----------------------------- | ----------------------------------------------------------- |
| ID del participante           | Código anónimo del participante, por ejemplo P01, P02 o P03 |
| Edad                          | Edad del participante                                       |
| Sexo                          | Sexo reportado por el participante                          |
| Puntaje PSS-10                | Estrés percibido antes de la adquisición                    |
| Señal ECG cruda               | Señal registrada con BITalino/OpenSignals                   |
| Intervalos R-R                | Intervalos entre picos R detectados                         |
| RMSSD basal                   | Métrica HRV durante reposo basal                            |
| RMSSD durante carga cognitiva | Métrica HRV durante tarea 2-back                            |
| RMSSD durante recuperación    | Métrica HRV durante reposo posterior                        |
| Accuracy 2-back               | Desempeño del participante en la tarea cognitiva            |
| Puntaje NASA-TLX              | Carga cognitiva percibida                                   |

---

## Control de calidad de la señal

Antes del inicio de cada sesión se verificó:

* Correcta adhesión de los electrodos.
* Presencia clara de complejos QRS.
* Ausencia de ruido excesivo.
* Ausencia de pérdida significativa de señal.
* Continuidad del registro durante las tres fases.

Los registros con artefactos excesivos o pérdida significativa de señal deberán ser descartados del análisis posterior.

### Imagen sugerida para control de calidad

Agregar una imagen donde se observe una señal ECG clara con complejos QRS identificables:

```markdown
![Control de calidad ECG](figures/ecg_quality_check.png)
```

Ruta sugerida:

```bash
figures/ecg_quality_check.png
```

---

## Organización del repositorio

La estructura sugerida del repositorio es la siguiente:

```bash
project/
│
├── README.md
│
├── data/
│   ├── raw/
│   │   ├── P01/
│   │   │   ├── basal/
│   │   │   ├── cognitive_task/
│   │   │   └── recovery/
│   │   │
│   │   ├── P02/
│   │   │   ├── basal/
│   │   │   ├── cognitive_task/
│   │   │   └── recovery/
│   │   │
│   │   └── P03/
│   │       ├── basal/
│   │       ├── cognitive_task/
│   │       └── recovery/
│   │
│   ├── processed/
│   │   ├── rr_intervals/
│   │   └── hrv_metrics/
│   │
│   └── metadata/
│       └── participants_metadata.csv
│
├── docs/
│   ├── protocol/
│   │   └── acquisition_protocol.pdf
│   │
│   ├── forms/
│   │   ├── pss10_form.pdf
│   │   └── nasa_tlx_form.pdf
│   │
│   └── images/
│       ├── electrode_placement.png
│       ├── protocol_timeline.png
│       └── nback_task_screenshot.png
│
├── figures/
│   ├── ecg_basal_example.png
│   ├── ecg_cognitive_task_example.png
│   ├── ecg_recovery_example.png
│   ├── ecg_quality_check.png
│   └── hrv_rmssd_preview.png
│
├── notebooks/
│   └── 01_signal_preview.ipynb
│
├── scripts/
│   ├── preprocessing.py
│   ├── r_peak_detection.py
│   └── hrv_analysis.py
│
└── results/
    ├── tables/
    └── plots/
```

---

## Ubicación sugerida de archivos

### Señales crudas

Las señales crudas exportadas desde OpenSignals deben colocarse en:

```bash
data/raw/P01/basal/
data/raw/P01/cognitive_task/
data/raw/P01/recovery/
```

Ejemplo de nombres de archivo:

```bash
data/raw/P01/basal/P01_basal.txt
data/raw/P01/cognitive_task/P01_2back.txt
data/raw/P01/recovery/P01_recovery.txt
```

Repetir la misma estructura para P02 y P03.

---

### Señales procesadas

Los datos procesados, como intervalos R-R o métricas HRV, deben colocarse en:

```bash
data/processed/rr_intervals/
data/processed/hrv_metrics/
```

Ejemplo:

```bash
data/processed/rr_intervals/P01_rr_intervals.csv
data/processed/hrv_metrics/P01_hrv_metrics.csv
```

---

### Imágenes del protocolo

Las imágenes relacionadas con el diseño experimental deben colocarse en:

```bash
docs/images/
```

Ejemplo:

```bash
docs/images/electrode_placement.png
docs/images/protocol_timeline.png
docs/images/nback_task_screenshot.png
```

---

### Figuras de señales

Las figuras generadas a partir de las señales deben colocarse en:

```bash
figures/
```

Ejemplo:

```bash
figures/ecg_basal_example.png
figures/ecg_cognitive_task_example.png
figures/ecg_recovery_example.png
figures/ecg_quality_check.png
```

---

### Formularios

Los formularios aplicados deben colocarse en:

```bash
docs/forms/
```

Ejemplo:

```bash
docs/forms/pss10_form.pdf
docs/forms/nasa_tlx_form.pdf
```

Si el formulario PSS-10 se aplicó mediante Google Forms, colocar también el link en esta sección:

```markdown
[PSS-10 - Google Forms](PEGAR_AQUI_LINK_DEL_GOOGLE_FORMS)
```

---

## Avance actual

En este avance se completaron las siguientes actividades:

* [x] Definición del protocolo experimental.
* [x] Preparación del sistema de adquisición ECG.
* [x] Colocación de electrodos según configuración definida.
* [x] Adquisición piloto en 3 participantes.
* [x] Registro ECG durante reposo basal.
* [x] Registro ECG durante tarea cognitiva 2-back.
* [x] Registro ECG durante recuperación fisiológica.
* [x] Aplicación del PSS-10.
* [x] Aplicación del NASA-TLX.
* [x] Verificación inicial de calidad de señal.
* [ ] Preprocesamiento de señales ECG.
* [ ] Detección de picos R.
* [ ] Cálculo de intervalos R-R.
* [ ] Extracción de métricas HRV.
* [ ] Análisis comparativo entre fases.

---

## Próximos pasos

Los próximos pasos del proyecto serán:

1. Organizar los archivos crudos por participante y fase.
2. Visualizar las señales ECG registradas.
3. Realizar el preprocesamiento de la señal ECG.
4. Detectar complejos QRS y picos R.
5. Calcular intervalos R-R.
6. Extraer métricas HRV, principalmente RMSSD.
7. Comparar las métricas entre basal, tarea cognitiva y recuperación.
8. Relacionar los resultados fisiológicos con el puntaje PSS-10.
9. Relacionar los resultados fisiológicos con el puntaje NASA-TLX.
10. Evaluar la recuperación autonómica posterior a la tarea cognitiva.

---

## Consideraciones éticas y de privacidad

Los datos deben ser almacenados de forma anonimizada. Cada participante será identificado mediante un código, por ejemplo P01, P02 o P03.

No se deben subir a un repositorio público:

* Nombres de participantes.
* Correos electrónicos.
* Respuestas individuales identificables.
* Datos clínicos sensibles.
* Formularios con información personal.
* Archivos que permitan identificar directamente a un participante.

Si el repositorio es público, se recomienda subir únicamente datos anonimizados o ejemplos representativos. Los datos completos deben mantenerse en almacenamiento privado.

---

## Estado del proyecto

```text
[x] Protocolo experimental definido
[x] Adquisición piloto realizada en 3 participantes
[x] PSS-10 aplicado
[x] NASA-TLX aplicado
[x] Señales ECG adquiridas
[ ] Preprocesamiento de señales
[ ] Detección de picos R
[ ] Extracción de intervalos R-R
[ ] Cálculo de métricas HRV
[ ] Análisis comparativo entre fases
```

---

## Referencias

* Cohen, S., Kamarck, T., & Mermelstein, R. (1983). A global measure of perceived stress. *Journal of Health and Social Behavior, 24*(4), 385–396.
* Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX: Results of empirical and theoretical research. *Advances in Psychology, 52*, 139–183.
* Shaffer, F., & Ginsberg, J. P. (2017). An overview of heart rate variability metrics and norms. *Frontiers in Public Health, 5*, 258.
