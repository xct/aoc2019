#!/usr/bin/env python3

import numpy as np
np.set_printoptions(edgeitems=10)
np.core.arrayprint._line_width = 180

#p1 = ['R8','U5','L5','D3']
#p2 = ['U7','R6','D4','L4']
#p1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
#p2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
#p1 = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']
#p2 = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']

with open('data/day3_p1.txt', 'r') as f:
    p1 = f.read().split(',')
with open('data/day3_p2.txt', 'r') as f:
    p2 = f.read().split(',')

def grid_move_steps(point, direction, distance, marker, steps):
    p = [point[0],point[1]]
    print(p)
    if direction == 'R':
        for i in range(distance):           
            x = p[0]
            y = p[1]
            if grid[x,y] == 0:
                grid[x,y] = marker
            elif grid[x,y] != marker:
                grid[x,y] = 3
                if (x,y) in step_map:
                    step_map[(x,y)] += steps + i
                else:
                    step_map[(x,y)] = steps + i
            p[0] += 1   
    elif direction == 'L':
        for i in range(distance):           
            x = p[0]
            y = p[1]
            if grid[x,y] == 0:
                grid[x,y] = marker
            elif grid[x,y] != marker:
                grid[x,y] = 3
                if (x,y) in step_map:
                    step_map[(x,y)] += steps + i
                else:
                    step_map[(x,y)] = steps + i
            p[0] -= 1   
    elif direction == 'U':
        for i in range(distance):           
            x = p[0]
            y = p[1]
            if grid[x,y] == 0:
                grid[x,y] = marker
            elif grid[x,y] != marker:
                grid[x,y] = 3   
                if (x,y) in step_map:
                    step_map[(x,y)] += steps + i
                else:
                    step_map[(x,y)] = steps + i
            p[1] += 1   
    elif direction == 'D':
        for i in range(distance):           
            x = p[0]
            y = p[1]
            if grid[x,y] == 0:
                grid[x,y] = marker
            elif grid[x,y] != marker:
                grid[x,y] = 3
                if (x,y) in step_map:
                    step_map[(x,y)] += steps + i
                else:
                    step_map[(x,y)] = steps + i
            p[1] -= 1       
    return p, steps+distance


#origin = [0,0]
origin = [20000,20000]

# = 1st pass =
grid = np.zeros(shape=(40000,40000))
step_map = {}

cur_steps = 0
p = origin
for i in range(len(p1)):    
    print(p1[i])
    p, cur_steps = grid_move_steps(p, p1[i][0], int(p1[i][1:]), 1, cur_steps)
cur_steps = 0
p = origin
for i in range(len(p2)):
    print(p2[i])
    p, cur_steps = grid_move_steps(p, p2[i][0], int(p2[i][1:]), 2, cur_steps)

min_dist = 9999999
min_coords = None
crosses = np.where(grid == 3)
crosses = list(zip(crosses[0], crosses[1]))
for i, cross in enumerate(crosses):
    dist = np.abs(origin[0] - cross[0]) + np.abs(origin[1]-cross[1])
    if dist != 0 and dist < min_dist:
        min_dist = dist
        min_coords = cross
print(f'Minimum dist: {min_dist} / {min_coords}') # 1017

# = 2nd pass = 
grid = np.zeros(shape=(40000,40000))

cur_steps = 0
p = origin
for i in range(len(p2)):
    print(p2[i])
    p, cur_steps = grid_move_steps(p, p2[i][0], int(p2[i][1:]), 2, cur_steps)
cur_steps = 0
p = origin
for i in range(len(p1)):    
    print(p1[i])
    p, cur_steps = grid_move_steps(p, p1[i][0], int(p1[i][1:]), 1, cur_steps)

min_dist = 9999999
min_coords = None
crosses = np.where(grid == 3)
crosses = list(zip(crosses[0], crosses[1]))
for i, cross in enumerate(crosses):
    dist = np.abs(origin[0] - cross[0]) + np.abs(origin[1]-cross[1])
    if dist != 0 and dist < min_dist:
        min_dist = dist
        min_coords = cross
print(f'Min dist: {min_dist} / {min_coords}') # 1017

# = aggregate results =
del step_map[(origin[0],origin[1])]
print(f'Min steps: {min(step_map.items(), key=lambda x: x[1])}')