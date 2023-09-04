def list_append():
    print("------------------list_append---------------")
    squares = []
    # 写法1
    for x in range(10):
        squares.append(x ** 2)
    print(squares)

    # 写法2
    squares = list(map(lambda x: x ** 2, range(10)))
    print(squares)

    # 写法3
    squares = [x ** 2 for x in range(10)]
    print(squares)


def list_tuidao():
    print("------------------list_tuidao---------------")
    combs = [(x, y) for x in [1, 2, 3] for y in [3, 1, 4] if x != y]
    print(combs)

    combs = []
    for x in [1, 2, 3]:
        for y in [3, 1, 4]:
            if x != y:
                combs.append((x, y))

    print(combs)


def meta_array():
    print("------------------meta_array---------------")
    vec = [-4, -2, 0, 2, 4]
    # create a new list with the values doubled
    print([x * 2 for x in vec])

    # filter the list to exclude negative numbers
    print([x for x in vec if x >= 0])

    # apply a function to all the elements
    print([abs(x) for x in vec])

    # call a method on each element
    fresh_fruit = ['  banana', '  loganberry ', 'passion fruit  ']
    print([weapon.strip() for weapon in fresh_fruit])

    # create a list of 2-tuples like (number, square)
    print([(x, x ** 2) for x in range(6)])

    # flatten a list using a listcomp with two 'for'
    vec = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print([num for elem in vec for num in elem])


if __name__ == "__main__":
    list_append()
    list_tuidao()
    meta_array()
