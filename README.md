# Breakout Game
This is a Breakout game implemented in Python using the Pygame library.

## Overview
Breakout is a classic arcade game where the player controls a paddle to bounce a ball and break bricks. The objective is to clear all the bricks on the screen by bouncing the ball off the paddle and walls. The player loses a life if the ball hits the bottom of the screen, and the game ends when all lives are lost.

## Features
- Multiple levels with increasing difficulty
- Different brick strengths
- Bonuses that fall from broken bricks
- Shooting ability to destroy bricks and obstacles
- Customizable settings for each level
- Background music and sound effects
- Creative mode with adjustable settings for experimentation

## Installation
1. Clone the repository:
~~~~
    git clone https://gitlab.fit.cvut.cz/BI-PYT/B232/rustafar.git
~~~~

2. Navigate to the project directory:
~~~~
    cd Breakout
~~~~

3. Install the required dependencies:
~~~~
    pip install -r requirements.txt
~~~~

4. Run the game:
~~~~
    python main.py
~~~~

## Project Structure
### Description of the structure of folders and files in the project.
├── asserts
│├──  images # Graphic Images
│├──  music  # Music
| └──  sounds # Sounds
├── tests
│ ├── test_main.py # Test file for main.py file
│ ├── test_ball.py # Test file for ball.py file
│ ├── test_brick.py # Test file for brick.py file
│ ├── test_bonus.py # Test file  for bonus.py file
│ ├── test_game.py # Test file for game.py file
│ ├── test_menu.py # Test file for menu.py file
│ ├── test_paddle.py # Test file for paddle.py file
│ ├── test_projectile.py # Test file for projectile.py file
│ └── test_settings.py # Test file for settings.py file
|
├── settings.py              # Project settings file
├── ball.py                  # File with class Ball
├── bonus.py                 # File with class Bonus
├── brick.py                 # File with class Brick
├── game.py                  # File with class Game
├── paddle.py                # File with class Paddle
├── projectile.py            # File with class Projectile
├── menu.py                  # File with class Menu
├── main.py                  # Main file for launching the game
├── levels_data.json         # File with the best times to complete levels
├── rustafar.pdf            # Progress report
├── README.md               # Project documentation
└── equirements.txt         # Project dependencies

## Main classes
1. The `Ball` class is responsible for creating and managing the ball object in the game. 
2. The `Bonus` class manages bonuses in the game.
3. The `Brick` class manages individual bricks in the game. 
4. The `Game` class initializes the game, sets up the display, loads level data, sets up game elements (paddle, ball, bricks, bonuses, etc.), and loads background and sounds.
5. The `levels_data.json` file stores information about the best times to complete each level.
6. The `main.py` file is the entry point for the game.
7. The `menu.py` file initializes Pygame and sets up the display window, clock, fonts, and buttons for the menu.
8. The `Paddle` class encapsulates the behavior and appearance of the paddle in the game, allowing it to move, resize, and be drawn on the game surface.
9. The `Projectile` class is used to represent projectiles in the Breakout game. 
10. The `settings.py` file contains various settings and configurations used throughout the game. 

## Testing
~~~~
To run tests use the following command:
   pytest tests/
   
Make sure you have pytest installed:
   pip install pytest
~~~~