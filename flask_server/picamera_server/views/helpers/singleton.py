"""
Singleton as a metaclass
"""


class Singleton(type):
    """
    Singleton to be used as a metaclass
    Ex. 'class SingletonClass(object, metaclass=Singleton): ...'
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
