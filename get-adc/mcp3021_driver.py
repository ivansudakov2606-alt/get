import time
import smbus


class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose
        self._closed = False

    def deinit(self):
        if self._closed:
            return
        self._closed = True
        try:
            self.bus.close()
        except Exception:
            pass

    def __del__(self):
        self.deinit()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)

        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)

        if self.verbose:
            print(
                f"Принятые данные: 0x{data:04x}, "
                f"Старший байт: 0x{upper_data_byte:02x}, "
                f"Младший байт: 0x{lower_data_byte:02x}, "
                f"Число: {number} ({number:010b})"
            )

        return number

    def get_voltage(self):
        """Возвращает измеренное напряжение в вольтах (10-битный АЦП)."""
        number = self.get_number()
        return number * self.dynamic_range / 1023.0


if __name__ == "__main__":
    DYNAMIC_RANGE = 5.0
    adc = None
    try:
        adc = MCP3021(DYNAMIC_RANGE, verbose=False)
        while True:
            voltage = adc.get_voltage()
            print(f"MCP3021: {voltage:.3f} В")
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        if adc is not None:
            adc.deinit()