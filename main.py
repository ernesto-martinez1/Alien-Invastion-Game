import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
import math

class AlienInvasion:
    def __init__(self):
        # init the game and game resources

        pygame.init()
        self.settings = Settings()
        self.settings.load_background("space.jpeg")
        # Screen Settings
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Ernesto's Alien Invasion")
        self.scroll = 0
        self.titles = math.ceil(self.settings.screen_width / self.settings.bg.get_width()) + 1
       # self.bg_color = (50,230,230)
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()
    
    def run_game(self):
        while True:
            self._check_events()
            self.clock.tick(self.settings.fps) 
            if self.stats.game_active:    
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
    
    def scroll_background(self):
        i = 0
        while i < self.titles:
            self.screen.blit(self.settings.bg, (self.settings.bg.get_width() * i + self.scroll, 0))
            i += 1
        self.scroll -= 6
        if abs(self.scroll) > self.settings.bg.get_width():
            self.scroll = 0
    
    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
             sys.exit()
        elif event.key == pygame.K_SPACE:
             self._fire_bullet()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False


    def _fire_bullet(self):
         if len(self.bullets) < self.settings.bullets_allowed:
              new_bullet = Bullet(self)
              self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        self.bullets.update()
        
        for bullet in self.bullets.copy():
         if bullet.rect.bottom <= 0:
              self.bullets.remove(bullet)
        self._check_bullet_collision_area()

    def _check_bullet_collision_area(self):
         collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
         if not self.aliens:
              self.bullets.empty()
              self._create_fleet()

    def _update_aliens(self):
         self._check_fleet_edges()
         self.aliens.update()
         self._check_aliens_bottom()
    
    def _create_fleet(self):
         #Make a single alien
         aliens = Alien(self)
         alien_width, alien_height = aliens.rect.size
         #Determine how much space you have on the screen for aliens
         available_space_x = self.settings.screen_width - (2*alien_width)
         number_aliens_x = available_space_x // (2 * alien_width)
        
        #Determine the number of rows of aliens that fit on the screen
         ship_height = self.ship.rect.height
         available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
         number_rows = available_space_y // (2 * alien_height)
        #Create the full fleet of aliens
         for row_number in range (number_rows):
              for alien_number in range(number_aliens_x):
                   self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
         aliens = Alien(self)
         alien_width, alien_height = aliens.rect.size
         alien_width = aliens.rect.width
         aliens.x = alien_width + 2 * alien_width * alien_number
         aliens.rect.x = aliens.x
         aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
         self.aliens.add(aliens)

    def _check_fleet_edges(self):
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
              
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
              self.stats.ships_left -= 1
              self.aliens.empty()
              self.bullets.empty()
              self._create_fleet()
              self.ship.center_ship()
              sleep(0.5)
        else:
             self.stats.game_active = False
        
    def _check_aliens_bottom(self):
         screen_rect = self.screen.get_rect()
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= screen_rect.bottom:
                   self._ship_hit()
                   break
             

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
             bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

quit()