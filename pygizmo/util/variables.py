
class FunctionVariable:
    def __init__(self, value, callback):
        self.read_value = value
        self.callback = callback

    def __call__(self, value=None):
        if value:
            self.read_value = value
            self.callback()
        else:
            return self.read_value

    def clear(self):
        self.read_value = None
        self.callback()
