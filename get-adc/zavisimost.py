
import csv
import time
from datetime import datetime
from pathlib import Path
import adc_plot
from mcp3021_driver import MCP3021

SUPPLY_VOLTAGE = 5.0 
DURATION = 30.0    
PAUSE = 0.02


def main():
    times = []
    voltages = []
    adc = None
    try:
        adc = MCP3021(SUPPLY_VOLTAGE)
        start = time.perf_counter()
        print("Запись началась. Нажми и отпусти кнопку RC-платы.")
        while time.perf_counter() - start < DURATION:
            voltage = adc.get_voltage()
            elapsed = time.perf_counter() - start
            if elapsed > DURATION:
                break
            times.append(elapsed)
            voltages.append(voltage)
            print(f"{elapsed:6.2f} с | {voltage:.4f} В")
            time.sleep(PAUSE)
    except KeyboardInterrupt:
        print("\nЗапись остановлена.")
    finally:
        if adc is not None:
            adc.deinit()

    if times:
        name = datetime.now().strftime("rc_data_%Y%m%d_%H%M%S_%f.csv")
        csv_path = Path(__file__).resolve().parent / name
        with csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["time_s", "voltage_V"])
            writer.writerows(zip(times, voltages))
        print(f"Сохранено {len(times)} измерений: {csv_path}")

        adc_plot.plot_voltage_vs_time(times, voltages, SUPPLY_VOLTAGE)


if __name__ == "__main__":
    main()