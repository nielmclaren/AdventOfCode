#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...


THRESHOLD = 4


grid_width = -1
grid_height = -1


def get_grid_value(grid, x, y):
    return grid[y * grid_width + x]


def set_grid_value(grid, x, y, v):
    grid[y * grid_width + x] = v


def is_in_grid(x, y):
    return x >= 0 and x < grid_width and y >= 0 and y < grid_height


def is_accessible(grid, cx, cy):
    count = 0
    for x in range(cx - 1, cx + 2):
        for y in range(cy - 1, cy + 2):
            if (cx != x or cy != y) and is_in_grid(x, y) and get_grid_value(grid, x, y):
                count += 1
                if count >= THRESHOLD:
                    return False

    return True


def count_accessible_cells(grid):
    result = 0
    for cx in range(grid_width):
        for cy in range(grid_height):
            if get_grid_value(grid, cx, cy) and is_accessible(grid, cx, cy):
                #print(f"{cx},{cy}", grid_value(grid, cx, cy))
                result += 1
    return result


def remove_first_accessible_cell(grid):
    for cx in range(grid_width):
        for cy in range(grid_height):
            if get_grid_value(grid, cx, cy) and is_accessible(grid, cx, cy):
                #print(f"{cx},{cy}", grid_value(grid, cx, cy))
                set_grid_value(grid, cx, cy, False)
                return grid
    return None


def remove_accessible_cells(grid):
    result = grid.copy()
    for cx in range(grid_width):
        for cy in range(grid_height):
            if get_grid_value(grid, cx, cy) and is_accessible(grid, cx, cy):
                #print(f"{cx},{cy}", grid_value(grid, cx, cy))
                set_grid_value(result, cx, cy, False)
    return result


def read_grid(filename):
    global grid_width
    global grid_height

    result = []
    with open(filename) as file:
        for line in file:
            for character in line.rstrip():
                result.append(character == '@')
            if grid_width < 0:
                grid_width = len(result)

        grid_height = int(len(result) / grid_width)

    return result


def solve(filename):
    grid = read_grid(filename)

    num_removed = 0
    while True:
        grid = remove_first_accessible_cell(grid)
        if not grid:
            break
        num_removed += 1

    print(num_removed)


def main():
    solve("input.txt")
    #solve("test.txt")


cProfile.run("main()")