import pygame
import random

class dot_anim():
    def __init__(self, x, y, color, duration, width):
        self.x = x
        self.y = y
        self.dir = None
        self.dir_2 = None
        self.c1, self.c2, self.c3 = color
        self.width = width
        self.duration = duration

    def draw(self, screen):
        self.dir = random.randint(-4, 4)
        self.dir_2 = random.randint(1, 2)
        pygame.draw.circle(screen, (self.c1, self.c2, self.c3), (self.x, self.y), self.width)

    def update(self):
        if self.c1 > 0:
            self.c1 -= self.duration
            self.c2 -= self.duration
            self.c3 -= self.duration
        self.x -= self.dir*2
        if self.dir_2 == 1:
            self.y -= self.dir*2
        else:
            self.y -= -self.dir * 2
        self.width -= 1