import pygame
from .label import Label
from .array import Bounds, Point, Dimension
from .core import Carrot, Gizmo, Recall


class EntryColor:
    def __init__(self):
        self.text = pygame.Color('white')
        self.hover = pygame.Color('aliceblue')
        self.border = pygame.Color('darkblue')
        self.selected = pygame.Color('lightskyblue')
        self.background = pygame.Color('dodgerblue')

class Entry(Gizmo):
    # default font
    font = pygame.font.Font(None, 16)

    def __init__(self, callback,
                 font = None,
                 dimension=None,
                 position=(0,0),
                 colors=EntryColor(),
                 box=False):

        if font is None:
            font = Entry.font

        if isinstance(dimension, Dimension):
            dimension = tuple(dimension)

        if dimension is None:
            dimension = 200, int(font.get_linesize() * 1.5)
        elif dimension[0] == -1:
            dimension = 200, dimension[1]
        elif dimension[1] == -1:
            dimension = dimension[0], int(font.get_linesize() * 1.5)

        Gizmo.__init__(self, (*position, *dimension))
        if box:
            position = Point(1, (self.bounds.h - font.get_linesize()) // 2)
        else:
            position = Point(self.bounds.x + 2, (self.bounds.h - font.get_linesize()) // 2 + self.bounds.y)

        self.label = Label("", font, colors.text, position.copy())
        self.carrot = Carrot(font, colors.text)
        self.carrot.position = position.copy()
        self.callback = callback
        self.recall = Recall()
        self.colors = colors
        self.buffer = []
        self.offset = Point(0,0)

        self.key_event = {
            pygame.KMOD_NONE: {
                pygame.K_BACKSPACE: self.keydown_backspace,
                pygame.K_DELETE: self.keydown_delete,
                pygame.K_DOWN: self.keydown_down,
                pygame.K_END: self.keydown_end,
                pygame.K_HOME: self.keydown_home,
                pygame.K_LEFT: self.keydown_left,
                pygame.K_RETURN: self.keydown_return,
                pygame.K_RIGHT: self.keydown_right,
                pygame.K_UP: self.keydown_up
            }
        }

    def keydown_backspace(self):
        if self.carrot.pos > 1:
            front = self.buffer[:self.carrot.pos - 1]
            back = self.buffer[self.carrot.pos:]
            self.buffer = front + back
            self.carrot.pos -= 1
        else:
            self.keydown_delete()

    def keydown_delete(self):
        self.carrot.pos = self.carrot.length
        self.carrot.left = 0
        self.buffer = self.carrot.carrot[:]
        self.offset = Point(0,0)

    def keydown_down(self):
        self.buffer = self.recall.down()
        if self.buffer:
            self.carrot.pos = len(self.buffer)
        else:
            self.keydown_delete()

    def keydown_end(self):
        self.carrot.pos = len(self.buffer)

    def keydown_home(self):
        self.carrot.pos = self.carrot.length

    def keydown_left(self):
        if self.carrot.pos > self.carrot.length:
            self.carrot.pos -= 1

    def keydown_return(self):
        self.recall.store(self.buffer)
        text = ''.join(self.buffer)
        self.keydown_delete()
        self.callback(text)

    def keydown_right(self):
        if self.carrot.pos < len(self.buffer):
            self.carrot.pos += 1

    def keydown_up(self):
        recall_buffer = self.recall.up()
        if recall_buffer:
            self.buffer = recall_buffer
            self.carrot.pos = len(self.buffer)

    def on_draw(self, surface, bounds):
        if bounds is None:
            bounds = self.bounds

        surface.fill(self.colors.background, self.bounds)

        if self._selected:
            foreground = self.colors.text
        elif self._hover:
            foreground = self.colors.selected
        else:
            foreground = self.colors.border

        if self._selected:
            self.carrot.draw(surface)

        self.label.color(foreground)
        self.label.draw(surface)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and self._selected:
            self.carrot.show = True
            ctrl = event.mod & pygame.KMOD_CTRL
            if ctrl == 0 and 31 < event.key < 127:
                self.buffer.insert(self.carrot.pos, event.unicode)
                self.carrot.pos += 1
                self.update_label()
            elif ctrl == 0:
                if self.key_event[pygame.KMOD_NONE].get(event.key, False):
                    self.key_event[pygame.KMOD_NONE][event.key]()
                    self.update_label()

    def update_label(self):
        if len(self.buffer) > 0:
            font = self.label.font()
            text = ''.join(self.buffer)

            if self.carrot.pos > self.offset.y:
                self.offset.y = self.carrot.pos
            elif self.carrot.pos < self.offset.x:
                self.offset.x = self.carrot.pos

            width = self.bounds.w - 3
            while font.size(text[self.offset.x:self.offset.y])[0] < width and self.offset.x > 0:
                self.offset.x -= 1

            while font.size(text[self.offset.x:self.offset.y])[0] > width and self.offset.x < self.carrot.pos:
                self.offset.x += 1

            while font.size(text[self.offset.x:self.offset.y])[0] < width and self.offset.y < len(self.buffer):
                self.offset.y += 1

            while font.size(text[self.offset.x:self.offset.y])[0] > width:
                self.offset.y -= 1

            self.label.text(text[self.offset.x:self.offset.y])

            self.carrot.left = font.size(text[self.offset.x:self.carrot.pos])[0]
        else:
            self.label.text.clear()
            self.keydown_delete()

class EntryBox(Entry):
    def __init__(self, callback,
                 font = None,
                 dimension=None,
                 position=(0,0),
                 colors=EntryColor()):

        Entry.__init__(self, callback, font, dimension, position, colors, True)
        dim = self.bounds.dimension + 4
        self.text_border = pygame.Surface(dim)
        self.text_background = pygame.Surface(self.bounds.dimension)

    def on_draw(self, surface, bounds):
        if bounds is None:
            bounds = self.bounds

        if self._selected:
            border = self.colors.selected
        elif self._hover:
            border = self.colors.hover
        else:
            border = self.colors.border

        self.text_border.fill(border)
        self.text_background.fill(self.colors.background)

        if self._selected:
            self.carrot.draw(self.text_background)

        self.label.draw(self.text_background)
        self.text_border.blit(self.text_background, (2,2))
        surface.blit(self.text_border, bounds)

    def on_event(self, event):
        Entry.on_event(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self._hover:
                self._selected = True
            else:
                self._selected = False
