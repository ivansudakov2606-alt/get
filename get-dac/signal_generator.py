import numpy as np
import time


##Синус от 0 до 1
def get_sin_wave_amplitude(freq, t):
    return (np.sin(2 * np.pi * freq * t) + 1) / 2


def wait_for_sampling_period(sampling_frequency):
    time.sleep(1.0 / sampling_frequency)

##Треугольник от 0 до 1
def get_triangle_wave_amplitude(freq, t):
    phase = (t * freq) % 1.0
    return 1 - abs(2 * phase - 1)