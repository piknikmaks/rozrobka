import socket
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5555))
server.listen(2)

print("Server started")

clients = []

spawn_positions = [
    (40, 400, "right", 100, [], 0),
    (700, 400, "left", 100, [], 0)
]

positions = spawn_positions.copy()

for i in range(2):
    conn, addr = server.accept()
    print("Connected:", addr)
    conn.send(pickle.dumps((i, spawn_positions[i])))

    clients.append(conn)

while True:
    for i, conn in enumerate(clients):
        data = conn.recv(1024)
        
        if not data:
            continue
        
        positions[i] = pickle.loads(data)
        other_index = 1 - i
        conn.send(pickle.dumps(positions[other_index]))
