#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...

def get_area(coords0, coords1):
    result = abs(coords1[0] - coords0[0] + 1) * abs(coords1[1] - coords0[1] + 1)
    #print(coords0, coords1, result)
    return result

def part1(filename):
    coords = []
    with open(filename) as file:
        for line in file:
            coords.append(list(map(int, line.split(","))))

    largest_coords0 = None
    largest_coords1 = None
    largest_area = 0
    for i in range(len(coords) - 1):
        for j in range(1, len(coords)):
            area = get_area(coords[i], coords[j])
            if area > largest_area:
                largest_area = area
                largest_coords0 = coords[i]
                largest_coords1 = coords[j]

    return largest_area


def main():
    #result = part1("test.txt")
    result = part1("input.txt")
    #result = part2("test.txt")
    #result = part2("input.txt")
    print(f"Result: {result}")


main()