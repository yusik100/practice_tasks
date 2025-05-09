import time
import threading
from collections import OrderedDict, defaultdict
from functools import wraps


def memoize(max_size=None, policy="LRU", expiry=None, custom_eviction=None):
    """
    Декоратор для мемоізації чистих функцій.

    Параметри:
      - max_size: максимальний розмір кешу (None = без обмежень)
      - policy: стратегія очищення: "LRU", "LFU", "TTL", "CUSTOM"
      - expiry: час життя запису для стратегії TTL (в секундах)
      - custom_eviction: функція(cache_dict) -> key для видалення при політиці CUSTOM
    """
    def decorator(func):
        cache = OrderedDict()       # зберігає ключі в порядку доступу
        freq = defaultdict(int)    # рахує частоту доступів для LFU
        lock = threading.Lock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            with lock:
                # TTL: видалити прострочені
                if policy == "TTL" and expiry is not None:
                    expired = [k for k, (_, ts) in cache.items() if now - ts >= expiry]
                    for k in expired:
                        cache.pop(k, None)
                        freq.pop(k, None)

                # Якщо в кеші — повертаємо та оновлюємо для LRU і LFU
                if key in cache:
                    result, ts = cache.pop(key)
                    cache[key] = (result, now)
                    freq[key] += 1
                    return result

                # Обчислюємо результат
                result = func(*args, **kwargs)

                # Евікція, якщо потрібно
                if max_size is not None and len(cache) >= max_size:
                    if policy == "LRU":
                        # Видалити найстаріший запис
                        cache.popitem(last=False)
                    elif policy == "LFU":
                        # Видалити найменш часто використовуваний
                        least = min(freq.items(), key=lambda x: x[1])[0]
                        cache.pop(least, None)
                        freq.pop(least, None)
                    elif policy == "CUSTOM" and callable(custom_eviction):
                        evict_key = custom_eviction(cache)
                        cache.pop(evict_key, None)
                        freq.pop(evict_key, None)
                    # TTL стратегия обробляється на початку

                # Додаємо новий запис
                cache[key] = (result, now)
                freq[key] += 1
                return result

        return wrapper
    return decorator