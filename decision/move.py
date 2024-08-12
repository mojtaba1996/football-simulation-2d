import exception
import settings.game
import settings.size
from .decision import Decision


class MoveDecision(Decision):
    def __init__(self, runner, player_number, player_color, destination, speed):
        super().__init__(runner, player_number, player_color)
        self.destination = destination
        self.speed = speed

    def validate(self):
        super().validate()
        if not 0 <= self.speed <= settings.game.MAX_PLAYER_SPEED:
            raise exception.DecisionException('Wrong move speed')
        if not -settings.size.FOOTBALL_PITCH_WIDTH // 2 < self.destination.x < settings.size.FOOTBALL_PITCH_WIDTH // 2 or \
                not -settings.size.FOOTBALL_PITCH_HEIGHT // 2 < self.destination.y < settings.size.FOOTBALL_PITCH_HEIGHT // 2:
            raise exception.DecisionException('Cannot move out of screen')

    def perform(self):
        self.player.move(self.destination, self.speed)
