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
        print("fresh ranges")
        for line in file:
            if not line.rstrip():
                print("ingredients")
                is_reading_ingredients = True
            elif is_reading_ingredients:
                print("ingredient:", line.rstrip())
                ingredients.append(int(line.rstrip()))
            else:
                print("range:", line.rstrip())
                fresh_range = line.split("-")
                fresh_ranges.append((int(fresh_range[0]), int(fresh_range[1])))

    return (fresh_ranges, ingredients)

def solve(fresh_ranges, ingredients):
    count = 0
    for ingredient in ingredients:
        for fresh_range in fresh_ranges:
            if fresh_range[0] <= ingredient and ingredient <= fresh_range[1]:
                count += 1
                break
    return count

def main():
    (fresh_ranges, ingredients) = read_input("input.txt")
    result = solve(fresh_ranges, ingredients)
    print("Result:", result)




main()