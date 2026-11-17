import numpy as np
import matplotlib.pyplot as plt

from const import START, STOP, STEP, VARIANT, VARIANTS

# шаг по тз
def x_range():
    return np.arange(START, STOP + STEP, STEP)


# y1(x) = a * x + b
def y1(x, a, b):
    return a * x + b


# y2(x) = (a + x) + c * cos(b * x)
def y2(x, a, b, c):
    return (a + x) + c * np.cos(b * x)


def main() -> None:
    if VARIANT not in VARIANTS:
        raise ValueError(f"Нет варианта {VARIANT}. Допустимы номера 1–10.")

    p = VARIANTS[VARIANT]

    a = p["a"]
    b = p["b"]
    c = p["c"]

    x = x_range()
    y1_values = y1(x, a, b)
    y2_values = y2(x, a, b, c)

    for xi, y1i, y2i in zip(x, y1_values, y2_values):
        print(f"{xi:8.1f} {y1i:14.4f} {y2i:14.4f}")

    _, axes = plt.subplots(figsize=(p["width"], p["height"]), layout="constrained")

    axes.plot(
        x,
        y1_values,
        color=p["y1_color"],
        linestyle=p["y1_linestyle"],
        linewidth=p["y1_linewidth"],
        label=r"$y_1(x) = ax + b$",
    )

    axes.scatter(
        x,
        y2_values,
        color=p["y2_color"],
        marker=p["y2_marker"],
        s=p["y2_size"],
        label=r"$y_2(x) = (a + x) + c\cos(bx)$",
    )

    label_kw = dict(
        fontsize=p["label_fontsize"],
        color=p["label_color"])

    axes.set_title("Графики функций\n$y_1(x)$ и $y_2(x)$", **label_kw)
    axes.set_xlabel("x", **label_kw)
    axes.set_ylabel("y", **label_kw)
    axes.legend(fontsize=8)

    plt.show()


if __name__ == "__main__":
    main()
