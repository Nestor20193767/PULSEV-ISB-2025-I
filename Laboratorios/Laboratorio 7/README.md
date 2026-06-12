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

![Protocolo experimental](Archivos/protocolo_eeg_.svg)

---

### 2.4 Preprocesamiento de la señal

El preprocesamiento debe describir claramente qué se hizo antes de analizar los resultados. Se recomienda reportar:

1. Importación de los archivos EEG.
2. Revisión visual de la señal cruda.
3. Eliminación de segmentos dañados, si corresponde.
4. Aplicación de filtro pasa banda.
5. Aplicación de filtro notch para ruido de red eléctrica, si corresponde.
6. Segmentación por condición experimental.
7. Cálculo de métricas temporales y espectrales.


Instalación de librerias:

```python
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import welch, butter, filtfilt, iirnotch, find_peaks
from scipy.stats import ttest_rel

plt.rcParams["figure.figsize"] = (12, 4)
plt.rcParams["axes.grid"] = True
```

---

## 3. Resultados

En esta sección se presentan las figuras obtenidas.

---

### 3.1 Señales EEG crudas y filtradas

![Basal cruda vs filtrada Fp1](Archivos/basal_ojos_cerrados_Fp1_raw_vs_filtrada.png)
![Basal cruda vs filtrada Fp2](Archivos/basal_ojos_cerrados_Fp2_raw_vs_filtrada.png)

- En la condición basal se espera una señal más estable debido a la reducción de estímulos externos.

![Ojos abiertos cruda vs filtrada Fp1](Archivos/ojos_abiertos_Fp1_raw_vs_filtrada.png)
![Ojos abiertos cruda vs filtrada Fp2](Archivos/ojos_abiertos_Fp2_raw_vs_filtrada.png)

- En ojos abiertos pueden aparecer cambios asociados a mayor entrada visual.

![Parpadeo cruda vs filtrada Fp1](Archivos/parpadeo_Fp1_raw_vs_filtrada.png)
![Parpadeo cruda vs filtrada Fp2](Archivos/parpadeo_Fp2_raw_vs_filtrada.png)

- En parpadeo se esperan deflexiones de gran amplitud producidas por actividad ocular.

![Masticación cruda vs filtrada Fp1](Archivos/masticacion_Fp1_raw_vs_filtrada.png)
![Masticación cruda vs filtrada Fp2](Archivos/masticacion_Fp2_raw_vs_filtrada.png)

- En masticación se espera mayor contaminación por actividad muscular.

![Música relajante cruda vs filtrada Fp1](Archivos/musica_relajante_Fp1_raw_vs_filtrada.png) 
![Música relajante cruda vs filtrada Fp2](Archivos/musica_relajante_Fp2_raw_vs_filtrada.png) 

![Música estresante cruda vs filtrada Fp1](Archivos/musica_estresante_Fp1_raw_vs_filtrada.png)
![Música estresante cruda vs filtrada Fp2](Archivos/musica_estresante_Fp2_raw_vs_filtrada.png)

- En música relajante y estresante se pueden explorar cambios de amplitud o potencia espectral.


---

### 3.2 PSD de Welch por condición

Se calcula la densidad espectral de potencia usando Welch con segmento de 2 s. Esto permite observar qué frecuencias tienen mayor contribución en cada condición.

|   |condition	| channel	frequency_hz | psd_uv2_per_hz |
|0	|basal_ojos_cerrados	| Fp1	| 0.0	| 437.023856 |
|1	|basal_ojos_cerrados	| Fp1	| 0.5	| 3158.686066 | 
|2	|basal_ojos_cerrados	| Fp1	| 1.0	| 15720.109946 | 
|3	|basal_ojos_cerrados	| Fp1	| 1.5	| 13457.445632 |
|4	|basal_ojos_cerrados	| Fp1	| 2.0	| 5207.903244 |


![PSD Welch por condicion Fp1](Archivos/PSD_Welch_comparacion_Fp1.png)
![PSD Welch por condicion Fp2](Archivos/PSD_Welch_comparacion_Fp2.png)

---

### 3.3 Potencia por bandas EEG

Se calcula la potencia absoluta y relativa por ventanas de 2 s en las bandas:

| Banda | Rango aproximado |
|---|---:|
| Delta | 0.5-4 Hz |
| Theta | 4-8 Hz |
| Alfa | 8-13 Hz |
| Beta | 13-30 Hz |
| Gamma | 30-45 Hz |

[Potencia de bandas por epoca](Archivos/potencia_bandas_por_epoca.csv)

[Resumen Potencia de bandas por epoca](Archivos/resumen_potencia_bandas.csv)


---

### 3.4 Comparación de potencia alfa: ojos cerrados vs ojos abiertos
Se usa la condición basal como equivalente de ojos cerrados / aislamiento parcial y se compara contra la condición ojos abiertos. La comparación se realiza con potencia alfa absoluta y relativa por ventanas de 2 s.

[Comparacion de potencia Alfa](Archivos/test_alpha_ojos_cerrados_vs_abiertos.csv)

*Gráfico comparativo de alfa relativa por canal*

![Comparacion de potencia alfa relativa Fp1](Archivos/alpha_rel_ojos_cerrados_vs_abiertos_Fp1.png)
![Comparacion de potencia alfa relativa Fp2](Archivos/alpha_rel_ojos_cerrados_vs_abiertos_Fp2.png)

---

### 3.5 Incremento de beta durante condición de carga/estrés
Como el protocolo descrito no incluye una tarea cognitiva clásica, este notebook usa por defecto:
-Condición basal/comparación: musica_relajante
-Condición de carga/estrés: musica_estresante

[Actividad beta de carga/estres](Archivos/test_beta_relajante_vs_estresante.csv)

*Gráfico comparativo de beta relativa por canal*

![Comparación de potencia beta relativa Fp1](Archivos/beta_rel_musica_relajante_vs_musica_estresante_Fp1.png)
![Comparación de potencia beta relativa Fp2](Archivos/beta_rel_musica_relajante_vs_musica_estresante_Fp2.png)



---

### 3.6 Detección de artefactos de parpadeo
El algoritmo busca picos en la señal centrada respecto a su mediana. Se contabilizan picos cuya amplitud absoluta supere 80 µV, separados al menos 0.25 s.

[Conteo de artefactos](Archivos/conteo_artefactos_parpadeo.csv)

*Gráfico de detección de artefactos*

![Detección de artefactos de parpadeo Fp1](Archivos/parpadeos_detectados_Fp1.png)
![Detección de artefactos de parpadeo Fp2](Archivos/parpadeos_detectados_Fp2.png)


---

### 3.6 Comparación Fp1 vs Fp2
La comparación se hace por potencia relativa de bandas.

[comparacion Fp1 vs Fp2](Archivos/comparacion_Fp1_Fp2.csv)

*Gráficos de comparacion Fp1 vs Fp2*

![Basal ojos cerrados Fp1 vs Fp2](Archivos/Fp1_vs_Fp2_basal_ojos_cerrados.png)
![Basal ojos cerrados Fp1 vs Fp2](Archivos/Fp1_vs_Fp2_ojos_abiertos.png)
![Basal ojos cerrados Fp1 vs Fp2](Archivos/Fp1_vs_Fp2_parpadeo.png)
![Basal ojos cerrados Fp1 vs Fp2](Archivos/Fp1_vs_Fp2_masticacion.png)
![Basal ojos cerrados Fp1 vs Fp2](Archivos/Fp1_vs_Fp2_musica_relajante.png)
![Basal ojos cerrados Fp1 vs Fp2](Archivos/Fp1_vs_Fp2_musica_estresante.png)



---

## 4. Discusión

### ¿Qué banda de frecuencia predomina al cerrar los ojos?
En la condición basal con ojos cubiertos o cerrados se evaluó la potencia relativa de las bandas EEG. Según los resultados obtenidos, la banda predominante fue [completar: alfa/theta/beta/etc.]. En EEG, la banda alfa suele aumentar durante reposo con ojos cerrados, aunque este efecto puede observarse mejor en regiones posteriores que en derivaciones frontales.

### ¿Qué filtro es imprescindible para EEG y por qué?
Para EEG es imprescindible controlar el contenido de frecuencia mediante un filtro pasa banda, porque la señal EEG es de baja amplitud y puede contaminarse por deriva DC, movimiento y ruido de alta frecuencia. En este laboratorio, el canal EEG de BITalino ya incluye un filtro hardware de aproximadamente 0.8-48 Hz, por lo que se atenúan componentes lentas y frecuencias por encima del rango EEG principal. Además, si aparece contaminación de red eléctrica, se puede usar un filtro notch de 50/60 Hz; sin embargo, en este caso puede no ser necesario porque el hardware ya limita la banda hasta aproximadamente 48 Hz.

### ¿Puedes modular conscientemente tu señal EEG? Da un ejemplo.
Sí, algunos patrones EEG pueden modificarse de manera consciente o voluntaria. Un ejemplo simple es abrir y cerrar los ojos: al cerrar los ojos, puede aumentar la actividad alfa en reposo. Otro ejemplo es el parpadeo, aunque este no representa modulación cerebral pura, sino un artefacto ocular claramente visible en la señal.

### ¿Se observan diferencias entre Fp1 y Fp2? ¿Por qué podrían ocurrir?
Si se adquirieron Fp1 y Fp2, las diferencias pueden deberse a varios factores: diferencias de impedancia entre electrodos, contacto desigual con la piel, asimetría en la colocación, actividad ocular lateralizada, actividad muscular facial o diferencias reales en la actividad registrada por cada derivación. Por ello, antes de interpretar diferencias fisiológicas, se debe verificar la calidad de la señal y la presencia de artefactos.

---

## 5. Conclusiones

En este laboratorio se adquirieron señales EEG bajo seis condiciones experimentales. La condición basal permitió obtener una señal de referencia, mientras que las condiciones de parpadeo y masticación facilitaron la identificación de artefactos fisiológicos. Las condiciones de música relajante y música estresante permitieron explorar posibles cambios en la señal ante estímulos auditivos, aunque los resultados deben interpretarse de manera descriptiva si el tamaño de muestra es reducido.

El análisis resalta la importancia de controlar el protocolo de adquisición, documentar adecuadamente las condiciones experimentales y diferenciar entre actividad cerebral y artefactos antes de realizar interpretaciones fisiológicas.

---

## 6. Código utilizado
El procesamiento fue realizado en Python usando Google Colab. El archivo principal de análisis debe ubicarse en:

[Codigo de Colab del laboratorio 7](Archivos/EEG_BITalino_Analisis.ipynb)

Los pasos aplicados fueron:
1. Carga de los archivos .txt.
2. Selección de los canales Fp1 y Fp2.
3. Conversión de la señal a microvoltios.
4. Aplicación de filtro pasa banda digital complementario.
5. Segmentación de la señal en ventanas de 2 segundos.
6. Cálculo de la densidad espectral de potencia mediante Welch.
7. Cálculo de potencia relativa por bandas EEG.
8. Comparación estadística mediante t-test pareado.
9. Detección de parpadeos mediante umbral de 80 µV.



---

## 7. Referencias


