def fib(n):  # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()



#只给出必选实参：ask_ok('Do you really want to quit?')
#给出一个可选实参：ask_ok('OK to overwrite the file?', 2)
#给出所有实参：ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!')
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


if __name__ == "__main__":
    # Now call the function we just defined:
    fib(2000)
