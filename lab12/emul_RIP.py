import random
import sys
import json
from collections import deque
import copy


MAX_HOPS = 15


class network:
    def __init__(self):
        self.nodes = {}
        self.routing_tables = {}

    def generate(self, file_name):
        try:
            f = open(file_name, 'r')
        except:
            print(f"File {file_name} does not exists")
            sys.exit(1)
        self.nodes = json.load(f)
        f.close()


    def init_rout_tables(self):
        routing_tables = {}
        for ip in self.nodes:
            routing_tables[ip] = {ip: ('-', 0)}
            for conn in self.nodes[ip]:
                routing_tables[ip][conn] = (conn, 1)

        return routing_tables


    def routing(self, print_steps = False):
        routing_tables = self.init_rout_tables()
        step = 0
        changed = True
        max_steps = 20 # чтоб циклов не было

        if print_steps:
            print(f"\nSimulation step {step}")
            self.print_tables(routing_tables)

        while changed and step < max_steps:
            step += 1

            if print_steps:
                print(f"\nSimulation step {step}")

            changed = False
            new_tables = copy.deepcopy(routing_tables)

            for ip in self.nodes:
                for conn in self.nodes[ip]:
                    conn_table = routing_tables[conn]
                    for target, (next_hop, metric) in conn_table.items():
                        if ip == target or metric >= MAX_HOPS:
                            continue

                        new_metric = metric + 1
                        if target not in new_tables[ip] or new_metric < new_tables[ip][target][1]:
                            new_tables[ip][target] = (conn, new_metric)
                            changed = True

            routing_tables = copy.deepcopy(new_tables)
            if print_steps:
                self.print_tables(routing_tables)

        if step == max_steps and print_steps:
            print("Maximum of steps was reached. Maybe there are a loop.")

        self.routing_tables = routing_tables


    def print_tables(self, tables):
        for ip in tables:
            print(f"\nTable of router {ip}")
            print(f"{'[Source IP]':20}  {'[Destination IP]':20}  {'[Next hop]':15}  [Metric]")

            for target in tables[ip]:
                next_hop, metric = tables[ip][target]
                print(f"{ip:20} {target:20} {next_hop:20} {metric}")

    def print_final_tables(self):
        self.routing()

        print("Final tables:")
        self.print_tables(self.routing_tables)


nw = network()
file_name = "system.json"

if len(sys.argv) == 1: #  если названия файла и флаги не передали, то печатаем конечые таблицы маршуртизатов для примера по умолчанию
    nw.generate(file_name)
    nw.print_final_tables()

if len(sys.argv) == 2:
    if sys.argv[1] == "steps":
        nw.generate(file_name)
        nw.routing(print_steps=True)
    else:
        file_name = sys.argv[1]
        nw.generate(file_name)
        nw.print_final_tables()

if len(sys.argv) == 3:
    file_name = sys.argv[1]
    if sys.argv[2] != "steps":
        print(f"Unknown command: {sys.argv[2]}")
        sys.exit(1)
    
    nw.generate(file_name)
    nw.routing(True)

        

    




