import pygame
from network import Network
from game import Game

WIDTH = 700
HEIGHT = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.font.init()
pygame.display.set_caption('Dots and Boxes')
window = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('comicsans', 25)

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 150

    def draw_button(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        text = font.render(self.text, True, WHITE)
        window.blit(text, (self.x + round((self.width - text.get_width())/2), (self.y + round(self.height - text.get_height())/2)))

    def button_clicked(self, mouse_position):
        mouse_position_x = mouse_position[0]
        mouse_position_y = mouse_position[1]

        if (self.x <= mouse_position_x <= self.x + self.width) and (self.y <= mouse_position_y <= self.y + self.height):
            return True
        else:
            return False

def redraw_window(window, game, player):
    window.fill(WHITE)

    if not game.connected():
        text = font.render('Esperando outro jogador', True, BLUE, True)
        window.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))
    else:
        text = font.render('Sua jogada', True, RED)
        window.blit(text, (80, 200))

        text = font.render('Oponente', True, RED)
        window.blit(text, (380, 200))

        player1_move = game.get_players_moves(0)
        player2_move = game.get_players_moves(1)

        if game.both_players_went():
            left_text = font.render(player1_move, 1, BLACK)
            right_text = font.render(player2_move, 2, BLACK)
        else:
            if player == 0 and game.player1_went == True:
                left_text = font.render(player1_move, 1, BLACK)
            elif game.player1_went == True:
                left_text = font.render('Movimento escolhido', 1, BLACK)
            else:
                left_text = font.render('Esperando', 1, BLACK)

            if player == 1 and game.player2_went == True:
                right_text = font.render(player2_move, 1, BLACK)
            elif game.player2_went == True:
                right_text = font.render('Movimento escolhido', 1, BLACK)
            else:
                right_text = font.render('Esperando', 1, BLACK)
            
            if player == 0:
                window.blit(left_text, (100, 350))
                window.blit(right_text, (400, 350))
            else:
                window.blit(right_text, (100, 350))
                window.blit(right_text, (400, 350))

            for button in buttons:
                button.draw_button(window)

    pygame.display.update()

buttons = [
    Button('Rock', 50, 500, RED), 
    Button('Paper', 250, 500, BLUE),
    Button('Scissors', 450, 500, GREEN)
]

def main():
    run = True

    network = Network()
    player = int(network.get_player())
    print('Você é o jogador ', player)
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(70)
        try:
            game = network.send('get_another_player')
        except:
            run = False
            print('Não foi possível conseguir um jogo')
            break

        if game.both_players_went():
            redraw_window(window, game, player)
            pygame.time.delay(500)
            try:
                game = network.send('reset_game')
            except:
                run = False
                print('Não foi possível conseguir um jogo')
                break
                
            if (game.winner_player == 0 and player == 0) or (game.winner_player == 1 and player == 1):
                text = font.render('Você venceu', True, GREEN)
            elif game.winner_player == -1:
                text = font.render('Empate', True, BLUE)
            else:
                text = font.render('Você perdeu', True, RED)

            window.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
            
                for button in buttons:
                    if button.button_clicked(mouse_position) and game.connected:
                        if player == 0:
                            if not game.player1_went:
                                network.send(button.text)
                        else:
                            if not game.player2_went:
                                network.send(button.text)
        
        redraw_window(window, game, player)
"""
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(70)
        window.fill(BLACK)
        text = font.render('Clique para jogar', True, BLUE)
        window.blit(text, (100, 200))
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
"""
main()