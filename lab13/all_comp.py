import socket
import sys
import tkinter as tk
from tkinter import ttk
from subprocess import Popen
import subprocess
import ipaddress
import threading
from collections import deque


def ping(ip):
    res = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode == 0

def get_mac(ip):
    try:
        pid = subprocess.run(["arp", "-n", ip], capture_output=True, text=True)
        s = pid.stdout
        mac = s.split()[3]
        
        return mac
    except:
        return "-"


def get_name(ip):
    try:
        name = socket.gethostbyaddr(ip)
        return name[0]
    except:
        return "-"
    

def scan(tree, progress):
    progress["value"] = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))

    host_ip = sock.getsockname()[0]
    host_name = socket.gethostname()

    proc = Popen('ifconfig', stdout=subprocess.PIPE)
    prev_lines = deque(["Господи", "помоги"])

    while True:
        line = proc.stdout.readline()
        prev_lines.append(line)
        if host_ip.encode() in line:
            mac_line = prev_lines.popleft()
            break

        prev_lines.popleft()

    host_mac = mac_line.split()[1].decode()
    mask = socket.inet_ntoa(bytes.fromhex(line.rstrip().split(b':')[-1].split()[3].decode()[2:]))

    # print(f"{"IP_addr":20} {"MAC_addr":20} {"Name":20}")
    # print(f"{host_ip:20} {host_mac:20} {host_name:20}\n")

    network = ipaddress.IPv4Network(f"{host_ip}/{mask}", strict=False)

    tree.insert("", "end", values=("Текущий ПК", "", ""))
    tree.insert("", 'end', values=(host_ip, host_mac, host_name))
    tree.insert("", "end", values=("Сеть", "", ""))
    num_of_hosts = network.num_addresses

    for i, ip in enumerate(network.hosts()):
        ip = str(ip)
        progress["value"] = ((i + 1) / num_of_hosts) * 100

        if ip == host_ip:
            continue
        
        if ping(ip):
            mac = get_mac(ip)
            name = get_name(ip)

            # print(f"{ip:20} {mac:20} {name:20}")
            tree.insert("", 'end', values=(ip, mac, name))



def start_scan(tree, progress):
    threading.Thread(target=scan, args=(tree, progress), daemon=True).start()

root = tk.Tk()
root.title("All computers in network")

columns = ("IP addr", "MAC addr", "Name")

tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("IP addr", text="IP addr")
tree.heading("MAC addr", text="MAC addr")
tree.heading("Name", text="Name")

tree.pack(expand=True, fill=tk.BOTH)

progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=300)
progress_bar.pack()

button = tk.Button(root, text="Начать поиск", command=lambda: start_scan(tree, progress_bar))
button.pack()

root.geometry("600x400")
root.mainloop()