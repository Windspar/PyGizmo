import pygame
from ..array import Bounds
from .enums import Anchor


# Gizmo variables
#   * bounds
#   * enable
#   * invisable
#   * parent
#   * show

# Gizmo methods
#   * draw(surface, rect=None)
class Gizmo:
    def __init__(self, bounds):
        self.bounds = Bounds(bounds)
        self.screen_bounds = self.bounds.copy()

        # Read Only Varaibles
        self._id = None
        self._hover = False
        self._selected = False

        # public varaibles
        self.enable = True
        # if object should be drawn. Bounds are visable
        self.invisable = False
        self.parent = None
        # if object should be drawn. Bounds are hidden
        self.show = True

    def draw(self, surface, bounds=None):
        if not self.invisable:
            if not self.enable and self.show:
                self.on_draw_disable(surface, bounds)
            elif self.show:
                self.on_draw(surface, bounds)

    def event(self, event):
        if self.enable and self.show and not self.invisable:
            if event.type == pygame.MOUSEMOTION:
                self._hover = self.screen_bounds.collidepoint(*event.pos)

            self.on_event(event)

    def get_screen_position(self):
        if self.parent:
            return self.bounds.topleft + self.parent.get_screen_position()

        return self.bounds.topleft

    def is_display(self):
        return False

    def on_draw(self, surface, bounds=None):
        pass

    def on_draw_disable(self, surface, bounds=None):
        pass

    def on_event(self, event):
        pass

    def position_to(self, bounds, anchor):
        if Anchor.H.center == anchor:
            self.bounds.centerx = bounds.centerx
        elif Anchor.H.left == anchor:
            self.bounds.left = bounds.left
        elif Anchor.H.right == anchor:
            self.bounds.right = bounds.right

        elif Anchor.V.center == anchor:
            self.bounds.centery = bounds.centery
        elif Anchor.V.top == anchor:
            self.bounds.top = bounds.top
        elif Anchor.V.bottom == anchor:
            self.bounds.bottom = bounds.bottom

        elif Anchor.Point.center == anchor:
            self.bounds.center = bounds.center
        elif Anchor.Point.topleft == anchor:
            self.bounds.topleft = bounds.topleft
        elif Anchor.Point.topright == anchor:
            self.bounds.topright = bounds.topright
        elif Anchor.Point.bottomleft == anchor:
            self.bounds.bottomleft = bounds.bottomleft
        elif Anchor.Point.bottomright == anchor:
            self.bounds.bottomright = bounds.bottomright

        elif Anchor.Edge.bottom == anchor:
            self.bounds.bottom = bounds.bottom
            self.bounds.centerx = bounds.centerx
        elif Anchor.Edge.top == anchor:
            self.bounds.top = bounds.top
            self.bounds.centerx = bounds.centerx
        elif Anchor.Edge.left == anchor:
            self.bounds.left = bounds.left
            self.bounds.centery = bounds.centery
        elif Anchor.Edge.right == anchor:
            self.bounds.right = bounds.right
            self.bounds.centery = bounds.centery

    def update_screen_bounds(self):
        if self.parent:
            self.screen_bounds = Bounds(self.bounds)
            self.screen_bounds.topleft = self.get_screen_position()
