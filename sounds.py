import pygame

class Sounds:
    def __init__(self):
        self.alien_hit_sound = pygame.mixer.Sound('sounds/alien_hit.mp3.mp3')
        self.new_fleet_sound = pygame.mixer.Sound('sounds/nueva_flota.mp3')
        self.init_sound = pygame.mixer.Sound('sounds/inicial.mp3')
        self.end_game = pygame.mixer.Sound('sounds/game-over-classic-206486.mp3')

        self.bandera_inicio_musica = True
        self.first_fleet_created = False