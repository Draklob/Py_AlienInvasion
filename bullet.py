import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai_stts, screen, player):
        """Create a bullet obj at the ship's current position"""
        super().__init__()  # To inherit properly from Sprite
        self.screen = screen

        # Create a bullect rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_stts.bullet_width, ai_stts.bullet_height)
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y - ai_stts.player_offset)

        self.color = ai_stts.bullet_color
        self.speed = ai_stts.bullet_speed

    def update(self):
        """Move the bullet to the screen"""
        # Update the decimal position of the bullet
        self.y -= self.speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect( self.screen, self.color, self.rect)