import pygame
from ..util import FunctionVariable


class Font:
    def __init__(self, fontname=None, size=16, foreground=(255,255,255), background=None):
        self.name = FunctionVariable(fontname, self.update_font)
        self.size = FunctionVariable(size, self.update_font)
        self.foreground = FunctionVariable(foreground, self.update)
        self.background = FunctionVariable(background, self.update)
        self.callbacks = []

        self.update_font()

    def __call__(self, foreground, background=None):
        return FontLink(self, foreground, background)

    def add_callback(self, item):
        self.callbacks.append(item)

    def copy(self):
        foreground = self.foreground.read_value
        background = self.background.read_value
        return Font(self.name(), self.size(), foreground, background)

    def remove_callback(self, item):
        self.callbacks.remove(item)

    def render(self, text):
        foreground = self.foreground.read_value
        background = self.background.read_value

        if background:
            return self.font.render(text, 1, foreground, background)
        return self.font.render(text, 1, foreground)

    def render_color(self, text, foreground, background='font'):
        if background == 'font':
            background = self.background.read_value

        if background:
            return self.font.render(text, 1, foreground, background)
        return self.font.render(text, 1, foreground)

    def text_size(self, text):
        return self.font.size(text)

    def get_linesize(self):
        return self.font.get_linesize()

    def update(self):
        for callback in self.callbacks:
            callback(self)

    def update_font(self):
        fontname = self.name.read_value
        size = self.size.read_value

        self.font = pygame.font.Font(fontname, size)
        for callback in self.callbacks:
            callback(self)

class FontLink(Font):
    def __init__(self, font, foreground, background=None):
        self.link = font
        self.foreground = FunctionVariable(foreground, self.update)
        self.background = FunctionVariable(background, self.update)
        self.callbacks = []

    def __call__(self, foreground, background=None):
        return FontLink(self.link, foreground, background)

    def copy(self):
        foreground = self.foreground.read_value
        background = self.background.read_value
        return FontLink(self.font, foreground, background)

    def name(self, fontname=None):
        if fontname:
            self.link.name(fontname)
        else:
            return self.link.name.read_value

    def size(self, size=None):
        if size:
             self.link.size(size)
        else:
            return self.link.size.read_value

    @property
    def font(self):
        return self.link.font
