from ...util import FunctionVariable
from ...array import Bounds
#from ..font import Font

# Uses PyGizmo Font
# Text(PyGizmo Font, python string, PyGizmo Text Effect)
class Text:
    def __init__(self, parent, font, text=None, effect=None):
        self.parent = parent
        self.text = FunctionVariable(text, self.on_update)
        font.add_callback(self.update_font)
        self.font = FunctionVariable(font, self.on_update)
        self.bounds = Bounds()
        self.set_effect(effect)

    def __call__(self, text=None):
        if text is None:
            return self.text.read_value
        self.text(text)

    def clear(self):
        self.text.clear()

    def draw_effect(self, surface, bounds):
        if self.effect is None:
            return True

        self.effect.draw(surface, bounds)
        return not self.effect.override_draw

    def on_draw(self, surface, bounds=None):
        if bounds is None:
            bounds = self.bounds

        if self.draw_effect(surface, bounds):
            if self.image and bounds is not None:
                surface.blit(self.image, bounds)

    def on_event(self, event):
        if self.effect:
            self.effect.event(event)

    def on_update(self):
        text = self.text.read_value
        font = self.font.read_value

        if font and text:
            if self.update_effect(text, font):
                self.image = font.render(text)
                self.bounds = Bounds(self.image.get_rect())
        else:
            self.image = None
            self.bounds = Bounds()

    def set_effect(self, effect):
        self.effect = effect
        if effect:
            self.effect.link['text'] = self

        self.on_update()

    def set_foreground(self, color):
        self.font.foreground = color
        self.on_update()

    def update_effect(self, text, font):
        if self.effect:
            self.effect.update(text, font)
            if self.effect.override_update:
                self.bounds = Bounds(self.image.get_rect())

            return not self.effect.override_update
        return True

    def update_font(self, font):
        self.on_update()
