import mcp4725_driver as mcp
import signal_generator as sg
import time


amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000


if __name__ == "__main__":
    try:
        dac = mcp.MCP4725(dynamic_range=(0.0, amplitude), verbose=False)

        t = 0.0
        dt = 1.0 / sampling_frequency

        while True:
            normalized = sg.get_sin_wave_amplitude(signal_frequency, t)
            voltage = normalized * amplitude
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)
            t += dt
    finally:
        dac.deinit()