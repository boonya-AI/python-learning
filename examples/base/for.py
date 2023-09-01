def for_loop():
    words = ['cat', 'window', 'defenestrate']
    for w in words:
        print(w, len(w))


def for_loop_range(num):
    for i in range(num):
        print(i)


def for_loop_range_array_simple():
    a = ['Mary', 'had', 'a', 'little', 'lamb']
    for i in range(len(a)):
        print(i, a[i])


def for_loop_range_list_ab(a, b):
    list(range(a, b))


def for_loop_range_list_abc(a, b, c):
    list(range(a, b, c))


def for_loop_range_list_simple():
    list(range(-10, -100, -30))


def for_loop_break_simple():
    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, 'equals', x, '*', n // x)
                break
        else:
            # loop fell through without finding a factor
            print(n, 'is a prime number')


def for_loop_continue_simple():
    for num in range(2, 10):
        if num % 2 == 0:
            print("Found an even number", num)
            continue
        print("Found an odd number", num)


def while_pass():
    while True:
        pass  # Busy-wait for keyboard interrupt (Ctrl+C)
    class MyEmptyClass:
        pass
    def initlog(*args):
        pass  # Remember to implement this!


