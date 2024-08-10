from .game import *
from .size import *


RED_PLAYERS_INITIAL_VALUES = []
BLUE_PLAYERS_INITIAL_VALUES = []

RED_PLAYERS_INITIAL_VALUES.append({
    'number': 0,
    'x': -FOOTBALL_PITCH_WIDTH // 2 + 3 * GOAL_DEPTH,
    'y': 0,
    'name': "Player{}".format(0),
    'radius': PLAYER_RADIUS + BALL_RADIUS,
})

BLUE_PLAYERS_INITIAL_VALUES.append({
    'number': 0,
    'x': FOOTBALL_PITCH_WIDTH // 2 - 3 * GOAL_DEPTH,
    'y': 0,
    'name': "Player{}".format(0),
    'radius': PLAYER_RADIUS + BALL_RADIUS,
})

for i in range(1, PLAYER_COUNT):
    x = (FOOTBALL_PITCH_WIDTH // 2 // (PLAYER_COUNT // 2) + 1) * (PLAYER_COUNT-i-1) // 2
    y = FOOTBALL_PITCH_HEIGHT // 3 if i % 2 == 1 else -FOOTBALL_PITCH_HEIGHT // 3
    RED_PLAYERS_INITIAL_VALUES.append({
        'number': i,
        'x':-x,
        'y': y,
        'name': "Player{}".format(i),
        'radius': PLAYER_RADIUS,
    })
    BLUE_PLAYERS_INITIAL_VALUES.append({
        'number': i,
        'x': x,
        'y': -y,
        'name': "Player{}".format(i),
        'radius': PLAYER_RADIUS,
    })

SHOULD_PRINT_DECISIONS_ERROR = True
