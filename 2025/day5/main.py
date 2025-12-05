#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...


def read_input(filename):
    fresh_ranges = []
    ingredients = []

    with open(filename) as file:
        is_reading_ingredients = False
        for line in file:
            if not line.rstrip():
                is_reading_ingredients = True
            elif is_reading_ingredients:
                ingredients.append(int(line.rstrip()))
            else:
                fresh_range = line.split("-")
                fresh_ranges.append((int(fresh_range[0]), int(fresh_range[1])))

    return (fresh_ranges, ingredients)

def solve(fresh_ranges):
    fresh_map = {}
    for fresh_range in fresh_ranges:
        for i in range(fresh_range[0], fresh_range[1] + 1):
            fresh_map[str(i)] = True
    return len(fresh_map)


def main():
    (fresh_ranges, _) = read_input("input.txt")
    result = solve(fresh_ranges)
    print("Result:", result)




main()