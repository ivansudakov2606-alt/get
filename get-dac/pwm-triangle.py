import pwm_dac as pwm
import signal_generator as sg
import time


amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

gpio_pin = 12
pwm_frequency = 500


if __name__ == "__main__":
    try:
        dac = pwm.PWM_DAC(gpio_pin, pwm_frequency, dynamic_range=amplitude, verbose=False)

        t = 0.0
        dt = 1.0 / sampling_frequency

        while True:
            normalized = sg.get_triangle_wave_amplitude(signal_frequency, t)
            voltage = normalized * amplitude
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)
            t += dt
    finally:
        dac.deinit()