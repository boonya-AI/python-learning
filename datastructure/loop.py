def loop_skill():
    knights = {'gallahad': 'the pure', 'robin': 'the brave'}
    for k, v in knights.items():
        print(k, v)


def loop_enumerate():
    for i, v in enumerate(['tic', 'tac', 'toe']):
        print(i, v)


def loop_zip():
    questions = ['name', 'quest', 'favorite color']
    answers = ['lancelot', 'the holy grail', 'blue']
    for q, a in zip(questions, answers):
        print('What is your {0}?  It is {1}.'.format(q, a))


def loop_reverse():
    for i in reversed(range(1, 10, 2)):
        print(i)


def loop_sorted():
    basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
    for i in sorted(basket):
        print(i)


def loop_sorted_set():
    basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
    for f in sorted(set(basket)):
        print(f)


def loop_math():
    import math
    raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8]
    filtered_data = []
    for value in raw_data:
        if not math.isnan(value):
            filtered_data.append(value)

    print(filtered_data)


if __name__ == "__main__":
    loop_skill()
    loop_enumerate()
    loop_zip()
    loop_reverse()
    loop_sorted()
    loop_sorted_set()
    loop_math()
