import warnings


# TODO: Replace with "warnings.deprecated" when switching to Python 3.13
def deprecated(message):

    def decorator(func):

        def inner(*args, **kwargs):
            warnings.warn(message, DeprecationWarning)
            return func(*args, **kwargs)

        return inner

    return decorator
