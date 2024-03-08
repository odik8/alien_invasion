import sys

import pygame


def check_keydown_events(event, ship):
    """Reacting to keydown events"""
    if event.key == pygame.K_RIGHT:
        # Move ship to right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move ship to left
        ship.moving_left = True


def check_keyup_events(event, ship):
    """Reacting to keyup events"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ship):
    """Handles keystrokes and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship):
    """Updates images on the screen and displays a new screen."""
    # Each time the loop passes, the screen is redrawn.
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # Displays the last drawn screen.
    pygame.display.flip()
