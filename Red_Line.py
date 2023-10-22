import pygame
import random

green = 150, 200, 20
blue = 67, 84, 255
orange = 255, 165, 0
red = 250, 0, 0
purple = 172, 79, 198
gray = 128, 128, 128
white = 255, 255, 255

vel = 1

class RED_LINE():
    def __init__(self, total_width, top):
        self.x = random.randint(0, total_width-100)
        self.y = random.randint(top, -500)
        self.total_width = total_width
        self.top = top

    def draw(self, screen):
        pygame.draw.line(screen, red, (self.x, self.y), (self.x + 100, self.y + 100), 6)
        pygame.draw.line(screen, (215, 215, 215), (self.x, self.y + 30), (self.x + 100, self.y + 30 + 100), 2)
        pygame.draw.line(screen,  (215, 215, 215), (self.x, self.y + 45), (self.x + 100, self.y + 45 + 100), 1)
        pygame.draw.circle(screen, red, (self.x, self.y), 10)
        pygame.draw.circle(screen, red, (self.x + 100, self.y + 100), 10)
        pygame.draw.circle(screen, red, (self.x, self.y), 20, 1)
        pygame.draw.circle(screen, red, (self.x + 100, self.y + 100), 20, 1)

    def update(self, total_height, dt):
        self.y += vel * dt
        if self.y > total_height:
            self.x = random.randint(0, self.total_width - 100)
            self.y = random.randint(self.top, 0)

    def reset(self):
        self.x = random.randint(0, self.total_width - 100)
        self.y = random.randint(self.top, 0)