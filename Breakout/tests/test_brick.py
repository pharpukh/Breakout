import unittest
import pygame
from brick import Brick
from settings import *


class TestBrick(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_init(self):
        x = 100
        y = 200
        strength = 3
        brick = Brick(x, y, strength)
        self.assertEqual(brick.rect.x, x)
        self.assertEqual(brick.rect.y, y)
        self.assertEqual(brick.rect.width, brick_width)
        self.assertEqual(brick.rect.height, brick_height)
        self.assertEqual(brick.strength, strength)
        self.assertEqual(brick.color, brick_colors[strength])
        self.assertIsNone(brick.image)

    def test_draw(self):
        brick = Brick(100, 200, 2)  # Create a brick with strength 2
        screen = pygame.Surface((800, 600))  # Create a surface to draw on
        brick.draw(screen)  # Draw the brick on the surface
        # Check if the brick is drawn correctly (either image or color)
        self.assertIsNotNone(screen.get_at((brick.rect.x, brick.rect.y)))

    def test_hit(self):
        brick = Brick(100, 200, 2)  # Create a brick with strength 2
        initial_strength = brick.strength
        destroyed = brick.hit()  # Hit the brick
        # Check if the strength decreased and the brick is not destroyed yet
        self.assertEqual(brick.strength, initial_strength - 1)
        self.assertFalse(destroyed)
        # Hit the brick until it's destroyed
        while not destroyed:
            destroyed = brick.hit()
        # Check if the brick is destroyed
        self.assertTrue(destroyed)


if __name__ == '__main__':
    unittest.main()
