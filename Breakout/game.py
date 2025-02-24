import pygame, sys, time, json
import numpy as np
from settings import *
from paddle import Paddle
from ball import Ball
from brick import Brick
from projectile import Projectile
from bonus import Bonus

class Game:
    def __init__(self, level, settings=None):
        pygame.init()
        self.level = level
        self.theme = customization
        if settings:
            self.level_data = settings
        else:
            self.level_data = levels[level]
        self.display_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(f'Breakout - Level {level}')
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)
        self.paddle = Paddle()
        self.paddle_speed = self.level_data.get("paddle_speed", paddle_speed)
        self.ball = Ball(self.level_data["ball_speed"], self.level_data.get("ball_size", ball_radius),
                         self.theme["ball"])
        self.bricks = self.create_bricks()
        self.projectiles = []  # List to store projectiles
        self.bonuses = []  # List to store bonuses
        self.shoot_enabled = self.level_data["shooting"]
        self.game_over = False
        self.victory = False
        self.start_time = time.time()
        self.best_time = self.load_best_time()
        self.last_f_press_time = 0  # Time of last "F" key press

        # Load background if specified
        if self.theme["background_game"]:
            self.background = pygame.image.load(self.theme["background_game"])
            self.background = pygame.transform.scale(self.background, (window_width, window_height))
        else:
            self.background = None

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

    def create_bricks(self):
        bricks = []
        for row in range(brick_rows):
            for col in range(brick_columns):
                x = col * (brick_width + 5) + 13
                y = row * (brick_height + 5) + 10
                strength = self.level_data["brick_strength"]  # Strength depending on the level
                brick_images = [self.theme["bricks"][i] for i in range(5)]
                bricks.append(Brick(x, y, strength, brick_images))
        return bricks

    def load_best_time(self):
        try:
            with open('levels_data.json', 'r') as file:
                data = json.load(file)
                return data.get(str(self.level), {}).get('best_time', 9999.59)
        except (FileNotFoundError, json.JSONDecodeError):
            return 9999.59

    def save_best_time(self, best_time):
        try:
            with open('levels_data.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if str(self.level) not in data:
            data[str(self.level)] = {}
        data[str(self.level)]['best_time'] = best_time
        with open('levels_data.json', 'w') as file:
            json.dump(data, file)
        print(f"Best time saved for level {self.level}: {best_time}")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.shoot_enabled and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.sounds["laser_shoot"].play()
                    self.shoot_projectile()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    current_time = time.time()
                    if current_time - self.last_f_press_time < 0.5:  # Check if the last press was less than 0.5 seconds ago
                        self.victory = True
                        self.end_game()
                        return
                    self.last_f_press_time = current_time

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move(-self.paddle_speed)
            if keys[pygame.K_RIGHT]:
                self.paddle.move(self.paddle_speed)

            self.ball.move()
            self.check_collisions()

            if self.ball.rect.top > window_height:
                self.game_over = True

            for projectile in self.projectiles[:]:
                projectile.move()
                if projectile.rect.bottom < 0:
                    self.projectiles.remove(projectile)

            for bonus in self.bonuses[:]:
                bonus.move()
                if bonus.rect.top > window_height:
                    self.bonuses.remove(bonus)
                elif bonus.rect.colliderect(self.paddle.rect):
                    self.sounds["bonus_collect"].play()
                    self.apply_bonus(bonus)
                    self.bonuses.remove(bonus)

            # Draw the background
            if self.background:
                self.display_surface.blit(self.background, (0, 0))
            else:
                self.display_surface.fill(bg_color)

            self.paddle.draw(self.display_surface)
            self.ball.draw(self.display_surface)
            for brick in self.bricks:
                brick.draw(self.display_surface)
            for projectile in self.projectiles:
                projectile.draw(self.display_surface)
            for bonus in self.bonuses:
                bonus.draw(self.display_surface)

            self.display_time()
            pygame.display.update()
            self.clock.tick(fps)

            if self.game_over or len(self.bricks) == 0:
                self.end_game()
                return

    def shoot_projectile(self):
        x = self.paddle.rect.centerx - projectile_width // 2
        y = self.paddle.rect.top - projectile_height
        self.projectiles.append(Projectile(x, y))

    def check_collisions(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            if self.ball.rect.bottom <= self.paddle.rect.top + (self.paddle.rect.height // 2):  # Check collision only with the top of the paddle
                self.ball.speed[1] = -self.ball.speed[1]
                self.sounds["hit_paddle"].play()
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                self.ball.speed[1] = -self.ball.speed[1]
                if brick.hit():
                    self.sounds["brick_break"].play()
                    self.bricks.remove(brick)
                    if self.level_data["bonuses"] and np.random.rand() < 0.2:
                        self.bonuses.append(Bonus(brick.rect.x, brick.rect.y))
                else:
                    self.sounds["brick_crack"].play()
        for projectile in self.projectiles[:]:
            for brick in self.bricks[:]:
                if projectile.rect.colliderect(brick.rect):
                    self.sounds["laser_hit"].play()
                    if brick.hit():
                        self.sounds["brick_break"].play()
                        self.bricks.remove(brick)
                        if self.level_data["bonuses"] and np.random.rand() < 0.2:
                            self.bonuses.append(Bonus(brick.rect.x, brick.rect.y))
                    else:
                        self.sounds["brick_crack"].play()
                    self.projectiles.remove(projectile)
                    break

    def apply_bonus(self, bonus):
        new_width = self.paddle.rect.width + 20
        max_width = window_width - 20  # Set a maximum width for the paddle
        self.paddle.resize(min(new_width, max_width))

    def display_time(self):
        elapsed_time = time.time() - self.start_time
        time_text = self.font.render(f"Time: {elapsed_time:.2f}", True, text_color)
        self.display_surface.blit(time_text, (10, 10))
        best_time_text = self.font.render(f"Best Time: {self.best_time:.2f}", True, text_color)
        self.display_surface.blit(best_time_text, (10, 40))

    def end_game(self):
        elapsed_time = time.time() - self.start_time
        if self.game_over:
            self.sounds["game_over"].play()
            self.show_message("Game Over")
        else:
            self.victory = True
            self.sounds["victory"].play()
            self.show_message("You Win!")
            if not self.best_time or elapsed_time < self.best_time:
                self.best_time = elapsed_time
                self.save_best_time(self.best_time)

        self.display_retry_menu()

    def show_message(self, message):
        message_text = self.font.render(message, True, text_color)
        self.display_surface.blit(message_text, (window_width // 2 - message_text.get_width() // 2, window_height // 2))
        pygame.display.update()

    def display_retry_menu(self):
        self.show_message("Game Over" if self.game_over else "You Win!")

        self.retry_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 50)
        self.menu_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 120, 200, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.retry_button.collidepoint(event.pos):
                        # Restart the game with the same settings
                        new_game = Game(self.level, self.level_data)
                        new_game.run()
                    if self.menu_button.collidepoint(event.pos):
                        self.return_to_main_menu()  # Return to main menu

            pygame.draw.rect(self.display_surface, (255, 255, 255), self.retry_button)
            retry_text = self.font.render("Retry", True, (0, 0, 0))
            self.display_surface.blit(retry_text, (
                self.retry_button.x + self.retry_button.width // 2 - retry_text.get_width() // 2,
                self.retry_button.y + 10))

            pygame.draw.rect(self.display_surface, (255, 255, 255), self.menu_button)
            menu_text = self.font.render("Menu", True, (0, 0, 0))
            self.display_surface.blit(menu_text, (
                self.menu_button.x + self.menu_button.width // 2 - menu_text.get_width() // 2, self.menu_button.y + 10))

            pygame.display.update()
            self.clock.tick(fps)

    def return_to_main_menu(self):
        print("Returning to main menu")
        pygame.quit()
        import menu
        menu.Menu().run()
