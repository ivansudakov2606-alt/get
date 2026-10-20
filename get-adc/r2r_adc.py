import time
import RPi.GPIO as GPIO


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        self._closed = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def number_to_dac(self, number):
        number = max(0, min(255, int(number)))

        for i, pin in enumerate(self.bits_gpio):
            bit = (number >> (7 - i)) & 1
            GPIO.output(pin, bit)

        if self.verbose:
            print(f"ЦАП: {number:3d} = 0b{number:08b}")

    def sequential_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)

            comp = GPIO.input(self.comp_gpio)

            if self.verbose:
                print(f"код={number:3d}, компаратор={comp}")

            if comp:
                return number

        return 255

    def successive_approximation_adc(self):
        low = 0
        high = 255

        while low < high:
            mid = (low + high) // 2

            self.number_to_dac(mid)
            time.sleep(self.compare_time)

            comp = GPIO.input(self.comp_gpio)

            if self.verbose:
                print(f"low={low:3d}, high={high:3d}, mid={mid:3d}, компаратор={comp}")

            if comp:
                high = mid
            else:
                low = mid + 1

        return low

    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        return code * self.dynamic_range / 255.0

    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        return code * self.dynamic_range / 255.0

    def cleanup(self):
        if getattr(self, "_closed", False):
            return

        self._closed = True

        try:
            self.number_to_dac(0)
        finally:
            GPIO.cleanup()

    def __del__(self):
        self.cleanup()


if __name__ == "__main__":
    DYNAMIC_RANGE = 3.3

    adc = None

    try:
        adc = R2R_ADC(DYNAMIC_RANGE, compare_time=0.01, verbose=False)

        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение SAR: {voltage:.3f} В")
            time.sleep(0.5)

    except KeyboardInterrupt:
        pass

    finally:
        if adc is not None:
            adc.cleanup()