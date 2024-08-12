import pygame as pg

from .geometry import convert_coordinate_cartesian_to_pygame


def write_text_on_pygame_screen(screen, font_size, color, text, cartesian_x, cartesian_y, font=None):
    pygame_x, pygame_y = convert_coordinate_cartesian_to_pygame(cartesian_x, cartesian_y)
    font = pg.font.Font(font, font_size)
    text_render = font.render(text, True, color)
    screen.blit(text_render, (pygame_x, pygame_y))
