import socket
import subprocess

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5555
CRLF = "\r\n\n"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print(f"Listening on port {SERVER_PORT} ...")

    while True:
        client_socket, client_address = server_socket.accept()

        print(f"New connection: {client_address}")

        while True:
            request = client_socket.recv(1500).decode().strip()
            print(f"Client request: {request}")

            if request == "quit":
                print("Client closed connection.")
                client_socket.send("Connection is closed\r\n".encode())
                client_socket.close()
                break

            process = subprocess.Popen(request, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for line in process.stdout:
                client_socket.send(line)
            stderr = process.stderr.read()
            if stderr:
                client_socket.send(stderr)

            client_socket.send(b"\0")


start_server()