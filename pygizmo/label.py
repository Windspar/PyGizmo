import pygame
import string
from .array import Point
from .core import Gizmo
from .util import CallVariable

class Letter:
    def __init__(self, letter, position):
        self.position = position
        self.letter = letter

    def draw(self, surface, position):
        p = position + self.position
        surface.blit(self.letter, p)

pygame.font.init()
class Label(Gizmo):
    # default font
    font = pygame.font.Font(None, 16)

    def __init__(self, text,
                 font = None,
                 color = pygame.Color('white'),
                 position = (0,0),
                 byletter = False):

        Gizmo.__init__(self, (*position,1,1))
        if font is None:
            font = Label.font

        self.byletter = CallVariable(byletter, self.update_text)
        self.color = CallVariable(color, self.update_text)
        self.font = CallVariable(font, self.update_text)
        self.text = CallVariable(text, self.update_text)
        self.update_text()
        self.effects = []

    def on_draw(self, surface, bounds):
        if bounds is None:
            bounds = self.bounds

        if self.image:
            if self.byletter():
                for letter in self.image:
                    letter.draw(surface, bounds.topleft)
            else:
                surface.blit(self.image, bounds)

    def update_text(self):
        if self.font() and self.color() and self.text():
            text = self.text()
            font = self.font()
            color = self.color()

            if self.byletter():
                printable = string.printable.replace(string.whitespace, '')
                self.image = []
                for enum, letter in enumerate(text):
                    if letter in printable:
                        l = font.render(text[enum], 1, color)
                        rect = l.get_rect()

                        if enum > 0:
                            rect.right = font.size(text[:enum + 1])[0]

                        self.image.append(Letter(l, Point(*rect.topleft)))
            else:
                self.image = font.render(text, 1, color)

            self.bounds.dimension = font.size(text)
        else:
            self.image = None
