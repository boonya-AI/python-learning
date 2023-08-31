a = 21
b = 10
c = 0


def add(a, b):
    c = a + b
    print("1 - c 的值为：", c)


def substract(a, b):
    c = a - b
    print("2 - c 的值为：", c)


def multiply(a, b):
    c = a * b
    print("3 - c 的值为：", c)


def devide(a, b):
    c = a / b
    print("4 - c 的值为：", c)


def mo(a, b):
    c = a % b
    print("5 - c 的值为：", c)


def multiply_simple(a, b):
    # 修改变量 a 、b 、c
    a = 2
    b = 3
    c = a ** b
    print("6 - c 的值为：", c)


def devide_cast(a, b):
    a = 10
    b = 5
    c = a // b
    print("7 - c 的值为：", c)
