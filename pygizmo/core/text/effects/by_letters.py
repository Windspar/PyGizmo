import string
from .text_effects import TextEffects
from ....array import Point

class Letter:
    def __init__(self, image, letter, position):
        self.position = position
        self.letter = letter
        self.image = image

    def draw(self, surface, position):
        p = position + self.position
        surface.blit(self.image, p)

class ByLetters(TextEffects):
    def __init__(self):
        TextEffects.__init__(self, True, True)

    def on_draw(self, surface, bounds):
        for letter in self.link['text'].image:
            letter.draw(surface, bounds.topleft)

    def on_update(self, text, font, color):
        printable = string.printable.replace(string.whitespace, '')
        self.link['text'].image = []
        for enum, letter in enumerate(text):
            if letter in printable:
                l = font.render(text[enum], 1, color)
                rect = l.get_rect()

                if enum > 0:
                    rect.right = font.size(text[:enum + 1])[0]

                self.image.append(Letter(l, letter, Point(*rect.topleft)))
