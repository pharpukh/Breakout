import unittest
import pygame
from paddle import Paddle
from settings import *


class TestPaddle(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((800, 600))  # Создаем поверхность для тестов
        self.paddle = Paddle()

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertIsInstance(self.paddle.rect, pygame.Rect)
        self.assertIsInstance(self.paddle.image, pygame.Surface)

    def test_move_left(self):
        initial_x = self.paddle.rect.x
        self.paddle.move(-10)
        self.assertEqual(self.paddle.rect.x, initial_x - 10)

    def test_move_right(self):
        initial_x = self.paddle.rect.x
        self.paddle.move(10)
        self.assertEqual(self.paddle.rect.x, initial_x + 10)


if __name__ == '__main__':
    unittest.main()
