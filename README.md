### How to Play the 2D Football Simulation

This 2D football simulation allows you to write custom strategies for a team and see how they perform against another team. Below are the key guidelines and rules you need to follow:

#### Implementing the `play` Method

- To participate in the simulation, you need to implement the `play` method. This method should be defined in either `team1.py` or `team2.py`.
- The `play` method will be executed in each cycle of the game, and it's responsible for making decisions based on the current state of the game.

#### Team Assignment

- You should always assume that your team is the **red team** and that you are attacking from **left to right**. This means that you can copy and paste the exact same code from `team1.py` to `team2.py`, and the runner code will handle the rest.
- If you place your code in `team1.py`, you will be the **red team**. If you place your code in `team2.py`, you will be the **blue team**. However, regardless of where you place your code, you should always write your strategy with the assumption that you are the **red team**.

#### Game Cycles

- The game consists of 500 cycles. In each cycle, your `play` method will be executed, and you must make decisions for that cycle. These decisions will affect the behavior of your players and potentially the outcome of the game.

#### Execution of Decisions

- In each cycle, the decisions from both teams will be executed in the order you specify in your decision list.
- However, there is a randomness factor in how the decisions from both teams are merged within that cycle. This randomness determines the order in which actions from each team are executed, simulating the unpredictability of real-world football.

#### Execution Time Limit

- Your `play` method must complete its execution within **0.5 seconds**. If your code takes longer than this to run, it will be timed out and ignored for that cycle, which could negatively impact your team's performance.

#### Ban Rules

- **Penalty Area Rule:** If more than 3 players from the same team are in their penalty area, the extra players will be kicked out of the game and banned for 20 cycles. Banned players cannot make any decisions during their ban.
- **Ball Proximity Rule:** If more than 2 players from the same team are within a distance of 54 units from the ball, the extra players will be kicked out of the game and banned for 25 cycles. Banned players cannot make any decisions during their ban.

#### Starting the Game

- To start the game, run the `main.py` script.

### Constants

- `ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER = 3`
- `ALLOWED_PLAYERS_AROUND_BALL_NUMBER = 1`
- `ALLOWED_PLAYERS_AROUND_BALL_RADIUS = make_even_number(3 * (PLAYER_RADIUS + BALL_RADIUS))  # 54`
- `BALL_CROWDED_BAN_CYCLES = 25`
- `PENALTY_ARIA_BAN_CYCLES = 20`

### Input and Output of the `play` Method

- **Input:** In each execution of the `play` method, you will receive input variables representing the current state of the game. The examples below use sample numbers for illustration:
  - **red_players:** (Example)
    <pre>
    [
        {'x': -428, 'y': 0, 'name': 'Player0', 'number': 0, 'radius': 18, 'ban_cycles': 0},
        {'x': -334, 'y': 216, 'name': 'Player1', 'number': 1, 'radius': 10, 'ban_cycles': 0},
        {'x': -250, 'y': -217, 'name': 'Player2', 'number': 2, 'radius': 10, 'ban_cycles': 0},
        {'x': -167, 'y': 216, 'name': 'Player3', 'number': 3, 'radius': 10, 'ban_cycles': 0},
        {'x': -83, 'y': -217, 'name': 'Player4', 'number': 4, 'radius': 10, 'ban_cycles': 0},
        {'x': 0, 'y': 216, 'name': 'Player5', 'number': 5, 'radius': 10, 'ban_cycles': 0},
    ]
    </pre>
  - **blue_players:** (Example)
    <pre>
    [
        {'x': 428, 'y': 0, 'name': 'Player0', 'number': 0, 'radius': 18, 'ban_cycles': 0},
        {'x': 334, 'y': -216, 'name': 'Player1', 'number': 1, 'radius': 10, 'ban_cycles': 0},
        {'x': 250, 'y': 217, 'name': 'Player2', 'number': 2, 'radius': 10, 'ban_cycles': 0},
        {'x': 167, 'y': -216, 'name': 'Player3', 'number': 3, 'radius': 10, 'ban_cycles': 0},
        {'x': 83, 'y': 217, 'name': 'Player4', 'number': 4, 'radius': 10, 'ban_cycles': 0},
        {'x': 0, 'y': -216, 'name': 'Player5', 'number': 5, 'radius': 10, 'ban_cycles': 0},
    ]
    </pre>
  - **ball:** (Example)
    <pre>
    {'x': 0, 'y': 0, 'radius': 8, 'owner_color': None, 'owner_number': None, 'speed': 0, 'direction': None}
    </pre>
    * `owner_color` choices: `red`, `blue`
    * `owner_number` choices: `0,1,2,3,4,5`
  - **scoreboard:** (Example)
    <pre>
    {'red_score': 0, 'blue_score': 0, 'cycle_number': 1}
    </pre>
    * max `cycle_number`: 500

- **Output:** The output of your `play` method must be a decision list. This list should contain the actions your players will take in that cycle. The available decisions are:
  - **Move Decision:** (Example)
    <pre>
    {
        'type': 'move',
        'player_number': 3,
        'destination': {'x': 190, 'y': 30},
        'speed': 10,
    }
    </pre>
    * `player_number`: from 0 to 5
    * `destination` must be inside the football screen
    * `speed`: from 1 to 10
  - **Grab Decision:** (Example)
    <pre>
    {
        'type': 'grab',
        'player_number': 3,
    }
    </pre>
    * The distance between the player and the ball must be less than 18 units to catch the ball (26 units for player number 0)
    * If the ball is not owned by any other player, the grab request will be successful with 100% probability
    * If the ball is owned by any other player, the grab request will be successful with 50% probability
  - **Kick Decision:** (Example)
    <pre>
    {
        'type': 'kick',
        'player_number': 3,
        'direction': 20,
        'power': 60,
    }
    </pre>
    * The player must be the owner of the ball
    * `direction`: from 0 to 360
    * You can use the `get_direction` function to obtain the direction
    * `power`: from 1 to 60
    * friction: 5

By following these guidelines and rules, you can develop a strategy and see how it performs in the simulation. Good luck, and may the best strategy win!
