#!/usr/bin/python3

import cProfile
import math
import re

# Guesses: ...


def get_dist_sq(coord0, coord1):
    return pow(coord1[0] - coord0[0], 2) + pow(coord1[1] - coord0[1], 2) + pow(coord1[2] - coord0[2], 2)

def merge_circuits(circuits, coord0_str, coord1_str):
    index0 = [i for i, x in enumerate(circuits) if coord0_str in x][0]
    index1 = [i for i, x in enumerate(circuits) if coord1_str in x][0]

    if index0 == index1:
        # Already in the same circuit.
        return circuits.copy()

    result = [circuits[index0] + circuits[index1]]
    for i, circuit in enumerate(circuits):
        if i != index0 and i != index1:
            result.append(circuit)

    return result

def solve(filename, num_connections):
    coords = []
    with open(filename) as file:
        for line in file:
            coord = list(map(int, line.split(",")))
            coords.append(coord)

    num_coords = len(coords)

    coord_pairs = []
    for i in range(num_coords - 1):
        for j in range(i + 1, num_coords):
            coord_pairs.append({
                "coord0": coords[i],
                "coord1": coords[j],
                "dist_sq": get_dist_sq(coords[i], coords[j])
            })

    coord_pairs.sort(key=lambda d: d["dist_sq"])

    # An array of array of coord strings.
    circuits = list(map(lambda d: [",".join(map(str, d))], coords))

    for i in range(num_connections):
        #print(circuits)
        coord_pair = coord_pairs[i]
        coord0_str = ",".join(map(str, coord_pair["coord0"]))
        coord1_str = ",".join(map(str, coord_pair["coord1"]))

        circuits = merge_circuits(circuits, coord0_str, coord1_str)


    circuits.sort(key=lambda d: -len(d))

    print("Circuits:")

    for circuit in circuits:
        print(circuit)

    TOP_THREE = 3
    mult = 1
    for i in range(TOP_THREE):
        mult *= len(circuits[i])
    return mult


def main():
    #result = solve("test.txt", 10)
    result = solve("input.txt", 1000)
    print(f"Result: {result}")


main()