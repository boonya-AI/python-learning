def dictionary():
    tel = {'jack': 4098, 'sape': 4139}
    tel['guido'] = 4127
    print(tel)

    print(tel['jack'])

    del tel['sape']
    tel['irv'] = 4127
    print(tel)

    list(tel)

    sorted(tel)

    print('guido' in tel)

    print('jack' not in tel)


def create_dictionary():
    d = dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
    print(d)

    d = {x: x ** 2 for x in (2, 4, 6)}
    print(d)

    d = dict(sape=4139, guido=4127, jack=4098)
    print(d)


if __name__ == "__main__":
    dictionary()
    create_dictionary()
