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


def calc_max_joltage(bank):
    tens_digit_index = get_highest_digit_index(bank, 0, len(bank) - 1)
    tens_digit = bank[tens_digit_index]
    ones_digit = bank[get_highest_digit_index(bank, tens_digit_index + 1, len(bank))]
    result = int(f"{tens_digit}{ones_digit}")
    print(bank, result)
    return result



def solve(filename):
    result = 0
    with open(filename) as file:
        for line in file:
            result += calc_max_joltage(line.rstrip())

    print(result)


solve("input.txt")
#solve("test.txt")