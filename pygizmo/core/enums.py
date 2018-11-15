from enum import Enum

Orientation = Enum('Orientation', 'horizontal, vertical', module=__name__)

class AnchorBound:
    def __init__(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical

    def __repr__(self):
        return 'AnchorBound: {}'.format(vars(self))

class Anchor:
    H = Enum('AnchorH', 'left, right, center')
    V = Enum('AnchorV', 'top, bottom, center')

    Edge = Enum('AnchorEdge', {
        'bottom': AnchorBound(H.center, V.bottom),
        'left'  : AnchorBound(H.left,   V.center),
        'right' : AnchorBound(H.right,  V.center),
        'top'   : AnchorBound(H.center, V.top)})

    Point = Enum('AnchorPoint', {
        'center'       : AnchorBound(H.center,   V.center),
        'bottomleft'   : AnchorBound(H.left,     V.bottom),
        'bottomright'  : AnchorBound(H.right,    V.bottom),
        'topleft'      : AnchorBound(H.left,     V.top),
        'topright'     : AnchorBound(H.right,    V.top)})
