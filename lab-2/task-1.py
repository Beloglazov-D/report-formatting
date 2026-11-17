from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "Salary.csv"
EXCEL_PATH = BASE_DIR / "Salary_cleaned.xlsx"

NUMERIC_COLUMNS = ["yrs.service", "salary", "age", "yrs.since.phd"]
NUMERIC_LABELS = {
    "yrs.service": "Стаж",
    "salary": "Зарплата",
    "age": "Возраст",
    "yrs.since.phd": "Стаж после защиты",
}
RANK_ORDER = ["AsstProf", "AssocProf", "Prof"]
RANK_LABELS = {
    "AsstProf": "Ассистент",
    "AssocProf": "Доцент",
    "Prof": "Профессор",
}
SUMMARY_COLUMNS = ["yrs.since.phd", "yrs.service", "salary", "age"]
HIST_BINS = 20


class SalaryTasks:
    def __init__(self):
        self.df = None

    def textColumns(self):
        # В pandas 3 текстовые столбцы имеют тип str
        return self.df.select_dtypes(include=["object", "str"]).columns

    def iqrBounds(self, series):
        quartile1 = series.quantile(0.25)
        quartile3 = series.quantile(0.75)
        iqr = quartile3 - quartile1
        return quartile1 - 1.5 * iqr, quartile3 + 1.5 * iqr

    def describeDistribution(self, series, title):
        mean = series.mean()
        median = series.median()
        if mean > median * 1.05:
            shape = "среднее выше медианы, распределение смещено вправо"
        elif median > mean * 1.05:
            shape = "медиана выше среднего, распределение смещено влево"
        else:
            shape = "среднее близко к медиане"
        print(
            f"{title}: min = {series.min():.1f}, max = {series.max():.1f}, "
            f"среднее = {mean:.1f}, медиана = {median:.1f}. {shape}."
        )

    def plotHistograms(self):
        _, axes = plt.subplots(2, 2, figsize=(10, 8), layout="constrained")
        for ax, column in zip(axes.ravel(), NUMERIC_COLUMNS):
            label = NUMERIC_LABELS[column]
            ax.hist(self.df[column].dropna(), bins=HIST_BINS, edgecolor="black")
            ax.set_title(label)
            ax.set_xlabel(label)
            ax.set_ylabel("Количество")

    def plotBoxplots(self):
        _, axes = plt.subplots(2, 2, figsize=(10, 8), layout="constrained")
        for ax, column in zip(axes.ravel(), NUMERIC_COLUMNS):
            label = NUMERIC_LABELS[column]
            ax.boxplot(self.df[column].dropna())
            ax.set_title(label)
            ax.set_ylabel(label)
            ax.set_xticks([1], [label])

    def plotRankCounts(self, counts):
        labels = [RANK_LABELS[rank] for rank in counts.index]
        _, axes = plt.subplots(figsize=(7, 5), layout="constrained")
        axes.bar(labels, counts.values)
        axes.set_title("Количество преподавателей по должностям")
        axes.set_ylabel("Количество")

    def plotDisciplineShares(self, shares):
        labels = [RANK_LABELS[rank] for rank in shares.index]
        x = np.arange(len(labels))
        width = 0.35

        _, axes = plt.subplots(figsize=(8, 5), layout="constrained")
        axes.bar(x - width / 2, shares["A"], width, label="A — теоретическая")
        axes.bar(x + width / 2, shares["B"], width, label="B — практическая")
        axes.set_xticks(x, labels)
        axes.set_ylabel("Доля, %")
        axes.set_ylim(0, 100)
        axes.set_title("Доля дисциплин A и B по должностям")
        axes.legend()

    # 1 Загрузить данные из файла Salary.csv
    def loadData(self):
        self.df = pd.read_csv(CSV_PATH)
        print("Данные загружены:", len(self.df), "строк,", self.df.shape[1], "столбцов")

    # 2 Вывести первые 10 строк полученного датафрейма
    def showHead(self):
        print("Первые 10 строк:")
        print(self.df.head(10))

    # 3 Вывести общую информацию о датафрейме методом info()
    def showInfo(self):
        print("Общая информация:")
        self.df.info()
        missing = self.df.isna().sum()
        filled = [name for name in self.df.columns if missing[name] == 0]
        top = missing.idxmax()
        print(
            f"В датафрейме {len(self.df)} наблюдений и {self.df.shape[1]} столбцов. "
            "Числовые столбцы: Unnamed, yrs.since.phd, yrs.service, salary, age. "
            "Текстовые столбцы: rank, discipline, gender. "
            f"Полностью заполнены: {', '.join(filled)}. "
            f"Пропуски есть в {int((missing > 0).sum())} столбцах, "
            f"больше всего в {top} ({int(missing[top])})."
        )

    # 4 Уникальные значения и их количество для столбцов типа object
    def showUniqueValues(self):
        print("Уникальные значения текстовых столбцов:")
        for column in self.textColumns():
            print(column)
            print(self.df[column].value_counts(dropna=False))
        print(
            "Должность принимает 3 значения, чаще всего Prof. "
            "Дисциплина — A или B, чаще A (теоретическая). "
            "Пол — Male или Female, мужчин существенно больше, чем женщин."
        )

    # 5 Статистические характеристики: отдельно числовые столбцы и столбцы object
    def showDescribe(self):
        print("Числовые столбцы:")
        print(self.df.select_dtypes(include="number").describe())
        print("Текстовые столбцы:")
        print(self.df[self.textColumns()].describe())
        for column in NUMERIC_COLUMNS:
            self.describeDistribution(self.df[column].dropna(), NUMERIC_LABELS[column])

        age_gap = (self.df["age"] - self.df["yrs.service"]).dropna()
        print(
            "Unnamed — идентификатор сотрудника, его минимум и максимум описывают номера, "
            "а не свойства преподавателей. "
            f"Разница возраста и стажа постоянна и равна {age_gap.iloc[0]:.0f}: "
            "возраст в этих данных восстанавливается из стажа."
        )
        service = self.df["yrs.service"].dropna()
        salary = self.df["salary"].dropna()
        age = self.df["age"].dropna()
        phd = self.df["yrs.since.phd"].dropna()
        print(
            f"У стажа максимум {service.max():.0f} при верхней квартили {service.quantile(0.75):.0f}, "
            f"у возраста максимум {age.max():.0f}, "
            f"у зарплаты максимум {salary.max():.0f} при медиане {salary.median():.0f}, "
            f"у стажа после защиты максимум {phd.max():.0f} при верхней квартили {phd.quantile(0.75):.0f}. "
            "Это признаки выбросов, их подтверждают диаграммы размаха."
        )

    # 6 Гистограммы и диаграммы размаха, удаление строк с выбросами
    def removeOutliers(self):
        self.plotHistograms()
        self.plotBoxplots()

        outlier_mask = pd.Series(False, index=self.df.index)
        columns = ["Unnamed", "rank", "yrs.since.phd", "yrs.service", "salary", "age"]
        for column in NUMERIC_COLUMNS:
            lower, upper = self.iqrBounds(self.df[column].dropna())
            column_outliers = self.df[column].lt(lower) | self.df[column].gt(upper)
            outlier_mask |= column_outliers.fillna(False)
            print(
                f"{column}: границы выбросов [{lower:.1f}; {upper:.1f}], "
                f"выбросов: {int(column_outliers.sum())}"
            )
            if column_outliers.any():
                print(self.df.loc[column_outliers, columns])

        print("Строк с выбросом хотя бы в одном числовом столбце:", int(outlier_mask.sum()))
        self.df = self.df.loc[~outlier_mask].copy()
        print("Строк после удаления выбросов:", len(self.df))
        print(
            "Выбросы — нетипично большой стаж (57, 60 и 141), "
            "возраст 77, 80 и 161 и зарплата выше верхней границы ящика. "
            "Стаж после защиты 45 тоже выходит за границу 1.5 IQR. "
            "Эти строки удалены. На гистограммах им соответствуют длинные правые хвосты, "
            "на диаграммах размаха — точки за усами."
        )

    # 7 Удалить нетипичные значения фильтрацией датафрейма
    def filterRows(self):
        phd_exceeds_service = self.df["yrs.since.phd"] > self.df["yrs.service"]
        unusual_age = self.df["age"].lt(18) | self.df["age"].gt(90)
        started_too_young = (self.df["age"] - self.df["yrs.service"]) <= 18
        print(
            "Стаж после защиты больше общего стажа:",
            int(phd_exceeds_service.fillna(False).sum()),
        )
        print("Возраст меньше 18 или больше 90:", int(unusual_age.fillna(False).sum()))
        print("Возраст минус стаж не больше 18:", int(started_too_young.fillna(False).sum()))
        self.df = self.df.loc[
            ~(
                phd_exceeds_service.fillna(False)
                | unusual_age.fillna(False)
                | started_too_young.fillna(False)
            )
        ].copy()
        print("Строк после фильтрации:", len(self.df))
        print(
            "Удалены строки, где стаж после защиты больше общего стажа. "
            "Возраст 161 уже удалён как выброс, других возрастов вне интервала 18–90 нет. "
            "Разница возраста и стажа во всех заполненных строках равна 20, "
            "поэтому условие «не больше 18» ни одной строки не отсекает."
        )

    # 8 Вывести количество пропущенных значений в каждом столбце
    def showMissing(self):
        print("Пропущенные значения:")
        print(self.df.isna().sum())

    # 9 В столбце salary заменить пропуски средним значением
    def fillSalary(self):
        salary_missing = int(self.df["salary"].isna().sum())
        salary_mean = self.df["salary"].mean()
        self.df["salary"] = self.df["salary"].fillna(salary_mean)
        print(f"Пропусков в salary: {salary_missing}. Подставлено среднее {salary_mean:.2f}.")

    # 10 В столбце discipline заменить пропуски наиболее частым значением
    def fillDiscipline(self):
        discipline_missing = int(self.df["discipline"].isna().sum())
        discipline_mode = self.df["discipline"].mode(dropna=True).iloc[0]
        self.df["discipline"] = self.df["discipline"].fillna(discipline_mode)
        print(
            f"Пропусков в discipline: {discipline_missing}. "
            f"Подставлено наиболее частое значение {discipline_mode}."
        )

    # 11 Удалить оставшиеся строки с пропущенными значениями
    def dropMissing(self):
        rows_before = len(self.df)
        self.df = self.df.dropna().copy()
        print(f"Удалено строк: {rows_before - len(self.df)}. Осталось строк: {len(self.df)}.")
        print("Пропуски после очистки:")
        print(self.df.isna().sum())

    # 12 Статистические характеристики после очистки данных
    def showDescribeCleaned(self):
        print("Числовые столбцы после очистки:")
        print(self.df.select_dtypes(include="number").describe())
        print("Текстовые столбцы после очистки:")
        print(self.df[self.textColumns()].describe())
        for column in NUMERIC_COLUMNS:
            self.describeDistribution(self.df[column].dropna(), NUMERIC_LABELS[column])
        print(
            f"После очистки осталось {len(self.df)} строк без пропусков. "
            f"Возраст не выше {self.df['age'].max():.0f}, "
            f"стаж не выше {self.df['yrs.service'].max():.0f}, "
            f"стаж после защиты не выше {self.df['yrs.since.phd'].max():.0f}, "
            f"зарплата не выше {self.df['salary'].max():.0f}. "
            "Мода должности по-прежнему Prof, дисциплины — A, пола — Male."
        )

    # 13 Максимальная и минимальная заработная плата
    def showSalaryBounds(self):
        min_salary = self.df["salary"].min()
        max_salary = self.df["salary"].max()
        print(f"Минимальная зарплата: {min_salary:.2f}")
        print(f"Максимальная зарплата: {max_salary:.2f}")
        print(self.df.loc[self.df["salary"].isin([min_salary, max_salary])])

    # 14 Минимум, максимум и среднее по каждой должности
    def showRankStats(self):
        by_rank = (
            self.df.groupby("rank")[SUMMARY_COLUMNS]
            .agg(["min", "max", "mean"])
            .reindex(RANK_ORDER)
        )
        print("Характеристики по должностям:")
        print(by_rank)

        mean_salary = self.df.groupby("rank")["salary"].mean().reindex(RANK_ORDER)
        mean_age = self.df.groupby("rank")["age"].mean().reindex(RANK_ORDER)
        mean_service = self.df.groupby("rank")["yrs.service"].mean().reindex(RANK_ORDER)
        mean_phd = self.df.groupby("rank")["yrs.since.phd"].mean().reindex(RANK_ORDER)
        print(
            "Средняя зарплата растёт вместе с должностью: "
            f"ассистенты {mean_salary['AsstProf']:.0f}, "
            f"доценты {mean_salary['AssocProf']:.0f}, "
            f"профессора {mean_salary['Prof']:.0f}."
        )
        print(
            "Тот же порядок у стажа и стажа после защиты: "
            f"средний стаж {mean_service['AsstProf']:.1f}, "
            f"{mean_service['AssocProf']:.1f} и {mean_service['Prof']:.1f}; "
            f"средний стаж после защиты {mean_phd['AsstProf']:.1f}, "
            f"{mean_phd['AssocProf']:.1f} и {mean_phd['Prof']:.1f}."
        )
        print(
            "Средний возраст повторяет стаж со сдвигом 20 лет: "
            f"{mean_age['AsstProf']:.1f}, {mean_age['AssocProf']:.1f}, {mean_age['Prof']:.1f}. "
            "Профессора в среднем старше, дольше работают и получают больше. "
            "Ассистенты — самая молодая группа с наименьшей средней зарплатой, "
            "доценты находятся между ними."
        )
        print(
            "Самая низкая и самая высокая зарплата в выборке принадлежат профессорам: "
            "разброс внутри этой должности шире, чем у ассистентов и доцентов."
        )

    # 15 Количество преподавателей каждой должности
    def showRankCounts(self):
        rank_counts = self.df["rank"].value_counts().reindex(RANK_ORDER)
        print("Количество преподавателей:")
        print(rank_counts)
        print((rank_counts / rank_counts.sum() * 100).round(1))
        self.plotRankCounts(rank_counts)
        print(
            "Профессоров больше, чем ассистентов и доцентов вместе. "
            f"Профессора — {rank_counts['Prof']} из {int(rank_counts.sum())} "
            f"({rank_counts['Prof'] / rank_counts.sum() * 100:.1f}%). "
            "Ассистентов и доцентов почти поровну. "
            "Выборка в основном описывает профессоров, а не младшие должности."
        )

    # 16 Количество мужчин и женщин для каждой должности
    def showGenderCounts(self):
        gender_counts = pd.crosstab(self.df["rank"], self.df["gender"]).reindex(RANK_ORDER)
        gender_share = (
            pd.crosstab(self.df["rank"], self.df["gender"], normalize="index").reindex(RANK_ORDER)
            * 100
        )
        print("Мужчины и женщины по должностям:")
        print(gender_counts)
        print("Доля, %:")
        print(gender_share.round(1))
        female_share = gender_share["Female"]
        print(
            "Во всех должностях мужчин больше. "
            f"Доля женщин: ассистенты {female_share['AsstProf']:.1f}%, "
            f"доценты {female_share['AssocProf']:.1f}%, "
            f"профессора {female_share['Prof']:.1f}%. "
            "В абсолютных числах женщин больше среди профессоров, "
            "но их доля в этой должности самая низкая."
        )

    # 17 Процентные соотношения дисциплин A и B по должностям
    def showDisciplineShares(self):
        discipline_share = (
            pd.crosstab(self.df["rank"], self.df["discipline"], normalize="index").reindex(RANK_ORDER)
            * 100
        )
        print("Доля дисциплин, %:")
        print(discipline_share.round(1))
        self.plotDisciplineShares(discipline_share)
        print(
            "У ассистентов и доцентов преобладает практическая дисциплина B "
            f"({discipline_share.loc['AsstProf', 'B']:.1f}% и "
            f"{discipline_share.loc['AssocProf', 'B']:.1f}%). "
            f"У профессоров преобладает теоретическая дисциплина A "
            f"({discipline_share.loc['Prof', 'A']:.1f}%). "
            "Ассистенты и доценты по дисциплинам близки друг к другу. "
            "Резкий переход к дисциплине A происходит на должности профессора."
        )

    # 18 Записать полученный датафрейм в файл Excel
    def saveExcel(self):
        self.df.to_excel(EXCEL_PATH, index=False)
        print(f"Файл записан: {EXCEL_PATH}")
        print(f"Строк в файле: {len(self.df)}, столбцов: {self.df.shape[1]}")

    def run(self):
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)

        self.loadData()
        self.showHead()
        self.showInfo()
        self.showUniqueValues()
        self.showDescribe()
        self.removeOutliers()
        self.filterRows()
        self.showMissing()
        self.fillSalary()
        self.fillDiscipline()
        self.dropMissing()
        self.showDescribeCleaned()
        self.showSalaryBounds()
        self.showRankStats()
        self.showRankCounts()
        self.showGenderCounts()
        self.showDisciplineShares()
        self.saveExcel()
        plt.show()


if __name__ == "__main__":
    SalaryTasks().run()
