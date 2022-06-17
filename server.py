import socket
import pickle
from _thread import *
from game import Game

server = '127.0.0.1'
port = 49372

# Criando o socket e definindo seus protocolos (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verificando a existência de erros ao conectar-se na porta
try:
    server_socket.bind((server, port))
except socket.error as error:
    print(error)

# Habilitando o server para aceitar conexões
server_socket.listen(2)
print('Esperando conexões... Servidor iniciado')

connected = set()
id_count = 0
games = {}

# Definindo como cada processo cliente irá se comportar
def threaded_client(connection_socket, player, game_id):
    global id_count
    connection_socket.send(str.encode(str(player)))
    answer = ''

    while True:
        try:
            data = connection_socket.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == 'reset_game':
                        game.reset_went()
                        game.update_match(game.winner_player())
                    elif data != 'get_another_player':
                        game.player_played(player, data)
                    
                    answer = game
                    connection_socket.sendall(pickle.dumps(answer))
            else:
                break
        except:
            break

    print('Conexão perdida')    
    try:
        del games[game_id]
        print('Encerrando jogo ', game_id)
    except:
        pass
    id_count = id_count - 1
    connection_socket.close()

# Servidor aberto, aceitando conexões
while True:
    connection_socket, address = server_socket.accept()
    print('Conectado a: ', address)

    id_count = id_count + 1
    current_player = 0
    game_id = (id_count - 1) // 2
    
    # Se id_count for ímpar, um jogador não está pareado
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print('Criando um novo jogo')
    else:
        games[game_id].game_ready = True
        current_player = 1

    start_new_thread(threaded_client, (connection_socket, current_player, game_id))