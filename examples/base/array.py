def append_array(a, L=[]):
    L.append(a)
    return L


def change_array(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L
