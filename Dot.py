import pygame

green = 150, 200, 20
blue = 67, 84, 255
orange = 255, 165, 0
red = 250, 0, 0
purple = 172, 79, 198
gray = 128, 128, 128
white = 255, 255, 255
black = 0, 0, 0

class PATH():
    def __init__(self, x1, y1):
        self.x1, self.y1 = x1, y1
        self.width = 10
        self.c1, self.c2, self.c3 = 67, 84, 255

    def draw(self, screen):
        pygame.draw.circle(screen, (self.c1, self.c2, self.c3), (self.x1, self.y1), self.width)

    def update(self):
        if self.width >= 0:
            #self.width -= 0.2
            self.width -= 0.15
        if self.c1 > 0:
            self.c1 -= 1
            self.c2 -= 1
            self.c3 -= 1