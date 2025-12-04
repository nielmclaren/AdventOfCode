#!/usr/bin/python3

import math
import re

# Guesses:


def get_highest_digit_index(bank, start, end):
    highest = 0
    highest_index = -1
    for index in range(start, end):
        digit = int(bank[index])
        if digit > highest:
            highest = digit
            highest_index = index
    return highest_index


def calc_max_joltage(bank, num_batts):
    accum = ""
    digit_index = -1
    for i in range(num_batts):
        digit_index = get_highest_digit_index(bank, digit_index + 1, len(bank) - num_batts + i + 1)
        accum += bank[digit_index]

    result = int(accum)
    print(bank, result)
    return result



def solve(filename, num_batts):
    result = 0
    with open(filename) as file:
        for line in file:
            result += calc_max_joltage(line.rstrip(), num_batts)

    print(result)


#solve("input.txt", 3)
solve("input.txt", 12)
#solve("test.txt", 2)
#solve("test.txt", 12)