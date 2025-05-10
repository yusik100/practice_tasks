import asyncio
import random

from mylib.generators import fibonacci_generator
from mylib.timeout import run_with_timeout
from mylib.memoization import memoize
from mylib.priority_queue import BiDirectionalPriorityQueue
from mylib.async_array_variants import AsyncArrayVariants


def demo_fibonacci_timeout():
    print("\nFibonacci with timeout (5 seconds)")
    fib = fibonacci_generator()
    run_with_timeout(fib, timeout_sec=5)


@memoize(max_size=10, policy="LRU")
def slow_square(x):
    import time
    time.sleep(0.5)
    return x * x


def demo_memoization():
    print("\nMemoization demo (slow_square)")
    inputs = [4, 4, 5, 4]
    for i in inputs:
        result = slow_square(i)
        print(f"slow_square({i}) = {result}")


def demo_priority_queue():
    print("\nPriority Queue demo")
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


def demo_async_array(loop: asyncio.AbstractEventLoop):
    print("\nAsync Array map demo (callback + promise)")

    async def example_async_fn(item, idx):
        await asyncio.sleep(random.random() * 0.3)
        return item * 10

    cancel_event = asyncio.Event()
    loop.call_later(0.15, cancel_event.set)
    items = [10, 20, 30]
    mapper = AsyncArrayVariants(items, cancel_event=cancel_event)

    def on_done_cb(results):
        print("Callback map results:", results)

    def on_error_cb(err):
        print("Callback map error:", err)

    mapper.callback_map(example_async_fn, on_done_cb, on_error_cb)

    async def run_promise_demo():
        try:
            results = await mapper.promise_map(example_async_fn)
            print("Promise map results:", results)
        except asyncio.CancelledError:
            print("Promise map was cancelled")
        finally:
            loop.stop()

    loop.call_later(0.5, lambda: asyncio.create_task(run_promise_demo()))


def main():
    demo_fibonacci_timeout()
    demo_memoization()
    demo_priority_queue()

    loop = asyncio.get_event_loop()
    loop.call_soon(demo_async_array, loop)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Interrupted by user")


if __name__ == "__main__":
    main()