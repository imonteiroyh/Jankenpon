import pygame
from network import Network
from game import Game
import pdb

WIDTH = 700
HEIGHT = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (202, 0, 42)
GREEN = (0, 82, 33)
BLUE = (6, 77, 135)

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption('Jankenpon')
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.music.load('Undertale - Asgore.mp3')
rock_image = pygame.image.load('images/rock.png')
paper_image = pygame.image.load('images/paper.png')
scissors_image = pygame.image.load('images/scissors.png')
background_image = pygame.image.load('images/background.png')

rps_dictionary = {
    "Rock" : "Pedra",
    "Paper" : "Papel",
    "Scissors" : "Tesoura"
}

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 162
        self.height = 162

    def draw_button(self, display_surface):
        pygame.draw.rect(display_surface, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('timesnewroman', 30)
        text = font.render(self.text, True, WHITE)
        display_surface.blit(text, (self.x + round((self.width - text.get_width())/2), (self.y + round(self.height - text.get_height())/2)))

    def button_clicked(self, mouse_position):
        mouse_position_x = mouse_position[0]
        mouse_position_y = mouse_position[1]

        if (self.x <= mouse_position_x <= self.x + self.width) and (self.y <= mouse_position_y <= self.y + self.height):
            return True
        else:
            return False

def write_music_copyright():
    font = pygame.font.SysFont('timesnewroman', 27)
    music_copyright = font.render('Tema de Asgore Dreemmur por Toby Fox', True, BLACK)
    music_cover = font.render('Cover acústico por Lenich & Kirya', True, BLACK)
    display_surface.blit(music_copyright, ((WIDTH - (music_copyright.get_width() + 20)), (HEIGHT - (music_cover.get_height() + 20) - music_copyright.get_height())))
    display_surface.blit(music_cover, ((WIDTH - (music_cover.get_width() + 20)), (HEIGHT - (music_cover.get_height() + 20))))

def write_title():
    font = pygame.font.SysFont('timesnewroman', 77)
    title = font.render('Jankenpon', True, BLACK)
    display_surface.blit(title, ((WIDTH - title.get_width())/2, 30))

def load_images():
    display_surface.blit(rock_image, (75, 450))
    display_surface.blit(paper_image, (275, 450))
    display_surface.blit(scissors_image, (475, 450))

def redraw_display_surface(display_surface, game, player):
    display_surface.fill(WHITE)
    write_title()
    write_music_copyright()
    font = pygame.font.SysFont('timesnewroman', 30)

    if not game.connected():
        font = pygame.font.SysFont('timesnewroman', 50)
        text = font.render('Esperando outro jogador...', True, BLACK)
        display_surface.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))
    else:
        text = font.render('Jogador', True, RED)
        display_surface.blit(text, (75, 200))

        text = font.render('Oponente', True, RED)
        display_surface.blit(text, (515, 200))

        text1 = font.render('Vitórias: ' + str(game.get_wins(0)), True, BLACK)
        text2 = font.render('Vitórias: ' + str(game.get_wins(1)), True, BLACK)
        text3 = font.render('Empates: ' + str(game.get_ties()), True, BLACK)
        if player == 0:
            display_surface.blit(text1, (75, 250))
            display_surface.blit(text2, (515, 250))
        else:
            display_surface.blit(text2, (75, 250))
            display_surface.blit(text1, (525, 250))
        display_surface.blit(text3, (295, 250))

        player1_move = game.get_players_moves(0)
        player2_move = game.get_players_moves(1)

        font = pygame.font.SysFont('timesnewroman', 30)
        if game.both_players_went():
            text1 = font.render(rps_dictionary[player1_move], 1, BLACK)
            text2 = font.render(rps_dictionary[player2_move], 2, BLACK)
        else:
            if player == 0 and game.player1_went == True:
                text1 = font.render(rps_dictionary[player1_move], 1, BLACK)
            elif game.player1_went == True:
                text1 = font.render('Escolheu!', 1, BLACK)
            else:
                text1 = font.render('Escolhendo...', 1, BLACK)

            if player == 1 and game.player2_went == True:
                text2 = font.render(rps_dictionary[player2_move], 1, BLACK)
            elif game.player2_went == True:
                text2 = font.render('Escolheu!', 1, BLACK)
            else:
                text2 = font.render('Escolhendo...', 1, BLACK)
            
            if player == 0:
                display_surface.blit(text1, (85, 350))
                display_surface.blit(text2, (475, 350))
            else:
                display_surface.blit(text2, (85, 350))
                display_surface.blit(text1, (475, 350))

            for button in buttons:
                button.draw_button(display_surface)
                
            load_images()

    pygame.display.update()

buttons = [
    Button('Rock', 75, 450, RED), 
    Button('Paper', 275, 450, BLUE),
    Button('Scissors', 475, 450, GREEN)
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
            redraw_display_surface(display_surface, game, player)
            pygame.time.delay(500)
            try:
                game = network.send('reset_game')
            except:
                run = False
                print('Não foi possível conseguir um jogo')
                break
                
            font = pygame.font.SysFont('timesnewroman', 50)
            if (game.winner_player() == 0 and player == 0) or (game.winner_player() == 1 and player == 1):
                text = font.render('Você venceu!', True, GREEN)
            elif game.winner_player() == -1:
                text = font.render('Empate', True, BLUE)
            else:
                text = font.render('Você perdeu...', True, RED)

            display_surface.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                #pdb.set_trace()
            
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
        
        redraw_display_surface(display_surface, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(70)
        display_surface.fill(WHITE)
        write_title()
        write_music_copyright()
        font = pygame.font.SysFont('timesnewroman', 80)
        text = font.render('Clique para Jogar!', True, BLACK)
        display_surface.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                #pdb.set_trace()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    pygame.mixer.music.play(-1)
    menu_screen()