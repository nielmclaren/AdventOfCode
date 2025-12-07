#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...

def solve(filename):
    with open(filename) as file:
        beams = []
        num_splits = 0

        first_line = file.readline()
        beams.append(first_line.find('S'))

        for line in file:
            next_beams = []
            for beam in beams:
                if line[beam] == '^':
                    num_splits += 1
                    if not beam - 1 in next_beams:
                        next_beams.append(beam - 1)
                    if not beam + 1 in next_beams:
                        next_beams.append(beam + 1)

                elif line[beam] == '.':
                    if not beam in next_beams:
                        next_beams.append(beam)

                else:
                    print("ERROR Bad character.")
            beams = next_beams
        return num_splits



def main():
    result = solve("input.txt")
    print(result)


main()