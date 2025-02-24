# brick.py
import pygame
from settings import *

class Brick:
    def __init__(self, x, y, strength, image_paths=None):
        # Limit the strength value within acceptable boundaries
        strength = max(0, min(strength, 4))
        # Create the brick rectangle
        self.rect = pygame.Rect(x, y, brick_width, brick_height)
        self.strength = strength  # The strength level of the brick
        self.color = brick_colors[self.strength]  # The color of the brick based on its strength

        self.images = []
        if image_paths:
            for path in image_paths:
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (brick_width, brick_height))
                self.images.append(image)
            self.image = self.images[self.strength]
        else:
            self.image = None

    def draw(self, surface):
        # Draw the brick on the screen
        if self.image:
            surface.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

    def hit(self):
        # Handle the brick being hit
        self.strength -= 1
        if self.strength >= 0:
            if self.images:
                self.image = self.images[self.strength]  # Update the brick image
            else:
                self.color = brick_colors[self.strength]  # Update the brick color
        return self.strength < 0  # Returns True if the brick is destroyed