import socket
import random

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5550
ADDR = (SERVER_HOST, SERVER_PORT)
GAMMA = 0.2

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    print(f"Listening on port {SERVER_PORT} ...")
    number_of_request = 0

    while True:
        number_of_request += 1
        data, client_address = server_socket.recvfrom(1500)
        request = data.decode()

        print(f"Request {number_of_request}: {request}")

        # Типо потеряли пакет
        if random.random() < GAMMA:
            print(f"Пакет {number_of_request} потерян")
            continue

        server_socket.sendto(request.upper().encode(), client_address)


start_server()