def flip(fn):
    def wrapper(*args):
        return fn(args[1], args[0])
    return wrapper

__all__ = [
    'flip',
]
