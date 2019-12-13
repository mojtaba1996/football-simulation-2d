import random
import time

import pygame as pg

from runner.exceptions.decision import DecisionException
from runner.settings.developement import SHOULD_PRINT_DECISIONS_ERROR
from runner.utils import convert_coordinate_normal_to_pygame, decision_factory, init_players, \
    unique_decisions
from runner.settings import GOAL_COLOR, GOAL_WIDTH, GOAL_DEPTH, SCREEN_HEIGHT, SCREEN_WIDTH, LINE_COLOR, \
    CENTER_POINT_RADIUS, CENTER_CIRCLE_RADIUS, LINE_THICKNESS, PENALTY_ARIA_X, PENALTY_ARIA_Y, \
    ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER, ALLOWED_PLAYERS_AROUND_BALL_NUMBER, ALLOWED_PLAYERS_AROUND_BALL_RADIUS, \
    PLAYER_NUMBER, BALL_CROWDED_BAN_CYCLES, PENALTY_ARIA_BAN_CYCLES


class Map:
    def __init__(self, red_players, blue_players, ball, score_board):
        self.red_players = red_players
        self.blue_players = blue_players
        self.ball = ball
        self.score_board = score_board

    @staticmethod
    def handle_decision_perform_with_exception(decision):
        try:
            decision.perform()
        except DecisionException as de:
            if SHOULD_PRINT_DECISIONS_ERROR:
                print(de)

    def perform_decisions(self, red_decisions_dict, blue_decisions_dict):
        red_decisions = []
        blue_decisions = []
        for red_decision_dict in red_decisions_dict:
            red_decision_dict['player_color'] = 'red'
            red_decisions.append(decision_factory(self, red_decision_dict))
        for blue_decision_dict in blue_decisions_dict:
            blue_decision_dict['player_color'] = 'blue'
            if 'direction' in blue_decision_dict:
                blue_decision_dict['direction'] = (blue_decision_dict['direction'] + 180) % 360
            if 'destination' in blue_decision_dict:
                blue_decision_dict['destination'] = {
                    'x': -blue_decision_dict['destination']['x'],
                    'y': -blue_decision_dict['destination']['y'],
                }
            blue_decisions.append(decision_factory(self, blue_decision_dict))

        red_decisions = unique_decisions(red_decisions)
        blue_decisions = unique_decisions(blue_decisions)

        while len(red_decisions) != 0 and len(blue_decisions) != 0:
            r = random.randint(0, 1)
            if r:
                decision = red_decisions.pop(0)
                self.handle_decision_perform_with_exception(decision)
            else:
                decision = blue_decisions.pop(0)
                self.handle_decision_perform_with_exception(decision)
        if len(red_decisions) == 0:
            for decision in blue_decisions:
                self.handle_decision_perform_with_exception(decision)
        else:
            for decision in red_decisions:
                self.handle_decision_perform_with_exception(decision)
        self.decrement_ban_cycles()

    def decrement_ban_cycles(self):
        for player in self.red_players + self.blue_players:
            if player.ban_cycles > 0:
                player.ban_cycles -= 1

    @staticmethod
    def show_football_pitch(screen):
        goal_y_for_pygame = SCREEN_HEIGHT // 2 - GOAL_WIDTH // 2
        center_x_for_pygame, center_y_for_pygame = convert_coordinate_normal_to_pygame(0, 0)
        ''' Draw goals '''
        pg.draw.rect(
            screen,
            GOAL_COLOR['red'],
            (0, goal_y_for_pygame, GOAL_DEPTH, GOAL_WIDTH),
            0,
        )
        pg.draw.rect(
            screen,
            GOAL_COLOR['blue'],
            (SCREEN_WIDTH - GOAL_DEPTH, goal_y_for_pygame, GOAL_DEPTH, GOAL_WIDTH),
            0,
        )
        ''' Draw lines  '''
        '''     center point    '''
        pg.draw.circle(
            screen,
            LINE_COLOR,
            (center_x_for_pygame, center_y_for_pygame),
            CENTER_POINT_RADIUS,
            0,
        )
        '''     center circle    '''
        pg.draw.circle(
            screen,
            LINE_COLOR,
            (center_x_for_pygame, center_y_for_pygame),
            CENTER_CIRCLE_RADIUS,
            LINE_THICKNESS,
        )
        '''     center line      '''
        pg.draw.line(
            screen,
            LINE_COLOR,
            (center_x_for_pygame - LINE_THICKNESS // 2, 0),
            (center_x_for_pygame - LINE_THICKNESS // 2, SCREEN_HEIGHT),
            LINE_THICKNESS,
        )
        ''' Draw penalty areas '''
        '''     Left     '''
        pg.draw.line(
            screen,
            LINE_COLOR,
            (0, (SCREEN_HEIGHT - PENALTY_ARIA_Y) // 2),
            (PENALTY_ARIA_X, (SCREEN_HEIGHT - PENALTY_ARIA_Y) // 2),
            LINE_THICKNESS,
        )
        pg.draw.line(
            screen,
            LINE_COLOR,
            (0, (SCREEN_HEIGHT + PENALTY_ARIA_Y) // 2),
            (PENALTY_ARIA_X, (SCREEN_HEIGHT + PENALTY_ARIA_Y) // 2),
            LINE_THICKNESS,
        )
        pg.draw.line(
            screen,
            LINE_COLOR,
            (PENALTY_ARIA_X, (SCREEN_HEIGHT - PENALTY_ARIA_Y) // 2),
            (PENALTY_ARIA_X, (SCREEN_HEIGHT + PENALTY_ARIA_Y) // 2),
            LINE_THICKNESS,
        )
        '''     Right     '''
        pg.draw.line(
            screen,
            LINE_COLOR,
            (SCREEN_WIDTH, (SCREEN_HEIGHT - PENALTY_ARIA_Y) // 2),
            (SCREEN_WIDTH - PENALTY_ARIA_X, (SCREEN_HEIGHT - PENALTY_ARIA_Y) // 2),
            LINE_THICKNESS,
        )
        pg.draw.line(
            screen,
            LINE_COLOR,
            (SCREEN_WIDTH, (SCREEN_HEIGHT + PENALTY_ARIA_Y) // 2),
            (SCREEN_WIDTH - PENALTY_ARIA_X, (SCREEN_HEIGHT + PENALTY_ARIA_Y) // 2),
            LINE_THICKNESS,
        )
        pg.draw.line(
            screen,
            LINE_COLOR,
            (SCREEN_WIDTH - PENALTY_ARIA_X, (SCREEN_HEIGHT - PENALTY_ARIA_Y) // 2),
            (SCREEN_WIDTH - PENALTY_ARIA_X, (SCREEN_HEIGHT + PENALTY_ARIA_Y) // 2),
            LINE_THICKNESS,
        )

    def show(self, screen):
        self.show_football_pitch(screen)
        for red_player in self.red_players:
            red_player.show(screen=screen)
        for blue_player in self.blue_players:
            blue_player.show(screen=screen)
        self.ball.show(screen=screen)
        self.score_board.show(screen=screen)

    def check_if_scored(self):
        if self.ball.x - self.ball.radius <= -SCREEN_WIDTH // 2 + GOAL_DEPTH and \
                (-GOAL_WIDTH // 2 <= self.ball.y <= GOAL_WIDTH // 2):
            self.score_board.blue_score += 1
            init_players(self.red_players, self.blue_players)
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = -1
            self.ball.owner = self.red_players[PLAYER_NUMBER - 1]
            self.ball.speed = 0
            self.red_players[PLAYER_NUMBER - 1].x, self.red_players[PLAYER_NUMBER - 1].y = self.ball.x, self.ball.y
            time.sleep(1)
        if self.ball.x + self.ball.radius >= SCREEN_WIDTH // 2 - GOAL_DEPTH and \
                (-GOAL_WIDTH // 2 <= self.ball.y <= GOAL_WIDTH // 2):
            self.score_board.red_score += 1
            init_players(self.red_players, self.blue_players)
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = -1
            self.ball.owner = self.blue_players[PLAYER_NUMBER - 1]
            self.ball.speed = 0
            self.blue_players[PLAYER_NUMBER - 1].x, self.blue_players[PLAYER_NUMBER - 1].y = self.ball.x, self.ball.y
            time.sleep(1)

    def check_if_crowded(self, point, players, radius, allowed_number, ban_cycles):
        players_in_area = []
        for player in players:
            if ((player.x - point['x']) ** 2 + (player.y - point['y']) ** 2) ** 0.5 < radius:
                if not player.is_in_his_penalty_area():
                    players_in_area.append(player)
        ''' Kick '''
        while len(players_in_area) > allowed_number:
            random_player = random.choice(players_in_area)
            if self.ball.owner == random_player:
                self.ball.owner = None
            random_player.ban_cycles = ban_cycles
            random_player.x = 0
            random_player.y = SCREEN_HEIGHT // 2 - random_player.radius * 2
            if random_player.color == 'red':
                random_player.y = -random_player.y
            players_in_area.remove(random_player)

    def check_if_the_bus_is_parked(self):
        ''' RED '''
        goal_center = {'x': -SCREEN_WIDTH // 2, 'y': 0}
        self.check_if_crowded(
            goal_center,
            self.red_players,
            PENALTY_ARIA_X,
            ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER,
            PENALTY_ARIA_BAN_CYCLES,
        )

        ''' BLUE '''
        goal_center['x'] = SCREEN_WIDTH // 2
        self.check_if_crowded(
            goal_center,
            self.blue_players,
            PENALTY_ARIA_X,
            ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER,
            PENALTY_ARIA_BAN_CYCLES,
        )

    def check_if_ball_is_crowded(self):
        ball_point = {'x': self.ball.x, 'y': self.ball.y}
        ''' RED '''
        self.check_if_crowded(
            ball_point,
            self.red_players,
            ALLOWED_PLAYERS_AROUND_BALL_RADIUS,
            ALLOWED_PLAYERS_AROUND_BALL_NUMBER,
            BALL_CROWDED_BAN_CYCLES,
        )
        ''' BLUE '''
        self.check_if_crowded(
            ball_point,
            self.blue_players,
            ALLOWED_PLAYERS_AROUND_BALL_RADIUS,
            ALLOWED_PLAYERS_AROUND_BALL_NUMBER,
            BALL_CROWDED_BAN_CYCLES,
        )
