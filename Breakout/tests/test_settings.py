import unittest
import pygame
from projectile import Projectile  # Assuming the Projectile class is in a file named projectile.py
from settings import projectile_width, projectile_height, projectile_speed


class TestProjectile(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.surface = pygame.Surface((800, 600))  # Example surface size
        self.x = 100
        self.y = 200

    def test_initialization(self):
        projectile = Projectile(self.x, self.y)
        self.assertEqual(projectile.rect.x, self.x)
        self.assertEqual(projectile.rect.y, self.y)
        self.assertEqual(projectile.rect.width, projectile_width)
        self.assertEqual(projectile.rect.height, projectile_height)
        self.assertEqual(projectile.speed, projectile_speed)
        self.assertIsNotNone(projectile.image)
        self.assertEqual(projectile.image.get_size(), (projectile_width, projectile_height))

    def test_move(self):
        projectile = Projectile(self.x, self.y)
        initial_y = projectile.rect.y
        projectile.move()
        self.assertEqual(projectile.rect.y, initial_y + projectile_speed)

    def test_draw(self):
        projectile = Projectile(self.x, self.y)
        projectile.draw(self.surface)
        # Since the draw method does not return a value, we ensure it runs without error.


if __name__ == '__main__':
    unittest.main()
