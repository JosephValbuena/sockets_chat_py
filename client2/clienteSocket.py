import socket
import struct
import threading

rute = r'C:\Users\josva\Desktop\Workspace\University\2022-2\Sistemas distribuidos\Chat\client2\hosts_received.txt'

host = 'localhost'
port = 8000

#Crear socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

#Solicito el nombre de usuario
username = input("Digite su nombre de usuario: ")

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

def clientSocket():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "@file":
                receive_file(client, "hosts-received.txt")
            elif message == "@username":
                client.send(username.encode())
            else:
                print(message)
        except:
            print("Algo ocurrio con el servidor")
            client.close()
            break

def write_mesage():
    while True:
        message = f"{username}: {input('')}"
        client.send(message.encode())

receive_thread = threading.Thread(target=clientSocket)
receive_thread.start()

write_thread = threading.Thread(target=write_mesage)
write_thread.start()