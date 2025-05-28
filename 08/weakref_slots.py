
import time
import cProfile
import pstats
import io
from functools import wraps


class Regular:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class WithSlots:
    __slots__ = ('a', 'b')

    def __init__(self, a, b):
        self.a = a
        self.b = b


class WithWeakref:
    __slots__ = ('a', 'b', '__weakref__')

    def __init__(self, a, b):
        self.a = a
        self.b = b


def benchmark_create(cls, n):
    t0 = time.perf_counter()
    instances = [cls(i, i+1) for i in range(n)]
    t1 = time.perf_counter()
    return instances, t1 - t0


def benchmark_access(instances):
    t0 = time.perf_counter()
    for inst in instances:
        inst.a
        inst.b
        inst.a = inst.a + 1
        inst.b = inst.b + 1
    t1 = time.perf_counter()
    return t1 - t0


_profiles = {}


def profile_deco(func):
    profiler = cProfile.Profile()
    _profiles[func.__name__] = profiler

    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        return result

    def print_stat():
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).strip_dirs().sort_stats('cumulative')
        ps.print_stats()
        print(f"Profile stats for {func.__name__}():")
        print(s.getvalue())

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


def main():
    N = 100_000

    for cls in [Regular, WithSlots, WithWeakref]:
        name = cls.__name__
        insts, create_time = benchmark_create(cls, N)
        access_time = benchmark_access(insts)
        print(f"{name}: Create: {create_time:.4f}s, Access: {access_time:.4f}s")

    add(1, 2)
    add(3, 4)
    sub(5, 2)
    add.print_stat()
    sub.print_stat()


if __name__ == '__main__':
    main()
