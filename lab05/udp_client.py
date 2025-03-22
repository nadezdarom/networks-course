import socket

SERVER_PORT = 5550

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.bind(("", SERVER_PORT))

def send_cmd():
    while True:
        response, addr = client_socket.recvfrom(1500)
        print(response.decode())

send_cmd()