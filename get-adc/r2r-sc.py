import time

from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time, plot_sampling_period_hist
DYNAMIC_RANGE = 3.3
COMPARE_TIME = 0.0001
DURATION = 3.0
voltage_values = []
time_values = []
adc = None

try:
    adc = R2R_ADC(DYNAMIC_RANGE, compare_time=COMPARE_TIME)

    start_time = time.time()

    while time.time() - start_time < DURATION:
        voltage_values.append(adc.get_sc_voltage())
        time_values.append(time.time() - start_time)

    plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    plot_sampling_period_hist(time_values)

finally:
    if adc is not None:
        adc.cleanup()