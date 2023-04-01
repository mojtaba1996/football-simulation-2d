import math


def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)


def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    if ball['owner_color'] != 'red':
        closest_player = red_players[1]
        for player in red_players[2:]:
            if get_distance(player, ball) < get_distance(closest_player, ball):
                closest_player = player
        if get_distance(closest_player, ball) >= 10:
            decisions.append({
                'type': 'move',
                'player_number': player['number'],
                'destination': ball,
                'speed': 10,
            })
        else:
            decisions.append({
                'type': 'grab',
                'player_number': player['number'],
            })
    else:
        maghsad = {'x': 300, 'y': -100}
        ball_owner = red_players[ball['owner_number']]
        distance = get_distance(ball_owner, maghsad)
        if distance >= 10:
            decisions.append({
                'type': 'move',
                'player_number': ball_owner['number'],
                'destination': maghsad,
                'speed': 10,
            })
        else:
            hadaf = {'x': 500, 'y': -60}
            direction = get_direction(ball_owner, hadaf)
            decisions.append({
                'type': 'kick',
                'player_number': ball_owner['number'],
                'direction': direction,
                'power': 60,
            })
    return decisions
