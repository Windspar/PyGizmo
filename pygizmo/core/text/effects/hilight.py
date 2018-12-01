from .text_effects import TextEffects

class Hilight(TextEffects):
    def __init__(self, foreground, background=None):
        TextEffects.__init__(self)
        self.foreground = foreground
        self.background = background
        self.image = None

    def on_draw(self, surface, bounds):
        self.override_draw = self.link['text'].parent._hover
        if self.link['text'].parent._hover:
            surface.blit(self.image, bounds)

    def on_update(self, text, font):
        foreground = font.foreground.read_value
        background = font.background.read_value

        if self.foreground:
            foreground = self.foreground

        if self.background:
            background = self.background

        self.image = font.render_color(text, foreground, background)
