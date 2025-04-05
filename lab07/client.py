import socket
import time
import sys
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5550
ADDR = (SERVER_HOST, SERVER_PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1)  # чтоб не ждал вечно потерянные пакеты


def send_cmd(number_of_requests):
    number_of_message = 0

    min_RTT = 10**5
    max_RTT = -10**5
    mean_RTT = 0
    lost_packeges = 0

    while number_of_message < number_of_requests:
        number_of_message += 1
        send_time = datetime.now()

        request = f"ping {number_of_message} {send_time}"
        request = request.encode()

        client_socket.sendto(request, ADDR)

        try:
            response, _ = client_socket.recvfrom(1500)
            get_time = datetime.now()
            curr_RTT = round((get_time - send_time).total_seconds() * 10**5)
            
            if curr_RTT < min_RTT:
                min_RTT = curr_RTT

            if curr_RTT > max_RTT:
                max_RTT = curr_RTT

            mean_RTT = round((mean_RTT * (number_of_message - 1) + curr_RTT) / number_of_message)

            print(f"Server's response: {response.decode()}")
            print(f"RTT: {curr_RTT}ms")
        except:
            lost_packeges +=1
            print(f"Request timed out")

        print(f"Statistic\nmax_RTT: {max_RTT if max_RTT > 0 else 0}ms, min_RTT: {min_RTT if min_RTT != 10**5 else 0}ms, average_RTT: {mean_RTT}ms, loss: {lost_packeges / number_of_message * 100}%\n")

num_of_requests = 10

if len(sys.argv) == 2:
    num_of_requests = sys.argv[1]

try:
    num_of_requests = int(num_of_requests)
except:
    print("Number of requests should be an integer")
    sys.exit(1)

send_cmd(num_of_requests)