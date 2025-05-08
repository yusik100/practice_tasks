def fibonacci_generator():
    """Нескінченний генератор чисел Фібоначчі: 0, 1, 1, 2, ..."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b