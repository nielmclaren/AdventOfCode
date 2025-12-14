#!/usr/bin/python3

import cProfile
import math
import re
import sys

# Guesses:

def parse_line(line):
    result = {}
    source = line[0:3]
    targets = line[5:].rstrip().split(" ")
    for target in targets:
        result[source] = targets
    return result

def count_paths(edges, source):
    targets = edges[source]
    if "out" in targets:
        return 1

    count = 0
    for target in targets:
        count += count_paths(edges, target)
    return count


def part1(filename):
    edges = {}
    with open(filename) as file:
        for line in file:
            curr_edges = parse_line(line)
            edges.update(curr_edges)

    return count_paths(edges, "you")




def main():
    filename = sys.argv[1]
    result = part1(filename)
    #result = part2(filename)
    print(f"Result: {result}")


main()
#cProfile.run('main()')
