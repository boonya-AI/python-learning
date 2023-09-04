def list_fruits():
    fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
    fruits.count('apple')

    fruits.count('tangerine')

    fruits.index('banana')

    fruits.index('banana', 4)  # Find next banana starting at position 4

    fruits.reverse()
    print(fruits)

    fruits.append('grape')
    print(fruits)

    fruits.sort()
    print(fruits)

    fruits.pop()
    print(fruits)


if __name__ == "__main__":
    list_fruits()
