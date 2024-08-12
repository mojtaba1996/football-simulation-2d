import settings.color
import settings.size
import utils.display


class Scoreboard:
    def __init__(self, red_score=0, blue_score=0, cycle_number=0):
        self.red_score = red_score
        self.blue_score = blue_score
        self.cycle_number = cycle_number

    def draw(self, screen):
        utils.display.write_text_on_pygame_screen(
            screen,
            settings.size.SCOREBOARD_FONT_SIZE,
            settings.color.SCOREBOARD_RED_SCORE_COLOR,
            str(self.red_score),
            -settings.size.SCREEN_WIDTH // 2 + settings.size.HORIZONTAL_MARGIN // 3,
            -300,
        )
        utils.display.write_text_on_pygame_screen(
            screen,
            settings.size.SCOREBOARD_FONT_SIZE,
            settings.color.SCOREBOARD_BLUE_SCORE_COLOR,
            str(self.blue_score),
            settings.size.SCREEN_WIDTH // 2 - settings.size.HORIZONTAL_MARGIN * 2 // 3,
            -300,
        )
        utils.display.write_text_on_pygame_screen(
            screen,
            settings.size.SCOREBOARD_FONT_SIZE,
            settings.color.SCOREBOARD_CYCLE_COLOR,
            str(self.cycle_number),
            0,
            -settings.size.FOOTBALL_PITCH_HEIGHT // 2 - settings.size.VERTICAL_MARGIN // 3,
        )

    @property
    def info(self):
        return {
            'red_score': self.red_score,
            'blue_score': self.blue_score,
            'cycle_number': self.cycle_number,
        }

    @property
    def info_reversed(self):
        return {
            'red_score': self.blue_score,
            'blue_score': self.red_score,
            'cycle_number': self.cycle_number,
        }
