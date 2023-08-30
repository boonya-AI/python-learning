import os


def run_program(file):
    os.system("python {}".format(file))


def run_program_simple():
    os.system("python simple.py")


def run_dir_b():
    os.system("dir /B")


def run_type(file):
    os.system("type {}".format(file))


def run_popen_read(file):
    return os.popen("type {}".format(file)).read()


def run_popen_read_lines(file):
    return os.popen("type {}".format(file)).readlines()


def run_popen_read_lines_from_dir_b():
    return os.popen("dir /B").readlines()


def run_popen_output():
    os.popen("python simple.py").read()
