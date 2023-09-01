def fib(n):  # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()


# 只给出必选实参：ask_ok('Do you really want to quit?')
# 给出一个可选实参：ask_ok('OK to overwrite the file?', 2)
# 给出所有实参：ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!')
def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)


# kwarg=value 关键字参数
def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")


def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])


def standard_arg(arg):
    print(arg)


def pos_only_arg(arg, /):
    print(arg)


def kwd_only_arg(*, arg):
    print(arg)


def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)


def foo(name, /, **kwds):
    return 'name' in kwds


def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))


def concat(*args, sep="/"):
    return sep.join(args)


def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")


# lambda
def lambda_incrementor(n):
    return lambda x: x + n


def lambda_array_sort():
    pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
    pairs.sort(key=lambda pair: pair[1])
    print(pairs)


# 函数字符串
def my_function():
    """Do nothing, but document it.

    No, really, it doesn't do anything.
    """
    pass


# 函数注解
def f_annotation(ham: str, eggs: str = 'eggs') -> str:
    print("Annotations:", f.__annotations__)
    print("Arguments:", ham, eggs)
    return ham + ' and ' + eggs


if __name__ == "__main__":
    # Now call the function we just defined:
    fib(2000)

    parrot(1000)  # 1 positional argument
    parrot(voltage=1000)  # 1 keyword argument
    parrot(voltage=1000000, action='VOOOOOM')  # 2 keyword arguments
    parrot(action='VOOOOOM', voltage=1000000)  # 2 keyword arguments
    parrot('a million', 'bereft of life', 'jump')  # 3 positional arguments
    parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword

    cheeseshop("Limburger", "It's very runny, sir.",
               "It's really very, VERY runny, sir.",
               shopkeeper="Michael Palin",
               client="John Cleese",
               sketch="Cheese Shop Sketch")
    print(foo(1, **{'name': 2}))

    concat("earth", "mars", "venus")
    concat("earth", "mars", "venus", sep=".")

    d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
    parrot(**d)

    # lambda 表达式
    f = lambda_incrementor(42)
    f(0)
    f(1)

    lambda_array_sort()

    print(my_function.__doc__)

    f_annotation('spam')
