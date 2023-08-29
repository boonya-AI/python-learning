import sys

def platform():
    sys.platform

def maxsize():
    sys.maxsize

def version():
    sys.version

def isWindows():
    return sys.platform[:3] == 'win'

def path():
    return sys.path

def models():
    return sys.modules


