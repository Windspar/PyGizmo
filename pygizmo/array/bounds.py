from pygame import Rect
import numpy as np
from . import properties as prop
from .dimension import Dimension
from .point import Point
from ..util import Attr


# Bounds(x, y, w, h)        # by value
# Bounds((x, y, w, h))      # tuple
# Bounds([x, y, w, h])      # list
# Bounds(w, h)              # dimension
# Bounds(Bounds)
# Bounds(Dimension)
# Bounds(Rect)

class Bounds(np.ndarray):
    def __new__(cls, x=None, y=None, w=None, h=None):
        if x is None:
            obj = np.asarray((0, 0, 0, 0)).view(cls)
        elif isinstance(x, (tuple, list)):
            if len(x) == 4:
                obj = np.asarray(x).view(cls)
            else:
                raise TypeError("Object:Bounds, Tuple or List must have size of 4")
        elif isinstance(x, Bounds):
            obj = np.asarray(x.tolist()).view(cls)
        elif isinstance(x, Rect):
            obj = np.asarray(tuple(x)).view(cls)
        elif isinstance(x, Dimension):
            obj = np.asarray((0, 0, x.w, x.h)).view(cls)
        elif isinstance(x, Point):
            obj = np.asarray((x.x, x.y, 0, 0)).view(cls)
        elif w is None:
            obj = np.asarray((0, 0, x, y)).view(cls)
        else:
            obj = np.asarray((x, y, w, h)).view(cls)

        obj.attr = Attr(obj)
        return obj

    def clamp(self, bounds, in_place=False):
        clamp_x, clamp_y = self[:2]

        if self[2] >= bounds[2]:
            clamp_x = bounds[0] + bounds[2] / 2 - self[2] / 2
        elif self[0] < bounds[0]:
            clamp_x = bounds[0]
        elif self[0] + self[2]:
            clamp_x = bounds[0] + bounds[2] - self[2]

        if self[3] >= bounds[3]:
            clamp_y = bounds[1] + bounds[3] / 2 - self[3] / 2
        elif self[1] < bounds[1]:
            clamp_y = bounds[1]
        elif self[1] + self[3]:
            clamp_y = bounds[1] + bounds[3] - self[3]

        if in_place:
            self[0] = clamp_x
            self[1] = clamp_y
        else:
            return Bounds(clamp_x, clamp_y, self[2], self[3])

    def clamp_ip(self, bounds):
        self.clamp(bounds, True)

    def collidepoint(self, x, y):
        return self[0] < x < self[0] + self[2] and self[1] < y < self[1] + self[3]

    def collidebounds(self, bounds):
        return (((self[0] > bounds[0] and self[0] < bounds[2] + bounds[0]) or
                (bounds[0] > self[0] and bounds[0] < self[2] + self[0])) and
                ((self[1] > bounds[1] and self[1] < bounds[3] + bounds[1]) or
                (bounds[1] > self[1] and bounds[1] < self[3] + self[1])))

    #def copy(self):
        #return Bounds(*self[:4])

    def inflate(self, x, y):
        bounds = self.copy()
        if x != 0:
            bounds.x -= x // 2
            bounds.w += x

        if y != 0:
            bounds.y -= y // 2
            bounds.h += y

        return bounds

    def inflate_ip(self, x, y):
        if x != 0:
            self[0] -= x // 2
            self[2] += x

        if y != 0:
            self[1] -= y // 2
            self[3] += y

    def move(self, x, y):
        return Bounds(self[0] + x, self[1] + y, self[2], self[3])

    def move_ip(self, x, y):
        self[0] += x
        self[1] += y

    def normalize(self):
        one = lambda v: [0, np.absolute(v) - 1][v < 0]
        abso = lambda v: [v, np.absolute(v) - 1][v < 0]
        self[0] -= one(self[2])
        self[1] -= one(self[3])
        self[2] = abso(self[2])
        self[3] = abso(self[3])

    def get_tuple(self, cast=None):
        if cast:
            data = self.astype(cast)
            return tuple(data.tolist())
        return tuple(self.tolist())

    @property
    def rect(self):
        return Rect(*(self.copy() + .5).astype(int))

    x = prop.ArrayProperty(0)
    y = prop.ArrayProperty(1)
    w = prop.ArrayProperty(2)
    h = prop.ArrayProperty(3)
    left = prop.ArrayProperty(0)
    top = prop.ArrayProperty(1)
    width = prop.ArrayProperty(2)
    height = prop.ArrayProperty(3)
    right = prop.ArrayCombineProperty(0, 2)
    bottom = prop.ArrayCombineProperty(1, 3)
    dimension = prop.ArrayDoubleProperty(2, 3, Dimension)
    topleft = prop.ArrayDoubleProperty(0, 1, Point)
    topright = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineProperty(0, 2),
        prop.ArrayProperty(1),
        Point)

    bottomleft = prop.ArrayTypeDoubleProperty(
        prop.ArrayProperty(0),
        prop.ArrayCombineProperty(1, 3),
        Point)

    bottomright = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineProperty(0, 2),
        prop.ArrayCombineProperty(1, 3),
        Point)

    center = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineCenterProperty(0, 2),
        prop.ArrayCombineCenterProperty(1, 3),
        Point)

    centerx = prop.ArrayCombineCenterProperty(0, 2)
    centery = prop.ArrayCombineCenterProperty(1, 3)
