import math

import pygame as pg

import utils


class Ball:
    def __init__(self, x=None, y=None, radius=None, img=None, owner=None, speed=None, direction=None):
        default_ball_image = pg.image.load(utils.BALL_IMG_LINK)
        default_ball_image = pg.transform.scale(default_ball_image, (2 * utils.BALL_RADIUS, 2 * utils.BALL_RADIUS))
        default_ball_image.convert_alpha()
        self.x = x or 0
        self.y = y or 0
        self.radius = radius or utils.BALL_RADIUS
        self.img = img or default_ball_image
        self.owner = owner
        self.speed = speed or 0
        self.direction = direction

    def draw(self, screen):
        pygame_x, pygame_y = utils.convert_coordinate_cartesian_to_pygame(self.x, self.y)
        screen.blit(
            self.img,
            (int(pygame_x) - self.radius, int(pygame_y) - self.radius)
        )

    def move(self):
        if self.owner is None:
            if self.speed == 0 or self.direction is None:
                return
            self.x += self.speed * math.cos(math.radians(self.direction))
            self.y += self.speed * math.sin(math.radians(self.direction))
            self.speed -= utils.FRICTION
            if self.speed < 0:
                self.speed = 0
                self.direction = None
            if self.x < -utils.FOOTBALL_PITCH_WIDTH // 2 + self.radius:
                self.x = -utils.FOOTBALL_PITCH_WIDTH // 2 + self.radius + 1
                self.direction = 180 - self.direction
            if self.x > utils.FOOTBALL_PITCH_WIDTH // 2 - self.radius:
                self.x = utils.FOOTBALL_PITCH_WIDTH // 2 - self.radius - 1
                self.direction = 180 - self.direction
            if self.y < -utils.FOOTBALL_PITCH_HEIGHT // 2 + self.radius:
                self.y = -utils.FOOTBALL_PITCH_HEIGHT // 2 + self.radius + 1
                self.direction = (self.direction + 180) % 360
                self.direction = 180 - self.direction
            if self.y > utils.FOOTBALL_PITCH_HEIGHT // 2 - self.radius:
                self.y = utils.FOOTBALL_PITCH_HEIGHT // 2 - self.radius - 1
                self.direction = (self.direction + 180) % 360
                self.direction = 180 - self.direction
        else:
            self.x = self.owner.x
            self.y = self.owner.y

    @property
    def info(self):
        return {
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
            'owner_color': None if self.owner is None else self.owner.color,
            'owner_number': None if self.owner is None else self.owner.number,
            'direction': self.direction,
            'speed': self.speed,
        }

    @property
    def info_reversed(self):
        owner_color = None
        if self.owner is not None:
            if self.owner.color == 'blue':
                owner_color = 'red'
            else:
                owner_color = 'blue'
        direction = self.direction
        if direction is not None:
            direction = (direction + 180) % 360
        return {
            'x': -self.x,
            'y': -self.y,
            'radius': self.radius,
            'owner_color': owner_color,
            'owner_number': None if self.owner is None else self.owner.number,
            'direction': direction,
            'speed': self.speed,
        }
