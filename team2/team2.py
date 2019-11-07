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

    if ball['owner_color'] != 'red':
        closest_id = 1
        closest_distance = get_distance(red_players[1], ball)
        for i in range(2, 6):
            player = red_players[i]
            distance = get_distance(player, ball)
            if distance < closest_distance:
                closest_distance = distance
                closest_id = i
        if closest_distance >= 18:
            move(decisions, closest_id, ball, 18)
        else:
            grab(decisions, closest_id)
    else:
        maghsad = {'x': 300, 'y': -100}
        ball_owner = red_players[ball['owner_number']]
        distance = get_distance(ball_owner, maghsad)
        if distance >= 18:
            move(decisions, ball_owner['number'], maghsad, 18)
        else:
            hadaf = {'x': 500, 'y': 60}
            direction = get_direction(ball_owner, hadaf)
            kick(decisions, ball_owner['number'], direction, 60)

    return decisions
