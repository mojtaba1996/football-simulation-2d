from runner.decisions import Decision, DecisionException
from runner.settings import MAX_KICK_POWER


class Kick(Decision):
    def __init__(self, the_map, player_number, player_color, direction, power):
        super().__init__(the_map, player_number, player_color)
        self.direction = direction
        self.power = power

    def check_errors(self):
        super().check_errors()
        if not 0 <= self.power <= MAX_KICK_POWER:
            # raise DecisionException(f'ERROR IN DECISION: Wrong kick power {self.power}')
            raise DecisionException('ERROR IN DECISION: Wrong kick power ' + str(self.power))
        if self.the_map.ball.owner != self.player:
            raise DecisionException('ERROR IN DECISION: The player is not the owner of the ball')

    def perform(self):
        self.check_errors()
        self.the_map.ball.owner = None
        self.the_map.ball.direction = self.direction
        self.the_map.ball.speed = self.power
