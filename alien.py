import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Alien"""

    def __init__(self, ai_settings, screen):
        """Inits alien and his position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Uploading image and rect appointment
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Each new alien spawns in the top-left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Saving the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Displays alien at his current position"""
        self.screen.blit(self.image, self.rect)
