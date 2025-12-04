#!/usr/bin/python3

import math
import re

# Guesses: 27180728081 (too high), 37556907 (too low), 19219513675 (too high), 19219508902 (just right!)
# Guesses:


def solve(num):
    num_str = str(num)
    length = len(num_str)

    for i in range(1, length):
        if length % i == 0:
            pattern = num_str[0:i]
            count = math.floor(length / i)
            regex = f"^({pattern}){{{count}}}$"
            result = re.search(regex, num_str)
            if result:
                print(num_str, pattern)
                return True

    return False


def solve_cases(cases):
    for num in cases:
        print(num, solve(num))


def solve_range(low, high):
    accum = 0
    for i in range(low, high + 1):
        if solve(i):
            accum += i
    return accum


def main():
    accum = 0
    with open("ranges.txt") as file:
        for line in file:
            ranges = line.split(",")
            for range_str in ranges:
                num_strs = range_str.split("-")
                accum += solve_range(int(num_strs[0]), int(num_strs[1]))

    print(accum)


def test():
    positive_cases = [11, 111, 1111, 1212, 11111, 111111, 121212, 123123]
    negative_cases = [12, 121, 1221, 12121, 21212, 11211, 121211, 123121]

    print("Positive")
    solve_cases(positive_cases)

    print("Negative")
    solve_cases(negative_cases)

def test2():
    print(solve_range(76756725,76781020))

main()