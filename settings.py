class Settings:
    '''Una clase para guardar toda la configuracion de Alien Invasion'''

    def __init__(self):
        '''Inicializa las configuraciones estáticas del juego'''
        #configuracion de la pantalla
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230,230,230)

        #configuración de la nave.
        #Configuraciones de estadisticas.
        self.ship_limit = 3

        #configuracion de las balas de la nave
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        #Configuraciones del alien
        self.fleet_drop_speed = 100
        #Configuración de las balas alienígenas
        self.alien_bullet_speed = 1.0 #Velocidad de las balas disparadas por los aliens.
        self.alien_fire_chance = 2  # Porcentaje de probabilidad de disparo en cada fotograma.

        #Configuración de los escudos
        self.shield_color = (0,128,0)
        self.shield_width = 60
        self.shield_height = 10


        #Rapidez con la que sehacelera el juego
        self.speedup_scale = 1.1
        #Lo rápido que aumenta el valor en puntos de los aliens
        self.score_scale = 1.5



        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Inicializa las configuraciones que cambian durante el juego.'''
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # fleet_direction de 1 representa derecha; -1 representa izquierda.
        self.fleet_direction = 1

        #Configuración de puntuación
        self.alien_points = 50

    def increase_speed(self):
        '''Incrementa las configuraciones de velocidad y los valores en puntos de los aliens.'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)