def generate():
    n = 0
    while True:
        n += 1
        str_n = str(n)
        for i in range(n):
            for char in str_n:
                yield char


def generate_n(n: int):
    it = generate()
    for i in range(n):
        yield next(it)


if __name__ == '__main__':
    n = int(input('Input N: '))
    for c in generate_n(n):
        print(c, end='')
