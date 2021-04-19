import pygame as pg

from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Initialize game and create a screen object.
    pg.init()  # Init background settings that pygame needs to work properly
    ai_stts = Settings()

    screen = pg.display.set_mode((ai_stts.screen_width, ai_stts.screen_height))  # Create the display window
    pg.display.set_caption("Alien Invasion")

    # Create an instance of GameStats to store game statistics
    stats = GameStats(ai_stts)
    gf.load_score(stats)

    # Create an instance of Scoreboard to create a scoreboard
    sb = Scoreboard( ai_stts, screen, stats)
    # self.rect.center = self.screen_rect.center
    # self.rect.centerx = self.screen_rect.width / 2
    # self.rect.centery += self.screen_rect.height / 4

    screen_rect = screen.get_rect()

    # Make the Play button.
    play_button = Button(ai_stts, screen, "Play", screen_rect.width / 2, screen_rect.height / 2 + screen_rect.height / 4)
    pause_button = Button(ai_stts, screen, "Pause", screen_rect.width / 2, screen_rect.height / 2 + screen_rect.height / 4 + play_button.rect.height * 2)

    # Player's instance
    player = Ship(ai_stts, screen)

    # Make aliens
    aliens = Group()

    # Make a group to store bullets in
    bullets = Group()

    #start_timer = 0  # starter timer for countdown

    # Start the main loop for the game.
    while 1:
        gf.check_events(ai_stts, stats, sb, screen, play_button, pause_button, player, bullets, aliens)

        if stats.game_active:
            if player.invulnerable:
                if not ai_stts.countdown_running:
                    start_timer = pg.time.get_ticks()
                    ai_stts.countdown_running = True
                elif ai_stts.countdown_running:
                    countdown_timer = (pg.time.get_ticks() - start_timer) / 1000
                    player.blinking(countdown_timer)

                    if countdown_timer > ai_stts.invulnerable_time:
                        player.invulnerable = False
                        ai_stts.countdown_running = False
                        player.blinking(countdown_timer)
                        print("Jugador vuelve a ser vulnerable")

            player.update()
            gf.update_bullets(ai_stts, stats, sb, screen, player, aliens, bullets)
            gf.update_aliens(ai_stts, stats, screen, player, aliens)
        gf.update_screen(ai_stts, stats, sb, screen, player, aliens, bullets, play_button, pause_button)

run_game()
