import pygame
import pygizmo as gizmo
from pygizmo.layout import Box

class Scene:
    def __init__(self):
        # basic pygame setup
        pygame.display.set_caption('PyGizmo Example')
        self.rect = pygame.Rect(0, 0, 800, 600)
        self.surface = pygame.display.set_mode(self.rect.size)
        self.clock = pygame.time.Clock()

        # panel will handle all gizmos
        self.panel = gizmo.Panel(self.rect.inflate(-10, -10))
        self.panel.background_color = (0,0,40)

        self.intro_font = gizmo.Font(None, 24)
        self.labels = [
            gizmo.Label('Welcome to PyGizmo.', self.intro_font),
            gizmo.Label('PyGizmo has', self.intro_font),
        ]

        for item in 'Buttons Labels Entries Panels'.split():
            label = gizmo.Label(item, self.intro_font)
            self.labels.append(label)

        # First box need bounds
        self.hbox = Box.h(gizmo.Anchor.H.center, bounds=self.panel.bounds)
        self.vbox = Box.v(spacing=self.intro_font.get_linesize() // 2)
        self.vbox.add(self.labels, center=True)
        self.hbox.add(self.vbox)

        self.hbox.update()
        self.panel.bind(self.hbox)

        # Text Effects and Font color change
        self.text_font = gizmo.Font()
        dimension = self.panel.bounds.dimension / 2
        self.labels_hbox = Box.h(spacing=40, bounds=(0, dimension.h, *dimension))
        self.text_vbox = Box.v(spacing=self.text_font.get_linesize() // 2)
        self.text_labels = [
            gizmo.Label('Let see text.', self.text_font),
            gizmo.Label('Change color.', self.text_font)
        ]

        self.text_vbox.add(self.text_labels)

        self.color_vbox = Box.v(spacing=self.text_font.get_linesize() // 2)
        self.color_labels = [
            gizmo.Label('firebrick'),
            gizmo.Label('dodgerblue'),
            gizmo.Label('lawngreen')
        ]

        for label in self.color_labels:
            hilight = gizmo.effects.Hilight(pygame.Color('seagreen'))
            hilight.set_effect(gizmo.effects.Clickable(self.click_label))
            label.set_effect(hilight)

        self.color_vbox.add(self.color_labels)
        self.labels_hbox.add(self.text_vbox)
        self.labels_hbox.add(self.color_vbox)

        self.labels_hbox.update()
        self.panel.bind(self.labels_hbox)

    def click_label(self, text, data):
        self.text_font.foreground(pygame.Color(text()))

    def push_button(self, button):
        print('Button Push')

    def entry_return(self, text):
        print('Entry', text)

    def loop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.panel.event(event)

            self.surface.fill((0,0,0))
            self.panel.draw(self.surface)
            pygame.display.flip()
            self.clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    scene = Scene()
    scene.loop()
    pygame.quit()
