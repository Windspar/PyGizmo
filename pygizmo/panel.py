import pygame
from .core import Display


class Panel(Display):
    def __init__(self, bounds):
        Display.__init__(self, bounds)
