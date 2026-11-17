import numpy as np
import matplotlib.pyplot as plt

MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь"]

# объёмы продаж, млн руб.
ENTERPRISE_1 = np.array([120, 135, 150, 142, 168, 190])
ENTERPRISE_2 = np.array([98, 110, 125, 160, 145, 175])


def bar_chart() -> None:
    x = np.arange(len(MONTHS))
    width = 0.35

    _, axes = plt.subplots(figsize=(8, 5), layout="constrained")

    axes.bar(x - width / 2, ENTERPRISE_1, width, label="Предприятие 1")
    axes.bar(x + width / 2, ENTERPRISE_2, width, label="Предприятие 2")

    axes.set_title("Объёмы продаж двух предприятий")
    axes.set_xlabel("Месяц")
    axes.set_ylabel("Объём продаж, млн руб.")
    axes.set_xticks(x, MONTHS)
    axes.legend()


def pie_chart() -> None:
    _, axes = plt.subplots(figsize=(6, 6), layout="constrained")

    axes.pie(
        ENTERPRISE_1,
        labels=MONTHS,
        autopct="%1.1f%%",
    )
    axes.set_title("Продажи первого предприятия")


def main() -> None:
    print(f"{'Месяц':<12} {'Предприятие 1':>14} {'Предприятие 2':>14}")
    for month, sales1, sales2 in zip(MONTHS, ENTERPRISE_1, ENTERPRISE_2):
        print(f"{month:<12} {sales1:14.0f} {sales2:14.0f}")

    bar_chart()
    pie_chart()
    plt.show()


if __name__ == "__main__":
    main()
