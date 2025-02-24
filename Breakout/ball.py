import pygame
import numpy as np
from settings import *

class Ball:
    def __init__(self, speed, radius=ball_radius, image_path=None):
        self.radius = radius
        self.rect = pygame.Rect(window_width // 2 - radius, window_height // 2 - radius, radius * 2, radius * 2)
        if isinstance(speed, list):
            self.speed = np.array(speed)
        else:
            self.speed = np.array([speed, -speed])  # Начальная скорость мяча

        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        else:
            self.image = None

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.left <= 0 or self.rect.right >= window_width:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.ellipse(surface, self.color, self.rect)
