import sys

import pygame

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


def update_screen(ai_settings, screen, ship, bullets):
    """Updates images on the screen and displays a new screen."""

    # Each time the loop passes, the screen is redrawn.
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # All bullets are displayed behind images of the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

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
