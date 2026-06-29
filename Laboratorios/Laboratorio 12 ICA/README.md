
# Laboratorio EEG: Uso de ICA y Welch

Este laboratorio tuvo como objetivo procesar señales EEG adquiridas con BITalino, explorar artefactos fisiológicos mediante condiciones de control y analizar la potencia espectral de la señal usando el método de Welch. Además, se evaluó de forma exploratoria el uso de ICA para identificar posibles componentes asociados a artefactos musculares.

---

## 1. Adquisición

Se registraron señales EEG de **2 canales** usando BITalino, con una frecuencia de muestreo de **1000 Hz**.

Las condiciones registradas fueron:

* **Basal:** registro en reposo.
* **Punto fijo:** registro con atención visual estable.
* **Parpadeo:** condición de control para artefactos oculares.
* **Masticación:** condición de control para artefactos musculares.
* **Música relajante:** estímulo auditivo de baja carga.
* **Música estresante:** estímulo auditivo de mayor carga.

Estas condiciones permitieron comparar la actividad EEG en reposo frente a estímulos o tareas que podían modificar el contenido espectral de la señal.

---

## 2. Preprocesamiento

El preprocesamiento incluyó los siguientes pasos:

1. **Lectura de archivos `.txt`** generados por BITalino.
2. **Conversión de unidades** de los valores digitales a microvoltios, considerando la resolución y ganancia del sistema.
3. **Filtrado pasa banda de 1–45 Hz**, con el objetivo de conservar las bandas EEG de interés y reducir componentes de muy baja frecuencia o ruido de alta frecuencia.
4. **Revisión visual de artefactos**, observando segmentos con amplitudes anómalas o patrones asociados a parpadeo, movimiento o actividad muscular.

Este paso permitió preparar la señal para el análisis espectral y la extracción de características por ventanas.

---

## 3. Artefactos

Se usaron las condiciones de **parpadeo** y **masticación** como controles experimentales para observar artefactos típicos en EEG:

* **Parpadeo:** asociado principalmente a artefactos oculares, generalmente visibles como deflexiones de gran amplitud en la señal.
* **Masticación:** asociado a actividad muscular, que suele manifestarse como componentes de mayor frecuencia y cambios abruptos en la señal.

Estas condiciones sirvieron como referencia para identificar posibles segmentos contaminados en las demás señales.

---

## 4. ICA

Se exploró el uso de **Análisis de Componentes Independientes, ICA**, como herramienta para separar componentes relacionados con actividad cerebral y artefactos.

Sin embargo, debido a que la adquisición cuenta solo con **2 canales EEG**, la aplicación de ICA es limitada. Con pocos canales, la separación de fuentes independientes no es tan robusta como en sistemas EEG multicanal.

Por ello:

* ICA se usó de manera exploratoria.
* La remoción de componentes se aplicó únicamente si los componentes fueron inspeccionados previamente.
* No se eliminó automáticamente ningún componente sin revisión visual.
* Se priorizó conservar la señal original cuando no existía evidencia clara de artefacto.

---

## 5. Welch

Se aplicó el método de **Welch** para estimar la densidad espectral de potencia, PSD, de las señales EEG.

El análisis se realizó por ventanas, extrayendo la potencia en las siguientes bandas:

| Banda      | Rango de frecuencia |
| ---------- | ------------------: |
| Theta      |              4–8 Hz |
| Alfa       |             8–13 Hz |
| Beta       |            13–30 Hz |
| Gamma baja |            30–45 Hz |

A partir de la PSD se calcularon potencias por banda para cada condición y canal. Esto permitió comparar cómo cambiaba el contenido espectral de la señal entre reposo, atención visual y estímulos auditivos.

---

## 6. Comparación

Se realizaron comparaciones entre la condición basal y las demás condiciones experimentales:

* **Basal vs punto fijo**
* **Basal vs música relajante**
* **Basal vs música estresante**

Estas comparaciones permitieron observar cambios relativos en la potencia de las bandas EEG. En particular, se buscó identificar variaciones en bandas como alfa y beta, relacionadas con estados de relajación, atención o activación mental.

---

## Archivos generados

Durante el procesamiento se generaron los siguientes archivos:

```text
window_features_all_conditions.csv
window_features_with_artifact_flags.csv
artifact_report.csv
summary_bandpowers_clean.csv
comparison_vs_basal.csv
```

Además, se generaron figuras en formato `.png`, incluyendo:

* Señales EEG en el tiempo.
* PSD por condición.
* Gráficos de barras de potencia por banda.
* Comparaciones entre basal y otras condiciones.

---

## Descripción de archivos

| Archivo                                   | Descripción                                                                                     |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `window_features_all_conditions.csv`      | Contiene las características extraídas por ventanas para todas las condiciones.                 |
| `window_features_with_artifact_flags.csv` | Incluye las características por ventana junto con etiquetas o indicadores de posible artefacto. |
| `artifact_report.csv`                     | Resume la detección o conteo de artefactos observados durante el procesamiento.                 |
| `summary_bandpowers_clean.csv`            | Resume la potencia promedio por banda luego de excluir o marcar segmentos con artefactos.       |
| `comparison_vs_basal.csv`                 | Contiene la comparación de cada condición frente a la condición basal.                          |
| Figuras `.png`                            | Visualizaciones de señales, espectros PSD y comparaciones de potencia por bandas.               |

---

## Flujo general del análisis

```text
Datos BITalino (.txt)
        ↓
Lectura y conversión a microvoltios
        ↓
Filtrado 1–45 Hz
        ↓
Revisión de artefactos
        ↓
Exploración con ICA
        ↓
Estimación PSD con Welch
        ↓
Cálculo de potencia theta, alfa, beta y gamma baja
        ↓
Comparación entre condiciones
        ↓
Exportación de tablas y figuras
```

---

## Consideraciones

El análisis con ICA debe interpretarse con cuidado debido al bajo número de canales disponibles. En este laboratorio, ICA se usó como una herramienta exploratoria para observar posibles componentes asociados a artefactos, pero no como un método automático de limpieza.

El método de Welch fue el análisis principal para cuantificar el contenido espectral de las señales EEG y comparar las condiciones experimentales.
