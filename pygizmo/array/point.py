import numpy as np
from .properties import ArrayProperty
from ..util import Attr


class Point(np.ndarray):
    def __new__(cls, x, y=None):
        if y is None:
            obj = np.asarray(x).view(cls)
        else:
            obj = np.asarray((x, y)).view(cls)

        obj.attr = Attr(obj)
        return obj

    def attr(self, key, value=None):
        if value is None:
            return getattr(self, key)
        setattr(self, key, value)

    def get_tuple(self, cast=None):
        if cast:
            self.astype(cast)
        return tuple(self.tolist())

    x = ArrayProperty(0)
    y = ArrayProperty(1)
