import random
import time
from threading import Thread

import pygame as pg

import exception
import models
import utils
from decision import get_decisions
from team1 import play as red_play
from team2 import play as blue_play


def red_fire(*args, **kwargs):
    global red_responses
    red_responses = red_play(*args, **kwargs)

def blue_fire(*args, **kwargs):
    global blue_responses
    blue_responses = blue_play(*args, **kwargs)


class Runner:
    def __init__(self, config):
        pg.init()
        self.config = config
        self.screen = pg.display.set_mode((utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT))
        self.ball = models.Ball()
        self._init_players()
        self.scoreboard = models.Scoreboard()
        self._show_and_increase_cycle_number()

    def run(self):
        global red_responses, blue_responses
        end = False
        pause = False
        while not end:
            # events: pause and quit
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        pause = not pause
                        print('pause')
                    if event.key == pg.K_ESCAPE:
                        end = True
                if event.type == pg.QUIT:
                    end = True
            if pause:
                continue
            if self.scoreboard.cycle_number > self.config.max_cycle:
                continue
            red_responses = None
            blue_responses = None
            red_thread = Thread(
                target=red_fire,
                args=self._get_args_for_red_team(),
            )
            blue_thread = Thread(
                target=blue_fire,
                args=self._get_args_for_blue_team(),
            )
            blue_thread.start()
            red_thread.start()
            for _ in range(self.config.delay_count):
                time.sleep(self.config.delay_amount)
                if red_responses is not None and blue_responses is not None:
                    break
            if not isinstance(red_responses, list):
                red_responses = []
            if not isinstance(blue_responses, list):
                blue_responses = []

            self.perform_decisions(red_responses, blue_responses)
            self.decrement_ban_cycles()
            self.ball.move()
            self.check_if_scored()
            self.check_if_the_bus_is_parked()
            self.check_if_ball_is_crowded()

            self._show_and_increase_cycle_number()
            if self.scoreboard.cycle_number > self.config.max_cycle:
                if self.config.additional_delay:
                    time.sleep(4)
                end = True

    @staticmethod
    def handle_decision_perform_with_exception(decision):
        try:
            decision.validate()
            decision.perform()
        except exception.DecisionException as de:
            if utils.SHOULD_PRINT_DECISIONS_ERROR:
                print(de)

    def perform_decisions(self, red_responses, blue_responses):
        red_decisions, blue_decisions = get_decisions(self, red_responses, blue_responses)
        
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

    def kick_players(self, players_in_area, allowed_number, ban_cycles):
        while len(players_in_area) > allowed_number:
            random_player = random.choice(players_in_area)
            if self.ball.owner == random_player:
                self.ball.owner = None
            random_player.ban_cycles = ban_cycles
            random_player.x = 0
            random_player.y = utils.SCREEN_HEIGHT // 2 - utils.VERTICAL_MARGIN + random_player.radius
            if random_player.color == 'red':
                random_player.y = -random_player.y
            players_in_area.remove(random_player)

    def check_if_the_bus_is_parked(self):
        ''' RED '''
        red_players_in_area = []
        for player in self.red_players:
            if -utils.FOOTBALL_PITCH_WIDTH//2<= player.x <= -utils.FOOTBALL_PITCH_WIDTH//2 + utils.PENALTY_AREA_WIDTH:
                if -utils.PENALTY_AREA_HEIGHT//2 <= player.y <= utils.PENALTY_AREA_HEIGHT//2:
                    if player.ban_cycles == 0:
                        red_players_in_area.append(player)
        self.kick_players(red_players_in_area, utils.ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER, utils.PENALTY_ARIA_BAN_CYCLES)

        ''' BLUE '''
        blue_players_in_area = []
        for player in self.blue_players:
            if utils.FOOTBALL_PITCH_WIDTH//2 - utils.PENALTY_AREA_WIDTH <= player.x <= utils.FOOTBALL_PITCH_WIDTH//2:
                if -utils.PENALTY_AREA_HEIGHT//2 <= player.y <= utils.PENALTY_AREA_HEIGHT//2:
                    if player.ban_cycles == 0:
                        blue_players_in_area.append(player)
        self.kick_players(blue_players_in_area, utils.ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER, utils.PENALTY_ARIA_BAN_CYCLES)

    def check_if_ball_is_crowded(self):
        ''' RED '''
        red_players_arround_ball = []
        for player in self.red_players:
            if utils.distance(self.ball, player) < utils.ALLOWED_PLAYERS_AROUND_BALL_RADIUS:
                if not player.is_in_own_penalty_area():
                    if player.ban_cycles == 0:
                        red_players_arround_ball.append(player)
        self.kick_players(red_players_arround_ball, utils.ALLOWED_PLAYERS_AROUND_BALL_NUMBER, utils.BALL_CROWDED_BAN_CYCLES)
        ''' BLUE '''
        blue_players_arround_ball = []
        for player in self.blue_players:
            if utils.distance(self.ball, player) < utils.ALLOWED_PLAYERS_AROUND_BALL_RADIUS:
                if not player.is_in_own_penalty_area():
                    if player.ban_cycles == 0:
                        blue_players_arround_ball.append(player)
        self.kick_players(blue_players_arround_ball, utils.ALLOWED_PLAYERS_AROUND_BALL_NUMBER, utils.BALL_CROWDED_BAN_CYCLES)

    def check_if_scored(self):
        if self.ball.x - self.ball.radius <= -utils.FOOTBALL_PITCH_WIDTH // 2 + utils.GOAL_DEPTH and \
                (-utils.GOAL_WIDTH // 2 <= self.ball.y <= utils.GOAL_WIDTH // 2):
            self.scoreboard.blue_score += 1
            self._init_players()
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = None
            self.ball.owner = self.red_players[utils.PLAYER_COUNT - 1]
            self.ball.speed = 0
            self.red_players[utils.PLAYER_COUNT - 1].x, self.red_players[utils.PLAYER_COUNT - 1].y = self.ball.x, self.ball.y
            if self.config.additional_delay:
                time.sleep(1)
        if self.ball.x + self.ball.radius >= utils.FOOTBALL_PITCH_WIDTH // 2 - utils.GOAL_DEPTH and \
                (-utils.GOAL_WIDTH // 2 <= self.ball.y <= utils.GOAL_WIDTH // 2):
            self.scoreboard.red_score += 1
            self._init_players()
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = None
            self.ball.owner = self.blue_players[utils.PLAYER_COUNT - 1]
            self.ball.speed = 0
            self.blue_players[utils.PLAYER_COUNT - 1].x, self.blue_players[utils.PLAYER_COUNT - 1].y = self.ball.x, self.ball.y
            if self.config.additional_delay:
                time.sleep(1)

    def end(self):
        result_file = open('result.txt', 'w')
        result_file.write(f"{self.scoreboard.red_score} {self.scoreboard.blue_score}")
        print('end')

    def _init_players(self):
        red_players = []
        blue_players = []
        for red_player in utils.RED_PLAYERS_INITIAL_VALUES:
            red_players.append(models.Player(
                color='red',
                **red_player,
            ))
        for blue_player in utils.BLUE_PLAYERS_INITIAL_VALUES:
            blue_players.append(models.Player(
                color='blue',
                **blue_player,
            ))
        self.red_players = red_players
        self.blue_players = blue_players

    def _get_args_for_red_team(self):
        red_players_info = []
        blue_players_info = []
        for red_player in self.red_players:
            red_players_info.append(red_player.info)
        for blue_player in self.blue_players:
            blue_players_info.append(blue_player.info)
        ball_info = self.ball.info
        scoreboard_info = self.scoreboard.info
        return red_players_info, blue_players_info, ball_info, scoreboard_info

    def _get_args_for_blue_team(self):
        red_players_info = []
        blue_players_info = []
        for red_player in self.red_players:
            red_players_info.append(red_player.info_reversed)
        for blue_player in self.blue_players:
            blue_players_info.append(blue_player.info_reversed)
        ball_info = self.ball.info_reversed
        scoreboard_info = self.scoreboard.info_reversed
        return blue_players_info, red_players_info, ball_info, scoreboard_info

    def _show_and_increase_cycle_number(self):
        if self.config.graphical_output:
            self.screen.fill(utils.GRASS_COLOR)
            self._draw_margins()
            self._draw_football_pitch()
            self._draw_team_names()
            for red_player in self.red_players:
                red_player.draw(self.screen)
            for blue_player in self.blue_players:
                blue_player.draw(self.screen)
            self.ball.draw(self.screen)
            self.scoreboard.draw(self.screen)
            pg.display.update()
        self.scoreboard.cycle_number += 1

    def _draw_football_pitch(self):
        # DRAW GOALS
        red_goal_pygame_x = utils.HORIZONTAL_MARGIN - utils.GOAL_DEPTH
        red_goal_pygame_y = utils.SCREEN_HEIGHT // 2 - utils.GOAL_WIDTH // 2
        pg.draw.rect(
            self.screen,
            utils.GOAL_COLOR['red'],
            (red_goal_pygame_x, red_goal_pygame_y, utils.GOAL_DEPTH, utils.GOAL_WIDTH),
            0,
        )
        blue_goal_pygame_x = utils.SCREEN_WIDTH - utils.HORIZONTAL_MARGIN
        blue_goal_pygame_y = utils.SCREEN_HEIGHT // 2 - utils.GOAL_WIDTH // 2
        pg.draw.rect(
            self.screen,
            utils.GOAL_COLOR['blue'],
            (blue_goal_pygame_x, blue_goal_pygame_y, utils.GOAL_DEPTH, utils.GOAL_WIDTH),
            0,
        )
        # DRAW CENTER POINT
        pg.draw.circle(
            self.screen,
            utils.LINE_COLOR,
            utils.convert_coordinate_cartesian_to_pygame(0, 0),
            utils.CENTER_POINT_RADIUS,
            0,
        )
        # DRAW CENTER CIRCLE
        pg.draw.circle(
            self.screen,
            utils.LINE_COLOR,
            utils.convert_coordinate_cartesian_to_pygame(0, 0),
            utils.CENTER_CIRCLE_RADIUS,
            utils.LINE_THICKNESS,
        )
        # DRAW CENTER LINE
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (utils.SCREEN_WIDTH // 2 - utils.LINE_THICKNESS // 2, utils.VERTICAL_MARGIN),
            (utils.SCREEN_WIDTH // 2 - utils.LINE_THICKNESS // 2, utils.SCREEN_HEIGHT - utils.VERTICAL_MARGIN),
            utils.LINE_THICKNESS,
        )
        # DRAW PENALTY AREA
            # LEFT
        left_x1 = utils.HORIZONTAL_MARGIN
        left_x2 = utils.HORIZONTAL_MARGIN + utils.PENALTY_AREA_WIDTH
        left_y1 = utils.SCREEN_HEIGHT // 2 - utils.PENALTY_AREA_HEIGHT // 2
        left_y2 = utils.SCREEN_HEIGHT // 2 + utils.PENALTY_AREA_HEIGHT // 2
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (left_x1, left_y1),
            (left_x2, left_y1),
            utils.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (left_x2, left_y1),
            (left_x2, left_y2),
            utils.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (left_x1, left_y2),
            (left_x2, left_y2),
            utils.LINE_THICKNESS,
        )
            # RIGHT
        right_x1 = utils.SCREEN_WIDTH - utils.HORIZONTAL_MARGIN
        right_x2 = right_x1 - utils.PENALTY_AREA_WIDTH
        right_y1 = left_y1
        right_y2 = left_y2
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (right_x1, right_y1),
            (right_x2, right_y1),
            utils.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (right_x2, right_y1),
            (right_x2, right_y2),
            utils.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (right_x1, right_y2),
            (right_x2, right_y2),
            utils.LINE_THICKNESS,
        )

    def _draw_team_names(self):
        utils.write_text_on_pygame_screen(
            self.screen,
            30,
            utils.SCOREBOARD_RED_SCORE_COLOR,
            self.config.team1_name,
            -utils.SCREEN_WIDTH // 4,
            utils.SCREEN_HEIGHT // 2 - 5,
        )
        utils.write_text_on_pygame_screen(
            self.screen,
            30,
            utils.SCOREBOARD_BLUE_SCORE_COLOR,
            self.config.team2_name,
            utils.SCREEN_WIDTH // 4,
            utils.SCREEN_HEIGHT // 2 - 5,
        )

    def _draw_margins(self):
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, 0, utils.SCREEN_WIDTH, utils.VERTICAL_MARGIN)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, utils.SCREEN_HEIGHT - utils.VERTICAL_MARGIN, utils.SCREEN_WIDTH, utils.VERTICAL_MARGIN)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, 0, utils.HORIZONTAL_MARGIN, utils.SCREEN_HEIGHT)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (utils.SCREEN_WIDTH - utils.HORIZONTAL_MARGIN, 0, utils.HORIZONTAL_MARGIN, utils.SCREEN_HEIGHT)
        )
