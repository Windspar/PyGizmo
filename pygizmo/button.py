import pygame
from .label import Label
from .core import Anchor, Gizmo
from .array import Bounds

pygame.init()
class Button(Gizmo):
    default_font = pygame.font.Font(None, 16)

    def __init__(self, label, bounds, callback, pydata=None, anchor=Anchor.H.center):
        Gizmo.__init__(self, bounds)
        if isinstance(label, str):
            self.label = Label(label, pygame.font.Font(None, 16), (255,255,255))
        else:
            self.label = label

        self.anchor = anchor
        self.callback = callback
        self.pydata = pydata
        self.bg_color = pygame.Color('mediumblue')
        self.hover_color = pygame.Color('dodgerblue')

    def on_draw(self, surface, bounds):
        if bounds is None:
            bounds = self.bounds

        if self._hover:
            surface.fill(self.hover_color, bounds)
        else:
            surface.fill(self.bg_color, bounds)

        self.label.bounds.center = self.bounds.center
        self.label.draw(surface)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self._hover:
                self.callback(self)
