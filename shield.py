import pygame
from pygame.sprite import Sprite

class Shield(Sprite):
    '''Clase que representa un escudo destructible.'''
    def __init__(self,ai_game,x,y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Crear el rectángulo del escudo.
        self.rect = pygame.Rect(0, 0, self.settings.shield_width, self.settings.shield_height)
        self.rect.x = x
        self.rect.y = y

        self.color = self.settings.shield_color  # Color del escudo.


    def draw_shield(self):
        '''Dibuja el escudo en la pantalla.'''
        pygame.draw.rect(self.screen,self.color,self.rect)