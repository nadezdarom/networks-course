import socket
import sys
import struct
import time
import random
import select


ID = random.randint(0, 10**4)


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
        sent = sock.sendto(packet, (addr, 1))
        packet = packet[sent:]


def recv_packet(sock, n, start_time):
    while True:
        timeout = 1

        ready = select.select([sock], [], [], timeout)
        if not ready[0]:
            return None

        time_recv = time.time()
        packet, _ = sock.recvfrom(1024)

        icmp_header = packet[20:28]
        _, _, _, recv_id, recv_n = struct.unpack("!bbHHH", icmp_header)

        if recv_id == ID and recv_n == n:
            rtt = (time_recv - start_time) * 1000 
            return rtt


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python ping.py <hostname> [n]")
    sys.exit(1)

n = 10

if len(sys.argv) == 3:
    try:
        n = int(sys.argv[2])
    except:
        print(f"Number of pings should be integer")
        sys.exit(1)

    if n <= 0:
        print(f"Number of pings shold be > 0")
        sys.exit(1)

dest = sys.argv[1]

try:
    addr = socket.gethostbyname(dest)
except:
    print(f"Destination {dest} does not exists")
    sys.exit(1)

print(f"Ping {addr}:")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

rtts = []
sent = 0
received = 0

for i in range(1, n + 1):
    sent += 1
    start = time.time()

    send_packet(client_socket, i)
    rtt = recv_packet(client_socket, i, start)

    if rtt:
        received += 1
        rtts.append(rtt)

    print(f"Ping {dest}, RTT: {rtt if rtt else None} ms")

    time.sleep(1)

client_socket.close()

print("\nStatistic:")
print(f"Packets: Sent = {sent}, Received = {received}, Lost = {sent - received} ({(sent - received)/sent*100}% loss)")

if rtts:
    print(f"RTT: Minimum = {min(rtts)} ms, Maximum = {max(rtts)} ms, Average = {sum(rtts)/len(rtts)} ms")
