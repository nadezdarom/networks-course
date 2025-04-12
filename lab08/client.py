import socket
import sys
import struct
import subprocess
import random
from checksum import calculate_checksum, check_checksum

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5550
ADDR = (SERVER_HOST, SERVER_PORT)
PACKET_SIZE = 512
COMMANDS = ["get", "send"]
GAMMA = 0.3


def check_packet(packet):
    checksum = struct.unpack("!I", packet[-4:])[0]
    packet = packet[:-4]

    return check_checksum(packet, checksum)


if len(sys.argv) > 2:
    print("Usage: client.py [timeout]")
    sys.exit(1)

if len(sys.argv) == 2:
    try:
        timeout = int(sys.argv[1])
    except:
        print("Timeout should be an integer")
        sys.exit(1)
else:
    timeout = 1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_file(file_name):
    PACKET_NUM = 0

    try:
        f = open(file_name, "rb")
    except:
        print(f"{file_name} does not exists\n")
        return

    packets = []

    packet = f.read(PACKET_SIZE)
    while packet:
        packets.append(packet)
        packet = f.read(PACKET_SIZE)

    f.close()

    num_of_packets = len(packets)

    print(f"Number of packets to send: {num_of_packets}\n")

    service_request = struct.pack('!BBI', 0, PACKET_NUM, num_of_packets) + file_name.encode()
    checksum_serv_req = calculate_checksum(service_request)
    service_request  += struct.pack("!I", checksum_serv_req)
    recv = -1

    # отправляем первый пакет с информайией по файлу, пока не получим ACK
    # я тут считаю, что сервер у нас не отваливается (как и клиент)
    while recv != PACKET_NUM:
        client_socket.sendto(service_request, ADDR)

        try:
            response, _ = client_socket.recvfrom(1500)
            recv = struct.unpack("!B", response)[0]
        except:
            continue

    PACKET_NUM = (PACKET_NUM + 1) % 2
    
    # отправляем пакеты
    for pack, num_of_packet in zip(packets, [i for i in range(1, num_of_packets + 1)]):
        request = struct.pack('!BB', 1, PACKET_NUM) + pack
        
        checksum_pack_req = calculate_checksum(request)
        request += struct.pack("!I", checksum_pack_req)
        
        recv = -1
        attempt = 0

        print(f"Number packet to send: {num_of_packet}")
        while recv != PACKET_NUM:
            client_socket.sendto(request, ADDR)
            attempt += 1
            try:
                response, _ = client_socket.recvfrom(1500)
                recv = struct.unpack("!B", response)[0]
            except:
                print(f"Attempt {attempt}: sanding packet {num_of_packet} failed. Trying again.")
                continue

        print(f"Attempt {attempt}: packet {num_of_packet} has been successfully sent\n")

        PACKET_NUM = (PACKET_NUM + 1) % 2
    
        if num_of_packet == num_of_packets:
            print(f"File {file_name} has been successfully sent!\n")
            print("Checking if files matched...")
            parts = file_name.rsplit('.', 1)
            new_file_name = parts[0] + "_recieved." + parts[1]
            subprocess.run(["python3", "check_files.py", file_name, new_file_name])


# Я буду считать, что мы запрашиваем у сервера файл и он нам его отправляет (если он у него есть) 
def get_file(file_name):
    num_of_packets = 0
    file = b''
    last_pack_number = 0
    PACKET_NUM = 0

    service_request = struct.pack('!BB', 2, PACKET_NUM) + file_name.encode()
    checksum_serv_req = calculate_checksum(service_request)
    service_request  += struct.pack("!I", checksum_serv_req)
    recv = -1

    while recv != PACKET_NUM:
        client_socket.sendto(service_request, ADDR)

        try:
            response, _ = client_socket.recvfrom(1500)
            recv = struct.unpack("!B", response)[0]
        except:
            continue

    PACKET_NUM = (PACKET_NUM + 1) % 2

    client_socket.settimeout(None)
    while True:
        data, _ = client_socket.recvfrom(1500)

        # Типо потеряли пакет
        if random.random() < GAMMA:
            print("Package has been lost")
            continue

        type_of_packet, packet_num = struct.unpack("!BB", data[:2])
        
        # пакет с информацией по файлу
        if type_of_packet == 0:
            if not check_packet(data):
                print("Wrong checksum")
                continue
            num_of_packets = struct.unpack("!I", data[2:6])[0]
            file_name = data[6:-4].decode()
            parts = file_name.rsplit('.', 1)
            file_name = parts[0] + "_recieved." + parts[1]
            # Отправили ACK, что получили пакет
            response = struct.pack("!B", packet_num)
            # типо теряем ack-пакет
            if random.random() >= GAMMA:
                client_socket.sendto(response, ADDR)
            else:
                print(f"ACK packet has been lost\n")
            # идем получать пакеты
            continue

        # пакеты самого файла
        if type_of_packet == 1:
            if not check_packet(data):
                print("Wrong checksum")
                continue
            response = struct.pack("!B", packet_num)
            # типо теряемм ack-пакет
            if random.random() >= GAMMA:
                client_socket.sendto(response, ADDR)
                print(f"Packet {packet_num} has been successfully recieved!\n")
            else:
                print(f"ACK packet has been lost\n")
                continue

            if last_pack_number != packet_num:
                packet = data[2:-4]
                file += packet
                num_of_packets -= 1
                last_pack_number = packet_num
            else:
                continue

        if type_of_packet == 3:
            if not check_packet(data):
                print("Wrong checksum")
                continue
            print(f"File {file_name} does not exists on server.")
            return

        if num_of_packets == 0:
            with open(file_name, 'wb') as f:
                f.write(file)

            print(f'File {file_name} has been successfully recieved!\n')
            return

while True:
    client_socket.settimeout(timeout)  
    try:
        command, file_name = input(">> ").strip().split()
    except:
        print("Usage: send/get file_name\n")
        continue

    if command.lower() not in COMMANDS:
        print("Allowed commands: send, get")
        continue

    if command.lower() == "send":
        send_file(file_name)

    if command.lower() == "get":  
        get_file(file_name)




