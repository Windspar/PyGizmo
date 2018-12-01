import pygame
from .gizmo import Gizmo


class Bin(Gizmo):
    def __init__(self, bounds):
        Gizmo.__init__(self, bounds)
        self._bin_id = 0
        self._gizmos = []

    def bind(self, gizmo):
        # Assign
        gizmo.parent = self
        gizmo.update_screen_bounds()
        gizmo._id = self.get_id()
        self._gizmos.append(gizmo)

    def bind_all(self, gizmos):
        for gizmo in gizmos:
            self.bind(gizmo)

    def draw(self, surface, bounds=None):
        if not self.invisable:
            if not self.enable and self.show:
                self.on_draw_disable(surface, bounds)
            elif self.show:
                self.on_draw(surface, bounds)
                for g in self._gizmos:
                    if bounds is None:
                        g.draw(surface)
                    else:
                        g.draw(surface, bounds)

    def event(self, event):
        if self.enable and self.show and not self.invisable:
            if event.type == pygame.MOUSEMOTION:
                self._hover = self.screen_bounds.collidepoint(*event.pos)

            self.on_event(event)
            for gizmo in self._gizmos:
                gizmo.event(event)

    def get_id(self):
        id = self._bin_id
        self._bin_id += 1
        return id

    def update_screen_bounds(self, bounds=None):
        Gizmo.update_screen_bounds(self, bounds)
        for g in self._gizmos:
            g.update_screen_bounds(bounds)
