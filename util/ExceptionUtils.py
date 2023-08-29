import sys

def sample(a, b):
    try:
        if (a == b):
            print('good morning')
        else:
            raise RuntimeError
    except:
        print('bad weather')
        exc_info = sys.exc_info()
        print(exc_info[0])
        print(exc_info[1])
