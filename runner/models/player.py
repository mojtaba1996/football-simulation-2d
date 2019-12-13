import math
import pygame as pg
from runner.settings import PLAYER_COLOR, PLAYER_NUMBER_FONT_SIZE, PLAYER_NAME_FONT_SIZE, PENALTY_ARIA_X
from runner.utils import convert_coordinate_normal_to_pygame, write_text_on_pygame_screen


class Player:
    def __init__(self, x, y, name, number, color, radius, ban_cycles=0):
        self.x = x
        self.y = y
        self.name = name
        self.number = number
        self.color = color
        self.radius = radius
        self.ban_cycles = ban_cycles

    def move(self, direction, amount):
        self.x += amount * math.cos(math.radians(direction))
        self.y += amount * math.sin(math.radians(direction))

    def show(self, screen):
        x_for_pygame, y_for_pygame = convert_coordinate_normal_to_pygame(self.x, self.y)
        (num_x_for_pygame,
         num_y_for_pygame) = convert_coordinate_normal_to_pygame(self.x - self.radius, self.y - self.radius)
        (name_x_for_pygame,
         name_y_for_pygame) = convert_coordinate_normal_to_pygame(self.x - self.radius // 2, self.y + self.radius // 2)
        pg.draw.circle(screen, PLAYER_COLOR[self.color], (int(x_for_pygame), int(y_for_pygame)), int(self.radius), 0)
        write_text_on_pygame_screen(
            screen,
            PLAYER_NUMBER_FONT_SIZE,
            (255, 255, 255),
            str(self.number),
            name_x_for_pygame,
            name_y_for_pygame,
        )
        write_text_on_pygame_screen(
            screen,
            PLAYER_NAME_FONT_SIZE,
            (255, 255, 255),
            self.name,
            num_x_for_pygame,
            num_y_for_pygame,
        )

    def is_in_his_penalty_area(self):
        distance = PENALTY_ARIA_X  # :D
        if self.color == 'red':
            distance = ((self.x + 500) ** 2 + (self.y ** 2)) ** 0.5
        elif self.color == 'blue':
            distance = ((self.x - 500) ** 2 + (self.y ** 2)) ** 0.5
        if distance < PENALTY_ARIA_X:
            return True
        else:
            return False
