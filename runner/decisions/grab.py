import random

from runner.decisions import Decision
from runner.exceptions.decision import DecisionException


class Grab(Decision):
    def __init__(self, the_map, player_number, player_color, priority):
        super().__init__(the_map, player_number, player_color, priority)

    def can_grab(self):
        grab_radius = self.player.radius + self.the_map.ball.radius
        distance = ((self.the_map.ball.x - self.player.x) ** 2 + (self.the_map.ball.y - self.player.y) ** 2) ** 0.5
        r = random.randint(0, 9)
        if distance < grab_radius and (r < 5 or self.the_map.ball.owner is None):
            return True
        return False

    def perform(self):
        if self.can_grab():
            self.the_map.ball.owner = self.player
            self.the_map.ball.speed = 0
