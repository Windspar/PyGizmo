import pygame
from enum import Enum
from ..core import Anchor, Bin, Gizmo, Orientation
from ..array import Bounds, Dimension

class ChildBox(Gizmo):
    def __init__(self, item, h_expand, v_expand, center):
        Gizmo.__init__(self, item.bounds.copy())
        self.item = item
        self.center = center
        self.h_expand = h_expand
        self.v_expand = v_expand

    def on_draw(self, surface, bounds=None):
        self.item.draw(surface, self.bounds)

    def on_event(self, event):
        self.item.event(event)

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
        self.expand_count = {'h': 0, 'v': 0}
        self.anchor = anchor
        self.position = 0
        self.flip = flip
        self.boxes = []
        self.box = None
        self.name = None

        self.spacing = spacing
        self.max_dimension = self.bounds.dimension

    def add(self, item, expand=False, expand_oppsite=False, center=False):
        if isinstance(item, (tuple, list)):
            for i in item:
                self.add_item(i, expand, expand_oppsite, center)
        else:
            self.add_item(item, expand, expand_oppsite, center)

    def add_item(self, item, expand=False, expand_oppsite=False, center=False):
        if isinstance(item, Gizmo):
            if self.orientation == Orientation.vertical:
                child = ChildBox(item, expand_oppsite, expand, center)
            else:
                child = ChildBox(item, expand, expand_oppsite, center)

            self.bind(child)
            if isinstance(item, Box):
                self.boxes.append(child)
                item.parent = self
                item.box = child

    def clear(self):
        self._gizmos = []
        self.update()

    def expand_and_shrink(self):
        if self.box:
            dimension = self.box.bounds.dimension
        else:
            dimension = self.bounds.dimension

        item_dim = self.item_bounds.dimension
        expand = Dimension(0, 0)
        if self.expand_count['h'] > 0:
            expand.w = (dimension.w - item_dim.w) // self.expand_count['h']

        if self.expand_count['v'] > 0:
            expand.h = (dimension.h - item_dim.h) // self.expand_count['v']

        if expand.w > 0 or expand.h > 0:
            for child in self._gizmos:
                if child.item.show:
                    dim = child.bounds.dimension
                    if child.h_expand and child.v_expand:
                        value = dim + expand
                    elif child.h_expand:
                        value = dim
                        value.w += expand.w
                    elif child.v_expand:
                        value = dim
                        value.h += expand.h

                    n = Dimension(*expand)
                    # Box max bounds dimension
                    if isinstance(child.item, Box):
                        max_dim = child.item.max_dimension
                        if value.w > max_dim.w:
                            value.w = max_dim.w
                            n.w = value.w - dim.w

                        if value.h > max_dim.h:
                            value.h = max_dim.h
                            n.h = value.h - dim.h

                    child.bounds.dimension = value
                    self.item_bounds.dimension += n

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
        self.expand_count = {'h': 0, 'v': 0}
        for child in self._gizmos:
            if child.item.show:
                if isinstance(child.item, Box):
                    child.item.update_item_bounds()

                child.bounds = Bounds(child.item.bounds)
                if child.v_expand:
                    self.expand_count['v'] += 1

                if child.h_expand:
                    self.expand_count['h'] += 1

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

        box_expand = {'v':0, 'h':0}
        height = []
        width = []
        for box in self.boxes:
            if box.item.show:
                height.append(box.item.item_bounds.h)
                width.append(box.item.item_bounds.w)
                if box.v_expand:
                    box_expand['v'] += 1

                if box.h_expand:
                    box_expand['h'] += 1

        if box_expand['h'] > 0 or box_expand['v'] > 0:
            if self.orientation == Orientation.horizontal:
                if box_expand['v'] > 0:
                    height = (self.max_dimension.h - max(height)) // box_expand['v']
                else:
                    height = 0

                if box_expand['h'] > 0:
                    width = (self.max_dimension.w - sum(width)) // box_expand['h']
                else:
                    width = 0
            else:
                if box_expand['v'] > 0:
                    height = (self.max_dimension.h - sum(height)) // box_expand['v']
                else:
                    height = 0

                if box_expand['h'] > 0:
                    width = (self.max_dimension.w - max(width))  // box_expand['h']
                else:
                    width = 0
        else:
            height = 0
            width = 0

        for box in self.boxes:
            if box.item.show:
                b = box.item.item_bounds.dimension
                if box.h_expand and box.v_expand:
                    box.item.max_dimension = b + Dimension(width, height)
                elif box.v_expand:
                    box.item.max_dimension = b + Dimension(0, height)
                elif box.h_expand:
                    box.item.max_dimension = b + Dimension(width, 0)
                else:
                    box.item.max_dimension = b

                box.item.update_max_dimension()

    def update_position(self):
        self.expand_and_shrink()

        x, y = self.get_position()
        children = self.get_children()

        for child in children:
            if child.item.show:
                if not isinstance(child.item, Box) and child.center:
                    center = (self.bounds.w - child.item.bounds.w) // 2
                    if self.orientation == Orientation.vertical:
                        child.bounds.x = x + center
                        child.bounds.y = y
                    else:
                        child.bounds.x = x
                        child.bounds.y = y + center
                else:
                    child.bounds.x = x
                    child.bounds.y = y

                #print('Updating Screen Bounds', child.bounds)
                #child.item.update_screen_bounds(child.bounds)
                child.item.screen_bounds = child.bounds
                #print('Child Screen Bounds', child.item.screen_bounds)

                if isinstance(child.item, Box):
                    child.item.update_position()

                if self.orientation == Orientation.horizontal:
                    x += child.bounds.w + self.spacing
                else:
                    y += child.bounds.h + self.spacing

        self.position = x, y
