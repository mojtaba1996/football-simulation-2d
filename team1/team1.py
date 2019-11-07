import math


def move(decisions, player_number, destination, speed):
    decisions.append({
        'action': 'move',
        'player_number': player_number,
        'destination': {'x': destination['x'], 'y': destination['y']},
        'speed': speed,
    })


def kick(decisions, player_number, direction, power):
    decisions.append({
        'action': 'kick',
        'player_number': player_number,
        'direction': clock_to_degree(direction),
        'power': power,
    })


def grab(decisions, player_number):
    decisions.append({
        'action': 'grab',
        'player_number': player_number
    })


def degree_to_clock(degree):
    if degree < 90:
        degree += 360
    degree = 450 - degree
    hour = degree // 30
    minute = degree % 30 // 6
    return hour + minute / 10


def clock_to_degree(clock):
    angle = int(clock // 1 * 30 + 10 * (clock % 1) * 6)
    angle = 450 - angle
    if angle >= 360:
        angle -= 360
    return angle


def get_direction(a, b):
    x = b['x'] - a['x']
    y = b['y'] - a['y']
    angle = math.degrees(math.atan2(y, x))
    return degree_to_clock(angle)


def get_distance(a, b):
    return int(((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2) ** 0.5)


def play(red_players, blue_players, red_score, blue_score, ball, time_passed):
    decisions = []
    ############ WRITE YOUR CODE HERE ###########

    #############################################
    return decisions
