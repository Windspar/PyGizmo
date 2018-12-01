class ColorFrame:
    def __init__(self, foreground=None,
                       background=None,
                       hover=None,
                       selected=None,
                       border=None):
                       
        self.hover = hover
        self.border = border
        self.selected = selected
        self.foreground = foreground
        self.background = background
