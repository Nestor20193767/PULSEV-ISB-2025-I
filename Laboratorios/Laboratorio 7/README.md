# Informe de Laboratorio 7: Adquisición y análisis de señales EEG

## Descripción general

Este repositorio contiene el informe y los recursos asociados al laboratorio de electroencefalografía (EEG), orientado a observar la señal cerebral en diferentes condiciones experimentales: reposo basal, ojos abiertos, artefactos por parpadeo, artefactos por masticación, música relajante y música estresante.

El objetivo principal del laboratorio es comparar visual y cuantitativamente cómo cambia la señal EEG entre una condición basal controlada y condiciones que pueden modificar la actividad registrada o introducir artefactos fisiológicos.

---

# Informe

## 1. Introducción

La electroencefalografía (EEG) es una técnica no invasiva que permite registrar la actividad eléctrica cerebral mediante sensores colocados sobre el cuero cabelludo. Esta señal puede analizarse en el dominio temporal y en el dominio de la frecuencia para identificar patrones asociados a estados de reposo, atención, relajación o presencia de artefactos.

En este laboratorio se realizó la adquisición de señales EEG bajo seis condiciones experimentales:

1. Condición basal con aislamiento sensorial parcial.
2. Ojos abiertos mirando un punto fijo.
3. Parpadeo voluntario.
4. Masticación.
5. Exposición a música relajante.
6. Exposición a música estresante.

La condición basal se utilizó como referencia inicial. Las condiciones de parpadeo y masticación permitieron observar artefactos fisiológicos asociados a movimiento ocular y actividad muscular. Finalmente, las condiciones con música relajante y música estresante permitieron explorar posibles cambios en la señal EEG ante estímulos auditivos emocionales.

> **Dónde colocar imágenes en esta sección:**  
> Agregar una imagen general del montaje experimental en:
>
> ```markdown
> ![Montaje experimental EEG](figures/protocolo/montaje_eeg.png)
> ```

---

## 2. Métodos

### 2.1 Participante

La adquisición fue realizada en un participante voluntario del grupo durante una sesión de laboratorio. El participante permaneció sentado, procurando reducir movimientos corporales durante las condiciones de reposo y estimulación.

| Variable | Descripción |
|---|---|
| Participante | Participante 01 |
| Edad | 22 |
| Sexo | Femenino |
| Fecha de adquisición | 08/05/2026 |
| Lugar de adquisición | UPCH La Molina |

---

### 2.2 Equipos y materiales

Completar esta sección con los datos reales del laboratorio:

| Elemento | Descripción |
|---|---|
| Sistema EEG |  BITalino (r)evolution Assembled Core BT  |
| Número de canales | 2 |
| Frecuencia de muestreo | 1000 Hz |
| Electrodos utilizados | Electrodos desechables |
| Software de adquisición | OpenSignal |
| Música relajante | Elegida por Usuario |
| Música estresante | Elegida por Usuario |

> **Dónde colocar imagen del equipo:**  
>
> ```markdown
> ![Equipo EEG utilizado](figures/protocolo/equipo_eeg.png)
> ```

---

### 2.3 Protocolo experimental

El protocolo consistió en seis etapas consecutivas de adquisición EEG. Primero se registró una condición basal, en la cual el participante permaneció aislado parcialmente de estímulos externos mediante cobertura de ojos y oídos. Luego se registró una condición de ojos abiertos, en la que el participante observó un punto fijo. Posteriormente, se adquirieron señales durante parpadeo voluntario y masticación para observar artefactos fisiológicos. Finalmente, se presentaron estímulos auditivos correspondientes a música relajante y música estresante.

| Orden | Condición | Duración aproximada | Descripción |
|---|---:|---:|---|
| 1 | Basal | 2 min | Participante con ojos y oídos cubiertos para reducir estímulos externos. |
| 2 | Ojos abiertos | 2 min | Participante mirando un punto fijo. |
| 3 | Parpadeo | 1 min | Participante realiza parpadeos voluntarios. |
| 4 | Masticación | 1 min | Participante mastica para inducir artefactos musculares. |
| 5 | Música relajante | 2 min | Participante escucha música asociada a relajación. |
| 6 | Música estresante | 2 min | Participante escucha música asociada a estrés o incomodidad. |

**Diagrama del protocolo**  

[Protocolo experimental](Archivos/protocolo_eeg_.svg)

---

### 2.4 Organización de los datos

Los archivos crudos deben colocarse en la carpeta:

```text
data/raw/
```

Ejemplo de nombres recomendados:

```text
basal.csv
ojos_abiertos.csv
parpadeo.csv
masticacion.csv
musica_relajante.csv
musica_estresante.csv
```

Los archivos procesados o filtrados deben colocarse en:

```text
data/processed/
```

Ejemplo:

```text
basal_filtrada.csv
ojos_abiertos_filtrada.csv
parpadeo_filtrada.csv
masticacion_filtrada.csv
musica_relajante_filtrada.csv
musica_estresante_filtrada.csv
```

---

### 2.5 Preprocesamiento de la señal

El preprocesamiento debe describir claramente qué se hizo antes de analizar los resultados. Se recomienda reportar:

1. Importación de los archivos EEG.
2. Revisión visual de la señal cruda.
3. Eliminación de segmentos dañados, si corresponde.
4. Aplicación de filtro pasa banda.
5. Aplicación de filtro notch para ruido de red eléctrica, si corresponde.
6. Segmentación por condición experimental.
7. Cálculo de métricas temporales y espectrales.

Ejemplo de comando para ejecutar el preprocesamiento:

```bash
python scripts/02_preprocesamiento.py
```

Ejemplo de bloque de código que puede incluirse en el notebook:

```python
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch

# Cargar señal EEG
senal = pd.read_csv("data/raw/basal.csv")

# Ejemplo: graficar señal cruda
plt.figure(figsize=(12, 4))
plt.plot(senal["tiempo"], senal["eeg"])
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud EEG")
plt.title("Señal EEG basal cruda")
plt.grid(True)
plt.show()
```

> **Dónde colocar capturas del código:**  
> Si el informe final requiere mostrar partes del código, colocar capturas o fragmentos relevantes en la sección de Métodos, especialmente en el apartado de preprocesamiento.
>
> Carpeta sugerida:
>
> ```text
> figures/protocolo/
> ```

---

### 2.6 Análisis de la señal

Para el análisis se recomienda incluir:

- Gráficas de señal EEG en el dominio temporal.
- Comparación entre señal cruda y filtrada.
- Análisis espectral mediante densidad espectral de potencia.
- Comparación de bandas EEG: delta, theta, alfa, beta y gamma, si la frecuencia de muestreo lo permite.
- Identificación visual de artefactos por parpadeo y masticación.

Bandas EEG de referencia:

| Banda | Rango aproximado |
|---|---:|
| Delta | 0.5-4 Hz |
| Theta | 4-8 Hz |
| Alfa | 8-13 Hz |
| Beta | 13-30 Hz |
| Gamma | >30 Hz |

> **Importante:** Los rangos pueden variar ligeramente según la referencia usada. En el informe se debe indicar qué rangos fueron utilizados y mantenerlos constantes en todo el análisis.

---

## 3. Resultados

En esta sección se deben presentar las figuras obtenidas y describir brevemente lo que se observa en cada condición. No basta con colocar imágenes; cada figura debe tener una interpretación breve.

---

### 3.1 Señales EEG crudas

Colocar aquí las gráficas de las señales sin filtrar.

```markdown
![Señal basal cruda](figures/raw_signals/basal_raw.png)

![Señal con ojos abiertos cruda](figures/raw_signals/ojos_abiertos_raw.png)

![Señal durante parpadeo cruda](figures/raw_signals/parpadeo_raw.png)

![Señal durante masticación cruda](figures/raw_signals/masticacion_raw.png)

![Señal durante música relajante cruda](figures/raw_signals/musica_relajante_raw.png)

![Señal durante música estresante cruda](figures/raw_signals/musica_estresante_raw.png)
```

Descripción sugerida:

- En la condición basal se espera una señal más estable debido a la reducción de estímulos externos.
- En ojos abiertos pueden aparecer cambios asociados a mayor entrada visual.
- En parpadeo se esperan deflexiones de gran amplitud producidas por actividad ocular.
- En masticación se espera mayor contaminación por actividad muscular.
- En música relajante y estresante se pueden explorar cambios de amplitud o potencia espectral, aunque no deben interpretarse de forma concluyente si solo se tiene un participante.

---

### 3.2 Señales filtradas

Colocar aquí las gráficas luego del preprocesamiento.

```markdown
![Señal basal filtrada](figures/filtered_signals/basal_filtrada.png)

![Señal ojos abiertos filtrada](figures/filtered_signals/ojos_abiertos_filtrada.png)

![Señal parpadeo filtrada](figures/filtered_signals/parpadeo_filtrada.png)

![Señal masticación filtrada](figures/filtered_signals/masticacion_filtrada.png)

![Señal música relajante filtrada](figures/filtered_signals/musica_relajante_filtrada.png)

![Señal música estresante filtrada](figures/filtered_signals/musica_estresante_filtrada.png)
```

Descripción sugerida:

- Comparar si el filtrado redujo ruido de alta frecuencia o ruido de red.
- Indicar si los artefactos siguen siendo visibles incluso después del filtrado.
- Explicar si se conservaron los segmentos con artefactos porque forman parte del objetivo del laboratorio.

---

### 3.3 Comparación entre condiciones

Colocar una figura comparativa con todas las condiciones o con ventanas representativas.

```markdown
![Comparación temporal entre condiciones](figures/results/comparacion_temporal.png)
```

Tabla sugerida:

| Condición | Observación principal | Interpretación |
|---|---|---|
| Basal | [Completar] | Señal de referencia con menor estimulación externa. |
| Ojos abiertos | [Completar] | Posible cambio por procesamiento visual. |
| Parpadeo | [Completar] | Artefacto ocular visible. |
| Masticación | [Completar] | Artefacto muscular visible. |
| Música relajante | [Completar] | Posible cambio asociado a estado de relajación. |
| Música estresante | [Completar] | Posible cambio asociado a estímulo auditivo estresante. |

---

### 3.4 Análisis en frecuencia

Colocar aquí la densidad espectral de potencia o el análisis por bandas.

```markdown
![Comparación de PSD](figures/results/comparacion_psd.png)

![Potencia por bandas EEG](figures/results/potencia_bandas.png)
```

Descripción sugerida:

- Comparar la potencia relativa entre condiciones.
- Reportar si existe mayor potencia en banda alfa durante el reposo con ojos cerrados o aislamiento sensorial.
- Comparar si los artefactos aumentan la potencia en rangos específicos.
- Evitar conclusiones clínicas si el análisis corresponde solo a una práctica de laboratorio.

---

### 3.5 Artefactos observados

Colocar una imagen donde se indiquen claramente los segmentos de parpadeo y masticación.

```markdown
![Artefactos EEG observados](figures/results/artefactos_eeg.png)
```

Descripción sugerida:

- Los parpadeos suelen observarse como deflexiones marcadas y repetitivas.
- La masticación puede generar componentes de mayor frecuencia debido a actividad muscular facial.
- Estos artefactos deben ser identificados antes de interpretar la señal como actividad cerebral.

---

## 4. Discusión

Los resultados del laboratorio permiten comparar diferentes condiciones de adquisición EEG y reconocer la importancia del control experimental. La condición basal fue diseñada para reducir estímulos externos mediante aislamiento parcial de ojos y oídos, por lo que puede utilizarse como referencia para contrastar las demás condiciones.

La condición de ojos abiertos permite observar cómo la entrada visual puede modificar la actividad registrada. En comparación, la condición basal o de ojos cerrados puede presentar mayor actividad en rangos asociados al reposo, como la banda alfa, dependiendo de la ubicación de los electrodos y de la calidad de la señal.

Las condiciones de parpadeo y masticación no deben interpretarse como actividad cerebral pura. Su valor en el laboratorio está en que permiten reconocer artefactos fisiológicos. El parpadeo introduce actividad ocular que puede dominar la señal EEG, mientras que la masticación introduce actividad muscular, principalmente por contracción de músculos faciales y mandibulares.

Las condiciones con música relajante y música estresante permiten una exploración preliminar de cambios inducidos por estímulos auditivos. Sin embargo, si solo se evaluó un participante, los resultados deben interpretarse como descriptivos y no concluyentes. Para afirmar diferencias entre relajación y estrés sería necesario evaluar más participantes, controlar el volumen, el tipo de música, el orden de presentación, el estado emocional previo y aplicar pruebas estadísticas.

### Limitaciones

- Se trabajó con un número reducido de participantes.
- La respuesta a la música puede variar según preferencias personales.
- La señal EEG es sensible a movimiento, impedancia de electrodos, parpadeos y actividad muscular.
- Si no se controló el orden de las condiciones, puede existir efecto de fatiga o habituación.
- Si no se registraron marcadores temporales, la segmentación puede depender de anotaciones manuales.

### Mejoras propuestas

- Registrar más participantes.
- Añadir marcadores de eventos durante la adquisición.
- Medir impedancia de electrodos antes de iniciar.
- Usar el mismo volumen para ambos tipos de música.
- Aplicar cuestionarios breves de relajación o estrés percibido.
- Comparar potencia relativa por bandas EEG.
- Reportar claramente filtros, frecuencia de muestreo y canales utilizados.

---

## 5. Conclusiones

En este laboratorio se adquirieron señales EEG bajo seis condiciones experimentales. La condición basal permitió obtener una señal de referencia, mientras que las condiciones de parpadeo y masticación facilitaron la identificación de artefactos fisiológicos. Las condiciones de música relajante y música estresante permitieron explorar posibles cambios en la señal ante estímulos auditivos, aunque los resultados deben interpretarse de manera descriptiva si el tamaño de muestra es reducido.

El análisis resalta la importancia de controlar el protocolo de adquisición, documentar adecuadamente las condiciones experimentales y diferenciar entre actividad cerebral y artefactos antes de realizar interpretaciones fisiológicas.

---

## 6. Código utilizado

Los scripts principales deben ubicarse en la carpeta:

```text
scripts/
```

Descripción recomendada:

| Script | Función |
|---|---|
| `01_cargar_senal.py` | Carga los archivos EEG desde `data/raw/`. |
| `02_preprocesamiento.py` | Aplica filtros y guarda archivos procesados. |
| `03_graficas_temporales.py` | Genera gráficas en el dominio temporal. |
| `04_analisis_frecuencia.py` | Calcula PSD y potencia por bandas. |
| `05_comparacion_condiciones.py` | Compara las condiciones experimentales. |

El notebook principal debe ubicarse en:

```text
notebooks/EEG_Analisis.ipynb
```

En el notebook se recomienda incluir:

1. Carga de datos.
2. Visualización de señales crudas.
3. Preprocesamiento.
4. Visualización de señales filtradas.
5. Análisis espectral.
6. Comparación entre condiciones.
7. Conclusiones parciales.

---

## 7. Referencias

Benbadis, S. R. (2024). *EEG Artifacts*. Medscape.

Goldman, R. I., Stern, J. M., Engel, J., & Cohen, M. S. (2002). Simultaneous EEG and fMRI of the alpha rhythm. *NeuroReport, 13*(18), 2487-2492.

Luck, S. J. (2014). *An Introduction to the Event-Related Potential Technique*. MIT Press.

Ronca, V., Capotorto, R., Di Flumeri, G., Giorgi, A., Vozzi, A., Germano, D., Di Virgilio, V., Borghini, G., Cartocci, G., & Aricò, P. (2024). Optimizing EEG Signal Integrity: A Comprehensive Guide to Ocular Artifact Correction. *Bioengineering, 11*(10), 1018.

Teplan, M. (2002). Fundamentals of EEG measurement. *Measurement Science Review, 2*(2), 1-11.

