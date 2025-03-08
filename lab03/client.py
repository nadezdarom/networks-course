import socket
import threading
import os
import sys
import requests


if len(sys.argv) != 4:
    print("Usage: python3 client.py server_host server_port filename")


SERVER_HOST = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
FILENAME = sys.argv[3]
CRLF = "\r\n\n"

request = f"GET /{FILENAME} HTTP/1.1\r\nHost: {SERVER_HOST}:{SERVER_PORT}" + CRLF

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")

client_socket.sendall(request.encode())

response = b""

while True:
    package = client_socket.recv(1500)
    if not package:
        break
    response += package

client_socket.close()

headers, file_content = response.split(CRLF.encode())

headers = headers.decode()
print(f"\nHeaders:\n{headers}")

content_type = ""
for header in headers.split("\r\n"):
    if header.startswith("HTTP"):
        code = header.split()[1]
    if header.startswith("Content-Type: "):
        content_type = header.split()[1]

if code == "200":
    if content_type == "text/plain":
        print(f"\nFile content:\n{file_content.decode()}")
    else:
        with open(FILENAME, "wb") as f:
            f.write(file_content)
        print(f"\nFile {FILENAME} was successfully saved.")
else:
    print(f"\nFile content:\n{file_content.decode()}")





