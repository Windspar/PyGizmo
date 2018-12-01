import pygame
import string
from .array import Point
from .core import Gizmo, Font
from .core.text import Text


pygame.font.init()
class Label(Gizmo):
    # default font
    font = Font()

    def __init__(self, text,
                 font = None,
                 position = (0,0),
                 effect = None):

        Gizmo.__init__(self, (*position,1,1))
        if font is None:
            font = Label.font

        self.text = Text(self, font, text, effect)
        self.bounds.dimension = self.text.bounds.dimension

    def set_effect(self, effect):
        self.text.set_effect(effect)

    def on_draw(self, surface, bounds):
        if bounds is None:
            bounds = self.bounds

        self.text.on_draw(surface, bounds)

    def on_event(self, event):
        self.text.on_event(event)
