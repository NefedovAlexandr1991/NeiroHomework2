import time
from functools import wraps

def ttl_cache(ttl_seconds):
    """Декоратор для кэширования с TTL."""
    def decorator(func):
        storage = {}  # ключ -> (значение, время записи)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем ключ из аргументов
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            if key in storage:
                value, saved_at = storage[key]
                if now - saved_at < ttl_seconds:
                    return value

            # Если ключ не в кэше или истёк срок, вычисляем и сохраняем
            value = func(*args, **kwargs)
            storage[key] = (value, now)
            return value

        return wrapper
    return decorator