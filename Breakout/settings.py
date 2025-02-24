# settings.py

# Window settings
window_width = 800
window_height = 600
bg_color = (0, 0, 0)
fps = 60

# Paddle settings
paddle_width = 100
paddle_height = 20
paddle_color = (255, 255, 255)
paddle_speed = 10

# Ball settings
ball_radius = 10
ball_color = (255, 255, 255)
ball_speed = [5, -5]

# Brick settings
brick_width = 60
brick_height = 20
brick_colors = {
    0: (128, 128, 128),  # Gray color for bricks with strength 0
    1: (255, 0, 0),  # Red color for bricks with strength 1
    2: (255, 165, 0),  # Orange color for bricks with strength 2
    3: (255, 255, 0),  # Yellow color for bricks with strength 3
    4: (0, 128, 0)   # Green color for bricks with strength 4
}
brick_rows = 5
brick_columns = 12

# Projectile settings
projectile_width = 5
projectile_height = 10
projectile_color = (255, 255, 255)  # White color for projectiles
projectile_speed = -10  # Speed of projectiles

# Bonus settings
bonus_width = 20
bonus_height = 20
bonus_color = (0, 255, 0)  # Green color for bonuses
bonus_speed = 5  # Falling speed of bonuses

# Text color
text_color = (255, 255, 255)

# Level settings
levels = {
    1: {"brick_strength": 0, "ball_speed": 5, "bonuses": False, "shooting": False, "unlocked": True},
    2: {"brick_strength": 1, "ball_speed": 6, "bonuses": False, "shooting": False, "unlocked": True},
    3: {"brick_strength": 2, "ball_speed": 7, "bonuses": True, "shooting": False, "unlocked": True},
    4: {"brick_strength": 4, "ball_speed": 9, "bonuses": True, "shooting": True, "unlocked": True},
    "creative": {"brick_strength": 0, "ball_speed": 5, "bonuses": True, "shooting": True, "unlocked": True, "paddle_speed": 10, "ball_size": 10}
}

# Customization settings
customization = {
    "background_menu": "image/backgrounds/neon_3.png",
    "background_creative": "image/backgrounds/neon_3.png",
    "background_game": "image/backgrounds/black.jpg",
    "ball": "image/ball/ball_2.png",
    "paddle": "image/other/paddle-hd.png",
    "projectile": "image/other/shot.png",
    "bonus": "image/other/star.png",
    "bricks": {
        0: "image/bricks/brick_2.png",
        1: "image/bricks/brick_5.png",
        2: "image/bricks/brick_1.png",
        3: "image/bricks/brick_3.png",
        4: "image/bricks/brick_4.png"
    },
    "sounds": {
        "hit_paddle": "sounds/impact.wav",
        "brick_crack": "sounds/impact.wav",
        "brick_break": "sounds/impact.wav",
        "bonus_collect": "sounds/upgrade.mp3",
        "game_over": "sounds/lose.mp3",
        "victory": "sounds/win.mp3",
        "level_select": "sounds/button.mp3",
        "laser_shoot": "sounds/laser.wav",
        "laser_hit": "sounds/laser_hit.wav"
    },
    # Music files
    "music": {
        "menu": "music/music_2.mp3",
        "creative": "music/music_2.mp3",
        "game": "music/music.mp3"
    }
}