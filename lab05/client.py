import sys, socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5555
CRLF = "\r\n\n"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")

def send_cmd():
    while True:
        command = input("\n>> ").strip()
        client_socket.send(command.encode())
        response = ""
        while True:
            package = client_socket.recv(1500).decode()
            if not package or package.endswith("\0"):
                response += package[:-1]
                break
            response += package

            print(package, end="")


        if command == "quit":
            client_socket.close()
            sys.exit(0)

send_cmd()
