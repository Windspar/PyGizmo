import pygame
from enum import Enum
from ..core import Anchor, Bin, Gizmo, Orientation
from ..array import Bounds, Dimension

class ChildBox(Gizmo):
    def __init__(self, item, expand):
        Gizmo.__init__(self, item.bounds.copy())
        self.expand = expand
        self.item = item

    def on_draw(self, surface, bounds=None):
        self.item.draw(surface, self.bounds)

class Box(Bin):
    @classmethod
    def h(cls, anchor_h=None, spacing=0, flip=False, bounds=None):
        if bounds is None:
            bounds = Bounds(0,0,0,0)

        if anchor_h:
            return cls(Orientation.horizontal, anchor_h, spacing, flip, bounds)
        else:
            return cls(Orientation.horizontal, Anchor.H.left, spacing, flip, bounds)

    @classmethod
    def v(cls, anchor_v=None, spacing=0, flip=False, bounds=None):
        if bounds is None:
            bounds = Bounds(0,0,0,0)

        if anchor_v:
            return cls(Orientation.vertical, anchor_v, spacing, flip, bounds)
        else:
            return cls(Orientation.vertical, Anchor.V.top, spacing, flip, bounds)

    def __init__(self, orientation, anchor, spacing=0, flip=False, bounds=None):
        if bounds is None:
            bounds = Bounds(0,0,0,0)

        Bin.__init__(self, bounds)
        self.item_bounds = Bounds(0,0,0,0)
        self.orientation = orientation
        self.expand_count = 0
        self.anchor = anchor
        self.position = 0
        self.flip = flip
        self.boxes = []
        self.box = None

        self.spacing = spacing
        self.max_dimension = self.bounds.dimension

    def add(self, item, expand=False):
        if isinstance(item, Gizmo):
            child = ChildBox(item, expand)
            self.bind(child)
            if isinstance(item, Box):
                self.boxes.append(child)
                item.parent = self
                item.box = child

    def clear(self):
        self._gizmos = []
        self.update()

    def expand_and_shrink(self, attr, expand_count, orientation):
        # Get the expanded bound attr
        if self.box:
            bound = self.box.bounds.attr[attr]
        else:
            bound = self.bounds.attr[attr]

        item_bound = self.item_bounds.attr[attr]
        if self.expand_count > 0:
            expand = (bound - item_bound) // expand_count

            if expand != 0:
                for child in self._gizmos:
                    if child.expand and child.item.show:
                        ga = child.bounds.attr[attr]
                        value = ga + expand
                        n = expand
                        # Box max bounds dimension
                        if isinstance(child, Box):
                            gamd = child.item.max_dimension.attr[attr]
                            if value > gamd:
                                value = gamd
                                n = value - ga

                        child.bounds.attr[attr] = value

                        # Add expanded amount to item_bounds.
                        self.item_bounds.attr[attr] += n

                        # Update the oppisite direction
                        if isinstance(child.item, Box):
                            if orientation != child.item.orientation:
                                child.item.expand_and_shrink(attr, 1, orientation)

    def get_children(self):
        if self.flip:
            return self._gizmos[::-1]
        else:
            return self._gizmos

    def get_mother(self):
        if self.parent is None:
            return self

        mother = self.parent
        while True:
            if mother.parent is None:
                break

            mother = mother.parent

        return mother

    def get_position(self):
        if self.box:
            bounds = self.box.bounds
        else:
            bounds = self.bounds

        x, y = bounds.topleft

        anchor = self.anchor
        if self.flip:
            if self.anchor == Anchor.H.left:
                anchor = Anchor.H.right
            elif self.anchor == Anchor.H.right:
                anchor = Anchor.H.left
            elif self.anchor == Anchor.V.top:
                anchor = Anchor.V.bottom
            elif self.anchor == Anchor.V.bottom:
                anchor = Anchor.V.top

        if self.orientation == Orientation.horizontal:
            if anchor == Anchor.H.right:
                x = bounds.right - self.item_bounds.w
            elif anchor == Anchor.H.center:
                x = bounds.centerx - self.item_bounds.w // 2
        else:
            if anchor == Anchor.V.bottom:
                y = bounds.bottom - self.item_bounds.h
            elif anchor == Anchor.V.center:
                y = bounds.centery - self.item_bounds.h // 2

        return x, y

    def update(self):
        mother = self.get_mother()
        mother.update_item_bounds()
        mother.update_max_dimension()
        mother.update_position()

    def update_item_bounds(self):
        width = []
        height = []
        self.expand_count = 0
        for child in self._gizmos:
            if child.item.show:
                if isinstance(child.item, Box):
                    child.item.update_item_bounds()

                child.bounds = Bounds(child.item.bounds)
                if child.expand:
                    self.expand_count += 1

                width.append(child.bounds.w)
                height.append(child.bounds.h)

        if len(self._gizmos) > 0:
            spacing = self.spacing * len(self._gizmos) - self.spacing
            if self.orientation == Orientation.horizontal:
                self.item_bounds.w = sum(width) + spacing
                self.item_bounds.h = max(height)
                if self.parent:
                    self.bounds.dimension = self.item_bounds.dimension
            else:
                self.item_bounds.w = max(width)
                self.item_bounds.h = sum(height) + spacing
                if self.parent:
                    self.bounds.dimension = self.item_bounds.dimension
        else:
            self.item_bounds.w = 0
            self.item_bounds.h = 0
            if self.parent:
                self.bounds.dimension = self.item_bounds.dimension

    def update_max_dimension(self):
        if self.parent:
            bounds = self.box.bounds
        else:
            bounds = self.bounds

        self.spread = {'w': bounds.w - self.item_bounds.w,
                       'h': bounds.h - self.item_bounds.h}

        box_expand = 0
        height = []
        width = []
        for box in self.boxes:
            if box.item.show:
                height.append(box.item.item_bounds.h)
                width.append(box.item.item_bounds.w)
                if box.expand:
                    box_expand += 1

        if box_expand > 0:
            if self.orientation == Orientation.horizontal:
                height = (self.max_dimension.h - max(height)) // box_expand
                width = (self.max_dimension.w - sum(width)) // box_expand
            else:
                height = (self.max_dimension.h - sum(height)) // box_expand
                width = (self.max_dimension.w - max(width))  // box_expand
        else:
            height = 0
            width = 0

        for box in self.boxes:
            if box.item.show:
                b = box.item.item_bounds.dimension
                if box.expand:
                    box.item.max_dimension = b + Dimension(width, height)
                else:
                    box.item.max_dimension = b

                box.item.update_max_dimension()

    def update_position(self):
        if self.orientation == Orientation.horizontal:
            self.expand_and_shrink('w', self.expand_count, self.orientation)
        else:
            self.expand_and_shrink('h', self.expand_count, self.orientation)

        print('Dimension', self.max_dimension)

        x, y = self.get_position()
        children = self.get_children()
        print('Parent', x, y, self.bounds)

        for child in children:
            if child.item.show:
                child.bounds.x = x
                child.bounds.y = y
                if isinstance(child.item, Box):
                    child.item.update_position()

                if self.orientation == Orientation.horizontal:
                    x += child.bounds.w + self.spacing
                else:
                    y += child.bounds.h + self.spacing

        self.position = x, y
