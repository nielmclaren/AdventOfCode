#!/usr/bin/python3

import math
import re

# Guesses: ...


THRESHOLD = 4


def grid_value(grid, grid_width, x, y):
    return grid[y * grid_width + x]


def is_in_grid(grid_width, grid_height, x, y):
    return x >= 0 and x < grid_width and y >= 0 and y < grid_height


def is_accessible(grid, grid_width, grid_height, cx, cy):
    count = 0
    for x in range(cx - 1, cx + 2):
        for y in range(cy - 1, cy + 2):
            if (cx != x or cy != y) and is_in_grid(grid_width, grid_height, x, y) and grid_value(grid, grid_width, x, y):
                count += 1
                if count >= THRESHOLD:
                    return False

    return True


def count_accessible_cells(grid, grid_width, grid_height):
    result = 0
    for cx in range(grid_width):
        for cy in range(grid_height):
            if grid_value(grid, grid_width, cx, cy) and is_accessible(grid, grid_width, grid_height, cx, cy):
                #print(f"{cx},{cy}", grid_value(grid, grid_width, cx, cy))
                result += 1
    return result


def solve(filename):
    grid = []
    grid_width = -1

    with open(filename) as file:
        for line in file:
            for character in line.rstrip():
                grid.append(character == '@')
            if grid_width < 0:
                grid_width = len(grid)

    grid_height = int(len(grid) / grid_width)

    result = count_accessible_cells(grid, grid_width, grid_height)
    print(result)


solve("input.txt")
#solve("test.txt")