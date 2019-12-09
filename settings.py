class Settings():
    '''A class to store all settings'''

    def __init__(self):
        '''Initialize game's settings'''
        # Screen settings
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (70, 70, 70)

        # Ship settings
        self.ship_limit = 3

        # Alien settings
        self.fleet_drop_speed = 5

        # Bullet settings
        self.bullet_height = 10
        self.bullets_allowed = 3

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # Rate at which alien points increase
        self.score_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        ''' Initialise settings that change throughout the game'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.bullet_width = 300
        self.bullet_color = (0, 0, 0)
        self.alien_speed_factor = 1

        # Fleet direction of 1 means right, -1 is left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 10

    def increase_speed(self):
        ''' Increase speed settings'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
