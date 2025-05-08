from mylib.generators import fibonacci_generator
from mylib.timeout   import run_with_timeout

def main():
    fib = fibonacci_generator()
    run_with_timeout(fib, timeout_sec=5)

if __name__ == "__main__":
    main()