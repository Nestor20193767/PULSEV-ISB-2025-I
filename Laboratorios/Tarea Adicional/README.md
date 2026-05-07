# Procesamiento de Señales Biomédicas: Filtros Digitales para EMG, EKG y EEG

Este repositorio contiene la descripción y ejemplos de implementación de 5 tipos de filtros digitales esenciales para el procesamiento de señales electromiográficas (EMG), electrocardiográficas (ECG) y electroencefalográficas (EEG).

---

## 1. Filtro Pasa Altas (High-Pass Filter)

**Descripción:**
Se utiliza para eliminar la **deriva de línea de base (baseline wander)**. Este ruido es de baja frecuencia y suele ser causado por la respiración del paciente, el movimiento de los electrodos o cambios en la impedancia de la piel.

* **Frecuencias de ruido:** Generalmente por debajo de 0.5 - 1 Hz en ECG/EEG y hasta 10-20 Hz en EMG (artefactos de movimiento).
* **Sustento Científico:** *Akhbari, M., et al. (2013). "A Hierarchical Method for Removal of Baseline Drift from Biomedical Signals".*

### Ejemplo en Python

```python
import numpy as np
from scipy import signal

def highpass_filter(data, cutoff=0.5, fs=1000, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return signal.filtfilt(b, a, data)
```

---

## 2. Filtro Pasa Bajos (Low-Pass Filter)

**Descripción:**
Diseñado para atenuar el ruido de alta frecuencia, como la interferencia electromagnética de equipos cercanos, ruido térmico o el ruido muscular cruzado (en el caso de EEG/ECG). También previene el *aliasing* antes de la digitalización.

* **Frecuencias de ruido:** Por encima de 50-70 Hz en EEG, 100-150 Hz en ECG y 500 Hz en EMG.
* **Sustento Científico:** *Sharma, A., et al. (2016). "Modeling of EXG (ECG, EMG and EEG) non-idealities using MATLAB". IEEE Xplore.*

### Ejemplo en Python

```python
def lowpass_filter(data, cutoff=150, fs=1000, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return signal.filtfilt(b, a, data)
```

---

## 3. Filtro Notch (Rechaza Banda)

**Descripción:**
Elimina específicamente la interferencia de la línea eléctrica (*Power-line Interference*). En el contexto de Perú, esta interferencia ocurre a los 60 Hz. Es crítico porque esta frecuencia se encuentra justo dentro del espectro de interés de la mayoría de las bioseñales.

* **Frecuencias de ruido:** 60 Hz (y sus armónicos: 120 Hz, 180 Hz).
* **Sustento Científico:** *Piskorowski, J. (2012). "Powerline interference rejection from sEMG signal using notch filter with transient suppression". IEEE.*

### Ejemplo en Python

```python
def notch_filter(data, f0=60.0, fs=1000, Q=30):
    b, a = signal.iirnotch(f0, Q, fs)
    return signal.filtfilt(b, a, data)
```

---

## 4. Filtro Pasa Banda (Band-Pass Filter)

**Descripción:**
Permite aislar una banda de frecuencia específica donde se concentra la mayor potencia de la señal fisiológica, eliminando simultáneamente ruidos por debajo y por encima de dicha banda. Es ideal para extraer el complejo QRS en ECG o ritmos específicos en EEG.

* **Frecuencias de interés:** 0.5-100 Hz (ECG), 0.5-40 Hz (EEG), 20-500 Hz (EMG).
* **Sustento Científico:** *Jirapong, P., et al. (2025). "High-Order Universal Filter for Bio-Signal Processing Applications". MDPI Applied Sciences.*

### Ejemplo en Python

```python
def bandpass_filter(data, lowcut=0.5, highcut=40.0, fs=1000, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, data)
```

---

## 5. Filtro Adaptativo (Adaptive Filter)

**Descripción:**
A diferencia de los filtros fijos, los adaptativos ajustan sus coeficientes dinámicamente. Son extremadamente efectivos para suprimir artefactos de movimiento no estacionarios donde el espectro del ruido se solapa con el de la señal.

* **Frecuencias de ruido:** Variable, típicamente artefactos de movimiento entre 0-20 Hz que cambian con la actividad del sujeto.
* **Sustento Científico:** *Xu, L., et al. (2022). "Motion-artifact reduction in capacitive heart-rate measurements by adaptive filtering". IEEE.*

### Ejemplo en Python (LMS simplificado)

```python
def adaptive_lms_filter(signal_in, noise_ref, mu=0.01, order=32):
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

## Bibliografía

1. Akhbari, M., et al. (2013). *A Hierarchical Method for Removal of Baseline Drift from Biomedical Signals: Application in ECG Analysis*. PMC.
2. Sharma, A., et al. (2016). *Modeling of EXG (ECG, EMG and EEG) non-idealities using MATLAB*. IEEE Xplore.
3. Piskorowski, J. (2012). *Powerline interference rejection from sEMG signal using notch filter with transient suppression*. IEEE International Instrumentation and Measurement Technology Conference.
4. Jirapong, P., et al. (2025). *0.5-V High-Order Universal Filter for Bio-Signal Processing Applications*. MDPI Applied Sciences.
5. Xu, L., et al. (2022). *Motion-artifact reduction in capacitive heart-rate measurements by adaptive filtering*. IEEE.

