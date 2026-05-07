Tarea dejada en el feriado
# Procesamiento de Señales Biomédicas: Filtros Digitales para EMG, EKG y EEG

Este repositorio contiene la descripción y ejemplos de implementación de 5 tipos de filtros digitales esenciales para el procesamiento de señales electromiográficas (EMG), electrocardiográficas (ECG) y electroencefalográficas (EEG).

## 1. Filtro Pasa Altas (High-Pass Filter)

**Descripción:** Se utiliza para eliminar la **deriva de línea de base (baseline wander)**. Este ruido es de baja frecuencia y suele ser causado por la respiración del paciente, el movimiento de los electrodos o cambios en la impedancia de la piel.

* **Frecuencias de ruido:** Generalmente por debajo de 0.5 - 1 Hz en ECG/EEG y hasta 10-20 Hz en EMG (artefactos de movimiento).
* **Sustento Científico:** *Akhbari, M., et al. (2013). "A Hierarchical Method for Removal of Baseline Drift from Biomedical Signals".*

### Ejemplo en Python:
```python
import numpy as np
from scipy import signal

def highpass_filter(data, cutoff=0.5, fs=1000, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return signal.filtfilt(b, a, data)´´´
