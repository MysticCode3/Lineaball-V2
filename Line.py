import pygame
import Line_Animation

green = 150, 200, 20
blue = 67, 84, 255
orange = 255, 165, 0
red = 250, 0, 0
purple = 172, 79, 198
gray = 128, 128, 128
white = 255, 255, 255
black = 0, 0, 0

vel = 1

animation_list = []

class LINE():
    def __init__(self, first_point, second_point):
        self.first_point = first_point
        self.second_point = second_point
        self.first_x = self.first_point[0]
        self.first_y = self.first_point[1]
        self.second_x = self.second_point[0]
        self.second_y = self.second_point[1]
        self.c1, self.c2, self.c3 = 255, 255, 255
        self.c11, self.c22, self.c33 = self.c1 - 40, self.c2 - 40, self.c3 - 40
        self.animation = 20

    def draw(self, screen, pause):
        if self.first_y > 0 and self.second_y > 0:
            pygame.draw.line(screen, (self.c1, self.c2, self.c3), (self.first_x, self.first_y), (self.second_x, self.second_y), 6)
            pygame.draw.line(screen, ( self.c11, self.c22, self.c33), (self.first_x, self.first_y + 30), (self.second_x, self.second_y + 30), 2)
            pygame.draw.line(screen, (self.c11, self.c22, self.c33), (self.first_x, self.first_y + 45), (self.second_x, self.second_y + 45), 1)
            pygame.draw.circle(screen, (self.c1, self.c2, self.c3), (self.second_x, self.second_y), 10)
            pygame.draw.circle(screen, (self.c1, self.c2, self.c3), (self.second_x, self.second_y), 20, 1)
            if not pause:
                animation_list.append(Line_Animation.dot_anim(self.second_x, self.second_y, (255, 255, 255), 1, 5))
        if self.animation < 70:
            pygame.draw.circle(screen, (self.c1, self.c2, self.c3), (self.second_x, self.second_y), self.animation, 1)

    def update(self, screen, dt):
        self.first_y += vel * dt
        self.second_y += vel * dt
        if self.c1 > 1:
            self.c1 -= 2
            self.c2 -= 1
            self.c3 -= 1
        if self.c11 > 1:
            self.c11 -= 1
            self.c22 -= 1
            self.c33 -= 1
        for animation in animation_list:
            animation.draw(screen)
            animation.update()
            if animation.width < 1:
                animation_list.remove(animation)
        if self.animation < 70:
            self.animation += 1

    def collided(self):
        self.first_y += vel*50
        self.second_y += vel*50

    def restart(self):
        animation_list.clear()
