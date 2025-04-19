import socket
import sys

if len(sys.argv) != 4:
    print("Usage: free_ports.py ip min_port max_port")
    sys.exit(1)

ip = sys.argv[1]

try:
    socket.inet_aton(ip)
except:
    print(f"ip address is incorrect")
    sys.exit(1)

def check_port(port):
    port = port if port >= 1024 else 1024
    port = port if port <= 65535 else 65535
    return port

try:
    min_port = int(sys.argv[2])
    min_port = check_port(min_port)
except:
    print(f"min_port should be an integer")
    sys.exit(1)

try:
    max_port = int(sys.argv[3])
    max_port = check_port(max_port)
except:
    print(f"max_port should be an integer")
    sys.exit(1)


ports = []


def free_ports(port=1024, max_port=65535):
    
    while port <= max_port:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        res = sock.connect_ex((ip, port))
        sock.close()
        if res != 0:
            ports.append(port)
        port += 1

    return
    
free_ports(min_port, max_port)

print(f"Free ports for {ip}:")
for port in ports:
    print(port)