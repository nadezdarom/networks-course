import socket
import time
import tkinter as tk
import threading
import random


received_packet_nums = set()
total_packets = None
total_bytes = 0
start_time = None
recv_time = None


def run_udp_server(ip, port):
    global start_time, total_packets, total_bytes, received_packet_nums
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    while True:
        request, _ = sock.recvfrom(4096)

        parts = request.split(b"--", 3)

        time_bytes, total_packets_bytes, packet_num_bytes, payload = parts

        try:
            sent_time = float(time_bytes.decode())
            total_packets = int(total_packets_bytes.decode())
            packet_num = int(packet_num_bytes.decode())
        except:
            print("Something went wrong with decoding data")

        if start_time is None:
            start_time = sent_time

        if random.random() < 0.1:
            continue  # типо профукали пакет

        if packet_num not in received_packet_nums:
            received_packet_nums.add(packet_num)
            total_bytes += len(payload)


def show_stats():
    if start_time is None or len(received_packet_nums) == 0:
        result_label.config(text="No data received yet")
        return

    duration = time.time() - start_time
    speed = total_bytes / duration / 1024 if duration > 0 else 0

    text = (f"Packets received: {len(received_packet_nums)} out of {total_packets}\n"
            f"Speed: {speed:.2f} KB/s\n")
    result_label.config(text=text)


def start_server():
    ip = ip_entry.get()
    
    try:
        port = int(port_entry.get())
    except:
        print("Port must be an integer")
    threading.Thread(target=run_udp_server, args=(ip, port), daemon=True).start()

root = tk.Tk()
root = root
root.title("UDP Server")

tk.Label(root, text="Listen IP:").grid(row=0, column=0)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1)

tk.Label(root, text="Listen Port:").grid(row=1, column=0)
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1)

start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.grid(row=2, column=0, columnspan=2, pady=5)

get_button = tk.Button(root, text="Get Data", command=show_stats)
get_button.grid(row=3, column=0, columnspan=2, pady=5)

result_label = tk.Label(root, text="Waiting for data...")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

ip = ip_entry.get()
port = port_entry.get()

root.mainloop()
