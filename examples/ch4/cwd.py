import os, sys


def print_info():
    print("os.getcwd =>", os.getcwd())  # 查看当前工作目录
    print("sys.path =>", sys.path[:6])  # 展示前6个引入的路径


if __name__ == "__main__":
    print_info()
