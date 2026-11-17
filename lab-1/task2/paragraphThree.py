import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cbook import boxplot_stats

SIZE = 50
LOW = 1
HIGH = 100
OUTLIER = 250
BINS = 5
REPLACE_INDEX = 10


def make_sample() -> np.ndarray:
    sample = np.random.randint(LOW, HIGH + 1, size=SIZE)
    sample[REPLACE_INDEX] = OUTLIER
    return sample


def histogram(sample: np.ndarray) -> None:
    _, axes = plt.subplots(figsize=(8, 5), layout="constrained")
    axes.hist(sample, bins=BINS, edgecolor="black")
    axes.set_title("Гистограмма случайных чисел")
    axes.set_xlabel("Значение")
    axes.set_ylabel("Частота")


def boxplot(sample: np.ndarray) -> None:
    _, axes = plt.subplots(figsize=(6, 5), layout="constrained")
    axes.boxplot(sample)
    axes.set_title("Диаграмма размаха")
    axes.set_ylabel("Значение")
    axes.set_xticks([1], ["Выборка"])


def print_histogram(sample: np.ndarray) -> None:
    counts, edges = np.histogram(sample, bins=BINS)
    print("Гистограмма, 5 бинов:")
    last = len(counts) - 1
    for index, (count, left, right) in enumerate(zip(counts, edges[:-1], edges[1:])):
        bracket = "]" if index == last else ")"
        print(f"  [{left:6.1f}; {right:6.1f}{bracket}  {count:2d}")

    print(
        f"Значение {OUTLIER} растягивает шкалу от {sample.min():.0f} до {OUTLIER}. "
        f"Остальные {SIZE - 1} чисел лежат не выше {HIGH} и попадают в первые два бина "
        f"({int(counts[0])} и {int(counts[1])}). "
        "Средние бины пустые, последний содержит только выброс."
    )


def print_boxplot(sample: np.ndarray) -> None:
    stats = boxplot_stats(sample)[0]
    q1 = stats["q1"]
    median = stats["med"]
    q3 = stats["q3"]
    iqr = q3 - q1
    fliers = stats["fliers"]

    print("Диаграмма размаха:")
    print(f"  медиана                 {median:.1f}")
    print(f"  нижний квартиль Q1      {q1:.1f}")
    print(f"  верхний квартиль Q3     {q3:.1f}")
    print(f"  межквартильный размах   {iqr:.1f}")
    print(f"  нижний ус               {stats['whislo']:.1f}")
    print(f"  верхний ус               {stats['whishi']:.1f}")
    if len(fliers) == 0:
        print("  выбросов нет")
    else:
        values = ", ".join(f"{value:.0f}" for value in fliers)
        print(f"  выбросы                 {values}")
        print(
            "250 лежит выше границы Q3 + 1,5·IQR, "
            "поэтому на диаграмме это единственный выброс. "
            "Медиана и квартили считаются по основной массе значений от 1 до 100."
        )


def main() -> None:
    np.random.seed(0)
    sample = make_sample()

    print(sample)
    print(f"Элемент с индексом {REPLACE_INDEX} заменён на {OUTLIER}.")
    print_histogram(sample)
    print_boxplot(sample)

    histogram(sample)
    boxplot(sample)
    plt.show()


if __name__ == "__main__":
    main()
