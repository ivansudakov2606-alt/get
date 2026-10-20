import matplotlib.pyplot as plt


def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)

    plt.title("Зависимость напряжения на выходе потенциометра от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")

    if time:
        plt.xlim(0, max(time))
    else:
        plt.xlim(0, 1)

    if max_voltage > 0:
        plt.ylim(0, max_voltage * 1.05)
    else:
        plt.ylim(0, 1)

    plt.grid(True)
    plt.show()


def plot_sampling_period_hist(time):
    sampling_periods = []

    for i in range(1, len(time)):
        sampling_periods.append(time[i] - time[i - 1])

    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods)

    plt.title("Распределение периодов измерений")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")

    plt.xlim(0, 0.06)
    plt.grid(True)
    plt.show()