import random

import utils
from .decision import Decision


class GrabDecision(Decision):
    def __init__(self, runner, player_number, player_color):
        super().__init__(runner, player_number, player_color)

    def perform(self):
        if self._can_grab():
            self.runner.ball.owner = self.player
            self.runner.ball.speed = 0
            self.runner.ball.direction = None

    def _can_grab(self):
        grab_radius = self.player.radius + self.runner.ball.radius
        distance = utils.distance(self.runner.ball, self.player)
        r = random.randint(0, 9)
        if distance < grab_radius and (r < 5 or self.runner.ball.owner is None):
            return True
        return False
