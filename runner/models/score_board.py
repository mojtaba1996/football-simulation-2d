from runner.utils.drawing import write_text_on_pygame_screen
from runner.settings.game import SCORE_BOARD_FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, VERTICAL_MARGIN
from runner.settings.colors import SCORE_BOARD_RED_SCORE_COLOR, SCORE_BOARD_BLUE_SCORE_COLOR, SCORE_BOARD_CYCLE_COLOR


class ScoreBoard:
    def __init__(self, red_score, blue_score, cycle_number):
        self.red_score = red_score
        self.blue_score = blue_score
        self.cycle_number = cycle_number

    def show(self, screen):
        write_text_on_pygame_screen(
            screen,
            SCORE_BOARD_FONT_SIZE,
            SCORE_BOARD_RED_SCORE_COLOR,
            str(self.red_score),
            SCORE_BOARD_FONT_SIZE,
            SCORE_BOARD_FONT_SIZE // 2 + VERTICAL_MARGIN,
        )
        write_text_on_pygame_screen(
            screen,
            SCORE_BOARD_FONT_SIZE,
            SCORE_BOARD_BLUE_SCORE_COLOR,
            str(self.blue_score),
            SCREEN_WIDTH - SCORE_BOARD_FONT_SIZE,
            SCORE_BOARD_FONT_SIZE // 2 + VERTICAL_MARGIN,
        )
        write_text_on_pygame_screen(
            screen,
            SCORE_BOARD_FONT_SIZE,
            SCORE_BOARD_CYCLE_COLOR,
            str(self.cycle_number),
            SCREEN_WIDTH - SCORE_BOARD_FONT_SIZE,
            SCREEN_HEIGHT - SCORE_BOARD_FONT_SIZE + VERTICAL_MARGIN,
        )
