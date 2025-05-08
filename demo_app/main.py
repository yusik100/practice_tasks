from mylib.generators import fibonacci_generator
from mylib.timeout import run_with_timeout
from mylib.memoization import memoize


def demo_fibonacci_timeout():
    """Демо: генератор Фібоначчі з тайм-аутом"""
    print("=== Fibonacci with timeout (5 seconds) ===")
    fib = fibonacci_generator()
    run_with_timeout(fib, timeout_sec=5)


@memoize(max_size=10, policy="LRU")
def slow_square(x):
    """Повільна функція множення з затримкою, обгорнута мемоізацією"""
    import time
    time.sleep(0.5)
    return x * x


def demo_memoization():
    """Демо: показує кешування результатів slow_square"""
    print("\n=== Memoization demo (slow_square) ===")
    inputs = [4, 4, 5, 4]
    for i in inputs:
        result = slow_square(i)
        print(f"slow_square({i}) = {result}")


def main():
    demo_fibonacci_timeout()
    demo_memoization()


if __name__ == "__main__":
    main()