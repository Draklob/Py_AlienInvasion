import pygame

from utils import Utils
from bullet import Bullet
from pygame.sprite import Group
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position
        :type ai_settings: settings.Settings
        """
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_stts = ai_settings

        self.progressive_speed = 1

        self.invulnerable = False
        self.blinking_bool = False

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.offset = ai_settings.player_offset

        self.horizontal = 0
        self.vertical = 0

        self.respawn()

        # Movement Flag
            # Horizontal
        self.moving_right = False
        self.moving_left = False
            # Vertical
        self.moving_up = False
        self.moving_down = False

    def set_progressive_speed(self, add_new_speed):
        self.progressive_speed += add_new_speed

    def update(self):
        """Update the ship's position based on the movement flag"""
        current_speed = self.ai_stts.player_speed * self.progressive_speed

        # Update the ship's center value, not rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.horizontal += current_speed
        elif self.moving_left and self.rect.left > 0:
            self.horizontal -= current_speed

        if self.moving_up and self.rect.top > 0 + self.offset:
            self.vertical -= current_speed
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.vertical += current_speed

        # We pass the pos info to the rect object
        self.rect.centerx = self.horizontal
        self.rect.centery = self.vertical

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def fire_bullet(self, ai_stts, screen, player, bullets ):
        """Fire a bullet if limit not reached yet."""
        if len(bullets) < ai_stts.bullets_allowed:
            # Create a new bullet and add it to the bullets group
            new_bullet = Bullet( ai_stts, screen, player)
            bullets.add(new_bullet)

    def prep_show_lives(self, stats):
        """Show how many lives are left.
        :type stats: game_stats.GameStats
        """
        self.lives = Group()
        for live_number in range( stats.player_lives):
            live = Ship( self.ai_stts, self.screen)
            live.image = pygame.transform.scale(live.image, (30, 24))
            live.rect = live.image.get_rect()
            live.rect.x = 10 + live_number * live.rect.width
            live.rect.y = 10
            self.lives.add(live)

    def show_lives(self):
        """Shows the lives are left."""
        #Draw the ships
        self.lives.draw(self.screen)

    def death(self, stats):
        """

        :type stats: game_stats.GameStats
        """
        if stats.player_lives == 0:
            stats.game_active = False
            stats.game_running = False
            print("Player death, 0 lives!")
            stats.reset_stats()
            return

        self.respawn()
        self.invulnerable = True
        self.prep_show_lives(stats)

    def respawn(self):
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - self.offset
    #    Utils.test_print_STR(self.rect)

        self.horizontal = float(self.rect.centerx)
        self.vertical = float(self.rect.centery)

        self.image.set_alpha(255)

    def blinking(self, timer):
        trigger_timer = 0.2
        idx_timer = 1
        self.image.set_alpha(0)

        if timer > trigger_timer * idx_timer:
            self.blinking_bool = not self.blinking_bool
            idx_timer += 1
            if self.blinking_bool:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)

        if not self.invulnerable:
            self.image.set_alpha(255)