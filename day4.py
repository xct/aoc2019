#/usr/bin/env python

# 6 digit number
# range given in input
# 2 adjacent digits are the same
# left to right digits same or increase
# How many different passwords possible following these criteria?

inp = '197487-673251'
s, e = inp.split('-')
s = int(s)
e = int(e)

# Part 1
part_1 = []
part_2 = []
for num in range(s, e, 1):      
    check_1 = 1 # digits increase or are the same
    check_2 = 0 # one digit occurs twice
    digits = [int(x) for x in str(num)]
    last_digit = 0
    for i, digit in enumerate(digits):
        if digit == last_digit:
            check_2 = 1
        if digit >= last_digit:
            last_digit = digit
        else:
            check_1 = 0
            break   
    if check_1 == 1 and check_2 == 1:
        part_1.append(str(num))
        # one occurance of a double digit -> count digits and look for occurance
        if 2 in [str(num).count(digit) for digit in str(num)]:
            part_2.append(str(num))

print(f'Part 1: {len(part_1)}')
print(f'Part 2: {len(part_2)}')