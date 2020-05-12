from runner.settings import SCREEN_HEIGHT, SCREEN_WIDTH, VERTICAL_MARGIN
import pygame as pg


def convert_coordinate_normal_to_pygame(x, y):
    new_x = SCREEN_WIDTH // 2 + x
    new_y = SCREEN_HEIGHT // 2 + VERTICAL_MARGIN - y
    return new_x, new_y


def write_text_on_pygame_screen(screen, font_size, color, text, x, y, font=None):
    font = pg.font.Font(font, font_size)
    text_render = font.render(text, True, color)
    screen.blit(text_render, (int(x), int(y)))
