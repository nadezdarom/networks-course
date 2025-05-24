import socket
import random
import time
import tkinter as tk
from tkinter import messagebox

def generate_random_data(length=512):
    return bytes(random.getrandbits(8) for _ in range(length))

def send_packets(ip, port, number_of_packets):
    try:
        port = int(port)
        number_of_packets = int(number_of_packets)
    except ValueError:
        messagebox.showerror("Error", "Port and number of packets must be integers.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        timestamp = str(time.time()).encode()
        for i in range(number_of_packets):
            data = generate_random_data()
            packet = timestamp + b"--" + str(number_of_packets).encode() + b"--" + str(i).encode() + b"--" + data
            sock.sendto(packet, (ip, port))
    finally:
        sock.close()

def start_sending(ip_entry, port_entry, num_packets_entry):
    ip = ip_entry.get()
    port = port_entry.get()
    number_of_packets = num_packets_entry.get()
    send_packets(ip, port, number_of_packets)


root = tk.Tk()
# Меня жоско забуллил этот ваш ткинтер
root.title("UDP Client")

tk.Label(root, text="IP").grid(row=0, column=0, padx=5, pady=5)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Port:").grid(row=1, column=0, padx=5, pady=5)
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Number of Packets").grid(row=2, column=0, padx=5, pady=5)
num_of_packets = tk.Entry(root)
num_of_packets.grid(row=2, column=1, padx=5, pady=5)

send_button = tk.Button(
    root,
    text="Send",
    command=lambda: start_sending(ip_entry, port_entry, num_of_packets)
)
send_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()

