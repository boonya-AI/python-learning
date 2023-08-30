a = 10
b = 20


def boolean_and():
    if a and b:
        print("1 - 变量 a 和 b 都为 True")
        return 1
    else:
        print("1 - 变量 a 和 b 有一个不为 True")
        return 0


def boolean_or():
    if a or b:
        print("2 - 变量 a 和 b 都为 True，或其中一个变量为 True")
        return 1
    else:
        print("2 - 变量 a 和 b 都不为 True")
        return 0


def boolean_and_with_param(number):
    a = number
    if a and b:
        print("3 - 变量 a 和 b 都为 True")
        return 1
    else:
        print("3 - 变量 a 和 b 有一个不为 True")
        return 0


def boolean_and_param(a, b):
    if a or b:
        print("4 - 变量 a 和 b 都为 True，或其中一个变量为 True")
        return 1
    else:
        print("4 - 变量 a 和 b 都不为 True")
        return 1


def boolean_not_and_param(a, b):
    if not (a and b):
        print("5 - 变量 a 和 b 都为 False，或其中一个变量为 False")
    else:
        print("5 - 变量 a 和 b 都为 True")
