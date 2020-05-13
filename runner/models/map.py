import random
import time

import pygame as pg

from runner.exceptions.decision import DecisionException
from runner.settings.developement import SHOULD_PRINT_DECISIONS_ERROR
from runner.utils import convert_coordinate_normal_to_pygame, decision_factory, \
    unique_decisions
from runner.models.player import init_players
from runner.settings import GOAL_COLOR, GOAL_WIDTH, GOAL_DEPTH, SCREEN_HEIGHT, SCREEN_WIDTH, LINE_COLOR, \
    CENTER_POINT_RADIUS, CENTER_CIRCLE_RADIUS, LINE_THICKNESS, PENALTY_ARIA_X, PENALTY_ARIA_Y, \
    ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER, ALLOWED_PLAYERS_AROUND_BALL_NUMBER, ALLOWED_PLAYERS_AROUND_BALL_RADIUS, \
    PLAYER_NUMBER, BALL_CROWDED_BAN_CYCLES, PENALTY_ARIA_BAN_CYCLES, VERTICAL_MARGIN


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
        ''' Draw goals '''
        red_goal_x_for_pygame, red_goal_y_for_pygame = convert_coordinate_normal_to_pygame(-SCREEN_WIDTH//2, GOAL_WIDTH//2)
        pg.draw.rect(
            screen,
            GOAL_COLOR['red'],
            (red_goal_x_for_pygame, red_goal_y_for_pygame, GOAL_DEPTH, GOAL_WIDTH),
            0,
        )
        blue_goal_x_for_pygame, blue_goal_y_for_pygame = convert_coordinate_normal_to_pygame(SCREEN_WIDTH//2 - GOAL_DEPTH, GOAL_WIDTH//2)
        pg.draw.rect(
            screen,
            GOAL_COLOR['blue'],
            (blue_goal_x_for_pygame, blue_goal_y_for_pygame, GOAL_DEPTH, GOAL_WIDTH),
            0,
        )
        ''' Draw lines  '''
        center_x_for_pygame, center_y_for_pygame = convert_coordinate_normal_to_pygame(0, 0)
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
        center_line_x1_for_pygame, center_line_y1_for_pygame = convert_coordinate_normal_to_pygame(-LINE_THICKNESS//2, SCREEN_HEIGHT//2)
        center_line_x2_for_pygame, center_line_y2_for_pygame = convert_coordinate_normal_to_pygame(-LINE_THICKNESS//2, -SCREEN_HEIGHT//2)
        pg.draw.line(
            screen,
            LINE_COLOR,
            (center_line_x1_for_pygame, center_line_y1_for_pygame),
            (center_line_x2_for_pygame, center_line_y2_for_pygame),
            LINE_THICKNESS,
        )
        ''' Draw penalty areas '''
        '''     Left     '''
        left_x1_for_pygame, left_y1_for_pygame = convert_coordinate_normal_to_pygame(-SCREEN_WIDTH//2, PENALTY_ARIA_Y//2)
        left_x2_for_pygame, left_y2_for_pygame = left_x1_for_pygame + PENALTY_ARIA_X, left_y1_for_pygame
        left_x3_for_pygame, left_y3_for_pygame = left_x2_for_pygame, left_y2_for_pygame + PENALTY_ARIA_Y
        left_x4_for_pygame, left_y4_for_pygame = left_x3_for_pygame - PENALTY_ARIA_X, left_y3_for_pygame
        pg.draw.line(
            screen,
            LINE_COLOR,
            (left_x1_for_pygame, left_y1_for_pygame),
            (left_x2_for_pygame, left_y2_for_pygame),
            LINE_THICKNESS,
        )
        pg.draw.line(
            screen,
            LINE_COLOR,
            (left_x2_for_pygame, left_y2_for_pygame),
            (left_x3_for_pygame, left_y3_for_pygame),
            LINE_THICKNESS,
        )
        pg.draw.line(
            screen,
            LINE_COLOR,
            (left_x3_for_pygame, left_y3_for_pygame),
            (left_x4_for_pygame, left_y4_for_pygame),
            LINE_THICKNESS,
        )
        '''     Right     '''
        right_x1_for_pygame, right_y1_for_pygame = convert_coordinate_normal_to_pygame(SCREEN_WIDTH//2, PENALTY_ARIA_Y//2)
        right_x2_for_pygame, right_y2_for_pygame = right_x1_for_pygame - PENALTY_ARIA_X, right_y1_for_pygame
        right_x3_for_pygame, right_y3_for_pygame = right_x2_for_pygame, right_y2_for_pygame + PENALTY_ARIA_Y
        right_x4_for_pygame, right_y4_for_pygame = right_x3_for_pygame + PENALTY_ARIA_X, right_y3_for_pygame
        pg.draw.line(
            screen,
            LINE_COLOR,
            (right_x1_for_pygame, right_y1_for_pygame),
            (right_x2_for_pygame, right_y2_for_pygame),
            LINE_THICKNESS,
        )
        pg.draw.line(
            screen,
            LINE_COLOR,
            (right_x2_for_pygame, right_y2_for_pygame),
            (right_x3_for_pygame, right_y3_for_pygame),
            LINE_THICKNESS,
        )
        pg.draw.line(
            screen,
            LINE_COLOR,
            (right_x3_for_pygame, right_y3_for_pygame),
            (right_x4_for_pygame, right_y4_for_pygame),
            LINE_THICKNESS,
        )

    @staticmethod
    def draw_margins(screen):
        pg.draw.rect(
            screen,
            (0, 0, 0),
            (0, 0, SCREEN_WIDTH, VERTICAL_MARGIN)
        )
        pg.draw.rect(
            screen,
            (0, 0, 0),
            (0, SCREEN_HEIGHT+VERTICAL_MARGIN, SCREEN_WIDTH, VERTICAL_MARGIN)
        )

    def show(self, screen):
        self.show_football_pitch(screen)
        self.draw_margins(screen)
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

    def kick_players(self, players_in_area, allowed_number, ban_cycles):
        while len(players_in_area) > allowed_number:
            random_player = random.choice(players_in_area)
            if self.ball.owner == random_player:
                self.ball.owner = None
            random_player.ban_cycles = ban_cycles
            random_player.x = 0
            random_player.y = SCREEN_HEIGHT // 2 + VERTICAL_MARGIN - random_player.radius
            if random_player.color == 'red':
                random_player.y = -random_player.y
            players_in_area.remove(random_player)

    def check_if_the_bus_is_parked(self):
        ''' RED '''
        red_players_in_area = []
        for player in self.red_players:
            if -SCREEN_WIDTH//2<= player.x <= -SCREEN_WIDTH//2 + PENALTY_ARIA_X:
                if -PENALTY_ARIA_Y//2 <= player.y <= PENALTY_ARIA_Y//2:
                    if player.ban_cycles == 0:
                        red_players_in_area.append(player)
        self.kick_players(red_players_in_area, ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER, PENALTY_ARIA_BAN_CYCLES)

        ''' BLUE '''
        blue_players_in_area = []
        for player in self.blue_players:
            if SCREEN_WIDTH//2 - PENALTY_ARIA_X <= player.x <= SCREEN_WIDTH//2:
                if -PENALTY_ARIA_Y//2 <= player.y <= PENALTY_ARIA_Y//2:
                    if player.ban_cycles == 0:
                        blue_players_in_area.append(player)
        self.kick_players(blue_players_in_area, ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER, PENALTY_ARIA_BAN_CYCLES)

    def check_if_ball_is_crowded(self):
        ''' RED '''
        red_players_arround_ball = []
        for player in self.red_players:
            if ((self.ball.x - player.x)**2 + (self.ball.y - player.y)**2)**0.5 < ALLOWED_PLAYERS_AROUND_BALL_RADIUS:
                if not player.is_in_his_penalty_area():
                    if player.ban_cycles == 0:
                        red_players_arround_ball.append(player)
        self.kick_players(red_players_arround_ball, ALLOWED_PLAYERS_AROUND_BALL_NUMBER, BALL_CROWDED_BAN_CYCLES)
        ''' BLUE '''
        blue_players_arround_ball = []
        for player in self.blue_players:
            if ((self.ball.x - player.x)**2 + (self.ball.y - player.y)**2)**0.5 < ALLOWED_PLAYERS_AROUND_BALL_RADIUS:
                if not player.is_in_his_penalty_area():
                    if player.ban_cycles == 0:
                        blue_players_arround_ball.append(player)
        self.kick_players(blue_players_arround_ball, ALLOWED_PLAYERS_AROUND_BALL_NUMBER, BALL_CROWDED_BAN_CYCLES)
