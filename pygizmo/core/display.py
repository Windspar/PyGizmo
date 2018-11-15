import pygame
from .bin import Bin


class Display(Bin):
    def __init__(self, bounds):
        Bin.__init__(self, bounds)
        self._surface = pygame.Surface(self.bounds.dimension.astype(int))
        self.background_color = pygame.Color('black')

    def draw(self, surface, bounds=None):
        self._surface.fill(self.background_color)
        Bin.draw(self, self._surface, bounds)
        surface.blit(self._surface, self.bounds)

    def is_display(self):
        return True
