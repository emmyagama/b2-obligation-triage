import random, time

def retry(fn, attempts=3, sleeper=time.sleep, jitter=random.random, retryable=lambda e: True):
    for n in range(1,attempts+1):
        try: return fn(), n-1
        except Exception as e:
            if n == attempts or not retryable(e):
                try: e.retry_count=n-1
                except Exception: pass
                raise
            sleeper(2**(n-1)+jitter())
