def meta():
    t = 12345, 54321, 'hello!'
    t[0]


def sef():
    empty = ()
    singleton = 'hello',  # <-- note trailing comma
    len(empty)

    len(singleton)

    print(singleton)


if __name__ == "__main__":
    sef()
    meta()
