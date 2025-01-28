import pygame

class Ship:
    '''A class to manage the ship'''

    def __init__(self, ai_game):
        '''Initalize the ship and set the starting position'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship
        original_image = pygame.image.load("assets/images/nasa_ship.png").convert_alpha()
        self.sprite_image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.sprite_image.get_rect()
        

        # Start new ship at botom of screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Mobement Flags
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        '''Draw Ship and current location'''
        self.screen.blit(self.sprite_image,self.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)

    def update(self):
        '''Update ships position based off the movement'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Update rect object
        self.rect.x = self.x
    
    def center_ship(self):
        pass
        