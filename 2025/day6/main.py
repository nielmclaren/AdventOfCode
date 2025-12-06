#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...


def read_input(filename):
    number_sets = []
    operators = []
    with open(filename) as file:
        for line in file:
            cols = re.split(r"\s+", line.strip())
            print(cols)
            for i, col in enumerate(cols):
                if col == '+' or col == '*':
                    operators.append(col)
                else:
                    if i >= len(number_sets):
                        number_sets.append([int(col)])
                    else:
                        number_sets[i].append(int(col))

    return (number_sets, operators)

def main():
    (number_sets, operators) = read_input("input.txt")
    sum = 0
    for i, operator in enumerate(operators):
        number_set = number_sets[i]
        result = number_set[0]
        for i in range(1, len(number_set)):
            if operator == '+':
                result += number_set[i]
            elif operator == '*':
                result *= number_set[i]
        sum += result
    print(sum)


main()