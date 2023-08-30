import sys,os

def os_dir():
    dir(os)
def sys_dir():
    dir(sys)

def split(str,char):
    return str.split(char)

def splitBySpace(str):
    return str.split()

def find(str,char):
    return str.find(char)


def replace(str,a,b):
    return str.replace(a,b)

def contains(str,char):
    return char in str

def trim(str):
    return str.trip()

def toLowercase(str):
    return str.lower()

def join(str,array):
    return str.join(array)

def charToList(str):
    return list(str)

def strToInt(str):
    return int(str)

def intToStr(num):
    return str(num)

