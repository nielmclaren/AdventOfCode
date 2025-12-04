#!/usr/bin/python3

import math

# Guesses: seven
# Guesses: 6380 (too high)

print("ohai")

pos = 50
prev_pos = 50
curr_zeros = 0
total_zeros = 0

with open("test.txt", "r") as file:
    for line in file:
        sign = 1 if line[0] == 'R' else -1
        dist = int(line[1:])

        pos += sign * dist

        if pos >= 100:
            curr_zeros += math.floor(pos / 100)
        if pos <= 0:
            curr_zeros += math.floor(abs(pos) / 100)

        pos = pos % 100

        while pos < 0:
            pos += 100

        print(f"{line.rstrip()}\t{prev_pos}\t{sign * dist}\t{pos}\t({curr_zeros})")
        total_zeros += curr_zeros
        curr_zeros = 0
        prev_pos = pos

print(total_zeros)
