#!/usr/bin/env python3
from collections import OrderedDict

with open('data/day8_p1.txt','r') as f:
    data = f.read()

sx = 25
sy = 6

layers = OrderedDict()
layer_idx = 0
y_idx = 0
for i in range(0,len(data),sx):
    x = data[i:i+25]
    if not layer_idx in layers:
        layers[layer_idx] = []
    layers[layer_idx].append(x)
    y_idx += 1
    if y_idx == sy:
        y_idx = 0
        layer_idx += 1

# find layer with fewest 0 digits
min_zeros = 99999
min_layer_idx = 0
for i, layer_idx in enumerate(layers.keys()):
    zeros = 0
    for number in layers[layer_idx]:
        zeros += list(number).count('0')
    if zeros < min_zeros:
        min_zeros = zeros
        min_layer_idx = layer_idx

print(f"Most zeros: {min_zeros}")
print(f"Layer with most zeros: {min_layer_idx}")

# Number of 1 digits multiplied by the number of 2 digits
total_ones = 0
total_twos = 0
for number in layers[min_layer_idx]:
    ones = list(number).count('1')
    twos = list(number).count('2')
    total_ones += ones
    total_twos += twos

print(f"Result: {total_ones*total_twos}")

# Part2, 0: black, 1: white, 2:transparent
pixels = OrderedDict()
for y in range(sy):
    for x in range(sx):
        px = '0'
        for k in layers.keys():
            layer = layers[k]
            px = list(layer[y])[x]
            if px != '2':
                break
        pixels[(x,y)] = px

# display
render = ''
for y in range(sy):
    for x in range(sx):
        px = pixels[(x,y)]
        # transparent, do not print
        if px == '2':
            px = ''
        # white is #
        elif px == '1':
            px = '#'
        # black is invisble
        else:
            px = ' '
        render += px
    render += "\n"
print(render)