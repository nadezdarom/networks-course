import socket
import sys

HOST = "::1"
PORT = 5004

server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT, 0, 0))
server_socket.listen(5)

print(f"Listening on port {PORT}...")

while True:
    client_socket, client_address = server_socket.accept()

    print(f"New connection: {client_address}")

    while True:

        request = client_socket.recv(1024).decode().strip()

        if request:
            print(f"Client request: {request}")
        
        if request == "quit":
            print(f"Client closed connection")
            client_socket.send("Connection is closed\r\n".encode())
            client_socket.close()
            break

        client_socket.sendall(request.upper().encode())
