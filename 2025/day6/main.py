#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...

def read_input(filename):
    number_lines = []
    operator_line = ""
    with open(filename) as file:
        for line in file:
            if line.find("+") < 0:
                # Reverse the string with [::-1]
                number_lines.append(line.rstrip("\n")[::-1] + " ")
            else:
                # Reverse the string with [::-1]
                operator_line = line[::-1]

    # Make sure lines are the same length.
    longest = 0
    for number_line in number_lines:
        if len(number_line) > longest:
            longest = len(number_line)

    for i, number_line in enumerate(number_lines):
        if len(number_line) < longest:
            number_lines[i] = " " + number_line

    return (number_lines, operator_line)


def get_number(number_lines, col):
    result = ""
    for line in number_lines:
        result += line[col:col+1].strip()
    if result == "":
        return 0
    return int(result)


def is_col_empty(number_lines, col):
    for line in number_lines:
        if line[col:col+1] != " ":
            return False
    return True


def mult(nums):
    result = nums[0]
    for i in range(1, len(nums)):
        result *= nums[i]
    return result


def main():
    (number_lines, operator_line) = read_input("input.txt")

    grand_total = 0
    problem_numbers = []
    operator = None
    for col in range(len(number_lines[0])):
        if is_col_empty(number_lines, col):
            if operator == '+':
                #print("sum", problem_numbers, sum(problem_numbers))
                grand_total += sum(problem_numbers)
            elif operator == '*':
                #print("mult", problem_numbers, mult(problem_numbers))
                grand_total += mult(problem_numbers)
            else:
                print("ERROR bad operator", operator)

            problem_numbers = []
            operator = None

        else:
            problem_numbers.append(get_number(number_lines, col))

            if operator is None and operator_line[col:col+1] != " ":
                operator = operator_line[col:col+1]

    print(grand_total)


main()