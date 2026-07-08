# PULSEV — Informe Final del Proyecto
### Curso: Introducción a Señales Biomédicas (ISB 2026-I)

> **Repositorio:** [PULSEV-ISB-2026-I](https://github.com/Nestor20193767/PULSEV-ISB-2026-I)

---

## Título

**Detección de recuperación autonómica post carga cognitiva mediante análisis de HRV en estudiantes universitarios**

---

## Resumen

La regulación autonómica del sistema cardiovascular puede verse afectada temporalmente por tareas que exigen un alto esfuerzo mental. Este proyecto explora si es posible determinar, de manera objetiva y no invasiva, si un estudiante universitario logra recuperar su estado autonómico basal después de realizar una tarea cognitiva demandante. Para ello se adquirieron señales de electrocardiografía (ECG) de tres participantes en tres condiciones experimentales secuenciales —reposo basal, carga cognitiva y recuperación— y se construyó un pipeline computacional en Python que filtra la señal, detecta los complejos QRS, calcula los intervalos RR y segmenta cada registro en ventanas de 30 segundos con paso de 15 segundos. A partir de cada ventana se extrajeron características de variabilidad de la frecuencia cardíaca (HRV) en el dominio temporal (HR_mean, RR_mean, SDNN, RMSSD, pNN50), así como variables relativas al basal individual de cada sujeto. Con estas variables se diseñó un *recovery score*, un índice porcentual que cuantifica cuánto se revirtió el cambio fisiológico inducido por la tarea cognitiva durante la fase de recuperación. Tras un análisis de sensibilidad de umbral, se fijó un criterio exploratorio de 60 % para etiquetar cada ventana como "recuperado" o "no_recuperado". Debido al tamaño reducido de la muestra, se generaron datos sintéticos únicamente en el espacio de características (bootstrap con ruido gaussiano controlado), preservando intactos los datos reales. Con este dataset aumentado se entrenó una red neuronal MLP pequeña, validada mediante *leave-one-subject-out*, que obtuvo un accuracy promedio de 0.49 y un F1 macro de 0.41. Estos resultados evidencian que el modelo aún no generaliza de forma estable entre participantes, por lo que el sistema se presenta como un estudio piloto exploratorio: el resultado principal es el recovery_score fisiológico, mientras que la predicción de la MLP se ofrece como apoyo complementario, y el cuestionario de estrés percibido (PSS-10/PSS-14) se integra únicamente como variable contextual y no como entrada del modelo.

---

## Palabras clave

`Variabilidad de la frecuencia cardíaca (HRV)` · `Electrocardiografía (ECG)` · `Carga cognitiva` · `Sistema nervioso autónomo` · `RMSSD` · `Recovery score` · `Aprendizaje automático` · `Estudio piloto`

---

## Introducción

La carga cognitiva se define como el esfuerzo mental requerido para ejecutar tareas que demandan memoria de trabajo, razonamiento o atención sostenida. En poblaciones universitarias, la exposición reiterada a exigencias académicas y estrés puede alterar la regulación del sistema nervioso autónomo (SNA), afectando la capacidad del organismo para retornar a un estado fisiológico basal tras un esfuerzo mental [1]. Evaluar esta capacidad de recuperación es relevante tanto desde una perspectiva de salud (identificar patrones de estrés sostenido) como desde una perspectiva de ingeniería biomédica (diseñar sistemas de monitoreo no invasivo del bienestar autonómico).

La variabilidad de la frecuencia cardíaca (HRV, por sus siglas en inglés) es una herramienta ampliamente utilizada para estimar de forma indirecta la actividad del SNA a partir de los intervalos RR derivados de la señal ECG y funciona como un indicador directo de la adaptabilidad del organismo al estrés. En términos generales, una mayor HRV se asocia con una mejor flexibilidad autonómica y predominio parasimpático; cuando el estrés aumenta, la HRV disminuye (reflejado en métricas como RMSSD o SDNN), y cuando el cuerpo se recupera, debería volver a subir [2]–[4].

Este proyecto propone un pipeline computacional capaz de procesar señales ECG adquiridas en tres condiciones —basal, carga cognitiva y recuperación—, extraer características HRV, y a partir de ellas estimar un índice de recuperación autonómica. Dado que el estudio se desarrolla con una muestra reducida de tres participantes, se plantea explícitamente como un **estudio piloto y exploratorio**, orientado a validar la viabilidad metodológica del pipeline antes que a generar conclusiones clínicas generalizables.

**Objetivo general**

Diseñar e implementar un sistema de procesamiento de señales ECG y análisis de HRV que permita estimar si un estudiante universitario presenta una recuperación autonómica adecuada tras una tarea de carga cognitiva.

**Objetivos específicos**

- Adquirir y procesar señales ECG en tres condiciones experimentales (basal, carga cognitiva y recuperación) mediante filtrado, detección de picos R y cálculo de intervalos RR.
- Extraer características HRV en el dominio temporal por ventana de análisis y calcular variables relativas al estado basal individual de cada participante.
- Diseñar un índice cuantitativo (*recovery score*) que permita clasificar la recuperación autonómica como adecuada o no adecuada.
- Explorar la viabilidad de un modelo de clasificación supervisado (MLP) como apoyo a la interpretación fisiológica, evaluando su desempeño mediante validación *leave-one-subject-out*.

---

## Planteamiento del problema

Actualmente existe una dificultad concreta para evaluar de manera **objetiva** si un estudiante logra recuperar su estado autonómico basal después de una tarea cognitiva: la evaluación de la carga cognitiva se basa principalmente en métodos subjetivos [5], [6], y los estudios de HRV disponibles se han enfocado mayormente en la respuesta autonómica *durante* la tarea cognitiva, más que en el proceso de recuperación posterior [7]. La HRV ofrece una vía fisiológica no invasiva para abordar esta pregunta, pero su interpretación requiere de un pipeline de procesamiento de señal robusto y de criterios claros para traducir los cambios en las métricas HRV en una etiqueta interpretable (recuperado / no recuperado).

A este vacío metodológico se suma un vacío científico más amplio: existe poca investigación centrada específicamente en la recuperación autonómica post carga cognitiva mediante HRV [7], [8], son escasos los estudios que aborden la recuperación fisiológica y el estrés académico en poblaciones de estudiantes universitarios [8]–[10], y no se dispone de algoritmos simples y accesibles para detectar recuperación autonómica a partir de ECG y HRV. Esta carencia dificulta la detección temprana de fatiga mental y sobrecarga cognitiva, con un posible impacto en el rendimiento académico y el estrés estudiantil [6], [8].

A esta dificultad conceptual se suma una limitación práctica relevante: por restricciones de tiempo de adquisición, el estudio cuenta únicamente con registros ECG de **tres participantes**, cada uno con tres segmentos (basal, cognitivo y recuperación) de aproximadamente 5 minutos de duración —con la excepción de un participante cuyo registro fue más corto por condiciones reales de adquisición—. Este tamaño muestral impide, por diseño, alcanzar significancia estadística o generalización clínica, y obliga a plantear el proyecto como una prueba de concepto metodológica.

Antes de la adquisición fisiológica, cada participante completó una encuesta de estrés percibido (PSS-10 o PSS-14, según la versión aplicada). Esta encuesta no se utiliza como entrada de ningún modelo computacional, sino como variable contextual que permite enriquecer la interpretación de los resultados fisiológicos.

El problema central que aborda el proyecto puede resumirse así: **¿es posible, a partir de un pipeline de procesamiento de ECG y extracción de features HRV, estimar de forma objetiva si un estudiante universitario recupera su estado autonómico tras una tarea cognitiva, incluso con una muestra piloto reducida?**

---

## 💡 Propuesta de solución

Se desarrolló un sistema de análisis basado en ECG y HRV compuesto por cuatro etapas principales: (A) procesamiento de la señal ECG, (B) extracción de features HRV, (C) cálculo de un *recovery score* y clasificación recuperado/no recuperado, y (D) entrenamiento exploratorio de un modelo MLP, con proyección hacia una futura integración en una aplicación web.

### 1. Adquisición de datos

Se adquirieron señales ECG de tres participantes (P01, P02, P03) durante tres condiciones experimentales secuenciales: **basal** (reposo), **cognitivo** (durante la tarea) y **recuperación** (posterior a la tarea). La señal se registró con un sistema BITalino y electrodos ECG desechables en configuración de tres derivaciones (hombro derecho, hombro izquierdo y cresta ilíaca), usando el software OpenSignals; el front-end de adquisición se basa en el chip AD8232 [11]. Antes del protocolo, cada participante completó el cuestionario PSS-10 como línea base de estrés percibido, y al finalizar la tarea cognitiva se aplicó el cuestionario NASA-TLX para confirmar que la tarea fue percibida como demandante. Cada señal cruda se almacenó por participante y por estado en archivos `.txt`/`.csv`, organizados de la siguiente forma:

```
Proyecto_HRV/
├── data_raw/
│   ├── P01/ { basal.txt, cognitivo.txt, recuperacion.txt }
│   ├── P02/ { basal.txt, cognitivo.txt, recuperacion.txt }
│   └── P03/ { basal.txt, cognitivo.txt, recuperacion.txt }
├── metadata/
│   └── pss_scores.csv
└── outputs/
```

### 2. Preprocesamiento ECG

Las señales crudas se procesan en Python mediante un pipeline propio: lectura flexible de archivos `.txt`/`.csv`, filtrado pasa banda orientado a resaltar el complejo QRS, detección de picos R y cálculo de los intervalos RR. El pipeline incorpora control de calidad visual y numérico: gráficas de la señal filtrada con picos R marcados, resumen de duración por archivo, número de ventanas válidas por participante/estado, estimación global de frecuencia cardíaca y marcado de ventanas sospechosas por valores extremos de HR o bajo número de intervalos NN.

### 3. Segmentación por ventanas

Para incrementar el número de observaciones sin introducir participantes ficticios, cada registro se segmenta en ventanas temporales de **30 segundos con paso de 15 segundos** (50 % de solapamiento). Cada ventana es un segmento derivado de una señal real, no un sujeto adicional.

### 4. Extracción de features HRV

Por cada ventana se calculan características de HRV en el dominio temporal: `HR_mean`, `HR_min`, `HR_max`, `RR_mean`, `RR_median`, `SDNN`, `RMSSD`, `pNN50` y `NN_count`. También se exploraron features estadísticos de la señal ECG filtrada (RMS, energía, desviación estándar, skewness, kurtosis), aunque el modelo final prioriza los features HRV por su relación directa y establecida con la regulación autonómica.

### 5. Features relativos al basal

Dado que cada participante tiene un nivel fisiológico basal distinto, se calcularon variables *delta* y *ratio* respecto al basal individual (por ejemplo, `RMSSD_delta_basal`, `RMSSD_ratio_basal`, y equivalentes para HR_mean, RR_mean, SDNN y pNN50). Estas variables permiten evaluar cuánto se aleja o aproxima cada ventana al estado basal propio del sujeto, en lugar de comparar valores absolutos entre participantes distintos.

### 6. Recovery score

En lugar de clasificar cada ventana como basal/cognitivo/recuperación, el enfoque final consiste en estimar si el participante presenta una **recuperación autonómica adecuada**. El *recovery score* se calcula comparando, para cada ventana de recuperación, el grado en que las métricas HRV retornan hacia el promedio basal del propio participante, tomando como referencia el cambio observado entre el estado basal y el estado cognitivo.

- Para variables que disminuyen durante la carga cognitiva y deberían aumentar durante la recuperación (RMSSD, SDNN, RR_mean, pNN50), se aplica una lógica de recuperación por incremento hacia el basal.
- Para HR_mean, que aumenta durante la carga cognitiva y debería disminuir durante la recuperación, se aplica la lógica inversa.

El score combina principalmente `RMSSD_recovery_pct` (40 %), `HR_recovery_pct` (25 %), `SDNN_recovery_pct` (20 %) y `RR_recovery_pct` (15 %), ponderaciones definidas de forma exploratoria dado el rol central de RMSSD como indicador de modulación vagal. El resultado se interpreta como un porcentaje aproximado de recuperación autonómica.

### 7. Etiqueta recuperado / no recuperado

Se realizó un análisis de sensibilidad probando umbrales de 40 %, 50 %, 60 %, 70 % y 80 %. Un umbral inicial de 70 % generó una distribución de clases muy desbalanceada. El umbral de **60 %** ofreció el mejor equilibrio entre exigencia fisiológica y balance de clases, por lo que se adoptó como criterio exploratorio del estudio piloto (no como criterio clínico universal):

- `recovery_score ≥ 60 %` → recuperado
- `recovery_score < 60 %` → no_recuperado

### 8. Aumento de datos sintéticos

Debido a que el estudio cuenta con solo tres participantes, se aplicó aumento de datos **únicamente en el espacio de características HRV**, no sobre la señal ECG cruda, ya que generar ECG sintético realista requeriría validar morfología de ondas P, complejos QRS, ondas T y patrones de ruido fisiológico, lo cual excede el alcance y el tiempo disponible del proyecto. La generación sintética se realizó mediante bootstrap de ventanas reales, adición de ruido gaussiano controlado por clase y limitación de los valores generados a rangos fisiológicamente plausibles. Los datos sintéticos se emplearon exclusivamente para entrenamiento; los datos reales permanecieron intactos, sin recorte (*clipping*).

### 9. Modelo de clasificación (MLP)

Se optó por una red neuronal MLP de arquitectura pequeña, adecuada para el carácter tabular del dataset final (features HRV, no señales crudas). La entrada incluye HR_mean, RR_mean, SDNN, RMSSD, pNN50 y sus variables delta/ratio respecto al basal. Deliberadamente **no se incluyó** `recovery_score` como feature de entrada, ya que fue la variable utilizada para construir la etiqueta y su inclusión generaría fuga de información (*data leakage*); tampoco se incluyó el puntaje PSS, dado que con solo tres participantes el modelo podría aprender diferencias individuales en lugar de patrones fisiológicos generalizables.

Arquitectura: capa densa de 32 neuronas (ReLU) → *batch normalization* → *dropout* → capa densa de 16 neuronas (ReLU) → *dropout* → capa de salida *softmax* con dos clases (recuperado / no_recuperado).

### 10. Validación

La validación se realizó mediante **leave-one-subject-out** (LOSO): en cada fold se entrena con dos participantes y se prueba con el tercero (P01 vs. P02+P03; P02 vs. P01+P03; P03 vs. P01+P02). Los datos sintéticos se generaron únicamente a partir de los participantes de entrenamiento en cada fold, nunca del participante de prueba, evitando fuga de información y ofreciendo una evaluación más conservadora que un split aleatorio de ventanas.

### 11. Exportación a Edge Impulse

El dataset final se exportó en formato CSV (`05_dataset_edge_impulse_recuperacion.csv`) con los features HRV seleccionados y la etiqueta recuperado/no_recuperado, para su uso como plataforma de entrenamiento e implementación del modelo MLP. La validación local LOSO se considera más conservadora que la validación aleatoria interna de Edge Impulse, ya que evita mezclar ventanas del mismo participante entre entrenamiento y prueba.

### 12. Aplicación web (propuesta)

Se plantea una aplicación web como herramienta de testeo e interpretación, con el siguiente flujo: ingreso del código del participante y del puntaje PSS → carga de las señales basal, cognitiva y de recuperación → procesamiento ECG y detección de picos R → extracción de features HRV → cálculo del recovery score → aplicación del modelo MLP entrenado → visualización de la predicción (recuperado/no_recuperado), del PSS como contexto y de una interpretación integrada.

---

## Resultados

**Adquisición y ventanas.** Se procesaron señales ECG de tres participantes en las tres condiciones experimentales, obteniéndose aproximadamente **55 ventanas reales** en la fase de recuperación tras la segmentación (ventanas de 30 s, paso de 15 s).

**Análisis de sensibilidad del umbral de recuperación.** La distribución de clases varió considerablemente según el umbral elegido:

| Umbral | no_recuperado | recuperado |
|---|---|---|
| 40 % | 32 | 23 |
| 50 % | 37 | 18 |
| **60 % (elegido)** | **39** | **16** |
| 70 % | 49 | 6 |
| 80 % | 51 | 4 |

Un umbral de 70 % —el primero considerado— generaba un desbalance severo (49 vs. 6). El umbral de 60 % se seleccionó por ofrecer el mejor compromiso entre exigencia fisiológica y balance de clases para el entrenamiento posterior.

**Aumento sintético.** Con `RECOVERY_THRESHOLD = 60 %` y 3 muestras sintéticas generadas por cada muestra real, el dataset aumentado alcanzó aproximadamente 156 muestras de la clase no_recuperado y 64 de la clase recuperado.

**Desempeño del modelo MLP (validación leave-one-subject-out).**

| Fold (sujeto de prueba) | Accuracy | F1 macro |
|---|---|---|
| P01 | 0.842 | 0.808 |
| P02 | 0.053 | 0.050 |
| P03 | 0.588 | 0.370 |
| **Promedio** | **0.494** | **0.409** |

El desempeño fue marcadamente heterogéneo entre participantes: el modelo generalizó razonablemente bien al predecir sobre P01, pero falló casi por completo al predecir sobre P02. Esta variabilidad es consistente con la distribución desigual de clases por sujeto —algunos participantes concentran mayoritariamente ventanas "recuperadas" y otros mayoritariamente "no_recuperadas"— y con el tamaño extremadamente reducido de la muestra a nivel de sujetos (n=3), que impide que el modelo aprenda patrones fisiológicos generalizables más allá de las particularidades individuales de cada participante.

Por estas razones, los resultados del sistema se interpretan en un orden jerárquico: (1) el **recovery_score** fisiológico y su clasificación por regla constituyen el resultado principal e interpretable del proyecto; (2) la **predicción de la MLP** se ofrece como apoyo exploratorio complementario, sin validez clínica; y (3) el **puntaje PSS-10/PSS-14** se reporta como contexto de estrés percibido, sin intervenir en el modelo.

---

## Conclusiones

- Se logró implementar un pipeline completo y funcional de extremo a extremo —desde la señal ECG cruda hasta un índice interpretable de recuperación autonómica— a pesar de contar con una muestra piloto de solo tres participantes.
- El *recovery_score*, construido a partir de la comparación de features HRV de cada ventana de recuperación contra los promedios basal y cognitivo individuales, resultó ser una métrica más coherente con la pregunta de investigación que una clasificación directa basal/cognitivo/recuperación, ya que responde explícitamente si el participante recuperó o no su estado autonómico.
- El umbral de 60 % demostró ser un criterio exploratorio razonable para balancear exigencia fisiológica y proporción de clases, pero debe entenderse como una decisión metodológica del estudio piloto y no como un estándar clínico validado externamente.
- El modelo MLP, si bien mostró un desempeño prometedor en algunos folds (P01), no generalizó de forma estable entre los tres participantes (accuracy promedio de 0.49 y F1 macro de 0.41 en validación leave-one-subject-out), lo que refleja principalmente la limitación del tamaño muestral (n=3) y la heterogeneidad individual, y no necesariamente una falla del enfoque metodológico.
- El uso de datos sintéticos restringido al espacio de características —evitando la generación de ECG crudo sintético— permitió aumentar el volumen de entrenamiento sin comprometer la validez fisiológica de los datos reales, aunque no sustituye la necesidad de una muestra más amplia y diversa de participantes.
- Como trabajo futuro, se recomienda ampliar la muestra a un número de participantes que permita evaluar significancia estadística, explorar features adicionales en el dominio de la frecuencia (por ejemplo, razón LF/HF), y completar la integración de la aplicación web para uso exploratorio en contextos académicos reales.
- En conjunto, el proyecto debe interpretarse como una **prueba de concepto metodológica válida**, no como un sistema clínicamente validado: sienta las bases de un pipeline reproducible de ECG-HRV para estudios de recuperación autonómica, cuya robustez estadística depende de futuras ampliaciones de la muestra.

---

## Referencias

[1] G. Laborie et al., "Mental workload alters heart rate variability, lowering non-linear dynamics," *Frontiers in Physiology*, 2019. PMC6528181.

[2] M. Malik, "Heart rate variability: standards of measurement, physiological interpretation, and clinical use," *IEEE Trans. Biomed. Eng.*, 1996.

[3] F. Shaffer and J. P. Ginsberg, "An overview of heart rate variability metrics and norms," *Front. Public Health*, 2017.

[4] H.-G. Kim, E.-J. Cheon, D.-S. Bai, et al., "Stress and heart rate variability: a meta-analysis," *Neurosci. Biobehav. Rev.*, 2018.

[5] J. Wei et al., "Cognitive Load Inference Using Physiological Markers in Virtual Reality," in *2025 IEEE Conference on Virtual Reality and 3D User Interfaces (VR)*, 2025.

[6] A. Bhatti et al., "CLARE: Cognitive Load Assessment in Realtime with Multimodal Data," arXiv:2404.17098, 2024.

[7] Z. Ahmad et al., "Multi-level Stress Assessment from ECG in a Virtual Reality Environment using Multimodal Fusion," arXiv:2107.04566, 2021.

[8] M. Pradeep et al., "Cross-Modal Computational Model of Brain-Heart Interactions via HRV and EEG Features," arXiv:2601.06792, 2026.

[9] A. Londoño-Vargas et al., "Longitudinal effects of stress in an academic context on HRV and wellbeing in university students," 2025. PMC12239435.

[10] P. Králíčková et al., "Heart rate variability, perceived stress and willingness to seek counselling in undergraduate students," *J. Psychosom. Res.*, 2022.

[11] Analog Devices, "AD8232 Single-Lead, Heart Rate Monitor Front End," Data Sheet Rev. D, Analog Devices Inc., 2020.

> *Nota:* de la bibliografía original del avance del proyecto se excluyeron las fuentes centradas en arquitecturas de red no utilizadas en la implementación final (p. ej., 1D-CNN, TCN causal, atención temporal) y aquellas de dominio no directamente relacionado con el proyecto (p. ej., ruido de habla irrelevante), ya que el sistema finalmente implementado usa un modelo MLP sobre features HRV y no dichas arquitecturas.

---

## Biografías de autores

### Néstor Allende
[Breve biografía: carrera, ciclo/semestre, universidad, intereses académicos relacionados con señales biomédicas o ciencia de datos, correo o contacto opcional.]

### Ana Angulo
[Breve biografía: carrera, ciclo/semestre, universidad, intereses académicos relacionados con señales biomédicas o ciencia de datos, correo o contacto opcional.]

### Luis Loayza
[Breve biografía: carrera, ciclo/semestre, universidad, intereses académicos relacionados con señales biomédicas o ciencia de datos, correo o contacto opcional.]

### Natalie Sante
[Breve biografía: carrera, ciclo/semestre, universidad, intereses académicos relacionados con señales biomédicas o ciencia de datos, correo o contacto opcional.]

### Nataly Deledesma
[Breve biografía: carrera, ciclo/semestre, universidad, intereses académicos relacionados con señales biomédicas o ciencia de datos, correo o contacto opcional.]


---

## Estructura del repositorio

```
PULSEV-ISB-2026-I/
├── README.md                          # Este informe final
├── data_raw/                          # Señales ECG crudas por participante y estado
├── metadata/
│   └── pss_scores.csv                 # Puntajes PSS-10/PSS-14 por participante
├── src/ o notebooks/                  # Pipeline de procesamiento (Python)
├── outputs/
│   └── 05_dataset_edge_impulse_recuperacion.csv
└── app/                                # Aplicación web (en desarrollo)
```

*(Ajusta esta estructura si el repositorio real está organizado de otra forma.)*
