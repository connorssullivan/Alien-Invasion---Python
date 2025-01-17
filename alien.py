import pygame
from pygame.sprite import Sprite 

class Alien(Sprite):
    '''A class to represent an enemy alien'''

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien ship
        original_image = pygame.image.load("assets/images/alien.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.image.get_rect()

        # Load each new alien at the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the aliens exact horizontal position
        self.x = float(self.rect.x)

        self.settings = ai_game.settings

    def update(self):
        """Move the alien to the right."""
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''Return true if alien is at edge'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    