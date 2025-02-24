import unittest
from menu import Menu

class TestMenu(unittest.TestCase):
    def test_menu_run(self):
        menu = Menu()  # Create a Menu instance
        with self.assertRaises(SystemExit):  # Check if the run method exits the system
            menu.run()

if __name__ == "__main__":
    unittest.main()
