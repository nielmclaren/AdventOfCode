#!/usr/bin/python3

import cProfile
import itertools
import math
import re
import sys

# Guesses: 17785 (too high), 17058 (too low), 17153 (too high)


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


# In each combination, each button may be pressed once or not at all.
def get_combinations(n):
    result = []
    for i in range(n):
        next_result = [[i]]
        for item in result:
            next_result.append(item)
            next_result.append(item + [i])
        result = next_result
    return result


# Get remaining joltages after pressing a button.
def get_remaining_joltages(joltages, button, num_presses=1):
    return [joltage - (num_presses if i in button else 0) for i, joltage in enumerate(joltages)]


# Get remaining joltages after pressing multiple buttons.
def get_remaining_joltages_multi(joltages, buttons, num_presses=1):
    result = joltages
    for button in buttons:
        result = get_remaining_joltages(result, button, num_presses)
    return result


def get_next_presses(presses, button_index, num_presses=1):
    result = presses.copy()
    result[button_index] += num_presses
    return result


def get_next_presses_multi(presses, button_indices, num_presses=1):
    result = presses.copy()
    for button_index in button_indices:
        result[button_index] += num_presses
    return result

def brute_solve(joltages, buttons, multiplier, num_presses, combos, depth=0):
    #print(depth, joltages, num_presses)
    lowest_total_presses = math.inf
    for button in buttons:
        next_joltages = get_remaining_joltages(joltages, button)
        if all(map(lambda d: d == 0, next_joltages)):
            print("found", num_presses + multiplier)
            return num_presses + multiplier

        if any(map(lambda d: d < 0, next_joltages)):
            continue

        total_presses = brute_solve(next_joltages, buttons, multiplier, num_presses + multiplier, combos,  depth+1)
        if total_presses > 0 and total_presses < lowest_total_presses:
            lowest_total_presses = total_presses

    if lowest_total_presses != math.inf:
        return lowest_total_presses

    return -1


def solve(joltages, buttons, multiplier=1, num_presses=0, combos=None):
    #print("solve", joltages)

    if not combos:
        # Build a list of all combinations of button presses to be used throughout.
        combos = get_combinations(len(buttons))

    if sum(joltages) == 0:
        return num_presses

    even_joltage_combos = []
    if all(map(lambda d: d % 2 == 0, joltages)):
        # The joltages are already even.
        even_joltage_combos.append([])

    else:
        # Filter out combinations that don't result in all joltages being even.
        for combo in combos:
            result_joltages = get_remaining_joltages_multi(joltages, list(map(lambda d: buttons[d], combo)))
            if all(map(lambda d: d % 2 == 0 and d >= 0, result_joltages)):
                even_joltage_combos.append(combo)

        if len(even_joltage_combos) <= 0:
            # No more combos. Solve it the old-fashioned way.
            #brute_solve(joltages, buttons, multiplier, num_presses, combos)
            print("ERROR", joltages)
            return -1

    # For each even-making combo, press the required buttons then halve the joltages.
    lowest_total_presses = math.inf
    for combo in even_joltage_combos:
        next_joltages = get_remaining_joltages_multi(joltages, [button for i, button in enumerate(buttons) if i in combo])
        next_num_presses = num_presses + multiplier * len(combo)

        halved_joltages = list(map(lambda d: int(d / 2), next_joltages))

        # Choose the result with the lowest number of total presses.
        total_presses = solve(halved_joltages, buttons, multiplier * 2, next_num_presses, combos)
        if total_presses > 0 and total_presses < lowest_total_presses:
            lowest_total_presses = total_presses

    if lowest_total_presses != math.inf:
        return lowest_total_presses
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

    total_num_presses = 0
    num_machines = len(machines)
    for i, machine in enumerate(machines):
        print(f"{i} / {num_machines}")
        print("Joltages:", machine["joltages"])
        print("Buttons:", machine["buttons"])
        num_presses = solve(machine["joltages"], machine["buttons"])
        print("Num presses:", num_presses)
        if num_presses <= 0:
            print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ")
        total_num_presses += num_presses

        print("")

    return (total_num_presses, expected)


def main():
    filename = sys.argv[1]
    (result, expected) = part2(filename)
    print(f"Result: {result}")
    if expected >= 0:
        print(f"Expected: {expected}")

    # TODO: Don't forget you need to address the issue with multiple buttons of the same length. (test7)


main()
#cProfile.run('main()')
