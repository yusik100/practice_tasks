import time
import threading
from collections import OrderedDict, defaultdict
from functools import wraps


def memoize(max_size=None, policy="LRU", expiry=None, custom_eviction=None):

    def decorator(func):
        cache = OrderedDict()       
        freq = defaultdict(int)    
        lock = threading.Lock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            with lock:
                if policy == "TTL" and expiry is not None:
                    expired = [k for k, (_, ts) in cache.items() if now - ts >= expiry]
                    for k in expired:
                        cache.pop(k, None)
                        freq.pop(k, None)

                if key in cache:
                    result, ts = cache.pop(key)
                    cache[key] = (result, now)
                    freq[key] += 1
                    return result

                result = func(*args, **kwargs)

                if max_size is not None and len(cache) >= max_size:
                    if policy == "LRU":
                        cache.popitem(last=False)
                    elif policy == "LFU":
                        least = min(freq.items(), key=lambda x: x[1])[0]
                        cache.pop(least, None)
                        freq.pop(least, None)
                    elif policy == "CUSTOM" and callable(custom_eviction):
                        evict_key = custom_eviction(cache)
                        cache.pop(evict_key, None)
                        freq.pop(evict_key, None)

                cache[key] = (result, now)
                freq[key] += 1
                return result

        return wrapper
    return decorator