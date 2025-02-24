# menu.py
import pygame, sys, json, os
from settings import *
from game import Game

class Menu:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Breakout Menu')
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 100)  # Increased font size for "Breakout" title
        self.font = pygame.font.Font(None, 36)  # Standard font size for other text
        self.level_buttons = self.create_level_buttons()
        self.selected_level = None
        self.levels_data = self.load_levels_data()
        self.creative_settings = {
            "brick_strength": 0,
            "ball_speed": 5,
            "bonuses": True,
            "shooting": True,
            "paddle_speed": 10,
            "ball_size": 10
        }
        # Load menu background
        self.menu_background = pygame.image.load(customization["background_menu"])
        self.menu_background = pygame.transform.scale(self.menu_background, (window_width, window_height))

        # Load sounds
        self.sounds = {
            "hit_paddle": pygame.mixer.Sound(customization["sounds"]["hit_paddle"]),
            "brick_crack": pygame.mixer.Sound(customization["sounds"]["brick_crack"]),
            "brick_break": pygame.mixer.Sound(customization["sounds"]["brick_break"]),
            "bonus_collect": pygame.mixer.Sound(customization["sounds"]["bonus_collect"]),
            "game_over": pygame.mixer.Sound(customization["sounds"]["game_over"]),
            "victory": pygame.mixer.Sound(customization["sounds"]["victory"]),
            "level_select": pygame.mixer.Sound(customization["sounds"]["level_select"]),
            "laser_shoot": pygame.mixer.Sound(customization["sounds"]["laser_shoot"]),
            "laser_hit": pygame.mixer.Sound(customization["sounds"]["laser_hit"])
        }

        # Play menu background music
        pygame.mixer.music.load(customization["music"]["menu"])
        pygame.mixer.music.play(-1)

    def create_level_buttons(self):
        buttons = []
        y_offset = 200  # Vertical position for the first button
        for level in levels:
            buttons.append((pygame.Rect(100, y_offset, 200, 50), level))
            y_offset += 70
        return buttons

    def load_levels_data(self):
        try:
            with open('rustafar/Breakout/levels_data.json', 'r') as file:
                levels_data = json.load(file)
                # Ensure boolean values are properly parsed
                for level, data in levels_data.items():
                    if "unlocked" in data:
                        data["unlocked"] = bool(data["unlocked"])
        except FileNotFoundError:
            levels_data = {str(level): {"best_time": 9999.59, "unlocked": levels[level]["unlocked"]} for level in levels}

        for level in levels:
            if str(level) not in levels_data:
                levels_data[str(level)] = {"best_time": 9999.59, "unlocked": levels[level]["unlocked"]}
            if "unlocked" not in levels_data[str(level)]:
                levels_data[str(level)]["unlocked"] = levels[level]["unlocked"]

        print(f"Loaded levels data: {levels_data}")
        return levels_data

    def save_levels_data(self):
        try:
            # Ensure that all data is serializable to JSON
            with open('rustafar/Breakout/levels_data.json', 'w') as file:
                json.dump(self.levels_data, file, indent=4)  # Pretty-print with indentation
            print(f"Levels data saved: {self.levels_data}")
        except TypeError as e:
            print(f"Error saving levels data: {e}")
            print(f"Current levels data: {self.levels_data}")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button, level in self.level_buttons:
                        if button.collidepoint(event.pos):
                            self.sounds["level_select"].play()
                            self.selected_level = level
                            if level == "creative":
                                pygame.mixer.music.load(customization["music"]["creative"])
                                pygame.mixer.music.play(-1)
                                self.show_settings(level)
                            else:
                                pygame.mixer.music.load(customization["music"]["game"])
                                pygame.mixer.music.play(-1)
                                self.start_game_loop(level)
                    if hasattr(self, 'retry_button') and self.retry_button.collidepoint(event.pos):
                        if self.selected_level:
                            self.start_game_loop(self.selected_level)

            self.display_surface.blit(self.menu_background, (0, 0))  # Display the menu background
            self.draw_menu()

            pygame.display.update()
            self.clock.tick(fps)

    def draw_menu(self):
        title_text = self.title_font.render("Breakout", True, (255, 255, 255))
        self.display_surface.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 50))

        for button, level in self.level_buttons:
            pygame.draw.rect(self.display_surface, (255, 255, 255), button)
            level_text = self.font.render(f"Level {level}", True, (0, 0, 0))
            self.display_surface.blit(level_text, (button.x + button.width // 2 - level_text.get_width() // 2, button.y + 10))

            best_time_x = button.x + button.width + 50
            if self.levels_data[str(level)]["unlocked"]:
                best_time_text = self.font.render(f"Best Time: {self.levels_data[str(level)]['best_time']:.2f}", True, (255, 255, 255))
            else:
                best_time_text = self.font.render("Locked", True, (255, 0, 0))
            self.display_surface.blit(best_time_text, (best_time_x, button.y + 10))

        if self.selected_level:
            self.retry_button = pygame.Rect(window_width // 2 - 100, 450, 200, 50)
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.retry_button)
            retry_text = self.font.render("Retry", True, (0, 0, 0))
            self.display_surface.blit(retry_text, (self.retry_button.x + self.retry_button.width // 2 - retry_text.get_width() // 2, self.retry_button.y + 10))

    def show_settings(self, level):
        settings = {
            "brick_strength": levels[level]["brick_strength"],
            "ball_speed": 5,
            "bonuses": levels[level]["bonuses"],
            "shooting": levels[level]["shooting"],
            "paddle_speed": levels[level].get("paddle_speed", 10),
            "ball_size": levels[level].get("ball_size", 10)
        }

        if level == "creative":
            settings = self.creative_settings

        # Load background for creative level
        creative_background = pygame.image.load(customization["background_creative"])
        creative_background = pygame.transform.scale(creative_background, (window_width, window_height))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button press
                    # Start game if start button is clicked
                    if self.start_button.collidepoint(event.pos):
                        self.start_game_loop(level, settings)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Check for left mouse button release
                    self.mouse_held = False
                if event.type == pygame.MOUSEMOTION and self.mouse_held:  # Mouse move while holding left mouse button
                    # Update sliders based on mouse position
                    if level == "creative" and self.brick_strength_slider.collidepoint(event.pos):
                        settings["brick_strength"] = (event.pos[0] - self.brick_strength_slider.x) * 100 // self.brick_strength_slider.width
                    if self.ball_speed_slider.collidepoint(event.pos):
                        settings["ball_speed"] = max(1, min(10, (event.pos[0] - self.ball_speed_slider.x) * 10 // self.ball_speed_slider.width))
                    if (level == "creative" or level == 4) and self.shooting_slider.collidepoint(event.pos):
                        settings["shooting"] = event.pos[0] > self.shooting_slider.centerx
                    if level == "creative" and self.paddle_speed_slider.collidepoint(event.pos):
                        settings["paddle_speed"] = max(1, min(20, (event.pos[0] - self.paddle_speed_slider.x) * 20 // self.paddle_speed_slider.width))
                    if level == "creative" and self.ball_size_slider.collidepoint(event.pos):
                        settings["ball_size"] = max(5, min(30, (event.pos[0] - self.ball_size_slider.x) * 30 // self.ball_size_slider.width))

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button press
                    self.mouse_held = True

            self.display_surface.blit(creative_background, (0, 0))  # Display background for creative level
            self.draw_settings(level, settings)
            pygame.display.update()
            self.clock.tick(fps)

    def draw_settings(self, level, settings):
        title_text = self.font.render(f"Level {level} Settings", True, (255, 255, 255))
        self.display_surface.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 50))

        column_1_x = 100
        column_2_x = 450
        y_offset = 100
        gap = 80

        if level == "creative":
            # Brick strength slider
            self.brick_strength_slider = pygame.Rect(column_1_x, y_offset + gap * 1, 300, 20)
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.brick_strength_slider)
            brick_strength_handle_position = self.brick_strength_slider.x + (settings["brick_strength"] * self.brick_strength_slider.width // 100)
            pygame.draw.circle(self.display_surface, (0, 0, 0), (brick_strength_handle_position, self.brick_strength_slider.y + self.brick_strength_slider.height // 2), 10)
            brick_strength_text = self.font.render(f"Brick Strength: {settings['brick_strength']}%", True, (255, 255, 255))
            self.display_surface.blit(brick_strength_text, (column_1_x, y_offset + gap * 1 - 30))

            # Paddle speed slider
            self.paddle_speed_slider = pygame.Rect(column_1_x, y_offset + gap * 2, 300, 20)
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.paddle_speed_slider)
            paddle_speed_handle_position = self.paddle_speed_slider.x + (settings["paddle_speed"] * self.paddle_speed_slider.width // 20)
            pygame.draw.circle(self.display_surface, (0, 0, 0), (paddle_speed_handle_position, self.paddle_speed_slider.y + self.paddle_speed_slider.height // 2), 10)
            paddle_speed_text = self.font.render(f"Paddle Speed: {settings['paddle_speed']}", True, (255, 255, 255))
            self.display_surface.blit(paddle_speed_text, (column_1_x, y_offset + gap * 2 - 30))

            # Ball size slider
            self.ball_size_slider = pygame.Rect(column_1_x, y_offset + gap * 3, 300, 20)
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.ball_size_slider)
            ball_size_handle_position = self.ball_size_slider.x + (settings["ball_size"] * self.ball_size_slider.width // 30)
            pygame.draw.circle(self.display_surface, (0, 0, 0), (ball_size_handle_position, self.ball_size_slider.y + self.ball_size_slider.height // 2), 10)
            ball_size_text = self.font.render(f"Ball Size: {settings['ball_size']}", True, (255, 255, 255))
            self.display_surface.blit(ball_size_text, (column_1_x, y_offset + gap * 3 - 30))

        # Ball speed slider
        self.ball_speed_slider = pygame.Rect(column_2_x, y_offset + gap * 1, 300, 20)
        pygame.draw.rect(self.display_surface, (255, 255, 255), self.ball_speed_slider)
        ball_speed_handle_position = self.ball_speed_slider.x + (settings["ball_speed"] * self.ball_speed_slider.width // 10)
        pygame.draw.circle(self.display_surface, (0, 0, 0), (ball_speed_handle_position, self.ball_speed_slider.y + self.ball_speed_slider.height // 2), 10)
        ball_speed_text = self.font.render(f"Ball Speed: {settings['ball_speed']}", True, (255, 255, 255))
        self.display_surface.blit(ball_speed_text, (column_2_x, y_offset + gap * 1 - 30))

        # Shooting slider
        self.shooting_slider = pygame.Rect(column_2_x, y_offset + gap * 2, 300, 20)
        pygame.draw.rect(self.display_surface, (255, 255, 255), self.shooting_slider)
        shooting_handle_position = self.shooting_slider.x + (self.shooting_slider.width if settings["shooting"] else 0)
        pygame.draw.circle(self.display_surface, (0, 0, 0), (shooting_handle_position, self.shooting_slider.y + self.shooting_slider.height // 2), 10)
        shooting_text = self.font.render(f"Shooting Enabled: {settings['shooting']}", True, (255, 255, 255))
        self.display_surface.blit(shooting_text, (column_2_x, y_offset + gap * 2 - 30))

        # Start Game button
        self.start_button = pygame.Rect(window_width // 2 - 100, y_offset + gap * 5, 200, 50)
        pygame.draw.rect(self.display_surface, (255, 255, 255), self.start_button)
        start_text = self.font.render("Start Game", True, (0, 0, 0))
        self.display_surface.blit(start_text, (self.start_button.x + self.start_button.width // 2 - start_text.get_width() // 2, self.start_button.y + 10))

    def start_game_loop(self, level, settings=None):
        game = Game(level, settings)
        game.run()
        if game.victory:
            print(f"Level {level} completed")
            self.levels_data[str(level)]["best_time"] = min(self.levels_data[str(level)]['best_time'], game.best_time)
            next_level = str(int(level) + 1)
            if next_level in self.levels_data:
                print(f"Unlocking level {next_level}")
                self.levels_data[next_level]["unlocked"] = True  # Update next level unlock status
                print(f"Level {next_level} unlocked")
        print(f"Saving levels data: {self.levels_data}")
        self.save_levels_data()
        self.selected_level = None

if __name__ == "__main__":
    menu = Menu()
    menu.run()
