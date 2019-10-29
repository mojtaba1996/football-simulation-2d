import pygame as pg
from runner.utils.drawing import write_text_on_pygame_screen
from runner.settings.game import SCORE_BOARD_FONT_SIZE as SBFS, SCREEN_WIDTH as SW, SCREEN_HEIGHT as SH
from runner.settings.colors import SCORE_BOARD_RED_SCORE_COLOR as SBRSC, SCORE_BOARD_BLUE_SCORE_COLOR as SBBSC, \
    SCORE_BOARD_CYCLE_COLOR as SBCC


class ScoreBoard:
    def __init__(self, red_score, blue_score, cycle_number):
        self.red_score = red_score
        self.blue_score = blue_score
        self.cycle_number = cycle_number

    def show(self, screen):
        write_text_on_pygame_screen(screen, SBFS, SBRSC, str(self.red_score), SBFS, SBFS // 2)
        write_text_on_pygame_screen(screen, SBFS, SBBSC, str(self.blue_score), SW - SBFS, SBFS // 2)
        write_text_on_pygame_screen(screen, SBFS, SBCC, str(self.cycle_number), SW - SBFS, SH - SBFS)
