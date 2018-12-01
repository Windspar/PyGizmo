import pygame


class Carrot:
    def __init__(self, font, carrot=None):
        self.update_font(font)
        font.add_callback(self.update_font)

        if carrot:
            self.carrot = list(carrot)
            self.length = len(carrot)
            self.pos = self.length
        else:
            self.carrot = []
            self.length = 0
            self.pos = 0

        self.inverse_letter = None
        self.position = (0,0)
        self.show = True
        self.left = 0

    def blink(self):
        self.show = not self.show

    def color(self, color):
        self.image.fill(color)

    def draw(self, surface):
        if self.show:
            x, y = self.position
            x += self.left
            surface.blit(self.image, (x, y + 1))
            if self.inverse_letter:
                surface.blit(self.inverse_letter, (x, y))

    def update_font(self, font):
        h = font.get_linesize() - 2
        self.image = pygame.Surface((1, h))
        self.image.fill(font.foreground.read_value)
