main_size = 10

PLAYER_NUMBER = 6

SCREEN_HEIGHT = main_size * 65  # 650
SCREEN_WIDTH = main_size * 100  # 1000

PLAYER_RADIUS = SCREEN_WIDTH // 100  # 10
PLAYER_NUMBER_FONT_SIZE = SCREEN_WIDTH // 50  # 20
PLAYER_NAME_FONT_SIZE = SCREEN_WIDTH // 200 * 3  # 15
BALL_RADIUS = int(PLAYER_RADIUS * 0.8)  # 8

FRICTION = 5  # 5
PLAYER_SPEED = [int(PLAYER_RADIUS // 2), PLAYER_RADIUS]  # [5, 10]
MAX_KICK_POWER = main_size * 6 # 60

''' Football Pitch '''

GOAL_WIDTH = SCREEN_HEIGHT * 30 // 100  # 195
GOAL_DEPTH = GOAL_WIDTH // 12  # 16
CENTER_POINT_RADIUS = BALL_RADIUS // 2  # 4
CENTER_CIRCLE_RADIUS = SCREEN_HEIGHT // 8  # 81
LINE_THICKNESS = CENTER_POINT_RADIUS  # 4
PENALTY_ARIA_X = SCREEN_WIDTH // 5  # 200
PENALTY_ARIA_Y = SCREEN_HEIGHT // 2  # 325

''' score board '''
SCORE_BOARD_FONT_SIZE = main_size * 4  # 56

''' rules '''
ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER = 3
ALLOWED_PLAYERS_AROUND_BALL_NUMBER = 1
ALLOWED_PLAYERS_AROUND_BALL_RADIUS = 3 * (PLAYER_RADIUS + BALL_RADIUS)  # 54
BALL_CROWDED_BAN_CYCLES = 25
PENALTY_ARIA_BAN_CYCLES = 20

''' players initial information '''

x_red_defense = -(SCREEN_WIDTH // 2 // 4 * 3)
x_blue_defense = SCREEN_WIDTH // 2 // 4 * 3
x_red_mid = -(SCREEN_WIDTH // 2 // 4 * 2)
x_blue_mid = SCREEN_WIDTH // 2 // 4 * 2
x_red_forward = -(SCREEN_WIDTH // 2 // 4 * 1)
x_blue_forward = SCREEN_WIDTH // 2 // 4 * 1
y_both = SCREEN_HEIGHT // 2 // 3

red_players_initial_position = [
    {'x': -(SCREEN_WIDTH // 2) + 4 * GOAL_DEPTH, 'y': 0, 'name': 'Beyranvand', 'radius': PLAYER_RADIUS + BALL_RADIUS},
    {'x': x_red_defense, 'y': -y_both, 'name': 'Shoja', 'radius': PLAYER_RADIUS},
    {'x': x_red_defense, 'y': y_both, 'name': 'Kananizadegan', 'radius': PLAYER_RADIUS},
    {'x': x_red_mid, 'y': 0, 'name': 'Norollahi', 'radius': PLAYER_RADIUS},
    {'x': x_red_forward, 'y': -y_both, 'name': 'Amiri', 'radius': PLAYER_RADIUS},
    {'x': x_red_forward, 'y': y_both, 'name': 'Alipour', 'radius': PLAYER_RADIUS},
]

blue_players_initial_information = [
    {'x': SCREEN_WIDTH // 2 - 4 * GOAL_DEPTH, 'y': 0, 'name': 'Hosseini', 'radius': PLAYER_RADIUS + BALL_RADIUS},
    {'x': x_blue_defense, 'y': -y_both, 'name': 'Ghafouri', 'radius': PLAYER_RADIUS},
    {'x': x_blue_defense, 'y': y_both, 'name': 'Cheshmi', 'radius': PLAYER_RADIUS},
    {'x': x_blue_mid, 'y': 0, 'name': 'esmaili', 'radius': PLAYER_RADIUS},
    {'x': x_blue_forward, 'y': -y_both, 'name': 'Tabrizi', 'radius': PLAYER_RADIUS},
    {'x': x_blue_forward, 'y': y_both, 'name': 'Esmaili', 'radius': PLAYER_RADIUS},
]

''' links '''

red_circle_img_link = 'runner/models/red-circle.png'
blue_circle_img_link = 'runner/models/blue-circle.png'
ball_circle_img_link = 'runner/models/ball-circle.png'
