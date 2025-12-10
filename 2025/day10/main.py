#!/usr/bin/python3

import cProfile
import math
import re
import sys

# Guesses: ...

def indicator_to_bool(char):
    return char == '#'


def get_indicator(line):
    match = re.search(r"\[([^]]*)\]", line)
    #print(match[0])
    result = list(map(indicator_to_bool, list(match[1])))
    return result


def button_to_ints(button):
    return list(map(lambda d: int(d), button.split(",")))


def get_buttons(line):
    match = re.search(r".*\] \((.*)\) \{", line)
    buttons = match[1].split(") (")
    result = list(map(button_to_ints, buttons))
    #print(result)
    return result


def get_state(state, button):
    result = state.copy()
    for wire in button:
        result[wire] = not state[wire]
    return result


def get_fewest_presses(machine):
    print(machine)
    num_presses = 0
    states = [[False] * len(machine["indicator"])]
    while True:
        next_states = []
        for state in states:
            for i, button in enumerate(machine["buttons"]):
                next_state = get_state(state, button)
                if next_state == machine["indicator"]:
                    print("FOUND", num_presses)
                    return num_presses + 1

                next_states.append(next_state)

        states = next_states
        num_presses += 1


def part1(filename):
    machines = []
    with open(filename) as file:
        for line in file:
            # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
            machine = {
                "indicator": get_indicator(line),
                "buttons": get_buttons(line)
            }
            machines.append(machine)

    num_presses = 0
    for machine in machines:
        num_presses += get_fewest_presses(machine)

    return num_presses


def main():
    filename = sys.argv[1]
    result = part1(filename)
    #result = part2(filename)
    print(f"Result: {result}")


main()