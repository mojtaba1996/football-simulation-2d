import math
import random

from runner.decisions import Move
from runner.decisions.grab import Grab
from runner.decisions.kick import Kick
from runner.models.player import Player
from runner.models.point import Point
from runner.settings import SCREEN_WIDTH as SW, SCREEN_HEIGHT as SH, GOAL_DEPTH as GD, PLAYER_RADIUS as PR
from runner.utils import Actions


def init_players(red_players, blue_players):
    red_players.clear()
    blue_players.clear()
    x_red_defense = -(SW // 2 // 4 * 3)
    x_red_mid = -(SW // 2 // 4 * 2)
    x_red_forward = -(SW // 2 // 4 * 1)
    y_both = SH // 2 // 3
    red_players.append(Player(
        x=-(SW // 2) + 4 * GD,
        y=0,
        name="Beyranvand",
        number=0,
        color='red',
        radius=3 * PR // 2,
    ))
    red_players.append(Player(
        x=x_red_defense,
        y=y_both,
        name="shoja",
        number=1,
        color='red',
        radius=PR,
    ))
    red_players.append(Player(
        x=x_red_defense,
        y=-y_both,
        name="kananizadegan",
        number=2,
        color='red',
        radius=PR,
    ))
    red_players.append(Player(
        x=x_red_mid,
        y=0,
        name="norollahi",
        number=3,
        color='red',
        radius=PR,
    ))
    red_players.append(Player(
        x=x_red_forward,
        y=y_both,
        name="amiri",
        number=4,
        color='red',
        radius=PR,
    ))
    red_players.append(Player(
        x=x_red_forward,
        y=-y_both,
        name="alipour",
        number=5,
        color='red',
        radius=PR,
    ))
    '''
    red_players.append(Player(
        x=x_red_mid,
        y=SH // 2 * 1 // 3,
        name="Hosseini",
        number=6,
        color='red',
        radius=PR,
    ))
    red_players.append(Player(
        x=x_red_mid,
        y=- (SH // 2 * 1 // 3),
        name="Shoja",
        number=7,
        color='red',
        radius=PR,
    ))
    red_players.append(Player(
        x=x_red_mid,
        y=- (SH // 2 * 2 // 3),
        name="Mahini",
        number=8,
        color='red',
        radius=PR,
    ))

    red_players.append(Player(
        x=x_red_forward,
        y=SH // 2 * 1 // 3,
        name="Shoja",
        number=9,
        color='red',
        radius=PR,
    ))
    red_players.append(Player(
        x=x_red_forward,
        y=- (SH // 2 * 1 // 3),
        name="Mahini",
        number=10,
        color='red',
        radius=PR,
    ))
    '''
    blue_players.append(Player(
        x=(SW // 2) - 4 * GD,
        y=0,
        name="hosseini",
        number=0,
        color='blue',
        radius=3 * PR // 2,
    ))
    blue_players.append(Player(
        x=-x_red_defense,
        y=-y_both,
        name="ghafouri",
        number=1,
        color='blue',
        radius=PR,
    ))
    blue_players.append(Player(
        x=-x_red_defense,
        y=y_both,
        name="cheshmi",
        number=2,
        color='blue',
        radius=PR,
    ))
    blue_players.append(Player(
        x=-x_red_mid,
        y=0,
        name="karimi",
        number=3,
        color='blue',
        radius=PR,
    ))
    blue_players.append(Player(
        x=-x_red_forward,
        y=-y_both,
        name="tabrizi",
        number=4,
        color='blue',
        radius=PR,
    ))
    blue_players.append(Player(
        x=-x_red_forward,
        y=y_both,
        name="esmaili",
        number=5,
        color='blue',
        radius=PR,
    ))
    '''
    blue_players.append(Player(
        x=-x_red_mid,
        y=-(SH // 2 * 1 // 3),
        name="Hosseini",
        number=6,
        color='blue',
        radius=PR,
    ))
    blue_players.append(Player(
        x=-x_red_mid,
        y=(SH // 2 * 1 // 3),
        name="Shoja",
        number=7,
        color='blue',
        radius=PR,
    ))
    blue_players.append(Player(
        x=-x_red_mid,
        y=(SH // 2 * 2 // 3),
        name="Mahini",
        number=8,
        color='blue',
        radius=PR,
    ))

    blue_players.append(Player(
        x=-x_red_forward,
        y=-(SH // 2 * 1 // 3),
        name="Shoja",
        number=9,
        color='blue',
        radius=PR,
    ))
    blue_players.append(Player(
        x=-x_red_forward,
        y=(SH // 2 * 1 // 3),
        name="Mahini",
        number=10,
        color='blue',
        radius=PR,
    ))
    '''


def degree_to_clock(degree):
    if degree < 90:
        degree += 360
    degree = 450 - degree
    hour = degree // 30
    minute = degree % 30 // 6
    return hour + minute / 10


def get_info(red_players, blue_players, ball):
    red_players_info = []
    blue_players_info = []
    for red_player in red_players:
        red_players_info.append({
            'x': red_player.x,
            'y': red_player.y,
            'name': red_player.name,
            'number': red_player.number,
        })
    for blue_player in blue_players:
        blue_players_info.append({
            'x': blue_player.x,
            'y': blue_player.y,
            'name': blue_player.name,
            'number': blue_player.number,
        })
    ball_info = {
        'x': ball.x,
        'y': ball.y,
        'speed': ball.speed,
        'direction': degree_to_clock(ball.direction),
        'owner_color': 'white' if ball.owner is None else ball.owner.color,
        'owner_number': -1 if ball.owner is None else ball.owner.number,
    }
    return red_players_info, blue_players_info, ball_info


def reverse_information(red_players_info, blue_players_info, ball_info):
    new_red_players_info = []
    new_blue_players_info = []
    new_ball_info = None
    for red_player_info in red_players_info:
        new_blue_players_info.append({
            'x': -red_player_info['x'],
            'y': -red_player_info['y'],
            'name': red_player_info['name'],
            'number': red_player_info['number'],
        })
    for blue_player_info in blue_players_info:
        new_red_players_info.append({
            'x': -blue_player_info['x'],
            'y': -blue_player_info['y'],
            'name': blue_player_info['name'],
            'number': blue_player_info['number'],
        })
    new_ball_info = {
        'x': -ball_info['x'],
        'y': -ball_info['y'],
        'speed': ball_info['speed'],
        'direction': (ball_info['direction'] + 180) % 360,
        'owner_color': ball_info['owner_color'],
        'owner_number': ball_info['owner_number'],
    }
    if new_ball_info['owner_color'] == 'red':
        new_ball_info['owner_color'] = 'blue'
    elif new_ball_info['owner_color'] == 'blue':
        new_ball_info['owner_color'] = 'red'
    return new_red_players_info, new_blue_players_info, new_ball_info


def get_direction(a, b):
    x = b['x'] - a['x']
    y = b['y'] - a['y']
    return math.degrees(math.atan2(y, x))


def get_distance(a, b):
    return ((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2) ** 0.5


def decision_factory(the_map, decision):
    if decision['action'] == Actions.MOVE:
        return Move(
            the_map=the_map,
            player_number=decision['player_number'],
            player_color=decision['player_color'],
            destination=Point(decision['destination']['x'], decision['destination']['y']),
            speed=decision['speed'],
            priority=300,
        )
    if decision['action'] == Actions.KICK:
        return Kick(
            the_map=the_map,
            player_number=decision['player_number'],
            player_color=decision['player_color'],
            direction=decision['direction'],
            power=decision['power'],
            priority=100,
        )
    if decision['action'] == Actions.GRAB:
        return Grab(
            the_map=the_map,
            player_number=decision['player_number'],
            player_color=decision['player_color'],
            priority=200,
        )


def sort_decisions(decisions):
    sorted_decisions = []
    for decision in decisions:
        i = -1
        while -i <= len(sorted_decisions) and decision.priority > sorted_decisions[i].priority:
            i -= 1
        sorted_decisions = sorted_decisions[:i + 1] + [decision] + sorted_decisions[i + 1:]
    return decisions


def unique_decisions(decisions):
    uniqued_decisions = []
    for decision in decisions:
        flag = True
        for uniqued_decision in uniqued_decisions:
            if type(decision) is type(uniqued_decision) and decision.player == uniqued_decision.player:
                flag = False
        if flag:
            uniqued_decisions.append(decision)
    return uniqued_decisions