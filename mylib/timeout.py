import time

def run_with_timeout(iterator, timeout_sec):
    end_time = time.time() + timeout_sec
    total = 0
    count = 0

    for value in iterator:
        if time.time() >= end_time:
            break

        print(f"Value: {value}")
        total += value
        count += 1
        average = total / count
        print(f"  Total: {total}, Average: {average:.2f}")