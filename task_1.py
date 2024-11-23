def generate():
    n = 0
    while True:
        n += 1
        str_n = str(n)
        for i in range(n):
            for char in str_n:
                yield char


def get_nth(n: int) -> str | None:
    res = None
    it = generate()
    for i in range(n):
        res = next(it)

    return res
