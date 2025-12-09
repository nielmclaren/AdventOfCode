#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...

NONE = 0
RED = 1
GREEN = 2
OUTER = 3

def get_area(coords0, coords1):
    result = abs(coords1[0] - coords0[0] + 1) * abs(coords1[1] - coords0[1] + 1)
    #print(coords0, coords1, result)
    return result

def part1(filename):
    coords = []
    with open(filename) as file:
        for line in file:
            coords.append(list(map(int, line.split(","))))

    largest_area = 0
    for i in range(len(coords) - 1):
        for j in range(1, len(coords)):
            area = get_area(coords[i], coords[j])
            if area > largest_area:
                largest_area = area

    return largest_area

def get_offset(step):
    match step:
        case (-1, 0):
            return (0, 1)
        case (1, 0):
            return (0, -1)
        case (0, -1):
            return (-1, 0)
        case (0, 1):
            return (1, 0)

    print("ERROR get_offset got bad step", step)


# Walk the border of the rectangle with opposite corners coord0 and coord1 to
# check whether it overlaps with an OUTER cell in the grid.
def border_has_outer(grid, width, coord0, coord1):
    if coord0[0] == coord1[0]:
        step = int((coord1[1] - coord0[1])/abs(coord1[1] - coord0[1]))
        for y in range(coord0[1], coord1[1], step):
            if grid[y * width + coord0[0]] == OUTER:
                return True

    elif coord0[1] == coord1[1]:
        step = int((coord1[0] - coord0[0])/abs(coord1[0] - coord0[0]))
        for x in range(coord0[0], coord1[0], step):
            if grid[coord0[1] * width + x] == OUTER:
                return True


    else:
        coords = [coord0, [coord1[0], coord0[1]], coord1, [coord0[0], coord1[1]]]
        prev_coord = coords[-1]
        for coord in coords:
            if coord[0] == prev_coord[0]:
                step = int((coord[1] - prev_coord[1])/abs(coord[1] - prev_coord[1]))
                for y in range(prev_coord[1], coord[1], step):
                    if grid[y * width + coord[0]] == OUTER:
                        return True

            elif coord[1] == prev_coord[1]:
                step = int((coord[0] - prev_coord[0])/abs(coord[0] - prev_coord[0]))
                for x in range(prev_coord[0], coord[0], step):
                    if grid[coord[1] * width + x] == OUTER:
                        return True

            prev_coord = coord

    return False



def part2(filename):
    global NONE, RED, GREEN, OUTER

    coords = []
    highest_x = 0
    highest_y = 0
    with open(filename) as file:
        for line in file:
            coord = list(map(int, line.split(",")))
            coords.append(coord)

            if coord[0] > highest_x:
                highest_x = coord[0]
            if coord[1] > highest_y:
                highest_y = coord[1]

    width = highest_x + 2
    height = highest_y + 2
    print(f"Width: {width}, Height: {height}")
    grid = [NONE] * width * height

    if True:
        # Outers
        prev_coord = coords[-1]
        for coord in coords:
            if coord[0] == prev_coord[0]:
                step = int((coord[1] - prev_coord[1])/abs(coord[1] - prev_coord[1]))
                offset = get_offset((0, step))
                for y in range(prev_coord[1], coord[1] + step, step):
                    grid[(y + offset[1]) * width + coord[0] + offset[0]] = OUTER

            elif coord[1] == prev_coord[1]:
                step = int((coord[0] - prev_coord[0])/abs(coord[0] - prev_coord[0]))
                offset = get_offset((step, 0))
                for x in range(prev_coord[0], coord[0] + step, step):
                    grid[(coord[1] + offset[1]) * width + x + offset[0]] = OUTER

            prev_coord = coord

    if True:
        # Borders
        prev_coord = coords[-1]
        for coord in coords:
            if coord[0] == prev_coord[0]:
                step = int((coord[1] - prev_coord[1])/abs(coord[1] - prev_coord[1]))
                offset = get_offset((0, step))
                for y in range(prev_coord[1] + step, coord[1], step):
                    grid[y * width + coord[0]] = GREEN

            elif coord[1] == prev_coord[1]:
                step = int((coord[0] - prev_coord[0])/abs(coord[0] - prev_coord[0]))
                offset = get_offset((step, 0))
                for x in range(prev_coord[0] + step, coord[0], step):
                    grid[coord[1] * width + x] = GREEN

            prev_coord = coord

    # Corners
    for i, coord in enumerate(coords):
        prev_coord = coords[(i - 1) % len(coords)]
        next_coord = coords[(i + 1) % len(coords)]
        grid[coord[1] * width + coord[0]] = RED


    if False:
        # Print
        print("")
        for y in range(height):
            for x in range(width):
                value = grid[y * width + x]
                if value == NONE:
                    print(".", end="")
                elif value == RED:
                    print("#", end="")
                elif value == GREEN:
                    print("@", end="")
                elif value == OUTER:
                    print("?", end="")
                else:
                    print("x", end="")
            print("")
        print("")

    largest_area = 0
    largest_coord0 = None
    largest_coord1 = None
    for i in range(len(coords) - 1):
        for j in range(1, len(coords)):
            area = get_area(coords[i], coords[j])
            if area > largest_area:
                if not border_has_outer(grid, width, coords[i], coords[j]):
                    largest_area = area
                    largest_coord0 = coords[i]
                    largest_coord0 = coords[j]

    print(largest_coord0, largest_coord1)

    return largest_area

def main():
    #result = part1("test.txt")
    #result = part1("input.txt")
    #result = part2("test.txt")
    result = part2("input.txt")
    print(f"Result: {result}")

# NOTE: You're assuming it's going clockwise, if it's bork try counter-clockwise.


main()