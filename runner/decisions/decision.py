from runner.exceptions.decision import DecisionException
from runner.settings import PLAYER_NUMBER as PN


class Decision:
    def __init__(self, the_map, player_number, player_color, priority):
        self.the_map = the_map
        self.player_number = player_number
        self.player_color = player_color
        self.priority = priority
        self.set_player()

    def set_player(self):
        if not 0 <= self.player_number < PN:
            # raise DecisionException(f'ERROR IN DECISION: wrong player number {self.player_number}')
            raise DecisionException('ERROR IN DECISION: wrong player number ' + str(self.player_number))
        if self.player_color == 'red':
            self.player = self.the_map.red_players[self.player_number]
        elif self.player_color == 'blue':
            self.player = self.the_map.blue_players[self.player_number]
