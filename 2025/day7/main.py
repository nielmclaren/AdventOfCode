#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...

def solve(filename):
    with open(filename) as file:
        beam_stack = []

        first_line = file.readline()
        beam_stack.append((0, first_line.find('S')))

        lines = file.readlines()
        num_lines = len(lines)

        result = 0

        while len(beam_stack) > 0:
            (row, col) = beam_stack.pop()

            if row >= num_lines:
                result += 1
                print(result)
                continue

            char = lines[row][col]

            if char == '^':
                beam_stack.append((row + 1, col - 1))
                beam_stack.append((row + 1, col + 1))

            elif char == '.':
                beam_stack.append((row + 1, col))

            else:
                print("ERROR Bad character.")

        return result



def main():
    result = solve("test.txt")
    print(f"Result: {result}")


main()