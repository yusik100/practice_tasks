from mylib.generators import fibonacci_generator
from mylib.timeout import run_with_timeout

def main():
    fib_gen = fibonacci_generator()
    run_with_timeout(fib_gen, timeout_sec=5)

if __name__ == "__main__":
    main()