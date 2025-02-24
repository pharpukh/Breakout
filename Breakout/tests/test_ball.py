import unittest
import pygame
from ball import Ball
from settings import *


class TestBall(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_init(self):
        ball = Ball(5)
        self.assertEqual(ball.speed.tolist(), [5, -5])
        self.assertEqual(ball.radius, ball_radius)
        self.assertEqual(ball.rect.width, ball_radius * 2)
        self.assertEqual(ball.rect.height, ball_radius * 2)
        self.assertIsNone(ball.image)

    def test_init_with_list_speed(self):
        ball = Ball([3, -4])
        self.assertEqual(ball.speed.tolist(), [3, -4])


if __name__ == '__main__':
    unittest.main()
