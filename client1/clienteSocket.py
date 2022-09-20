import socket
import struct
import threading

rute = r'hosts_received.txt'

# -------------------------------------- DECLARACIÓN DE VARIABLES -------------------------------------
serverHost = '172.17.0.2'
serverPort = 8000

#Crear socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverHost, serverPort))

clients = []
usernames = []

#Solicito el nombre de usuario
cUsername = input("Digite su nombre de usuario: ")

# -------------------------------------- DECLARACIÓN DE MÉTODOS AUXILIARES ---------------------------------------

def receive_file_size(sck: socket.socket):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize

def receive_file(sck, filename):
    filesize = receive_file_size(sck)
    with open(filename, "wb") as f:
        received_bytes = 0
        while received_bytes < filesize:
            chunk = sck.recv(1024)
            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)
    f = open(filename, 'r')
    for fas in f.readlines():
        splited = fas.split(',')
        clientSp = []
        clientSp.append(splited[0])
        clientSp.append(splited[1])
        clients.append(clientSp)
        usernameSP = splited[2].split('\n')
        usernames.append(usernameSP[0])
    write_thread = threading.Thread(target=write_mesage)
    write_thread.start()
# -------------------------------- DECLARACIÓN DE MÉTODOS PRINCIPALES ----------------------------------

def clientSocket():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "@file":
                receive_file(client, "hosts-received.txt")
            elif message == "@username":
                client.send(cUsername.encode())
            else:
                print(message)
        except:
            print("Algo ocurrio con el servidor")
            client.close()
            break

def write_mesage():
    while True:
        message = f"{cUsername}: {input('')}"
        client.send(message.encode())

receive_thread = threading.Thread(target=clientSocket)
receive_thread.start()

write_thread = threading.Thread(target=write_mesage)
write_thread.start()

