import os


def create(path, content):
    file = open(path, 'w')
    file.write(content)
    file.close()


def read(path):
    file = open(path)
    return file.read()


def read_as_string(path):
    return open(path).read()


# def readContentAsBytes(path):
#     return open(path).read(N)
def read_as_list(path):
    return open(path).readlines()


def read_as_text(path):
    return open(path).readline()


def is_dir(path):
    os.path.isdir(path)


def is_file(path):
    os.path.isfile(path)


def is_link(path):
    os.path.islink(path)


def is_exists(path):
    os.path.exists(path)


def get_size(path):
    if is_file(path) and is_exists(path):
        return os.path.getsize(path)
    else:
        return -1


# 得到array = [文件夹路径，带扩展名文件名称]
def split_dir_and_file(path):
    return os.path.split(path)


# String 合并路径和文件名
def join_dir_and_file(dir, file):
    return os.path.join(dir, file)


def dir_name(path):
    return os.path.dirname(path)


def file_name(path):
    return os.path.basename(path)


# 获取array=[文件路径不包含扩展名，文件扩展名]
def split_text(path):
    return os.path.splitext(path)


# 文件分割符 \\
def sep():
    return os.sep


# 分割路径
def split_array(path):
    return path.split(os.sep)


# 解决文件路径分割符不规范问题
def format_path(path):
    return os.path.normpath(path)


# 获取当前路径
def cwd():
    return os.getcwd()


# cwd绝对路径,支持.  ..
def abs_path(path):
    os.path.abspath(path)
