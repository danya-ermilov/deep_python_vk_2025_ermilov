from functools import wraps


def default_print(func, args, kwargs, attempt):
    return f'run {func.__name__} with positional {args=}, with keyword {kwargs=}, {attempt=}'


def retry_deco(max_tries, check_exceptions=None):
    if check_exceptions is None:
        check_exceptions = ()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_tries + 1):
                try:
                    result = func(*args, **kwargs)
                    print(default_print(func, args, kwargs, attempt), f'{result=}')
                    return result

                except check_exceptions as exc:
                    print(default_print(func, args, kwargs, attempt), f'{exc=}')
                    raise exc

                except Exception as exc:
                    last_exception = exc
                    print(default_print(func, args, kwargs, attempt), f'{exc=}')

            raise last_exception if last_exception else RuntimeError("No attempts made")

        return wrapper
    return decorator
