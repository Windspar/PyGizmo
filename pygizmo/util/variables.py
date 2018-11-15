
class CallVariable:
    def __init__(self, value, callback):
        self.variable = value
        self.callback = callback

    def __call__(self, value=None):
        if value:
            self.variable = value
            self.callback()
        else:
            return self.variable

    def clear(self):
        self.variable = None
        self.callback()
