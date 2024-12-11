import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    '''Clase para gestionar las balas disparadas por los alienígenas.'''
    def __init__(self,ai_game,alien):
        '''Inicializa una bala alienígena en la posición del alien.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255,0,0)

        #Crea el rectangulo de la bala en la posicíon del alien.
        self.rect = pygame.Rect(0,0,3,15)
        self.rect.midtop = alien.rect.midbottom

        #Guarda la posición como un valor flotante.
        self.y = float(self.rect.y)

    def update(self):
        '''Mueve la bala hacia abajo.'''
        self.y += self.settings.alien_bullet_speed #Incrementa la posición en y
        self.rect.y = self.y #Actualiza el rectángulo con la nueva posición.

    def draw_bullet(self):
        '''Dibuja la bala en la pantalla.'''
        pygame.draw.rect(self.screen,self.color,self.rect)
