import pygame
from .text_effects import TextEffects

class Clickable(TextEffects):
    def __init__(self, callback, pydata=None):
        TextEffects.__init__(self)
        self.callback = callback
        self.pydata = None

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.link['text'].parent._hover:
                    self.callback(self.link['text'], self.pydata)
