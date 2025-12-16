#!/usr/bin/python3

import cProfile
import itertools
import math
import re
import sys
from button_ref import ButtonRef
from traversal import Traversal

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


def get_next_presses(presses, button_index, num_presses):
    result = presses.copy()
    result[button_index] = num_presses
    return result


def is_solved(joltages):
    return sum(joltages) == 0


# joltages (remaining) [23, 45, 52]
# buttons [ [0, 2, 3],  [1, 2],  [2, 3],  [3] ]
#
def solve(joltages, buttons):
    traversal = Traversal(buttons)
    ref = ButtonRef()

    # Accumulate the number of presses for the button at the same index.
    presses = [0] * len(buttons)

    #print("---")
    #print("Joltages", "\t", "Presses")

    # Iterate through all permutations of the first group and return the lowest num presses.
    lowest_total_num_presses = math.inf
    for button_ref in traversal.get_permutations(ref.group):
        num_presses = helper(joltages, traversal, button_ref, presses)
        if num_presses >= 0 and num_presses < lowest_total_num_presses:
            lowest_total_num_presses = num_presses

    return lowest_total_num_presses


#def helper(joltages, buttons, button_permu_groups, group_index, permu_index, permu_button_index, presses):
def helper(remaining_joltages, traversal, button_ref, presses):
    button_index = traversal.get_button_index(button_ref)

    #print(joltages, "\t", presses, group_index, permu_index, permu_button_index)

    if not traversal.all_reachable_joltages(remaining_joltages, button_ref):
        #print(remaining_joltages, "\t", presses, "UNREACHABLE")
        return -1

    button = traversal.get_button(button_ref)
    max_presses = get_max_presses(remaining_joltages, button)

    if traversal.is_last_button(button_ref):
        # For the last button just max out the number of presses, no decrementing.
        next_presses = get_next_presses(presses, button_index, max_presses)
        next_joltages = get_remaining_joltages(remaining_joltages, button, max_presses)

        # Check for the end condition.
        if is_solved(next_joltages):
            #print(next_joltages, "\t", next_presses, "FOUND", sum(next_presses))
            return sum(next_presses)

        # If maxing out the last button didn't satisfy the end condition then it's a dead end.
        #print(next_joltages, "\t", next_presses, "DEAD END")
        return -1

    else:
        # Start with the maximum number of presses possible and decrement.
        for num_presses in range(max_presses, -1, -1):
            next_presses = get_next_presses(presses, button_index, num_presses)
            next_joltages = get_remaining_joltages(remaining_joltages, button, num_presses)

            # Check for the end condition.
            if is_solved(next_joltages):
                #print(next_joltages, "\t", next_presses, "FOUND", sum(next_presses))
                return sum(next_presses)

            if traversal.is_last_button_in_group(button_ref):
                # Reached the end of the current permutation. Onto the next one.
                next_group_index = traversal.next_group_index(button_ref)

                lowest_total_num_presses = math.inf
                for next_button_ref in traversal.get_permutations(next_group_index):
                    total_num_presses = helper(next_joltages, traversal, next_button_ref, next_presses)
                    if total_num_presses >= 0 and total_num_presses < lowest_total_num_presses:
                        lowest_total_num_presses = total_num_presses
                if lowest_total_num_presses != math.inf:
                    return lowest_total_num_presses

            else:
                # Continue with the next button in the current permutation.
                next_button_ref = traversal.next(button_ref)
                total_num_presses = helper(next_joltages, traversal, next_button_ref, next_presses)
                if total_num_presses >= 0:
                    return total_num_presses

    #print(remaining_joltages, "\t", presses, "END END")
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
        sorted_buttons = machine["buttons"]
        sorted_buttons.sort(key=len, reverse=True)

        print(f"{i} / {num_machines}")
        print("Joltages:", machine["joltages"])
        num_presses = solve(machine["joltages"], sorted_buttons)
        print("Num presses:", num_presses)
        total_num_presses += num_presses

        print("")
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
