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


def get_joltages(line):
    match = re.search(r"\{(.*)\}", line)
    joltages = match[1].split(",")
    result = list(map(int, joltages))
    #print(result)
    return result


def get_next_indicator_state(state, button):
    result = state.copy()
    for wire in button:
        result[wire] = not state[wire]
    return result


def get_fewest_indicator_presses(machine):
    num_presses = 0
    states = [[False] * len(machine["indicator"])]
    while True:
        next_states = []
        for state in states:
            for i, button in enumerate(machine["buttons"]):
                next_state = get_next_indicator_state(state, button)
                if next_state == machine["indicator"]:
                    print("FOUND", num_presses)
                    return num_presses + 1

                next_states.append(next_state)

        states = next_states
        num_presses += 1


def get_next_joltage_state(state, button):
    result = state.copy()
    for wire in button:
        result[wire] += 1
    return result


def is_valid_state(machine, state):
    for i, value in enumerate(state):
        if machine["joltages"][i] < value:
            return False
    return True


def get_state_value(machine, state):
    result = 0
    for i, value in enumerate(state):
        diff = machine["joltages"][i] - value
        result -= pow(diff, 2)
    return result


def get_fewest_joltage_presses(machine, state, presses):
    next_valued_states = []
    for i, button in enumerate(machine["buttons"]):
        next_state = get_next_joltage_state(state, button)
        next_presses = presses + [i]

        if next_state == machine["joltages"]:
            next_presses.sort()
            print("FOUND", len(next_presses), next_presses)
            return len(next_presses)

        elif is_valid_state(machine, next_state):
            valued_state = {
                "state": next_state,
                "value": get_state_value(machine, next_state),
                "presses": next_presses
            }
            next_valued_states.append(valued_state)


    if len(next_valued_states) <= 0:
        return -1

    next_valued_states.sort(key=lambda d: d["value"], reverse=True)

    for valued_state in next_valued_states:
        #print(valued_state["value"], valued_state["state"], valued_state["presses"])
        result = get_fewest_joltage_presses(machine, valued_state["state"], valued_state["presses"])
        if result >= 0:
            return result

    return -1


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
        num_presses += get_fewest_indicator_presses(machine)

    return num_presses


def part2(filename):
    machines = []
    with open(filename) as file:
        for line in file:
            # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
            machine = {
                "buttons": get_buttons(line),
                "joltages": get_joltages(line)
            }
            machines.append(machine)

    num_machines = len(machines)
    num_presses = 0
    for i, machine in enumerate(machines):
        print(f"{i} / {num_machines} ({i / num_machines})")
        num_presses += get_fewest_joltage_presses(machine, [0] * len(machine["joltages"]), [])
        break

    return num_presses


def main():
    filename = sys.argv[1]
    #result = part1(filename)
    result = part2(filename)
    print(f"Result: {result}")


main()