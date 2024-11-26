class GameStats:
    '''Sigue las estadisticas de Alien invasion.'''

    def __init__(self,ai_game):
        '''Inicializa las estadisticas.'''
        self.settings = ai_game.settings
        self.reset_stats()

        #La puntuación mas alta no debería restablecerse nunca.
        self.high_score = 0


    def reset_stats(self):
        '''Inicializa las estadísticas que pueden cambiar durante el juego.'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1