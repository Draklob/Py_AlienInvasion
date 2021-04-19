import sys
import time
import pygame as pg
from alien import Alien


def save_score(stats):
    """
    Save the high score before closing the game.
    :type stats: game_stats.GameStats
    """
    with open("score.txt", 'w') as file_obj:
        file_obj.write(str(stats.high_score))

def load_score(stats):
    """
    Load the high score before starting the game.
    :param stats:
    :return:
    """
    try:
        with open('score.txt') as file_obj:
            high_score = file_obj.read()
            stats.high_score = int(high_score)
    except FileNotFoundError:
        msg = "Sorry, the file not exist!"
        print(msg)

def close_game(stats):
    save_score(stats)
    print("Closing game...")
    sys.exit()

def switch_mouse_cursor():
    state_mouse_cursor = pg.mouse.get_visible()
    print(str(state_mouse_cursor))
    pg.mouse.set_visible(not state_mouse_cursor)

def init_game(ai_stts, stats, sb, screen, player, aliens, bullets):
    """
    First run of the game, we set every value.
    :type sb: scoreboard.Scoreboard
    :type stats: game_stats.GameStats
    :type ai_stts: settings.Settings
    """
    stats.game_active = True
    stats.game_running = True
    # Empty the list of aliens ad bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_stts, screen, player, aliens)

    player.respawn()

    # Hiding cursor
    switch_mouse_cursor()

    # Reset the game settings in case they were increased
    ai_stts.initialize_dynamic_settings()
    sb.prep_score()
    sb.prep_level()
    sb.prep_high_score()
    player.prep_show_lives(stats)

def check_play_button(ai_stts, stats, sb, screen, player, aliens, bullets, play_button, mouse_x, mouse_y):
    """Start a new game when the player clicks Play.
    :type stats: game_stats.GameStats
    :type ai_stts: settings.Settings
    :type play_button: button.Button
    :type player: ship.Ship
    """
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        init_game( ai_stts, stats, sb, screen, player, aliens, bullets)

def check_pause_button(stats, pause_button, mouse_x, mouse_y):
    """Start a new game when the player clicks Play.
    :type ai_stts: settings.Settings
    :type play_button: button.Button
    :type player: ship.Ship
    """
    if pause_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True
        switch_mouse_cursor()

def check_events(ai_stts, stats, sb, screen, play_button, pause_button, player, bullets, aliens):
    """Respond to keypresses and mouse events."""

    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            close_game(stats)
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(ai_stts, stats, sb, screen, player, aliens, bullets, play_button, mouse_x, mouse_y)
            check_pause_button(stats, pause_button, mouse_x, mouse_y)
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event, ai_stts, stats, sb, screen, player, aliens, bullets)
        elif event.type == pg.KEYUP:
            check_keyup_events(event, player)


def pause_game(stats):
    switch = stats.game_active
    stats.game_active = not switch
    switch_mouse_cursor()

def check_keydown_events(event, ai_stts, stats, sb, screen, player, aliens, bullets):
    """Responds to keypresses
    :type stats: game_stats.GameStats
    """
    if event.key == pg.K_q:
        close_game(stats)
    elif event.key == pg.K_p:
        if not stats.game_active and not stats.game_running:
            init_game( ai_stts, stats, sb, screen, player, aliens, bullets)
        elif stats.game_running:
            pause_game(stats)

    elif event.key == pg.K_RIGHT:
        # Move the ship to the right
        player.moving_right = True
    elif event.key == pg.K_LEFT:
        # Move the ship to the left
        player.moving_left = True
    elif event.key == pg.K_SPACE:
        player.fire_bullet(ai_stts, screen, player, bullets)

    if event.key == pg.K_UP:
        # Move the ship to the right
        player.moving_up = True
    elif event.key == pg.K_DOWN:
        # Move the ship to the left
        player.moving_down = True


def check_keyup_events(event, player):
    """Responds to key releases."""
    if event.key == pg.K_RIGHT:
        # Stop moving right
        player.moving_right = False
    elif event.key == pg.K_LEFT:
        player.moving_left = False

    if event.key == pg.K_UP:
        # Move the ship to the right
        player.moving_up = False
    elif event.key == pg.K_DOWN:
        # Move the ship to the left
        player.moving_down = False


def update_screen(ai_stts, stats, sb, screen, player, aliens, bullets, play_button, pause_button):
    """Update images on the screen adn flip to the new screen.
    :type player: ship.Ship
    :type sb: scoreboard.Scoreboard
    :type stats: game_stats.GameStats
    :type pause_button: button.Button
    :type play_button: button.Button
    """
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_stts.bg_color)
    # screen.blit(ai_stts.img_background, (0, 0))

    if stats.game_active:

        player.blitme()
        aliens.draw(screen)

        for bullet in bullets:
            bullet.draw_bullet()

    # Draw the play or pause buttons according to the state of the game.
    if not stats.game_active:       # GAME PAUSED
        if stats.game_running:      # GAME IF IT WAS ALREADY STARTED AND IT'S PAUSED
            pause_button.draw_button()
            sb.show_score()
            player.show_lives()
        elif not stats.game_running:    # GAME DONT STARTED YET
            play_button.draw_button()

    if stats.game_active:
        sb.show_score()
        player.show_lives()

    pg.display.flip()  # Make the most recently drawn screen visible


def update_bullets(ai_stts, stats, sb, screen, player, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets)) ## Takes more time to write output to the terminal than it does to draw graphics

    check_bullet_alien_collision(ai_stts, stats, sb, screen, player, aliens, bullets)


def check_bullet_alien_collision(ai_stts, stats, sb, screen, player, aliens, bullets):
    """Respond to bullet-alien collisions.
    :type sb: scoreboard.Scoreboard
    :type stats: game_stats.GameStats
    :type ai_stts: settings.Settings
    :type player: ship.Ship
    """
    # Remove any bullets and aliens that have collided
    # Check for any bullets that have hit aliens
    # If so, get rid of the bullet and the alien.

    collisions = pg.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_stts.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets and create a new fleet.
        bullets.empty()
        create_fleet(ai_stts, screen, player, aliens)
        #player.set_progressive_speed( 0.3)
        ai_stts.increase_speed()
        # Increase the level
        stats.level += 1
        sb.prep_level()


def get_number_aliens_x(ai_stts, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_stts.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_stts, player_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_stts.screen_height - (3 * alien_height) - player_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_stts, screen, aliens, alien_idx, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_stts, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_idx
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_stts, screen, player, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width
    alien = Alien(ai_stts, screen)
    number_aliens_x = get_number_aliens_x(ai_stts, alien.rect.width)
    number_rows = get_number_rows(ai_stts, player.rect.height, alien.rect.height)

    # FOR TESTING
    number_aliens_x = 3
    number_rows = 2

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_idx in range(number_aliens_x):
            # Create an alien and place it in the row
            create_alien(ai_stts, screen, aliens, alien_idx, row_number)


def update_aliens(ai_stts, stats, screen, player, aliens):
    """Update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_stts, aliens)
    aliens.update()

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(stats, screen, player, aliens)

    if not player.invulnerable:
        check_player_alien_collisions(stats, player, aliens)


def check_player_alien_collisions(stats, player, aliens):
    """Checking if player collisions with any enemy."""
    collision = pg.sprite.spritecollide(player, aliens, True)
    # collision = pg.sprite.spritecollideany(player, aliens) # Using this one, dont destroy the enemy when it collides
    if collision:
        player_being_hit(stats, player)


def player_being_hit(stats, player):
    """
    What happen when player gets hit.
    :type player: ship.Ship
    :type stats: game_stats.GameStats
    """
    if stats.player_lives > 0:
        print("Player got hit")
        stats.player_lives -= 1
        player.death(stats)


        # We could reset everything, I mean, reset bullets and enemies
        # aliens.empty()
        # bullets.empty()
        # Create a new fleet and center the ship
        # create_fleet( ai_sts, screen, player, aliens)


def check_aliens_bottom(stats, screen, player, aliens, ):
    """Check if any aliens have reached the bottom of the screen.
    :type player: ship.Ship
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            stats.player_lives -= 1
            aliens.empty()
            player.death(stats)
            player.prep_show_lives(stats)
            break


def check_fleet_edges(ai_stts, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_stts, aliens)
            break


def change_fleet_direction(ai_stts, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_stts.fleet_drop_speed
    ai_stts.fleet_direction *= -1

def check_high_score(stats, sb):
    """
    Check to see if there's a new score.
    :type sb: scoreboard.Scoreboard
    :type stats: game_stats.GameStats
    """

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()