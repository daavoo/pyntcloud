MAJOR = 0
MINOR = 1
MICRO = 0

__version__ = "{}.{}.{}".format(MAJOR, MINOR, MICRO)


try:
    from .core_class import PyntCloud
except ImportError:
    pass
