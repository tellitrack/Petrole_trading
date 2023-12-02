def iterable(cls):
    """ Décorateur pour rendre une classe iterable. """

    def iter_fn(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    cls.__iter__ = iter_fn
    return cls
