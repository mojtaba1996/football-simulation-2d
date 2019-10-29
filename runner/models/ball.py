from runner.settings import FRICTION, BALL_COLOR, SCREEN_WIDTH as SW, SCREEN_HEIGHT as SH
from runner.utils import convert_coordinate_normal_to_pygame
import math
import pygame as pg


class Ball:
    def __init__(self, x, y, speed, direction, radius):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.radius = radius
        self.owner = None

    def move(self):
        if self.owner is None:
            self.x += self.speed * math.cos(math.radians(self.direction))
            self.y += self.speed * math.sin(math.radians(self.direction))
            self.speed -= FRICTION
            if self.speed < 0:
                self.speed = 0
            if self.x < -SW // 2 + self.radius:
                self.x = -SW // 2 + self.radius + 1
                self.direction = 180 - self.direction
            if self.x > SW // 2 - self.radius:
                self.x = SW // 2 - self.radius - 1
                self.direction = 180 - self.direction
            if self.y < -SH // 2 + self.radius:
                self.y = -SH // 2 + self.radius + 1
                self.direction = (self.direction + 180) % 360
                self.direction = 180 - self.direction
            if self.y > SH // 2 - self.radius:
                self.y = SH // 2 - self.radius - 1
                self.direction = (self.direction + 180) % 360
                self.direction = 180 - self.direction

        else:
            self.x = self.owner.x
            self.y = self.owner.y

    def show(self, screen):
        x_for_pygame, y_for_pygame = convert_coordinate_normal_to_pygame(self.x, self.y)
        pg.draw.circle(screen, BALL_COLOR, (int(x_for_pygame), int(y_for_pygame)), self.radius, 0)
