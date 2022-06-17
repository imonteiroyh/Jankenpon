class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.game_ready = False
        self.player1_went = False
        self.player2_went = False
        self.players_moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def connected(self):
        return self.game_ready

    def get_players_moves(self, player):
        return self.players_moves[player]

    def player_played(self, player, move):
        self.players_moves[player] = move
        if player == 0:
            self.player1_went = True
        else:
            self.player2_went = True

    def both_players_went(self):
        return self.player1_went and self.player2_went

    def winner_player(self):
        # Atribuindo a cada jogador seu movimento
        player1 = self.players_moves[0].upper()[0]
        player2 = self.players_moves[1].upper()[0]

        """
        Verificando o ganhador
        Rock (R)
        Paper (P)
        Scissors (S)
        """
        winner_player = -1
        if player1 == 'R' and player2 == 'P':
            winner_player = 1
        elif player1 == 'R' and player2 == 'S':
            winner_player = 0
        elif player1 == 'P' and player2 == 'R':
            winner_player = 0
        elif player1 == 'P' and player2 == 'S':
            winner_player = 1
        elif player1 == 'S' and player2 == 'R':
            winner_player = 1
        elif player1 == 'S' and player2 == 'P':
            winner_player = 0
        return winner_player

    def reset_went(self):
        self.player1_went = False
        self.player2_went = False
