import exception
import utils

class Decision:
    def __init__(self, runner, player_number, player_color):
        self.runner = runner
        self.set_player(player_number, player_color)

    def set_player(self, player_number, player_color):
        if not 0 <= player_number < utils.PLAYER_COUNT:
            raise exception.DecisionException("Wrong player number {}".format(player_number))
        if player_color == 'red':
            self.player = self.runner.red_players[player_number]
        elif player_color == 'blue':
            self.player = self.runner.blue_players[player_number]
        else:
            raise exception.DecisionException("Wrong player color {}".format(player_color))

    def validate(self):
        if self.player.ban_cycles > 0:
            raise exception.DecisionException("Player is banned for {} cycles".format(self.player.ban_cycles))
