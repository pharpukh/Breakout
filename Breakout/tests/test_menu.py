import unittest
from unittest.mock import patch, MagicMock, mock_open
import pygame
from menu import Menu


class TestMenu(unittest.TestCase):
    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.font.Font')
    @patch('pygame.image.load')
    @patch('pygame.mixer.Sound')
    @patch('pygame.mixer.music.load')
    @patch('Menu.load_levels_data')
    def setUp(self, mock_load_levels_data, mock_music_load, mock_sound, mock_image_load,
              mock_font, mock_display_set_mode, mock_init):
        self.menu = Menu()

    def test_init(self):
        self.assertIsInstance(self.menu.display_surface, pygame.Surface)
        self.assertIsInstance(self.menu.clock, pygame.time.Clock)
        self.assertIsInstance(self.menu.title_font, MagicMock)
        self.assertIsInstance(self.menu.font, MagicMock)
        self.assertEqual(self.menu.selected_level, None)
        self.assertIsInstance(self.menu.levels_data, dict)
        self.assertIsInstance(self.menu.menu_background, MagicMock)
        self.assertTrue(pygame.mixer.music.load.called)

    def test_create_level_buttons(self):
        buttons = self.menu.create_level_buttons()
        self.assertEqual(len(buttons), 5)
        for button, level in buttons:
            self.assertIsInstance(button, pygame.Rect)
            self.assertIsInstance(level, str)

    def test_load_levels_data(self):
        with patch('builtins.open', mock_open(read_data='{"1": {"best_time": 50.0, "unlocked": true}}')):
            data = self.menu.load_levels_data()
            self.assertEqual(data, {"1": {"best_time": 50.0, "unlocked": True}})

    @patch('Menu.save_levels_data')
    @patch('pygame.mixer.music.load')
    def test_start_game_loop(self):
        mock_game = MagicMock()
        mock_game.victory = True
        mock_game.best_time = 40.0
        self.menu.save_levels_data = MagicMock()
        self.menu.start_game_loop("1", {})
        self.assertTrue(self.menu.save_levels_data.called)
        self.assertEqual(self.menu.levels_data["1"]["best_time"], 40.0)
        self.assertTrue(self.menu.levels_data["2"]["unlocked"])


if __name__ == '__main__':
    unittest.main()
