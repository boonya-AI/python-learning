def while_loop(count):
    while (count < 9):
        print('The count is:', count)
        count = count + 1
    print("Good bye!")


# continue  用法
def while_continue(i):
    while i < 10:
        i += 1
        if i % 2 > 0:  # 非双数时跳过输出
            continue
        print(i)  # 输出双数2、4、6、8、10


# break 用法
def while_break(i):
    while 1:  # 循环条件为1必定成立
        print(i)  # 输出1~10
        i += 1
        if i > 10:  # 当i大于10时跳出循环
            break


def while_true():
    num = input("Enter a number  :")
    print("You entered: ", num)
    condition = int(num) == 1
    print("num == 1 : condition", condition)
    while condition:  # 该条件永远为true，循环将无限执行下去
        print("this is a true while")

    print("Good bye!")


def while_else():
    count = 0
    while count < 5:
        print(count, " is  less than 5")
        count = count + 1
    else:
        print(count, " is not less than 5")


def while_print_simple():
    flag = 1
    while (flag): print('Given flag is really true!')
    print("Good bye!")


def while_while():
    i = 2
    while (i < 100):
        j = 2
        while (j <= (i / j)):
            if not (i % j): break
            j = j + 1
        if (j > i / j): print(i, " 是素数")
        i = i + 1
    print("Good bye!")


if __name__ == "__main__":
    while_true()
