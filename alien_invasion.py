import sys
from time import sleep
import pygame
import random
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from alien_bullet import AlienBullet
from shield import Shield
from sounds import Sounds


class AlienInvasion:
    '''Clase general para gestionar los recursos y el comportamiento del juego'''

    def __init__(self):
        '''Inicializa el juego y crea recursos'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        #Cargar sonidos.
        self.sound = Sounds()

        #Crea una instancia para guardar las estadisticas del juego.
        #Y crea un marcador.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        # Crear tres escudos en posiciones específicas.
        for i in range(3):
            shield = Shield(self, 200 + i * 200, 500)
            self.shields.add(shield)

        self._create_fleet()
        #Inicia Alien Invasion en estado activo.
        self.game_active = False


        #Crea el boton play.
        self.play_button = Button(self,'Play')



        #Crea el boton play.
        self.play_button = Button(self,'Play')

        # Reproduce la música de introducción en bucle
        self.sound.init_sound.play(-1)

    def run_game(self):
        '''Inicia el bucle principal para el juego'''
        while True:
            self._check_events()
            if self.game_active:
                self.sound.init_sound.set_volume(0) #Se ajusta el sonido para que no se escuche al desaparecer la flota
                self.sound.init_sound.stop() #Se elimina el sonido para que no se siga reproduciendo en silencio
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # responde a pulsaciones de teclas y eventos de raton
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._save_high_score()
                sys.exit()
            #Mover la nave
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        '''Inicia un juego nuevo cuando el jugador hace clic en Play.'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #Reestablece las configuraciones del juego.
            self.settings.initialize_dynamic_settings()
            self._start_game()


    def _start_game(self):
        # Restablece las estadísticas del juego.
        self.stats.reset_stats()
        self.game_active = True
        self.sb._prep_images()

        # Se deshace de los aliens y las balas que quedan.
        self.aliens.empty()
        self.bullets.empty()

        # Crea una nueva flota y centra la nave.
        self._create_fleet()
        self.ship.center_ship()

        # Oculta el cursor del ratón.
        pygame.mouse.set_visible(False)

        # Detiene la música de introducción
        self.sound.init_sound.stop()

    def _check_keydown_events(self,event):
        '''Responde a las pulsaciones de teclas.'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_j:
            if not self.game_active:
                self.settings.initialize_dynamic_settings()
                self._start_game()


    def _check_keyup_events(self,event):
        '''Responde a liberaciones de teclas.'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _save_high_score(self):
        '''Guarda la puntuación mas alta en un archivo.'''
        with open('high_score.txt', 'w') as file:
            file.write(str(self.stats.high_score))

    def _fire_bullet(self):
        '''Crea una bala y la añade al grupo de balas.'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _alien_fire(self):
        '''Hace que un alienígena dispare una bala.'''
        if self.aliens: #Solo si hay alienígenas vivos.
            alien = random.choice(self.aliens.sprites()) #Selecciona al alienígena al azar.
            bullet = AlienBullet(self,alien)
            self.alien_bullets.add(bullet) #Añade la bala al grupo.

    def _update_alien_bullets(self):
        '''Actualiza la posición de las balas alienígenas y comprueba colisiones.'''
        self.alien_bullets.update() #Actualiza todas las balas.

        #Elimina las balas que salen de la pantalla.
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        #Comprueba si alguna bala golpea la nave.
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()

        # Comprueba colisiones entre balas alienígenas y escudos.
        collisions = pygame.sprite.groupcollide(self.alien_bullets, self.shields, True, True)

    def _update_bullets(self):
        '''actualiza la posición de las balas y se deshace de las viejas.'''
        #actualiza las posiciones de las balas.
        self.bullets.update()

        # Se deshace de las balas que han desaparecido.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''Responde a las colisiones bala alien.'''
        #Retira todas las balas y aliens que han chocado.
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        if collisions:
            #Reproduce el sonido para cada alien que es alcanzado
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points + len(self.aliens)
                self.sound.alien_hit_sound.play() # Sonido de colisión
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            self._start_new_level()




    def _start_new_level(self):
        #Destruye las balas existentes y crea una flota nueva.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        #Aumenta el nivel.
        self.stats.level += 1
        self.sb.prep_level()

        self.sound.init_sound.stop()


    def _create_fleet(self):
        '''Crea la flota de alienígenas.'''
        #Crea un alienigena y va añadiendo alienigenas hasta que no haya espacio.
        #El espaciado entre alienigenas es de un alien de ancho y otro de alto.
        self.aliens.empty()
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x,current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width

            #Fila terminada; resetea valor de x e incrementa valor de y.
            current_x = alien_width
            current_y += 2 * alien_height


    def _check_fleet_edges(self):
        '''Responde adecuadamente si algún alien ha llegado a un borde.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Baja toda la flota y cambia su direccion.'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self,x_position,y_position):
        '''Crea un alienigena y lo coloca en la fila.'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        '''Comprueba si la flota esta en un borde, después actualiza las posiciones.'''
        self._check_fleet_edges()
        self.aliens.update()

        #Llama al método para que los aliens disparen aleatoriamente.
        if random.randint(1,10) <= self.settings.alien_fire_chance:
            self._alien_fire()

        #Busca colisiones alien-nave.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #Busca aliens llegando al fondo de la pantalla.
        self._check_aliens_bottom()

    def _ship_hit(self):
        '''Responde al impacto de un alien en la nave.'''
        if self.stats.ships_left > 0:
            #Disminuye ships_left y actualiza el marcador.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Se deshace de los aliens y balas restantes.
            self.aliens.empty()
            self.bullets.empty()

            #Crea una nueva flota y centra la nave.
            self._create_fleet()
            self.ship.center_ship()

            #Pausa.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        '''Comprueba si un alien ha llegado al fondo de la pantalla.'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Trata esto como si la nave hubiese sido alcanzada
                self._ship_hit()
                break

    def _update_screen(self):
        '''Actualiza las imagenes en la pantalla y cambia a la pantalla nueva'''
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #Dibuja la información de la puntuación.
        self.sb.show_score()

        #Dibuja el botón para jugar si el juego está inactivo.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    #Hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    print('ALIEN INVASION')
    ai.run_game()


