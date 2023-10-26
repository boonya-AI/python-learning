import jmespath


def data():
    d = {"a": {"b": "boonya"}}
    print(jmespath.search("a.b", d))


if __name__ == '__main__':
    data()
