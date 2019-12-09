import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
from ship import Ship
import game_functions as gf
from pygame.sprite import Group


def run_game():
    # Initialize game and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button
    play_button = Button(ai_settings, screen, 'Play')

    # Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, stats, screen)

    # Make a ship
    ship = Ship(ai_settings, stats, screen)

    # Make a group to store bullets and aliens
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, stats, screen, sb, play_button, ship,
                        aliens, bullets)

        if stats.game_active:
            ship.update()
            # During level change only ship updates
            if not stats.level_change:
                gf.update_bullets(ai_settings, stats, screen, sb, ship,
                                  aliens, bullets)
                gf.update_aliens(ai_settings, stats, screen, sb, ship,
                                 aliens, bullets)

        gf.update_screen(ai_settings, stats, screen, sb, ship, aliens, bullets,
                         play_button)


run_game()
