import os


def start_file(file):
    os.startfile(file)


def start_file_html():
    os.startfile("file.html")


def start_file_doc():
    os.startfile("file.doc")


def start_file_py():
    os.startfile("file.py")


if __name__ == "__main__":
    start_file_html()
