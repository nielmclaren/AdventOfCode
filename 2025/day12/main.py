#!/usr/bin/python3

import cProfile
import math
import re
import sys

# Guesses:

SHAPE_WIDTH = 3
SHAPE_HEIGHT = 3

def parse_shapes(file):
    global SHAPE_HEIGHT

    NUM_SHAPES = 6

    result = []
    for i in range(NUM_SHAPES):
        line = file.readline()
        assert(str(i) == line[0:line.find(":")])

        shape = 0

        for _ in range(SHAPE_HEIGHT):
            line = file.readline().rstrip()
            for char in line:
                shape <<= 1
                shape += (1 if char == '#' else 0)

        assert(file.readline().rstrip() == "")
        result.append(shape)
    return result


def parse_regions(file):
    result = []
    for line in file:
        match = re.search(r"^(\d*)x(\d*): (.*)$", line.rstrip())
        width = int(match[1])
        height = int(match[2])
        counts = list(map(int, match[3].split(" ")))
        result.append({
            "width": width,
            "height": height,
            "counts": counts,
        })
    return result


def parse(file):
    shapes = parse_shapes(file)
    regions = parse_regions(file)
    return (shapes, regions)


def get_shape_area(shape):
    result = 0
    while shape != 0:
        result += shape & 1
        shape >>= 1
    return result


def get_min_area(shape_areas, counts):
    return sum([shape_areas[i] * count for i, count in enumerate(counts)])


def print_stats(shapes, regions):
    shape_areas = [get_shape_area(shape) for shape in shapes]

    num_definitely_fits = 0
    num_definitely_doesnt = 0
    num_not_sure = 0

    for region in regions:
        available_area = region["width"] * region["height"]
        counts = region["counts"]
        max_area = SHAPE_WIDTH * SHAPE_HEIGHT * sum(counts)
        min_area = get_min_area(shape_areas, counts)

        if available_area >= max_area:
            num_definitely_fits += 1
        elif available_area < min_area:
            num_definitely_doesnt += 1
        else:
            num_not_sure += 1
            print(f"{available_area}\t{min_area} - {max_area}\t({sum(counts)})")


    print(f"Definitely fits: {num_definitely_fits}")
    print(f"Definitely doesn't: {num_definitely_doesnt}")
    print(f"Not sure: {num_not_sure}")


def part1(filename):
    with open(filename) as file:
        (shapes, regions) = parse(file)

    print_stats(shapes, regions)

    return 0


def main():
    filename = sys.argv[1]
    result = part1(filename)
    #result = part2(filename)
    print(f"Result: {result}")


main()
#cProfile.run('main()')
