class GameStats:
    '''Sigue las estadisticas de Alien invasion.'''

    def __init__(self,ai_game):
        '''Inicializa las estadisticas.'''
        self.settings = ai_game.settings
        self.reset_stats()

        #La puntuación mas alta no debería restablecerse nunca.
        self.high_score = self._load_high_score()


    def reset_stats(self):
        '''Inicializa las estadísticas que pueden cambiar durante el juego.'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _load_high_score(self):
        '''Carga la puntuación mas alta desde un archivo.'''
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0










