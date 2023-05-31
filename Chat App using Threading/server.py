from socket import *
from threading import *

s = socket(AF_INET, SOCK_STREAM)

server = '127.0.0.1'
port = 19999

s.bind((server, port))

s.listen(5)

print("Server on listening mode, waiting for connections")

clients = []
aliases = []

def broadcast_message(data):
    for client in clients:
        client.send(data)


def handling_clients(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast_message(message)
        except:
            index = clients.index(client)
            clients.remove(index)
            client.close()
            alias = aliases[index]
            broadcast_message(f'{alias} has left the room!'.encode())
            aliases.remove(alias)
            break

def main():
    # accept connection
    client, addr = s.accept()
    print("Accepted connection from: ", str(addr))
    client.send("Name?".encode())
    username = client.recv(1024)
    clients.append(client)
    aliases.append(username)
    # broadcast message
    broadcast_msg = f'{username} has joined the room'.encode()
    broadcast_message(broadcast_msg)
    t1 = Thread(target=handling_clients, args=(client,))
    t1.start()
    

main()