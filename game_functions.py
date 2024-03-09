import sys

import pygame

from alien import Alien
from bullet import Bullet


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


def check_keyup_events(event, ship):
    """Reacting to keyup events"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):
    """Handles keystrokes and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Updates images on the screen and displays a new screen."""

    # Each time the loop passes, the screen is redrawn.
    screen.fill(ai_settings.bg_color)

    # All bullets are displayed behind images of the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Displays the last drawn screen.
    pygame.display.flip()


def update_bullets(bullets):
    """Updates bullet position and destroys old bullets"""
    # Updating position
    bullets.update()

    # Destroying
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


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
