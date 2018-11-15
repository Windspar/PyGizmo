Gizmo
=====
* Work in progress
* widget framework for pygame

## Requirements ##
* Made in linux (Antergos (Arch Linux))
* Made in python 3.7
* pygame
* numpy

### Under Construction ###
* layout

##### Example #####
``` python
import pygame
import pygizmo as gizmo

class Scene:
    def __init__(self):
        # basic pygame setup
        pygame.display.set_caption('PyGizmo Example')
        self.rect = pygame.Rect(0, 0, 800, 600)
        self.surface = pygame.display.set_mode(self.rect.size)
        self.clock = pygame.time.Clock()

        # panel will handle all gizmos
        self.panel = gizmo.Panel(self.rect.inflate(-10, -10))
        self.panel.background_color = (40,0,0)
        # simple button
        button = gizmo.Button('Button', (20, 20, 120, 40), self.push_button)
        # bind it to the panel
        self.panel.bind(button)
        # simple Label
        label = gizmo.Label('Label', position=(20, 80))
        self.panel.bind(label)
        # if you want key held in EntryBox to repeat
        pygame.key.set_repeat(80, 80)
        # entrybox
        entry = gizmo.EntryBox(self.entry_return, position=(20, 110))
        self.panel.bind(entry)

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
```
