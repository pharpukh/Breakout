# bonus.py
import pygame
from settings import *

class Bonus:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, bonus_width, bonus_height)
        self.image = pygame.image.load(customization["bonus"])
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.speed = bonus_speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
