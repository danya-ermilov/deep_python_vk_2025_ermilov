from functools import wraps


def default_print(func, args, kwargs, attempt):
    return f'run {func.__name__} with positional {args=}, with keyword {kwargs=}, {attempt=}'


def retry_deco(max_tries, check_exceptions=None):
    if check_exceptions is None:
        check_exceptions = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_tries + 1):
                try:
                    result = func(*args, **kwargs)
                    print(default_print(func, args, kwargs, attempt), f'{result=}')
                    return args, kwargs, attempt, result
                except Exception as exc:
                    exception = exc
                    print(default_print(func, args, kwargs, attempt), f'{exception=}')
                    if any(isinstance(exception, check_exc) for check_exc in check_exceptions):
                        return args, kwargs, attempt, exception
            return args, kwargs, attempt, exception
        return wrapper
    return decorator
