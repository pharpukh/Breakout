# projectile.py
import pygame
from settings import *

class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, projectile_width, projectile_height)
        self.image = pygame.image.load(customization["projectile"])
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.speed = projectile_speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)