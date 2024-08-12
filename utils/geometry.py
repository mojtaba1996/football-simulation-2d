import settings.size


def convert_coordinate_cartesian_to_pygame(cartesian_x, cartesian_y):
    pygame_x = settings.size.SCREEN_WIDTH // 2 + cartesian_x
    pygame_y = settings.size.SCREEN_HEIGHT // 2 - cartesian_y
    return pygame_x, pygame_y

def distance(cartesian_p1, cartesian_p2):
    return ((cartesian_p1.x - cartesian_p2.x) ** 2 + (cartesian_p1.y - cartesian_p2.y) ** 2) ** 0.5
