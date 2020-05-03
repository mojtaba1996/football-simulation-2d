from runner.settings import FRICTION, BALL_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, ball_circle_img_link, BALL_RADIUS
from runner.utils import convert_coordinate_normal_to_pygame
import math
import pygame as pg


class Ball:
    def __init__(self, x, y, speed, direction, radius, img):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.radius = radius
        self.img = img
        self.owner = None

    def move(self):
        if self.owner is None:
            self.x += self.speed * math.cos(math.radians(self.direction))
            self.y += self.speed * math.sin(math.radians(self.direction))
            self.speed -= FRICTION
            if self.speed < 0:
                self.speed = 0
            if self.x < -SCREEN_WIDTH // 2 + self.radius:
                self.x = -SCREEN_WIDTH // 2 + self.radius + 1
                self.direction = 180 - self.direction
            if self.x > SCREEN_WIDTH // 2 - self.radius:
                self.x = SCREEN_WIDTH // 2 - self.radius - 1
                self.direction = 180 - self.direction
            if self.y < -SCREEN_HEIGHT // 2 + self.radius:
                self.y = -SCREEN_HEIGHT // 2 + self.radius + 1
                self.direction = (self.direction + 180) % 360
                self.direction = 180 - self.direction
            if self.y > SCREEN_HEIGHT // 2 - self.radius:
                self.y = SCREEN_HEIGHT // 2 - self.radius - 1
                self.direction = (self.direction + 180) % 360
                self.direction = 180 - self.direction

        else:
            self.x = self.owner.x
            self.y = self.owner.y

    def show(self, screen):
        x_for_pygame, y_for_pygame = convert_coordinate_normal_to_pygame(self.x, self.y)
        screen.blit(self.img, (int(x_for_pygame)-self.radius, int(y_for_pygame)-self.radius))

def init_ball():
    ball_image = pg.image.load(ball_circle_img_link)
    ball_image = pg.transform.scale(ball_image, (2*BALL_RADIUS, 2*BALL_RADIUS))
    ball_image.convert_alpha()
    return Ball(x=0, y=0, speed=0, direction=-1, radius=BALL_RADIUS, img=ball_image)