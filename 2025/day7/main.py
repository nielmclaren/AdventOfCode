#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...

def solve(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines.reverse()

        totals = [1] * len(lines[0])

        for line in lines:
            next_totals = []

            for i, char in enumerate(line.rstrip()):
                if char == '^':
                    next_totals.append(totals[i - 1] + totals[i + 1])

                elif char == '.':
                    next_totals.append(totals[i])

                elif char == 'S':
                    return totals[i]

                else:
                    print("ERROR Bad character.", char)

            totals = next_totals




def main():
    result = solve("input.txt")
    print(f"Result: {result}")


main()