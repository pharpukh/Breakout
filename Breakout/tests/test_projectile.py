import unittest

import pygame

from projectile import Projectile


# Создаем заглушку для поверхности Pygame
class MockSurface:
    def blit(self, image, rect):
        pass

class TestProjectile(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.projectile = Projectile(100, 100)

    def test_initialization(self):
        self.assertIsInstance(self.projectile.rect, pygame.Rect)
        self.assertIsInstance(self.projectile.image, pygame.Surface)
        self.assertIsInstance(self.projectile.speed, int)

    def test_move(self):
        initial_y = self.projectile.rect.y
        self.projectile.move()
        self.assertEqual(self.projectile.rect.y, initial_y + self.projectile.speed)

    def test_draw(self):
        # Создаем заглушку для поверхности Pygame
        mock_surface = MockSurface()
        # Проверяем, что метод draw не вызывает ошибок
        try:
            self.projectile.draw(mock_surface)
        except Exception as e:
            self.fail(f"draw() method raised exception: {e}")

if __name__ == '__main__':
    unittest.main()
