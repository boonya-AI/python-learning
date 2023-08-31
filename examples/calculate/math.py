# Python math 模块提供了许多对浮点数的数学运算函数。
# Python cmath 模块包含了一些用于复数运算的函数。
import math, cmath


class Math:

    # CONSTRUCT
    def __init__(self, x):
        self.x = x

    #  返回数字的绝对值，如abs(-10) 10
    def abs(self):
        print(abs(self.x))

    #  返回数字的上入整数，如math.ceil(4.1) 5
    def ceil(self):
        print(math.ceil(self.x))


class CMath:

    # CONSTRUCT
    def __init__(self, x):
        self.x = x

    def sin(self):
        print(cmath.sin(self.x))

    def cos(self):
        print(cmath.cos(self.x))


if __name__ == "__main__":
    print(math.e)
    print(math.pi)
    print(dir(math))
    print(dir(cmath))
    m = Math(-10.57)
    m.abs()
    m.ceil()
    cm = CMath(10.57)
    cm.sin()
    cm.cos()
