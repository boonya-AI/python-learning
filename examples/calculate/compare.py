# !/usr/bin/python
# -*- coding: UTF-8 -*-

a = 21
b = 10
c = 0


def equals(a, b):
    if a == b:
        print("1 - a 等于 b")
    else:
        print("1 - a 不等于 b")


def not_equals(a, b):
    if a != b:
        print("2 - a 不等于 b")
    else:
        print("2 - a 等于 b")


def little_than():
    if a < b:
        print("4 - a 小于 b")
    else:
        print("4 - a 大于等于 b")


def bigger_than():
    if a > b:
        print("5 - a 大于 b")
    else:
        print("5 - a 小于等于 b")


def little_or_equals_than():
    # 修改变量 a 和 b 的值
    a = 5
    b = 20
    if a <= b:
        print("6 - a 小于等于 b")
    else:
        print("6 - a 大于  b")


def bigger_or_equals_than():
    if b >= a:
        print("7 - b 大于等于 a")
    else:
        print("7 - b 小于 a")
