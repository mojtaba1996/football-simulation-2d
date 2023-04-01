import pygame as pg

from .size import *


def convert_coordinate_cartesian_to_pygame(cartesian_x, cartesian_y):
    pygame_x = SCREEN_WIDTH // 2 + cartesian_x
    pygame_y = SCREEN_HEIGHT // 2 - cartesian_y
    return pygame_x, pygame_y


def write_text_on_pygame_screen(screen, font_size, color, text, cartesian_x, cartesian_y, font=None):
    pygame_x, pygame_y = convert_coordinate_cartesian_to_pygame(cartesian_x, cartesian_y)
    font = pg.font.Font(font, font_size)
    text_render = font.render(text, True, color)
    screen.blit(text_render, (pygame_x, pygame_y))

def distance(cartesian_p1, cartesian_p2):
    return ((cartesian_p1.x - cartesian_p2.x) ** 2 + (cartesian_p1.y - cartesian_p2.y) ** 2) ** 0.5
