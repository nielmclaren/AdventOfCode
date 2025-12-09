#!/usr/bin/python3

import cProfile
import math
import re

# Guesses:
# 4472716059 (too high),
# 1389211740 (too low),
# 1544327824 (too low)
# 1544327824 - still same with fix for boundaries writing over bad cells.
#

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

def get_border_coords(coords):
    print("Get border coords... ", end="")
    result = []
    prev_coord = coords[-1]
    for coord in coords:
        if coord[0] == prev_coord[0]:
            step = int((coord[1] - prev_coord[1])/abs(coord[1] - prev_coord[1]))
            for y in range(prev_coord[1], coord[1], step):
                border_coord = [coord[0], y]
                result.append(border_coord)

        elif coord[1] == prev_coord[1]:
            step = int((coord[0] - prev_coord[0])/abs(coord[0] - prev_coord[0]))
            for x in range(prev_coord[0], coord[0], step):
                border_coord = [x, coord[1]]
                result.append(border_coord)

        prev_coord = coord
    print("done.")
    return result

def get_border_coords_grid(coords, result):
    print("Get border coords grid... ", end="")
    prev_coord = coords[-1]
    for coord in coords:
        if coord[0] == prev_coord[0]:
            step = int((coord[1] - prev_coord[1])/abs(coord[1] - prev_coord[1]))
            for y in range(prev_coord[1], coord[1], step):
                border_coord = [coord[0], y]
                result[coord_to_str(border_coord)] = False

        elif coord[1] == prev_coord[1]:
            step = int((coord[0] - prev_coord[0])/abs(coord[0] - prev_coord[0]))
            for x in range(prev_coord[0], coord[0], step):
                border_coord = [x, coord[1]]
                result[coord_to_str(border_coord)] = False

        prev_coord = coord
    print("done.")
    return result

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

def get_dir(a, b):
    if a[0] == b[0]:
        diff = b[1] - a[1]
        return [0, int(diff / abs(diff))]
    if a[1] == b[1]:
        diff = b[0] - a[0]
        return [int(diff / abs(diff)), 0]
    print("ERROR")


def get_bad_coords(coords):
    print("Get bad coords... ", end="")
    result = []

    # Corners
    for i, curr_coord in enumerate(coords):
        prev_coord = coords[(i - 1) % len(coords)]
        next_coord = coords[(i + 1) % len(coords)]
        start_dir = get_dir(prev_coord, curr_coord)
        end_dir = get_dir(curr_coord, next_coord)

        if start_dir[0] == 0:
            # Vertical to horizontal
            if start_dir[1] == end_dir[0]:
                # Inner corner
                result.append([x - y + z for x, y, z in zip(curr_coord, start_dir, end_dir)])
            else:
                # Outer corner
                result.append([x + y - z for x, y, z in zip(curr_coord, start_dir, end_dir)])
                result.append([x + y for x, y, z in zip(curr_coord, start_dir, end_dir)])
                result.append([x - z for x, y, z in zip(curr_coord, start_dir, end_dir)])
        else:
            # Horizontal to vertical
            if start_dir[0] == end_dir[1]:
                # Outer corner
                result.append([x + y - z for x, y, z in zip(curr_coord, start_dir, end_dir)])
                result.append([x + y for x, y, z in zip(curr_coord, start_dir, end_dir)])
                result.append([x - z for x, y, z in zip(curr_coord, start_dir, end_dir)])
            else:
                # Inner corner
                result.append([x - y + z for x, y, z in zip(curr_coord, start_dir, end_dir)])

    if True:
        # Outers
        prev_coord = coords[-1]
        for i, coord in enumerate(coords):
            if coord[0] == prev_coord[0]:
                step = int((coord[1] - prev_coord[1])/abs(coord[1] - prev_coord[1]))
                offset = get_offset((0, step))
                for y in range(prev_coord[1] + step, coord[1], step):
                    result.append([coord[0] + offset[0], y + offset[1]])

            elif coord[1] == prev_coord[1]:
                step = int((coord[0] - prev_coord[0])/abs(coord[0] - prev_coord[0]))
                offset = get_offset((step, 0))
                for x in range(prev_coord[0] + step, coord[0], step):
                    result.append([x + offset[0], coord[1] + offset[1]])

            prev_coord = coord

    print("done.")
    return result

def get_bad_coords_grid(coords, grid):
    result = []
    print("Get bad coords grid... ", end="")

    # Corners
    for i, curr_coord in enumerate(coords):
        prev_coord = coords[(i - 1) % len(coords)]
        next_coord = coords[(i + 1) % len(coords)]
        start_dir = get_dir(prev_coord, curr_coord)
        end_dir = get_dir(curr_coord, next_coord)

        if start_dir[0] == 0:
            # Vertical to horizontal
            if start_dir[1] == end_dir[0]:
                # Inner corner
                bad_coord = [x - y + z for x, y, z in zip(curr_coord, start_dir, end_dir)]
                grid[coord_to_str(bad_coord)] = True
                result.append(bad_coord)
            else:
                # Outer corner
                bad_coord = [x + y - z for x, y, z in zip(curr_coord, start_dir, end_dir)]
                grid[coord_to_str(bad_coord)] = True
                result.append(bad_coord)

                bad_coord = [x + y for x, y, z in zip(curr_coord, start_dir, end_dir)]
                grid[coord_to_str(bad_coord)] = True
                result.append(bad_coord)

                bad_coord = [x - z for x, y, z in zip(curr_coord, start_dir, end_dir)]
                grid[coord_to_str(bad_coord)] = True
                result.append(bad_coord)

        else:
            # Horizontal to vertical
            if start_dir[0] == end_dir[1]:
                # Outer corner
                bad_coord = [x + y - z for x, y, z in zip(curr_coord, start_dir, end_dir)]
                grid[coord_to_str(bad_coord)] = True
                result.append(bad_coord)

                bad_coord = [x + y for x, y, z in zip(curr_coord, start_dir, end_dir)]
                grid[coord_to_str(bad_coord)] = True
                result.append(bad_coord)

                bad_coord = [x - z for x, y, z in zip(curr_coord, start_dir, end_dir)]
                grid[coord_to_str(bad_coord)] = True
                result.append(bad_coord)

            else:
                # Inner corner
                bad_coord = [x - y + z for x, y, z in zip(curr_coord, start_dir, end_dir)]
                grid[coord_to_str(bad_coord)] = True
                result.append(bad_coord)

    if True:
        # Outers
        prev_coord = coords[-1]
        for i, coord in enumerate(coords):
            if coord[0] == prev_coord[0]:
                step = int((coord[1] - prev_coord[1])/abs(coord[1] - prev_coord[1]))
                offset = get_offset((0, step))
                for y in range(prev_coord[1] + step, coord[1], step):
                    bad_coord = [coord[0] + offset[0], y + offset[1]]
                    grid[coord_to_str(bad_coord)] = True
                    result.append(bad_coord)

            elif coord[1] == prev_coord[1]:
                step = int((coord[0] - prev_coord[0])/abs(coord[0] - prev_coord[0]))
                offset = get_offset((step, 0))
                for x in range(prev_coord[0] + step, coord[0], step):
                    bad_coord = [x + offset[0], coord[1] + offset[1]]
                    grid[coord_to_str(bad_coord)] = True
                    result.append(bad_coord)

            prev_coord = coord

    print("done.")
    return (result, grid)

# Options are (1, 0) to (0, 1)

def rect_contains_coord(coord0, coord1, test_coord):
    low_x = min(coord0[0], coord1[0])
    low_y = min(coord0[1], coord1[1])
    high_x = max(coord0[0], coord1[0])
    high_y = max(coord0[1], coord1[1])
    x = test_coord[0]
    y = test_coord[1]
    return low_x < x and x < high_x and low_y < y and y < high_y

def contains_any_bad_coord(coords, i, j, bad_coords):
    for bad_coord in bad_coords:
        if rect_contains_coord(coords[i], coords[j], bad_coord):
            return True
    return False


def coord_to_str(coord):
    return ",".join(list(map(str, coord)))


def part2(filename):
    coords = []
    highest_x = 0
    highest_y = 0

    print("Reading coords")
    with open(filename) as file:
        for line in file:
            coord = list(map(int, line.split(",")))
            coords.append(coord)

            if coord[0] > highest_x:
                highest_x = coord[0]
            if coord[1] > highest_y:
                highest_y = coord[1]
    print("Done")

    width = highest_x + 2
    height = highest_y + 2
    print(f"Width: {width}, Height: {height}")

    num_coords = len(coords)

    grid = {}
    (bad_coords, grid) = get_bad_coords_grid(coords, grid)
    grid = get_border_coords_grid(coords, grid)

    if False:
        # Print grid
        print("Printing the grid.")
        for y in range(height):
            for x in range(width):
                coord_id = coord_to_str([x, y])
                if coord_id in grid and grid[coord_id]:
                    print("x", end="")
                elif [x, y] in coords:
                    print("#", end="")
                else:
                    print(".", end="")
            print("")
        print("Done")

    rects = []
    for i in range(num_coords - 1):
        for j in range(1, num_coords):
            area = get_area(coords[i], coords[j])
            rects.append({
                "coord0": coords[i],
                "coord1": coords[j],
                "coord0_index": i,
                "coord1_index": j,
                "area": area
            })

    print("Sorting rects by area.")
    rects.sort(key=lambda d: d["area"], reverse=True)
    print("Done")

    if True:
        largest_rect = None
        num_rects = len(rects)
        for i, rect in enumerate(rects):
            if i % 1000 == 0:
                print(f"{i} / {num_rects} ({i / num_rects})")
            if not contains_any_bad_coord(coords, rect["coord0_index"], rect["coord1_index"], bad_coords):
                largest_rect = rect
                break

        return largest_rect["area"]

def main():
    #result = part1("test.txt")
    #result = part1("input.txt")
    #result = part2("test.txt")
    #result = part2("test2.txt")
    #result = part2("test3.txt")
    result = part2("input.txt")
    print(f"Result: {result}")

# NOTE: You're assuming it's going clockwise, if it's bork try counter-clockwise. Can just reverse coords after read.
#
# ^ tried this but then the guess is much too low. It seems like it _is_ clockwise.



main()