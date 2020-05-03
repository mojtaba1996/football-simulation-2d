import math
import pygame as pg
from runner.settings import PLAYER_COLOR, PLAYER_NUMBER_FONT_SIZE, PLAYER_NAME_FONT_SIZE, PENALTY_ARIA_X, PLAYER_RADIUS, red_players_initial_position, red_circle_img_link, \
    blue_players_initial_information, blue_circle_img_link, BALL_RADIUS, PLAYER_NUMBER
from runner.utils import convert_coordinate_normal_to_pygame, write_text_on_pygame_screen


class Player:
    def __init__(self, x, y, name, number, color, radius, img, ban_cycles=0):
        self.x = x
        self.y = y
        self.name = name
        self.number = number
        self.color = color
        self.radius = radius
        self.img = img
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
        screen.blit(self.img, (int(x_for_pygame)-self.radius, int(y_for_pygame)-self.radius))
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

def init_players(red_players, blue_players):
    red_players.clear()
    blue_players.clear()
    for i in range(PLAYER_NUMBER):
        red_radius = red_players_initial_position[i]['radius']
        red_image = pg.image.load(red_circle_img_link)
        red_image = pg.transform.scale(red_image, (2*red_radius, 2*red_radius))
        red_image.convert_alpha()
        red_players.append(Player(
            x=red_players_initial_position[i]['x'],
            y=red_players_initial_position[i]['y'],
            name=red_players_initial_position[i]['name'],
            number=i,
            color='red',
            radius=red_radius,
            img=red_image,
            ban_cycles=0,
        ))
        blue_radius = red_players_initial_position[i]['radius']
        blue_image = pg.image.load(blue_circle_img_link)
        blue_image = pg.transform.scale(blue_image, (2*blue_radius, 2*blue_radius))
        blue_image.convert_alpha()
        blue_players.append(Player(
            x=blue_players_initial_information[i]['x'],
            y=blue_players_initial_information[i]['y'],
            name=red_players_initial_position[i]['name'],
            number=i,
            color='blue',
            radius=blue_radius,
            img=blue_image,
            ban_cycles=0,
        ))
