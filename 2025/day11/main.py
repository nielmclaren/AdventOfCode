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
    result[source] = targets
    return result


def count_all_paths(edges, source):
    targets = edges[source]
    if "out" in targets:
        return 1

    count = 0
    for target in targets:
        count += count_all_paths(edges, target)
    return count


def count_paths_after(edges, source, path=None):
    if not path:
        path = source

    targets = edges[source]
    if "out" in targets:
        return 1

    count = 0
    for target in targets:
        count += count_paths_after(edges, target, path + " " + target)
    return count


def count_paths_before(reverse_edges, source, path=None):
    if not path:
        path = source

    if source == "svr":
        print(path)
        return 1

    targets = reverse_edges[source]
    if "svr" in targets:
        print("SVR", path)
        return 1

    count = 0
    for target in targets:
        count += count_paths_before(reverse_edges, target, target + " " + path)
    return count


def count_paths_between(edges, source, target_node, max_depth, path=None):
    if not path:
        path = source

    if max_depth <= 0:
        return 0

    if source == "out":
        return 0

    if source == target_node:
        #print(f"Found {target_node} path ({max_depth}): {path}")
        return 1

    targets = edges[source]

    count = 0
    for target in targets:
        count += count_paths_between(edges, target, target_node, max_depth - 1, path + " " + target)
    return count


def print_breadths_after(edges, source, max_depth):
    frontier = edges[source]
    for depth in range(max_depth):
        print(depth, len(frontier))
        next_frontier = []
        for node in frontier:
            if node != "out" and node != "svr":
                next_frontier.extend(edges[node])
        frontier = next_frontier


def part1(filename):
    edges = {}
    with open(filename) as file:
        for line in file:
            curr_edges = parse_line(line)
            edges.update(curr_edges)

    return count_all_paths(edges, "you")


def part2(filename):
    edges = {}
    with open(filename) as file:
        for line in file:
            curr_edges = parse_line(line)
            edges.update(curr_edges)

    reverse_edges = {}
    for source, targets in edges.items():
        for target in targets:
            if target in reverse_edges:
                reverse_edges[target].append(source)
            else:
                reverse_edges[target] = [source]

    #return count_paths_before(reverse_edges, "dac")
    return count_paths_between(edges, "fft", "dac", 20)


def main():
    filename = sys.argv[1]
    #result = part1(filename)
    result = part2(filename)
    print(f"Result: {result}")


main()
#cProfile.run('main()')
