import math

from runner.decisions import Decision
from runner.exceptions.decision import DecisionException
from runner.settings import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


# from runner.utils import get_direction, get_distance


def get_direction(a, b):
    x = b.x - a.x
    y = b.y - a.y
    return math.degrees(math.atan2(y, x))


def get_distance(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


class Move(Decision):
    def __init__(self, the_map, player_number, player_color, destination, speed):
        super().__init__(the_map, player_number, player_color)
        self.destination = destination
        self.speed = speed

    def check_errors(self):
        super().check_errors()
        if not 0 <= self.speed <= PLAYER_SPEED[-1]:
            raise DecisionException(f'ERROR IN DECISION: Wrong movement speed {self.speed}')
        if not -SCREEN_WIDTH // 2 < self.destination.x < SCREEN_WIDTH // 2 or \
                not -SCREEN_HEIGHT // 2 < self.destination.y < SCREEN_HEIGHT // 2:
            # raise DecisionException(f'ERROR IN DECISION: Cannot move out of screen')
            raise DecisionException('ERROR IN DECISION: Cannot move out of screen')

    def perform(self):
        self.check_errors()
        distance = get_distance(self.player, self.destination)
        if distance < self.speed:
            self.player.x = self.destination.x
            self.player.y = self.destination.y
        else:
            self.player.move(get_direction(self.player, self.destination), self.speed)
