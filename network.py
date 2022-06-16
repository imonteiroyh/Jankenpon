import socket
import pickle

class Network():
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '127.0.0.1'
        self.port = 49372
        self.address = (self.server, self.port)
        self.player = self.connect()
        
    def get_player(self):
        return self.player

    # Definindo a conexão
    def connect(self):
        try:
            self.client_socket.connect(self.address)
            return self.client_socket.recv(2048).decode()
        except:
            pass

    # Definindo um método para enviar informações   
    def send(self, data):
        try:
            self.client_socket.send(str.encode(data))
            return pickle.loads(self.client_socket.recv(2048))
        except socket.error as error:
            print('Erro ao enviar informações.')
            print(error)
