class TextEffects:
    def __init__(self, o_draw=False, o_update=False, show=False, effect=None):
        self.link = {'text':None}
        self.override_draw = o_draw
        self.override_update = o_update
        self.always_show = show
        self.effect = effect

    def draw(self, surface, bounds):
        if self.draw_effect(surface, bounds):
            self.on_draw(surface, bounds)
            return False
        return True

    def draw_effect(self, surface, bounds):
        if self.effect is None:
            return True

        boolean = self.effect.draw(surface, bounds)
        return not self.effect.override_draw and not boolean

    def event(self, event):
        self.on_event(event)
        if self.effect:
            self.effect.event(event)

    def on_draw(self, surface, bounds):
        pass

    def on_update(self, text, font):
        pass

    def on_event(self, event):
        pass

    def set_effect(self, effect):
        self.effect = effect
        if effect:
            self.effect.link = self.link

    def update(self, text, font):
        if self.update_effect(text, font):
            self.on_update(text, font)
            return False
        return True

    def update_effect(self, text, font):
        if self.effect:
            boolean = self.effect.update(text, font)
            if self.effect.override_update:
                self.bounds = Bounds(self.image.get_rect())

            return not self.effect.override_update and not boolean
        return True
