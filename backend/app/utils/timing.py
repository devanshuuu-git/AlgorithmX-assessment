import time
from functools import wraps

def measure_latency(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = (time.time() - start) * 1000
        return result

    return wrapper
