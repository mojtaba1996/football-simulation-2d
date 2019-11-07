from runner.decisions import Decision, DecisionException
from runner.settings import MAX_KICK_POWER as MKP


class Kick(Decision):
    def __init__(self, the_map, player_number, player_color, direction, power, priority):
        super().__init__(the_map, player_number, player_color, priority)
        self.direction = direction
        self.power = power

    def check_errors(self):
        if not 0 <= self.power <= MKP:
            raise DecisionException(f'ERROR IN DECISION: Wrong kick power {self.power}')
        if self.the_map.ball.owner != self.player:
            raise DecisionException(f'ERROR IN DECISION: The player is not the owner of the ball')

    def perform(self):
        self.check_errors()
        self.the_map.ball.owner = None
        self.the_map.ball.direction = self.direction
        self.the_map.ball.speed = self.power
