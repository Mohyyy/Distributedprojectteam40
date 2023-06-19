import socket

bind_host = '127.0.0.1'  # Change this to the bind host for Server 2
bind_port = 8000  # Change this to the bind port for Server 2

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to a specific address and port
server_socket.bind((bind_host, bind_port))

# Listen for incoming connections
server_socket.listen(2)
print("Synch Server listening on", bind_host + ":" + str(bind_port))

while True:
    # Accept a client connection
    client_socket, addr = server_socket.accept()
    print("Accepted connection from", addr[0] + ":" + str(addr[1]))

    # Receive data from the client
    data = client_socket.recv(4096).decode()
    print("dataaaa", data)
    if data == "Hello from Server 1!":
        print("[Received from Client Server]:", data)
        client_socket.send("3000".encode())
    elif data == "Hello from Server 2!":
        print("[Received from Chat Server]:", data)
    client_socket.send("9999".encode())
    # Close the client connection
    client_socket.close()