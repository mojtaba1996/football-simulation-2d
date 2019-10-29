import random
import time

import pygame as pg
from runner.utils import convert_coordinate_normal_to_pygame, Actions, decision_factory, init_players, sort_decisions, \
    unique_decisions
from runner.settings import GOAL_COLOR as GC, GOAL_WIDTH as GW, GOAL_DEPTH as GD, SCREEN_HEIGHT as SH, \
    SCREEN_WIDTH as SW, LINE_COLOR as LC, CENTER_POINT_RADIUS as CPR, CENTER_CIRCLE_RADIUS as CCR, \
    LINE_THICKNESS as LTH, PENALTY_ARIA_X as PAX, PENALTY_ARIA_Y as PAY, \
    ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER as APIPAN, ALLOWED_PLAYERS_AROUND_BALL_NUMBER as APABN, \
    ALLOWED_PLAYERS_AROUND_BALL_RADIUS as APABR, PLAYER_NUMBER as PN


class Map:
    def __init__(self, red_players, blue_players, ball, score_board):
        self.red_players = red_players
        self.blue_players = blue_players
        self.ball = ball
        self.score_board = score_board

    def perform_decisions(self, red_decisions, blue_decisions):
        all_decisions = []
        for red_decision in red_decisions:
            red_decision['player_color'] = 'red'
            all_decisions.append(decision_factory(self, red_decision))
        for blue_decision in blue_decisions:
            blue_decision['player_color'] = 'blue'
            if 'direction' in blue_decision:
                blue_decision['direction'] = (blue_decision['direction'] + 180) % 360
            if 'destination' in blue_decision:
                blue_decision['destination']['x'] = -blue_decision['destination']['x']
                blue_decision['destination']['y'] = -blue_decision['destination']['y']
            all_decisions.append(decision_factory(self, blue_decision))
        random.shuffle(all_decisions)

        all_decisions = sort_decisions(all_decisions)

        all_decisions = unique_decisions(all_decisions)

        for decision in all_decisions:
            decision.perform()

    @staticmethod
    def show_football_pitch(screen):
        goal_y_for_pygame = SH // 2 - GW // 2
        center_x_for_pygame, center_y_for_pygame = convert_coordinate_normal_to_pygame(0, 0)
        ''' Draw goals '''
        pg.draw.rect(screen, GC['red'], (0, goal_y_for_pygame, GD, GW), 0)
        pg.draw.rect(screen, GC['blue'], (SW - GD, goal_y_for_pygame, GD, GW), 0)
        ''' Draw lines  '''
        '''     center point    '''
        pg.draw.circle(screen, LC, (center_x_for_pygame, center_y_for_pygame), CPR, 0)
        '''     center circle    '''
        pg.draw.circle(screen, LC, (center_x_for_pygame, center_y_for_pygame), CCR, LTH)
        '''     center line      '''
        pg.draw.line(screen, LC, (center_x_for_pygame - LTH // 2, 0), (center_x_for_pygame - LTH // 2, SH), LTH)
        ''' Draw penalty areas '''
        '''     Left     '''
        pg.draw.line(screen, LC, (0, (SH - PAY) // 2), (PAX, (SH - PAY) // 2), LTH)
        pg.draw.line(screen, LC, (0, (SH + PAY) // 2), (PAX, (SH + PAY) // 2), LTH)
        pg.draw.line(screen, LC, (PAX, (SH - PAY) // 2), (PAX, (SH + PAY) // 2), LTH)
        '''     Right     '''
        pg.draw.line(screen, LC, (SW, (SH - PAY) // 2), (SW - PAX, (SH - PAY) // 2), LTH)
        pg.draw.line(screen, LC, (SW, (SH + PAY) // 2), (SW - PAX, (SH + PAY) // 2), LTH)
        pg.draw.line(screen, LC, (SW - PAX, (SH - PAY) // 2), (SW - PAX, (SH + PAY) // 2), LTH)

    def show(self, screen):
        self.show_football_pitch(screen)
        for red_player in self.red_players:
            red_player.show(screen=screen)
        for blue_player in self.blue_players:
            blue_player.show(screen=screen)
        self.ball.show(screen=screen)
        self.score_board.show(screen=screen)

    def check_if_scored(self):
        if self.ball.x - self.ball.radius <= -SW // 2 + GD and (-GW // 2 <= self.ball.y <= GW // 2):
            self.score_board.blue_score += 1
            init_players(self.red_players, self.blue_players)
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = -1
            self.ball.owner = self.red_players[PN - 1]
            self.ball.speed = 0
            self.red_players[PN - 1].x, self.red_players[PN - 1].y = self.ball.x, self.ball.y
            time.sleep(1)
        if self.ball.x + self.ball.radius >= SW // 2 - GD and (-GW // 2 <= self.ball.y <= GW // 2):
            self.score_board.red_score += 1
            init_players(self.red_players, self.blue_players)
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = -1
            self.ball.owner = self.blue_players[PN - 1]
            self.ball.speed = 0
            self.blue_players[PN - 1].x, self.blue_players[PN - 1].y = self.ball.x, self.ball.y
            time.sleep(1)

    @staticmethod
    def check_if_crowded(point, players, radius, allowed_number):
        players_in_area = []
        for player in players:
            if ((player.x - point['x']) ** 2 + (player.y - point['y']) ** 2) ** 0.5 < radius:
                players_in_area.append(player)
        while len(players_in_area) > allowed_number:
            random_player = random.choice(players_in_area)
            random_player.x = 0
            random_player.y = SH // 2 - random_player.radius * 2
            players_in_area.remove(random_player)

    def check_if_the_bus_is_parked(self):
        ''' RED '''
        goal_center = {'x': -SW // 2, 'y': 0}
        self.check_if_crowded(goal_center, self.red_players, PAX, APIPAN)

        ''' BLUE '''
        goal_center['x'] = SW // 2
        self.check_if_crowded(goal_center, self.blue_players, PAX, APIPAN)

    def check_if_ball_is_crowded(self):
        ball_point = {'x': self.ball.x, 'y': self.ball.y}
        ''' RED '''
        self.check_if_crowded(ball_point, self.red_players, APABR, APABN)
        ''' BLUE '''
        self.check_if_crowded(ball_point, self.blue_players, APABR, APABN)
