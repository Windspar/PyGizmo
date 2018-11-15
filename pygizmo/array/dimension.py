import numpy as np
from .properties import ArrayProperty
from ..util import Attr


class Dimension(np.ndarray):
    def __new__(cls, w, h=None):
        if w is None:
            obj = np.asarray(w).view(cls)
        else:
            obj = np.asarray((w, h)).view(cls)

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

    w = ArrayProperty(0)
    h = ArrayProperty(1)
    width = ArrayProperty(0)
    height = ArrayProperty(1)
