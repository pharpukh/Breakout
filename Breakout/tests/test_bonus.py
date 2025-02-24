import unittest
from unittest.mock import MagicMock, patch
from bonus import Bonus


class TestBonus(unittest.TestCase):
    @patch("pygame.Rect")
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def setUp(self, mock_scale, mock_load, mock_rect):
        mock_rect.return_value.x = 100
        mock_rect.return_value.y = 100
        mock_rect.return_value.width = 50
        mock_rect.return_value.height = 50
        mock_load.return_value = MagicMock()
        self.bonus = Bonus(100, 100)

    def test_initialization(self):
        self.assertEqual(self.bonus.rect.x, 100)
        self.assertEqual(self.bonus.rect.y, 100)
        self.assertEqual(self.bonus.rect.width, 50)
        self.assertEqual(self.bonus.rect.height, 50)
        self.assertEqual(self.bonus.speed, 5)

    def test_move(self):
        initial_y = self.bonus.rect.y
        self.bonus.move()
        self.assertEqual(self.bonus.rect.y, initial_y + self.bonus.speed)


if __name__ == "__main__":
    unittest.main()
