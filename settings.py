class Settings:
    '''A class to store all the settings'''

    def __init__(self):
        '''Initalize games settings'''
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,0,230)
        self.ship_speed = 1
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = .2
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

