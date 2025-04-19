import socket
import fcntl
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
except:
    ip = "127.0.1.1"

iface = b"eth0"
mask = socket.inet_ntoa(fcntl.ioctl(s, 35099, struct.pack('256' + 's', iface))[20:24])
s.close()


print(f"ip: {ip}")
print(f"mask: {mask}")
