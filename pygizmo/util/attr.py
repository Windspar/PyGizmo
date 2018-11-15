
class Attr:
    def __init__(self, parent):
        self.parent = parent

    def __getitem__(self, key):
        return  getattr(self.parent, key)

    def __setitem__(self, key, value):
        setattr(self.parent, key, value)

    def __repr__(self):
        return 'Attr'
