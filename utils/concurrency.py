from concurrent.futures import ThreadPoolExecutor, TimeoutError


def run_with_timeout(func, timeout, default=None, *args, **kwargs):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            print(f"{func.__name__} timed out after {timeout} seconds")
            return default
