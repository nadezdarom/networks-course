import socket
import sys

HOST = "::1"
PORT = 5004

client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT, 0, 0))

print(f"Connnected to {HOST}:{PORT}")

while True:
    request = input("\n>> ").strip()
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()

    print(f"\nServer response: {response}")
    if request == "quit":
        client_socket.close()
        sys.exit(0)


