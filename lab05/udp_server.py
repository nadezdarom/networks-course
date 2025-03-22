import socket
import time
import datetime

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5550
CRLF = "\r\n\n"
ADDR = (SERVER_HOST, SERVER_PORT)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    print(f"Listening on port {SERVER_PORT} ...")

    while True:
        date = datetime.datetime.now().strftime("%H:%M:%S")
        server_socket.sendto(date.encode(), ADDR)
        time.sleep(1)

start_server()

