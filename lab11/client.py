import socket
import sys
import struct
import time
import random
import select


ID = random.randint(0, 10**4)
MAX_HOP = 30


def calculate_checksum(data):
    if len(data) % 2 == 1:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + (data[i + 1])
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum = ~checksum & 0xFFFF
    return checksum


def create_ICMP_packet(n):
    type_ICMP = 8
    code_ICMP = 0
    checksum = 0
    header = struct.pack("!bbHHH", type_ICMP, code_ICMP, checksum, ID, n)
    data = b"some data, let it be: fdblkfsdlnsn"

    checksum = calculate_checksum(header + data)

    header = struct.pack("!bbHHH", type_ICMP, code_ICMP, checksum, ID, n)

    return header + data


def send_packet(sock, n):
    packet = create_ICMP_packet(n)

    while packet:
        sent = sock.sendto(packet, (dest_addr, 1))
        packet = packet[sent:]


def recv_packet(sock, n, start_time):
    while True:
        timeout = 1

        ready = select.select([sock], [], [], timeout)
        if not ready[0]:
            return None

        time_recv = time.time()
        packet, addr = sock.recvfrom(1024)

        icmp_header = packet[20:28]
        type_ICMP, _, _, recv_id, recv_n = struct.unpack("!bbHHH", icmp_header)

        rtt = (time_recv - start_time) * 1000 

        return rtt, addr, type_ICMP


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python ping.py <hostname> [n], where n - number of packets to be sent")
    sys.exit(1)

n = 3

if len(sys.argv) == 3:
    try:
        n = int(sys.argv[2])
    except:
        print(f"Number of packets should be integer")
        sys.exit(1)

    if n <= 0:
        print(f"Number of packets should be > 0")
        sys.exit(1)

dest = sys.argv[1]

try:
    dest_addr = socket.gethostbyname(dest)
except:
    print(f"Destination {dest} does not exists")
    sys.exit(1)

addr = None
reached = False
print(f"Traceroute to {dest} ({dest_addr}), 30 hops max\n")
for ttl in range(1, MAX_HOP):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack("I", ttl))
    client_socket.settimeout(1)
    
    inter_addr = None
    print(f"Hop: {ttl}", end='')
    for j in range(n):
        start = time.time()
        send_packet(client_socket, ttl)
        result = recv_packet(client_socket, ttl, start)
        if result is None:
            print(" *", end='')
        else:
            rtt, addr, code = result
            if code == 0:
                reached = True
            inter_addr = addr
            print(f" {rtt:.3f}ms", end='')

    if inter_addr:
        try:
            host_name = socket.gethostbyaddr(inter_addr[0])[0]
            print(f" {host_name} {inter_addr[0]}")
        except:
            print(f" {inter_addr[0]}")
    else:
        print(" Timeout")

    if reached:
        print(f"\nThe end of traceroute. Reached destination in {ttl} hops")
        break

client_socket.close()


