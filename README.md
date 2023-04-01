# red_players:
<pre>
[
    {'x': -428, 'y': 0, 'name': 'Player0', 'number': 0, 'color': 'red', 'radius': 18, 'ban_cycles': 0},
    {'x': -334, 'y': 216, 'name': 'Player1', 'number': 1, 'color': 'red', 'radius': 10, 'ban_cycles': 0},
    {'x': -250, 'y': -217, 'name': 'Player2', 'number': 2, 'color': 'red', 'radius': 10, 'ban_cycles': 0},
    {'x': -167, 'y': 216, 'name': 'Player3', 'number': 3, 'color': 'red', 'radius': 10, 'ban_cycles': 0},
    {'x': -83, 'y': -217, 'name': 'Player4', 'number': 4, 'color': 'red', 'radius': 10, 'ban_cycles': 0},
    {'x': 0, 'y': 216, 'name': 'Player5', 'number': 5, 'color': 'red', 'radius': 10, 'ban_cycles': 0},
]
</pre>

# blue_players:
<pre>
[
    {'x': 428, 'y': 0, 'name': 'Player0', 'number': 0, 'color': 'blue', 'radius': 18, 'ban_cycles': 0},
    {'x': 334, 'y': -216, 'name': 'Player1', 'number': 1, 'color': 'blue', 'radius': 10, 'ban_cycles': 0},
    {'x': 250, 'y': 217, 'name': 'Player2', 'number': 2, 'color': 'blue', 'radius': 10, 'ban_cycles': 0},
    {'x': 167, 'y': -216, 'name': 'Player3', 'number': 3, 'color': 'blue', 'radius': 10, 'ban_cycles': 0},
    {'x': 83, 'y': 217, 'name': 'Player4', 'number': 4, 'color': 'blue', 'radius': 10, 'ban_cycles': 0},
    {'x': 0, 'y': -216, 'name': 'Player5', 'number': 5, 'color': 'blue', 'radius': 10, 'ban_cycles': 0},
]
</pre>

# ball:
<pre>
{'x': 0, 'y': 0, 'radius': 8, 'owner_color': None, 'owner_number': None, 'speed': 0, 'direction': None}
</pre>

* owner_color choices: red, blue
* owner_number choices: 0,1,2,3,4,5

# scoreboard:
<pre>
{'red_score': 0, 'blue_score': 0, 'cycle_number': 1}
</pre>

* max cycle_number: 500

# move decision:
<pre>
{
    'type': 'move',
    'player_number': 3,
    'destination': {'x': 190, 'y': 30},
    'speed': 10,
}
</pre>

* player_number: from 0 to 5
* destination must be inside the football screen
* speed: from 1 to 10

# grab decision:
<pre>
{
    'type': 'grab',
    'player_number': 3,
}
</pre>

* The distance between the player and the ball must be less than 18 pixels to catch the ball (26 px for player number 0)
* If the ball is not owned by any other player, grab request will be successful with 100% probability
* If the ball is owned by any other player, grab request will be successful with 50% probability

# kick decision:
<pre>
{
    'type': 'kick',
    'player_number': 3,
    'direction': 20,
    'power': 60,
}
</pre>

* The player must be the owner of the ball
* direction: from 0 to 360
* You can use get_direction function to obtain direction
* power: from 1 to 60
* friction: 5

### ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER = 3
### ALLOWED_PLAYERS_AROUND_BALL_NUMBER = 1
### ALLOWED_PLAYERS_AROUND_BALL_RADIUS = make_even_number(3 * (PLAYER_RADIUS + BALL_RADIUS))  # 54
### BALL_CROWDED_BAN_CYCLES = 25
### PENALTY_ARIA_BAN_CYCLES = 20
