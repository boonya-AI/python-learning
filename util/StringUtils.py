import sys, os


def os_dir():
    dir(os)


def sys_dir():
    dir(sys)


def split(str, char):
    return str.split(char)


def split_by_space(str):
    return str.split()


def find(str, char):
    return str.find(char)


def replace(str, a, b):
    return str.replace(a, b)


def contains(str, char):
    return char in str


def trim(str):
    return str.trip()


def to_lowercase(str):
    return str.lower()


def join(str, array):
    return str.join(array)


def char_to_list(str):
    return list(str)


def str_to_int(str):
    return int(str)


def int_to_str(num):
    return str(num)
