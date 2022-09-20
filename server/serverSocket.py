import socket
import os
import struct
import threading

host = 'localhost'
port = 8000
rute= r'C:\Users\josva\Desktop\Workspace\University\2022-2\Sistemas distribuidos\Chat\server\hosts.txt'
clients = []
usernames = []

# se crea y se abre el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print(f"Servidor corrriendo {host}:{port}")

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def broadcast_file():
    for client in clients:
        client.send("@file".encode())
        filesize = os.path.getsize("hosts.txt")
        client.sendall(struct.pack("<Q", filesize))
        with open("hosts.txt", 'rb') as f:
            while read_bytes := f.read(1024):
                client.sendall(read_bytes)

def writeInFile(rute, content):
    fileT = open(rute, 'a+')
    fileT.write(content)
    fileT.close()

def handle_message(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f'{username} desconectado'.encode())
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def socketServer():
    while True:
        content = ''
        client, addr = server.accept()
        client.send("@username".encode())
        username = client.recv(1024).decode()
        clients.append(client)
        usernames.append(username)

        print(f"El usuario {username} se ha conectado")
        content = ''
        content = f'{addr[0]},{addr[1]},{username}\n'
        writeInFile(rute, content)
        broadcast_file()
        broadcast(f'{username} se ha conectado al chat.'.encode(), client)

        thead = threading.Thread(target=handle_message, args=(client,))
        thead.start()

socketServer()