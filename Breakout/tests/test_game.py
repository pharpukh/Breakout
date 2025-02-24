import unittest
from unittest.mock import MagicMock

import pygame

from ball import Ball
from game import Game
from paddle import Paddle


class TestGame(unittest.TestCase):
    def setUp(self):
        self.level = 1
        self.game = Game(self.level)
        self.game.theme = {"ball": "ball_image_path.png", "background_game": None, "bricks": {}}

    def test_initialization(self):
        self.assertEqual(self.game.level, self.level)
        self.assertIsInstance(self.game.paddle, Paddle)
        self.assertIsInstance(self.game.ball, Ball)
        self.assertIsInstance(self.game.bricks, list)
        self.assertIsInstance(self.game.projectiles, list)
        self.assertIsInstance(self.game.bonuses, list)
        self.assertTrue(self.game.shoot_enabled)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.victory)
        self.assertEqual(self.game.start_time, 0)
        self.assertIsInstance(self.game.font, pygame.font.Font)
        self.assertIsInstance(self.game.display_surface, pygame.Surface)
        self.assertIsInstance(self.game.clock, pygame.time.Clock)
        self.assertEqual(self.game.last_f_press_time, 0)
        self.assertIsNone(self.game.background)

    def test_create_bricks(self):
        bricks = self.game.create_bricks()
        self.assertEqual(len(bricks), 0)  # As no brick image are provided

    def test_load_best_time(self):
        self.assertEqual(self.game.load_best_time(), 9999.59)

    def test_save_best_time(self):
        self.game.save_best_time(5000.0)  # Test saving the best time

    def test_shoot_projectile(self):
        self.game.paddle.rect.centerx = 100
        self.game.paddle.rect.top = 200
        self.game.projectiles = []
        self.game.shoot_projectile()
        self.assertEqual(len(self.game.projectiles), 1)  # Projectile added

    def test_check_collisions(self):
        # Mocking methods to avoid pygame dependencies
        self.game.ball.move = MagicMock()
        self.game.ball.rect = MagicMock()
        self.game.paddle.rect = MagicMock()
        self.game.paddle.rect.top = 100
        self.game.paddle.rect.height = 20
        self.game.paddle.rect.left = 0
        self.game.paddle.rect.right = 50
        self.game.check_collisions()  # No assertion, just test if it runs without error

    def test_apply_bonus(self):
        bonus = MagicMock()
        bonus.rect.width = 100
        self.game.paddle.rect.width = 50
        self.game.apply_bonus(bonus)
        self.assertEqual(self.game.paddle.rect.width, 70)  # Width increased by 20

    def test_display_time(self):
        # Mocking methods to avoid pygame dependencies
        self.game.font.render = MagicMock()
        self.game.display_time()  # No assertion, just test if it runs without error

if __name__ == "__main__":
    unittest.main()
