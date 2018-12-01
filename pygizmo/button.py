import pygame
from .core import Anchor, Gizmo, ColorFrame, Font
from .core.text import Text
from .array import Bounds

pygame.init()
class Button(Gizmo):
    default_font = Font()

    def __init__(self, text, bounds, callback, pydata=None, anchor=Anchor.H.center):
        Gizmo.__init__(self, bounds)
        self.text = Text(self, Font(), text)
        self.anchor = anchor
        self.callback = callback
        self.pydata = pydata
        self.color = ColorFrame(background = pygame.Color('mediumblue'),
                                hover = pygame.Color('dodgerblue'))

    def on_draw(self, surface, bounds):
        if bounds is None:
            bounds = self.bounds

        if self._hover:
            surface.fill(self.color.hover, bounds)
        else:
            surface.fill(self.color.background, bounds)

        self.text.bounds.center = self.bounds.center
        self.text.on_draw(surface)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self._hover:
                self.callback(self)
