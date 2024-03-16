import sys

import pygame

from alien import Alien
from bullet import Bullet
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Reacting to keydown events"""
    if event.key == pygame.K_RIGHT:
        # Move ship to right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move ship to left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_play_button(ai_settings, screen, stats, play_button, ship,
                      aliens, bullet, mouse_x, mouse_y):
    """launch the game with press "Play" button"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.reset_stats()
        stats.game_active = True

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keyup_events(event, ship):
    """Reacting to keyup events"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Handles keystrokes and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, ship, aliens, bullets,
                  play_button):
    """Updates images on the screen and displays a new screen."""

    # Each time the loop passes, the screen is redrawn.
    screen.fill(ai_settings.bg_color)

    # All bullets are displayed behind images of the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()
    # Displays the last drawn screen.
    pygame.display.flip()

    # The Play button is displayed when the game is inactive.


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Updates bullet position and destroys old bullets"""
    # Updating position
    bullets.update()

    # Destroying
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_collisions(ai_settings, screen, ship, aliens, bullets):
    """Collision Handling"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # Destroys bullets b creates new fleet
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fires a bullet if the maximum has not yet been reached."""
    # Create a new bullet and add it in the bullets group
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_alien_x(ai_settings, alien_width):
    """calculating the number of aliens in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Creating alien in a row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = (alien.rect.height + 2
                    * alien.rect.height * row_number)
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creates alien fleet"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens,
                         alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количство рядов, помещающихся на экране"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_row = int(available_space_y / (2 * alien_height))
    return number_row


def check_fleet_edges(ai_settings, aliens):
    """Reacts to alien edge touch"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Lowers the fleet and change the direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Updates all aliens position"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # "Ship-Alien" collision check
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Handles a collision between a ship and an alien."""
    # Decreasing ships_left
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # Aliens and bullets lists clearing
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Checks if aliens have reached the bottom edge of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
