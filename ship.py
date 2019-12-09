import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, stats, screen):
        ''' Initialize the ship and sets its starting position.'''
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats

        # Load the ship image.
        self.image = pygame.image.load('images/ship.bmp')
        # Ship's rect
        self.rect = self.image.get_rect()
        # Screen's rect
        self.screen_rect = screen.get_rect()

        # Start each ship at bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        # self.level_clear = False

    def update(self):
        ''' Update the ship's position based on the movement flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        if self.moving_up and self.rect.top > 0:
            self.bottom -= self.ai_settings.ship_speed_factor

        if self.moving_down and self.rect.bottom < self.ai_settings.screen_height:
            self.bottom += self.ai_settings.ship_speed_factor

        if self.stats.level_change and self.rect.bottom >= 0:
            self.bottom -= 0.3

        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def center_ship(self):
        ''' Center the ship on the screen'''
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom

    def blitme(self):
        ''' Draw the ship at it's current location'''
        self.screen.blit(self.image, self.rect)
