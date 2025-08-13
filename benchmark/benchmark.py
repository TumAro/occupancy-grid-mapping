import time

def benchmark_process(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, (end - start) * 1000