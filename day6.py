#!/usr/bin/env python3
from networkx import *

with open('data/day6_p1.txt','r') as f:
    data =f.readlines()

edges = [x.strip().split(')') for x in data]
G = nx.Graph(edges)

count = sum(nx.shortest_path_length(G, "COM").values())
l = nx.shortest_path_length(G, "YOU", "SAN")

print(f'Part 1: {count}')
print(f'Part 2: {l-2}')