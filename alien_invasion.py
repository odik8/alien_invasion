import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien


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
    gf.create_fleet(ai_settings, screen, ship,aliens)

    pygame.display.set_caption("Alien Invasion")

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()
