import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 5555))

        self.id, spawn = pickle.loads(self.client.recv(1024))

        self.start_x, self.start_y, self.start_dir, self.start_hp, self.start_hooks, self.start_damage = spawn

    def send(self, data):
        self.client.send(pickle.dumps(data))
        return pickle.loads(self.client.recv(1024))
