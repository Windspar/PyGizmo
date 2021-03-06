import pygame

def alpha(surface, alpha, op='set'):
    array = pygame.surfarray.pixels_alpha(surface)
    w, h = array.shape
    for x in range(w):
        for y in range(h):
            if op == 'set':
                array[x][y] = alpha
            elif op == 'sub':
                if array[x][y] - alpha < 0:
                    array[x][y] = 0
                else:
                    array[x][y] = array[x][y] - alpha
            elif op == 'add':
                if array[x][y] + alpha > 255:
                    array[x][y] = 255
                else:
                    array[x][y] = array[x][y] + alpha
            elif op == 'mul':
                if array[x][y] * alpha > 255:
                    array[x][y] = 255
                else:
                    array[x][y] = array[x][y] * alpha
            else:
                return
