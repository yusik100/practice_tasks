from mylib.generators import fibonacci_generator
from mylib.timeout import run_with_timeout
from mylib.memoization import memoize
from mylib.priority_queue import BiDirectionalPriorityQueue


def demo_fibonacci_timeout():
    """Демо: генератор Фібоначчі з тайм-ау́том"""
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


def demo_priority_queue():
    """Демо: двонаправлена черга пріоритетів"""
    print("\n=== Priority Queue demo ===")
    pq = BiDirectionalPriorityQueue()
    pq.enqueue("apple", priority=5)
    pq.enqueue("banana", priority=2)
    pq.enqueue("cherry", priority=8)

    print("peek highest:", pq.peek(highest=True))
    print("peek lowest: ", pq.peek(lowest=True))
    print("peek oldest: ", pq.peek(oldest=True))
    print("peek newest: ", pq.peek(newest=True))

    print("dequeue lowest:", pq.dequeue(lowest=True))
    print("dequeue highest:", pq.dequeue(highest=True))
    print("dequeue oldest:",  pq.dequeue(oldest=True))


def main():
    demo_fibonacci_timeout()
    demo_memoization()
    demo_priority_queue()


if __name__ == "__main__":
    main()