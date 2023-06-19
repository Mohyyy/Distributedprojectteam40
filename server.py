import socket
import threading
import signal
import sys

HOST = ""
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []  # List to store client sockets
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    global racing_started
    while True:
        try:
            message = client.recv(1024)
            if not racing_started:  # If the race hasn't started, ignore client messages
                continue
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except Exception as e:
            print(f"Error handling client {client}: {e}")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    global racing_started, race_track
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}!")
            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024)
            nicknames.append(nickname)
            clients.append(client)
            print(f"Nickname of the client is {nickname}")
            broadcast(f"{nickname} connected to the server !\n".encode('utf-8'))
            client.send("Connected to the server".encode('utf-8'))
            if racing_started:  # If the race has already started, send the race track to the new client
                for line in race_track:
                    client.send(line.encode('utf-8'))
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

def start_race():
    global racing_started, race_track
    racing_started = True


def shutdown_server(signal, frame):
    print("Shutting down server...")
    server.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_server)

print("Server running")
receive()