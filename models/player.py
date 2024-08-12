import math

import pygame as pg

import settings.color
import settings.links
import settings.size
import utils.geometry
from .point import Point


class Player:
    def __init__(self, x, y, name, number, color, radius=settings.size.PLAYER_RADIUS, img=None, ban_cycles=0):
        img_link = settings.links.RED_PLAYER_IMG_LINK
        if color == 'blue':
            img_link = settings.links.BLUE_PLAYER_IMG_LINK
        default_img = pg.image.load(img_link)
        default_img = pg.transform.scale(default_img, (2 * radius, 2 * radius))
        default_img.convert_alpha()
        self.x = x
        self.y = y
        self.name = name
        self.number = number
        self.color = color
        self.radius = radius
        self.img = img or default_img
        self.ban_cycles = ban_cycles

    def draw(self, screen):
        pygame_x, pygame_y = utils.geometry.convert_coordinate_cartesian_to_pygame(self.x , self.y)
        screen.blit(self.img, (int(pygame_x)-self.radius, int(pygame_y)-self.radius))
        utils.display.write_text_on_pygame_screen(
            screen,
            settings.size.PLAYER_NUMBER_FONT_SIZE,
            settings.color.PLAYER_TEXTS_COLOR,
            str(self.number),
            self.x - self.radius // 2,
            self.y + self.radius // 2,
        )
        utils.display.write_text_on_pygame_screen(
            screen,
            settings.size.PLAYER_NAME_FONT_SIZE,
            settings.color.PLAYER_TEXTS_COLOR,
            self.name,
            self.x - self.radius,
            self.y - self.radius,
        )

    def move(self, destination, speed):
        distance = utils.geometry.distance(self, destination)
        if distance < speed:
            self.x = int(destination.x)
            self.y = int(destination.y)
        else:
            alpha = math.atan2((destination.y - self.y), (destination.x - self.x))
            self.x += int(speed * math.cos(alpha))
            self.y += int(speed * math.sin(alpha))

    def is_in_own_penalty_area(self):
        if self.color == 'red':
            p = Point(-settings.size.FOOTBALL_PITCH_WIDTH // 2, 0)
        elif self.color == 'blue':
            p = Point(settings.size.FOOTBALL_PITCH_WIDTH // 2, 0)
        if utils.geometry.distance(self, p) < settings.size.PENALTY_AREA_WIDTH:
            return True
        else:
            return False

    @property
    def info(self):
        return {
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'number': self.number,
            'radius': self.radius,
            'ban_cycles': self.ban_cycles
        }

    @property
    def info_reversed(self):
        return {
            'x': -self.x,
            'y': -self.y,
            'name': self.name,
            'number': self.number,
            'radius': self.radius,
            'ban_cycles': self.ban_cycles,
        }
