__all__ = [
    'placeholder',
    '_',
]

class PlaceHolder:
    def __getattribute__(self, action):
        def wrapper(*argv, **kwargv):
            return lambda data: getattr(data, action)(*argv, **kwargv)
        return wrapper

_ = placeholder = PlaceHolder()
