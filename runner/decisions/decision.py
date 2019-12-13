from runner.exceptions.decision import DecisionException
from runner.settings import PLAYER_NUMBER


class Decision:
    def __init__(self, the_map, player_number, player_color):
        self.the_map = the_map
        self.player = None
        self.set_player(player_number, player_color)

    def set_player(self, player_number, player_color):
        if not 0 <= player_number < PLAYER_NUMBER:
            # raise DecisionException(f'ERROR IN DECISION: wrong player number {self.player_number}')
            raise DecisionException('ERROR IN DECISION: wrong player number ' + str(player_number))
        if player_color == 'red':
            self.player = self.the_map.red_players[player_number]
        elif player_color == 'blue':
            self.player = self.the_map.blue_players[player_number]

    def check_errors(self):
        if self.player.ban_cycles > 0:
            raise DecisionException(
                'ERROR IN DECISION: player_' +
                str(self.player.number) +
                ' is banned for ' +
                str(self.player.ban_cycles) +
                ' cycles'
            )
