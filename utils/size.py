def make_even_number(n):
    if n % 2 == 0:
        return n
    else:
        return n+1


main_size = 10

FOOTBALL_PITCH_WIDTH = make_even_number(main_size * 100) # 1000
FOOTBALL_PITCH_HEIGHT = make_even_number(main_size * 65) # 650

PLAYER_RADIUS = make_even_number(FOOTBALL_PITCH_WIDTH // 100) # 10
PLAYER_NUMBER_FONT_SIZE = make_even_number(FOOTBALL_PITCH_WIDTH // 50) # 20
PLAYER_NAME_FONT_SIZE = make_even_number(FOOTBALL_PITCH_WIDTH // 200 * 3) # 16
BALL_RADIUS = make_even_number(int(PLAYER_RADIUS * 0.8)) # 8

VERTICAL_MARGIN = make_even_number(int((PLAYER_RADIUS + BALL_RADIUS) * 2.5)) # 46
HORIZONTAL_MARGIN = make_even_number(int((PLAYER_RADIUS + BALL_RADIUS) * 2.5)) # 46

SCREEN_WIDTH = make_even_number(FOOTBALL_PITCH_WIDTH + HORIZONTAL_MARGIN) # 1000
SCREEN_HEIGHT = make_even_number(FOOTBALL_PITCH_HEIGHT + VERTICAL_MARGIN * 2) # 742


# FOOTBALL PITCH
GOAL_WIDTH = make_even_number(FOOTBALL_PITCH_HEIGHT * 30 // 100) # 196
GOAL_DEPTH = make_even_number(BALL_RADIUS * 3) # 24
CENTER_POINT_RADIUS = make_even_number(BALL_RADIUS // 2) # 4
CENTER_CIRCLE_RADIUS = make_even_number(FOOTBALL_PITCH_HEIGHT // 8) # 92
LINE_THICKNESS = CENTER_POINT_RADIUS # 4
PENALTY_AREA_HEIGHT = make_even_number(FOOTBALL_PITCH_HEIGHT // 2) # 326
PENALTY_AREA_WIDTH = make_even_number(FOOTBALL_PITCH_WIDTH // 5) # 200


# SCOREBOARD
SCOREBOARD_FONT_SIZE = make_even_number(main_size * 3) # 40
