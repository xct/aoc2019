#!/usr/bin/env python3

'''
https://adventofcode.com/2019/day/1

Fuel required to launch a given module is based on its mass. 
Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
'''

data = []
with open('data/day1.txt','r') as f:
	data = f.readlines()

# Part 1 (Fuel for the base mass)
sum1 = 0
for mass in data:
	mass = int(mass)
	fuel = mass//3 - 2
	sum1 += fuel
print(f'Sum = {sum1}')
# That's the right answer! You are one gold star closer to rescuing Santa.

# Part 2 (Fuel for the fuel)
def get_fuel(mass):	
	fuel_sum = 0
	remaining_mass = mass
	while True:		
		fuel = remaining_mass//3 - 2
		if fuel <= 0:
			break
		fuel_sum += fuel
		remaining_mass = fuel
	return fuel_sum

sum2 = 0
for mass in data:
	mass = int(mass)
	fuel = get_fuel(mass)
	sum2 += fuel
print(f'Sum = {sum2}')