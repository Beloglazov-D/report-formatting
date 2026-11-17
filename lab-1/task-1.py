import numpy as np


class ArrayTasks:
    def __init__(self):
        self.evenlyArr = None
        self.twodimensionalB = None
        self.twodimensionalC = None
        self.twodimensionalD = None

        self.createEvenlyArr()
        self.createTwodimensionalB()
        self.createTwodimensionalC()


    def showEvenlyArr(self):
        print('Одномерный массив:\n', self.evenlyArr)

    def showTwodimensionalC(self):
        print("Массив C:\n", self.twodimensionalC)
    
    # 1 Сформировать одномерный массив a (размерность 10) с использованием функции linspace
    def createEvenlyArr(self):
        self.evenlyArr = np.linspace(0, 10, 10, 'int')

    # 2 Сформировать два двумерных массива b и c размера (4,4).
    def createTwodimensionalB(self):
        self.twodimensionalB = np.empty((4, 4), 'int')

    # 2 Массив b ввести с клавиатуры. Массив c заполнить случайными числами
    def showTwodimensionalB(self):
        print("Введите массив B: 4 строки по 4 числа через пробел")
        for i in range(4):
            self.twodimensionalB[i] = input().split()
        print("Массив B:\n", self.twodimensionalB)
    
    # 2 Массив c заполнить случайными числами
    def createTwodimensionalC(self):
        self.twodimensionalC = np.random.randint(0, 10, (4, 4), 'int')

    # 3 Вывести на экран каждый массив и его атрибуты (shape, size, ndim, dtype)
    def showParametersArrays(self):
        print("Одномерный массив:")
        print(self.evenlyArr)
        print("shape:", self.evenlyArr.shape)
        print("size:", self.evenlyArr.size)
        print("ndim:", self.evenlyArr.ndim)
        print("dtype:", self.evenlyArr.dtype)

        print("Массив B:")
        print(self.twodimensionalB)
        print("shape:", self.twodimensionalB.shape)
        print("size:", self.twodimensionalB.size)
        print("ndim:", self.twodimensionalB.ndim)
        print("dtype:", self.twodimensionalB.dtype)

        print("Массив C:")
        print(self.twodimensionalC)
        print("shape:", self.twodimensionalC.shape)
        print("size:", self.twodimensionalC.size)
        print("ndim:", self.twodimensionalC.ndim)
        print("dtype:", self.twodimensionalC.dtype)
    
    # 4 Провести сортировку элементов массива a по возрастанию
    def sortEvenlyArr(self):
        self.evenlyArr.sort()
        print("Отсортированный массив:")
        print(self.evenlyArr)

    # 5 Сформировать из исходного массива a двумерный массив размера (2,5);
    def reshapeEvenlyArr(self):
        reshapedArr = self.evenlyArr.reshape(2, 5)
        print("Двумерный массив размера (2, 5):")
        print(reshapedArr)

    # 6 Перемножить массивы b и c
    def multiplyArrays(self):
        result = np.dot(self.twodimensionalB, self.twodimensionalC)
        print("Произведение массивов B и C:")
        print(result)

    # 7 Преобразовать массив c в одномерный
    def flattenArrayC(self):
        oneDimensionalC = self.twodimensionalC.flatten()
        print("Одномерный массив C:")
        print(oneDimensionalC)

    # 8 Сформировать массив размера (2,3) из последних 6 элементов массива b
    def lastSixFromB(self):
        oneDimensionalB = self.twodimensionalB.flatten()
        lastSix = oneDimensionalB[-6:]
        result = lastSix.reshape(2, 3)
        print("Массив (2, 3) из последних 6 элементов B:")
        print(result)

    # 9 Сформировать и вывести на экран новый массив d, соединив массивы b и c по вертикали
    def createArrayD(self):
        self.twodimensionalD = np.vstack((self.twodimensionalB, self.twodimensionalC))
        print("Массив D (B и C по вертикали):")
        print(self.twodimensionalD)

    # 10 Удалить 2 и 3 столбец массива d
    def deleteColumnsD(self):
        result = np.delete(self.twodimensionalD, [1, 2], axis=1)
        print("Массив D без 2 и 3 столбца:")
        print(result)

    def run(self):
        self.showEvenlyArr()
        self.showTwodimensionalB()
        self.showTwodimensionalC()
        self.showParametersArrays()
        self.sortEvenlyArr()
        self.reshapeEvenlyArr()
        self.multiplyArrays()
        self.flattenArrayC()
        self.lastSixFromB()
        self.createArrayD()
        self.deleteColumnsD()


if __name__ == "__main__":
    ArrayTasks().run()
