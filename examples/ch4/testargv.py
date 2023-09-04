import os, sys

print(sys.argv)


def print_argv():
    print("python argv.py spam eggs cheese")
    os.system("python argv.py spam eggs cheese")
    os.system("python argv.py -i data.txt -o result.txt")


def print_argv2():
    print("python argv2.py spam eggs cheese")
    os.system("python argv2.py")
    os.system("python argv2.py -i data.txt -o result.txt")


if __name__ == "__main__":
    print_argv()
    print_argv2()