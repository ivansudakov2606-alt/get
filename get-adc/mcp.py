import time

from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time, plot_sampling_period_hist

DYNAMIC_RANGE = 5.0
DURATION = 3.0

voltage_values = []
time_values = []
adc = None

try:
    adc = MCP3021(DYNAMIC_RANGE, verbose=False)

    start_time = time.time()

    while time.time() - start_time < DURATION:
        voltage_values.append(adc.get_voltage())
        time_values.append(time.time() - start_time)

    plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    plot_sampling_period_hist(time_values)

finally:
    if adc is not None:
        adc.deinit()