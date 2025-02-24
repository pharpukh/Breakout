import pygame
from settings import *

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(window_width // 2 - paddle_width // 2, window_height - paddle_height - 10, paddle_width, paddle_height)
        self.image = pygame.image.load(customization["paddle"])
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, window_width - self.rect.width)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def resize(self, new_width):
        self.rect.width = new_width
        self.image = pygame.image.load(customization["paddle"])
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
