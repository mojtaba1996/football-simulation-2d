import random
import time
from concurrent.futures import ThreadPoolExecutor

import pygame as pg

import exception
import models
import settings.color
import settings.game
import settings.size
import settings.init_values
import utils.concurrency
from decision import get_decisions
from team1 import play as red_play
from team2 import play as blue_play


class Runner:
    def __init__(self, config):
        pg.init()
        self.config = config
        self.screen = pg.display.set_mode((settings.size.SCREEN_WIDTH, settings.size.SCREEN_HEIGHT))
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

            with ThreadPoolExecutor() as executor:
                red_future = executor.submit(
                    utils.concurrency.run_with_timeout,
                    red_play,
                    self.config.play_timeout,
                    [],
                    *self._get_args_for_red_team(),
                )
                blue_future = executor.submit(
                    utils.concurrency.run_with_timeout,
                    blue_play,
                    self.config.play_timeout,
                    [],
                    *self._get_args_for_blue_team(),
                )
                red_response = red_future.result()
                blue_response = blue_future.result()

            self.perform_decisions(red_response, blue_response)
            self.decrement_ban_cycles()
            self.ball.move()
            self.check_if_scored()
            self.check_if_the_bus_is_parked()
            self.check_if_ball_is_crowded()
            self._show_and_increase_cycle_number()
            time.sleep(self.config.cycle_delay)
            if self.scoreboard.cycle_number > self.config.max_cycle:
                if self.config.additional_delay:
                    time.sleep(4)
                end = True

    def handle_decision_perform_with_exception(self, decision):
        try:
            decision.validate()
            decision.perform()
        except exception.DecisionException as de:
            if self.config.print_decision_errors:
                print(de)

    def perform_decisions(self, red_response, blue_response):
        red_decisions, blue_decisions = get_decisions(self, red_response, blue_response)
        
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
            random_player.y = settings.size.SCREEN_HEIGHT // 2 - settings.size.VERTICAL_MARGIN + random_player.radius
            if random_player.color == 'red':
                random_player.y = -random_player.y
            players_in_area.remove(random_player)

    def check_if_the_bus_is_parked(self):
        ''' RED '''
        red_players_in_area = []
        for player in self.red_players:
            if -settings.size.FOOTBALL_PITCH_WIDTH//2<= player.x <= -settings.size.FOOTBALL_PITCH_WIDTH//2 + settings.size.PENALTY_AREA_WIDTH:
                if -settings.size.PENALTY_AREA_HEIGHT//2 <= player.y <= settings.size.PENALTY_AREA_HEIGHT//2:
                    if player.ban_cycles == 0:
                        red_players_in_area.append(player)
        self.kick_players(
            red_players_in_area,
            settings.game.ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER,
            settings.game.PENALTY_ARIA_BAN_CYCLES,
        )

        ''' BLUE '''
        blue_players_in_area = []
        for player in self.blue_players:
            if settings.size.FOOTBALL_PITCH_WIDTH//2 - settings.size.PENALTY_AREA_WIDTH <= player.x <= settings.size.FOOTBALL_PITCH_WIDTH//2:
                if -settings.size.PENALTY_AREA_HEIGHT//2 <= player.y <= settings.size.PENALTY_AREA_HEIGHT//2:
                    if player.ban_cycles == 0:
                        blue_players_in_area.append(player)
        self.kick_players(
            blue_players_in_area,
            settings.game.ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER,
            settings.game.PENALTY_ARIA_BAN_CYCLES,
        )

    def check_if_ball_is_crowded(self):
        ''' RED '''
        red_players_arround_ball = []
        for player in self.red_players:
            if utils.geometry.distance(self.ball, player) < settings.game.ALLOWED_PLAYERS_AROUND_BALL_RADIUS:
                if not player.is_in_own_penalty_area():
                    if player.ban_cycles == 0:
                        red_players_arround_ball.append(player)
        self.kick_players(
            red_players_arround_ball,
            settings.game.ALLOWED_PLAYERS_AROUND_BALL_NUMBER,
            settings.game.BALL_CROWDED_BAN_CYCLES,
        )
        ''' BLUE '''
        blue_players_arround_ball = []
        for player in self.blue_players:
            if utils.geometry.distance(self.ball, player) < settings.game.ALLOWED_PLAYERS_AROUND_BALL_RADIUS:
                if not player.is_in_own_penalty_area():
                    if player.ban_cycles == 0:
                        blue_players_arround_ball.append(player)
        self.kick_players(
            blue_players_arround_ball,
            settings.game.ALLOWED_PLAYERS_AROUND_BALL_NUMBER,
            settings.game.BALL_CROWDED_BAN_CYCLES,
        )

    def check_if_scored(self):
        if self.ball.x - self.ball.radius <= -settings.size.FOOTBALL_PITCH_WIDTH // 2 + settings.size.GOAL_DEPTH and \
                (-settings.size.GOAL_WIDTH // 2 <= self.ball.y <= settings.size.GOAL_WIDTH // 2):
            self.scoreboard.blue_score += 1
            self._init_players()
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = None
            self.ball.owner = self.red_players[settings.game.PLAYER_COUNT - 1]
            self.ball.speed = 0
            self.red_players[settings.game.PLAYER_COUNT - 1].x, self.red_players[settings.game.PLAYER_COUNT - 1].y = self.ball.x, self.ball.y
            if self.config.additional_delay:
                time.sleep(1)
        if self.ball.x + self.ball.radius >= settings.size.FOOTBALL_PITCH_WIDTH // 2 - settings.size.GOAL_DEPTH and \
                (-settings.size.GOAL_WIDTH // 2 <= self.ball.y <= settings.size.GOAL_WIDTH // 2):
            self.scoreboard.red_score += 1
            self._init_players()
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = None
            self.ball.owner = self.blue_players[settings.game.PLAYER_COUNT - 1]
            self.ball.speed = 0
            self.blue_players[settings.game.PLAYER_COUNT - 1].x, self.blue_players[settings.game.PLAYER_COUNT - 1].y = self.ball.x, self.ball.y
            if self.config.additional_delay:
                time.sleep(1)

    def end(self):
        with open('result.txt', 'w') as result_file:
            result_file.write(f"{self.scoreboard.red_score} {self.scoreboard.blue_score}")
        print('end')

    def _init_players(self):
        red_players = []
        blue_players = []
        for red_player in settings.init_values.RED_PLAYERS_INITIAL_VALUES:
            red_players.append(models.Player(
                color='red',
                **red_player,
            ))
        for blue_player in settings.init_values.BLUE_PLAYERS_INITIAL_VALUES:
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
            self.screen.fill(settings.color.GRASS_COLOR)
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
        red_goal_pygame_x = settings.size.HORIZONTAL_MARGIN - settings.size.GOAL_DEPTH
        red_goal_pygame_y = settings.size.SCREEN_HEIGHT // 2 - settings.size.GOAL_WIDTH // 2
        pg.draw.rect(
            self.screen,
            settings.color.GOAL_COLOR['red'],
            (red_goal_pygame_x, red_goal_pygame_y, settings.size.GOAL_DEPTH, settings.size.GOAL_WIDTH),
            0,
        )
        blue_goal_pygame_x = settings.size.SCREEN_WIDTH - settings.size.HORIZONTAL_MARGIN
        blue_goal_pygame_y = settings.size.SCREEN_HEIGHT // 2 - settings.size.GOAL_WIDTH // 2
        pg.draw.rect(
            self.screen,
            settings.color.GOAL_COLOR['blue'],
            (blue_goal_pygame_x, blue_goal_pygame_y, settings.size.GOAL_DEPTH, settings.size.GOAL_WIDTH),
            0,
        )
        # DRAW CENTER POINT
        pg.draw.circle(
            self.screen,
            settings.color.LINE_COLOR,
            utils.geometry.convert_coordinate_cartesian_to_pygame(0, 0),
            settings.size.CENTER_POINT_RADIUS,
            0,
        )
        # DRAW CENTER CIRCLE
        pg.draw.circle(
            self.screen,
            settings.color.LINE_COLOR,
            utils.geometry.convert_coordinate_cartesian_to_pygame(0, 0),
            settings.size.CENTER_CIRCLE_RADIUS,
            settings.size.LINE_THICKNESS,
        )
        # DRAW CENTER LINE
        pg.draw.line(
            self.screen,
            settings.color.LINE_COLOR,
            (settings.size.SCREEN_WIDTH // 2 - settings.size.LINE_THICKNESS // 2, settings.size.VERTICAL_MARGIN),
            (settings.size.SCREEN_WIDTH // 2 - settings.size.LINE_THICKNESS // 2, settings.size.SCREEN_HEIGHT - settings.size.VERTICAL_MARGIN),
            settings.size.LINE_THICKNESS,
        )
        # DRAW PENALTY AREA
            # LEFT
        left_x1 = settings.size.HORIZONTAL_MARGIN
        left_x2 = settings.size.HORIZONTAL_MARGIN + settings.size.PENALTY_AREA_WIDTH
        left_y1 = settings.size.SCREEN_HEIGHT // 2 - settings.size.PENALTY_AREA_HEIGHT // 2
        left_y2 = settings.size.SCREEN_HEIGHT // 2 + settings.size.PENALTY_AREA_HEIGHT // 2
        pg.draw.line(
            self.screen,
            settings.color.LINE_COLOR,
            (left_x1, left_y1),
            (left_x2, left_y1),
            settings.size.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            settings.color.LINE_COLOR,
            (left_x2, left_y1),
            (left_x2, left_y2),
            settings.size.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            settings.color.LINE_COLOR,
            (left_x1, left_y2),
            (left_x2, left_y2),
            settings.size.LINE_THICKNESS,
        )
            # RIGHT
        right_x1 = settings.size.SCREEN_WIDTH - settings.size.HORIZONTAL_MARGIN
        right_x2 = right_x1 - settings.size.PENALTY_AREA_WIDTH
        right_y1 = left_y1
        right_y2 = left_y2
        pg.draw.line(
            self.screen,
            settings.color.LINE_COLOR,
            (right_x1, right_y1),
            (right_x2, right_y1),
            settings.size.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            settings.color.LINE_COLOR,
            (right_x2, right_y1),
            (right_x2, right_y2),
            settings.size.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            settings.color.LINE_COLOR,
            (right_x1, right_y2),
            (right_x2, right_y2),
            settings.size.LINE_THICKNESS,
        )

    def _draw_team_names(self):
        utils.display.write_text_on_pygame_screen(
            self.screen,
            30,
            settings.color.SCOREBOARD_RED_SCORE_COLOR,
            self.config.team1_name,
            -settings.size.SCREEN_WIDTH // 4,
            settings.size.SCREEN_HEIGHT // 2 - 5,
        )
        utils.display.write_text_on_pygame_screen(
            self.screen,
            30,
            settings.color.SCOREBOARD_BLUE_SCORE_COLOR,
            self.config.team2_name,
            settings.size.SCREEN_WIDTH // 4,
            settings.size.SCREEN_HEIGHT // 2 - 5,
        )

    def _draw_margins(self):
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, 0, settings.size.SCREEN_WIDTH, settings.size.VERTICAL_MARGIN)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, settings.size.SCREEN_HEIGHT - settings.size.VERTICAL_MARGIN, settings.size.SCREEN_WIDTH, settings.size.VERTICAL_MARGIN)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, 0, settings.size.HORIZONTAL_MARGIN, settings.size.SCREEN_HEIGHT)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (settings.size.SCREEN_WIDTH - settings.size.HORIZONTAL_MARGIN, 0, settings.size.HORIZONTAL_MARGIN, settings.size.SCREEN_HEIGHT)
        )
