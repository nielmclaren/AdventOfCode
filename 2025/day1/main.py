#!/usr/bin/python3

# Guesses: seven

print("ohai")

pos = 50
prev_pos = 50
zeros = 0
with open("input.txt", "r") as file:
    for line in file:
        sign = 1 if line[0] == 'R' else -1
        dist = int(line[1:])
        pos += sign * dist
        pos = pos % 100
        while pos < 0:
            pos += 100
        #print(line.rstrip(), prev_pos, sign * dist, pos)
        if pos == 0:
            zeros += 1
        prev_pos = pos

print(zeros)

