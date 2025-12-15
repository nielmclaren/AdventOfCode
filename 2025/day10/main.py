#!/usr/bin/python3

import cProfile
import math
import re
import sys

# Guesses: 17785 (too high)

def indicator_to_bool(char):
    return char == '#'


def get_indicator(line):
    match = re.search(r"\[([^]]*)\]", line)
    #print(match[0])
    result = list(map(indicator_to_bool, list(match[1])))
    return result


def button_to_ints(button):
    return list(map(int, button.split(",")))


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


def get_max_presses(joltages, button):
    return min([joltages[wire] for wire in button])


def get_remaining_joltages(joltages, button, num_presses):
    return [joltage - (num_presses if i in button else 0) for i, joltage in enumerate(joltages)]


def get_joltages_after_presses(starting_joltages, buttons, presses):
    result = starting_joltages.copy()
    for i, button in enumerate(buttons):
        num_presses = presses[i]
        for wire in button:
            result[wire] -= num_presses
    return result


def is_reachable_joltage_index(joltage_index, buttons, start_button_index):
    for button_index in range(start_button_index, len(buttons)):
        if joltage_index in buttons[button_index]:
            return True
    return False


def all_reachable_joltages(joltages, buttons, start_button_index):
    for i, joltage in enumerate(joltages):
        if joltage > 0 and not is_reachable_joltage_index(i, buttons, start_button_index):
            return False
    return True


def solve(joltages, buttons, button_index=0, presses=None):
    num_buttons = len(buttons)

    if not presses:
        presses = [0] * num_buttons

    if button_index >= num_buttons:
        return -1

    if not all_reachable_joltages(joltages, buttons, button_index):
        return -1

    button = buttons[button_index]
    max_presses = get_max_presses(joltages, button)

    for num_presses in range(max_presses, -1, -1):
        presses[button_index] = num_presses
        next_joltages = get_remaining_joltages(joltages, button, num_presses)

        if sum(next_joltages) == 0:
            print("FOUND", sum(presses), presses, next_joltages)
            return sum(presses)

        #print(presses, next_joltages)

        total_num_presses = solve(next_joltages, buttons, button_index + 1, presses)
        if total_num_presses >= 0:
            return total_num_presses

    return -1


def part2(filename):
    EXPECTED_PREFIX = "Expected: "
    machines = []
    expected = -1
    with open(filename) as file:
        for line in file:
            if line[0:len(EXPECTED_PREFIX)] == EXPECTED_PREFIX:
                expected = int(line[len(EXPECTED_PREFIX):])
                continue

            # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
            machine = {
                "buttons": get_buttons(line),
                "joltages": get_joltages(line)
            }
            machines.append(machine)

    num_presses = 0
    num_machines = len(machines)
    for i, machine in enumerate(machines):
        sorted_buttons = machine["buttons"]
        sorted_buttons.sort(key=len, reverse=True)

        print(f"{i} / {num_machines}")
        print(machine["joltages"])
        print(sorted_buttons)
        print("---")
        num_presses += solve(machine["joltages"], sorted_buttons)

    return (num_presses, expected)


def main():
    filename = sys.argv[1]
    (result, expected) = part2(filename)
    print(f"Result: {result}")
    if expected >= 0:
        print(f"Expected: {expected}")

    # TODO: Don't forget you need to address the issue with multiple buttons of the same length. (test7)


main()
#cProfile.run('main()')
