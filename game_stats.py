import json


class GameStats():
    ''' Track statistics for Alien Invasion'''

    def __init__(self, ai_settings):
        ''' Initialise statistics'''
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.level_change = False
        self.high_score = 0
        self.file_name = 'highscore.json'
        self.load_high_score(self.file_name)

    def reset_stats(self):
        ''' Initialise statistics that can change during the game'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self, file):
        ''' Load the high score from a file'''
        try:
            with open(file) as f_obj:
                high_score = json.load(f_obj)
        except FileNotFoundError:
            None
        else:
            self.high_score = high_score
