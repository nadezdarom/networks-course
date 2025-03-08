import socket
import os
import sys

if len(sys.argv) < 2:
    print("Missing port: python main.py <port>")
    sys.exit(1)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = int(sys.argv[1])
CRLF = "\r\n\n"

if SERVER_PORT < 1000 or SERVER_PORT > 65535:
    print("Wrong port")
    sys.exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"Listening on port {SERVER_PORT} ...")

def contentType(fileName):
    if fileName.endswith(".jpg"):
        return "image/jpg"
    if fileName.endswith(".png"):
        return "image/png"
    if fileName.endswith(".htm") or fileName.endswith(".html"):
        return "text/html"
    if fileName.endswith(".ram") or fileName.endswith(".ra"):
        return "audio/x-pn-realaudio"
    
    return "application/octet-stream"


def countContentLength(content):
    return str(len(content))


while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1500).decode()
    headers = request.split('\n')
    first_header_components = headers[0].split()

    http_method = first_header_components[0]
    filePath = "." + first_header_components[1]

    fileExists = False

    statusLine = ""
    contentTypeLine = ""
    contentLengthLine = ""
    entityBody = ""

    if http_method == "GET":

        if os.path.isfile(filePath):
            fileExists = True

        if fileExists:
            statusLine = "HTTP/1.1 200 OK" + "\r\n"
            contentTypeLine = "Content-Type: " + contentType(filePath) + "\r\n"

            with open(filePath, "rb") as f:
                file = f.read()

            contentLengthLine = "Conentn-Length: " + countContentLength(file)

        else:
            statusLine = "HTTP/1.1 404 Not Found" + "\r\n"
            contentTypeLine = "Content-Type: text/html" + "\r\n"
            entityBody = "<HTML>" +\
            "<HEAD><TITLE>404 Not Found</TITLE></HEAD>" +\
            "<BODY>404 Not Found</BODY></HTML>"

            contentLengthLine = "Conentn-Length: " + countContentLength(entityBody)
        
        response = statusLine + contentTypeLine + contentLengthLine + CRLF

    else:
        response = "HTTP/1.1 405 Method not allowed" + CRLF + "Allow: GET"

    client_socket.sendall(response.encode())

    if fileExists:
        client_socket.sendall(file)
    else:
        client_socket.sendall(entityBody.encode())

    client_socket.close()

