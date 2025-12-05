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


def merge_ranges(a, b):
    if a[0] <= b[0] and b[0] <= a[1] and a[1] <= b[1]:
        return (a[0], b[1])
    if b[0] <= a[0] and a[0] <= b[1] and b[1] <= a[1]:
        return (b[0], a[1])
    if a[0] <= b[0] and b[1] <= a[1] :
        return (a[0], a[1])
    if b[0] <= a[0] and a[1] <= b[1] :
        return (b[0], b[1])
    return None

def merge_all_ranges(fresh_ranges):
    result = []

    num_ranges = len(fresh_ranges)
    for i in range(num_ranges):
        is_added = False
        for j in range(len(result)):
            merged = merge_ranges(fresh_ranges[i], result[j])
            #print("merge_ranges", fresh_ranges[i], result[j], " -> ", merged)
            if merged:
                result[j] = merged
                is_added = True
                break

        if not is_added:
            result.append(fresh_ranges[i])

    return result

def solve(fresh_ranges):
    prev_len = 0
    result = fresh_ranges
    while True:
        result = merge_all_ranges(result)
        if prev_len == len(result):
            break
        prev_len = len(result)

    count = 0
    for result_range in result:
        #print(result_range[0], result_range[1])
        count += result_range[1] - result_range[0] + 1
    return count


def main():
    (fresh_ranges, _) = read_input("input.txt")
    result = solve(fresh_ranges)
    print("Result:", result)




main()