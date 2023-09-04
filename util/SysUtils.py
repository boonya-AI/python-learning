import sys


def platform():
    return sys.platform


def maxsize():
    return sys.maxsize


def version():
    return sys.version


def is_windows():
    return sys.platform[:3] == 'win'


def path():
    return sys.path


def models():
    return sys.modules
