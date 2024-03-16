import pygame
from pygame.sprite import Group

from button import Button
from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from game_stats import GameStats


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )

    ship = Ship(ai_settings, screen)
    bullets = Group()
    # alien = Alien(ai_settings, screen)
    aliens = Group()

    # Creating alien fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    pygame.display.set_caption("Alien Invasion")

    play_button = Button(ai_settings, screen, "Play")

    stats = GameStats(ai_settings)

    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen,
                             ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets,
                         play_button)


if __name__ == "__main__":
    run_game()
