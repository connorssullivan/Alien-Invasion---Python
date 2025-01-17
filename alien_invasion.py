import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button

class AlienInvasion:
    '''Class to manage game and asset behavior'''

    def __init__(self):
        '''Initalize game and resources'''
        pygame.init()
        self.settings = Settings()

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Set the screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Sets game to full screen
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Create alien group
        self.aliens = pygame.sprite.Group()
        self._create_fleat()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    
    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                #print(len(self.bullets))
                self._update_aliens()
            self._update_screen()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        '''Respond if aliens reach end'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleat(self):
        '''Create an alien fleet'''
        # Make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine num of rows can fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # Create full flete
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create aliens
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        '''Update the screen and flip to new screen'''
        # Redraw the screen during each pass
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Display Alien
        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        #Make moset recenty drawn scen visible
        pygame.display.flip()

    def _check_events(self):
        '''Respond to keypress'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Check for key presse
            if event.type == pygame.KEYDOWN:
                self.check_keydown(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True
            
    def check_keydown(self, event):
        '''Executes movement for keydown'''
        # Move to the right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # Move the ship Left
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Quit the game
        if event.key == pygame.K_q:
            sys.exit()
        # If fire bullet
        if event.key == pygame.K_SPACE:
            self.fire_bullet()
    
    def fire_bullet(self):
        '''Create bullet and add it to the group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
        

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        
        if not self.aliens:
            # Destroy existing bullets and create fleet
            self.bullets.empty()
            self._create_fleat()

    def check_keyup(self, event):
        '''Executes movement for keyup'''
        # Move to the right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        # Move the ship Left
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False


                
                


'''Main function'''
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()