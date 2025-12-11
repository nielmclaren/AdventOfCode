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


def get_next_joltage_state(state, button, count=1):
    result = state.copy()
    for wire in button:
        result[wire] -= count
    return result


def is_valid_state(state):
    for joltage in state:
        if joltage < 0:
            return False
    return True


def is_end_state(state):
    for joltage in state:
        if joltage > 0:
            return False
    return True


def get_state_value(state):
    result = 0
    for joltage in state:
        result -= joltage * joltage
    return result


def get_relevant_buttons(buttons, state):
    for i, joltage in enumerate(state):
        if joltage == 0:
            for j, button in enumerate(buttons):
                if i in button:
                    # Just remove the first one.
                    # TODO: Remove all irrelevant buttons at once.
                    result = [x for k, x in enumerate(buttons) if k != j]
                    #print("removed", buttons, state, result)
                    return result
    return buttons


num_visits = 0

low_num_presses = math.inf
high_num_presses = 0
high_num_presses_presses = None

low_value = 0
high_value = -math.inf
high_value_presses = None

def get_fewest_joltage_presses(state, buttons, presses, num_presses):
    global num_visits, low_num_presses, high_num_presses, high_num_presses_presses, low_value, high_value, high_value_presses

    if num_presses < low_num_presses:
        low_num_presses = num_presses
    if num_presses > high_num_presses:
        high_num_presses = num_presses
        high_num_presses_presses = presses

    BUTTON_CHECK_INTERVAL = 5

    next_valued_states = []
    for i, button in enumerate(buttons):
        next_state = get_next_joltage_state(state, button)

        if is_end_state(next_state):
            print("FOUND", num_presses + 1)
            print(f"\tPresses: {presses + str(i)}")
            return num_presses + 1

        elif is_valid_state(next_state):
            valued_state = {
                "state": next_state,
                "value": get_state_value(next_state),
                "pressed": str(i),
            }
            next_valued_states.append(valued_state)


    if len(next_valued_states) <= 0:
        return -1

    next_valued_states.sort(key=lambda d: d["value"], reverse=True)

    for valued_state in next_valued_states:
        next_state = valued_state["state"]
        next_buttons = buttons

        next_value = valued_state["value"]
        if next_value < low_value:
            low_value = next_value
        if next_value > high_value:
            high_value = next_value
            high_value_presses = presses

        if num_presses % BUTTON_CHECK_INTERVAL == 0:
            next_buttons = get_relevant_buttons(buttons, next_state)

        result = get_fewest_joltage_presses(next_state, next_buttons, presses + valued_state["pressed"], num_presses + 1)
        if result >= 0:
            return result

        num_visits += 1
        if num_visits % 100000 == 0:
            print(f"Visits: {num_visits}\tPresses: {low_num_presses} : {high_num_presses}\tValue: {low_value} : {high_value}")
            print(f"\tHigh num presses state: {high_num_presses_presses}")
            print(f"\tHigh value state: {high_value_presses}")
            low_num_presses = math.inf
            high_num_presses = -math.inf
            low_value = math.inf
            high_value = -math.inf

    return -1


# Returns true iff at least one of the buttons has the given index.
def has_index(buttons, index):
    for button in buttons:
        if index in button:
            return True
    return False


# Build an array where the index is the button index and the value is
# an array of indices which no later button affects but this one does.
def get_button_only_indices(buttons):
    result = []
    for button_index, button in enumerate(buttons):
        remaining_buttons = buttons[button_index+1:]
        button_result = []
        for index in button:
            if not has_index(remaining_buttons, index):
                button_result.append(index)
        result.append(button_result)
    return result


button_only_indices = []


def get_button_only_index(button_index, state):
    indices = button_only_indices[button_index]
    if len(indices) <= 0:
        return -1

    if len(indices) == 1:
        return indices[0]

    indices.sort(key=lambda d: state[d], reverse=True)

    return indices[0]


def get_fewest_joltage_presses_ordered(state, buttons, presses, num_presses):
    global button_only_indices

    buttons.sort(key=len, reverse=True)

    button_only_indices = get_button_only_indices(buttons)

    return get_fewest_joltage_presses_ordered_helper(state, buttons, 0, presses, num_presses)


def get_fewest_joltage_presses_ordered_helper(state, buttons, button_start_index, presses, num_presses):
    if is_end_state(state):
        print("FOUND", num_presses)
        print(presses)
        return num_presses

    elif not is_valid_state(state):
        #print(num_presses, "\t", state, "\t", presses)
        return -1

    num_buttons = len(buttons)
    for button_index in range(button_start_index, num_buttons):
        button = buttons[button_index]

        index = get_button_only_index(button_index, state)
        if index >= 0 and state[index] > 0:
            # Jump
            jump_count = state[index]
            next_state = get_next_joltage_state(state, button, jump_count)
            #print(f"JUMP {button} by {state[index]}", index, state, next_state)
            result = get_fewest_joltage_presses_ordered_helper(next_state, buttons, button_index, presses + (str(button_index) * jump_count), num_presses + jump_count)
            if result >= 0:
                return result

        else:
            next_state = get_next_joltage_state(state, button)
            result = get_fewest_joltage_presses_ordered_helper(next_state, buttons, button_index, presses + str(button_index), num_presses + 1)
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
        #num_presses += get_fewest_joltage_presses(machine["joltages"], machine["buttons"], "", 0)
        num_presses += get_fewest_joltage_presses_ordered(machine["joltages"], machine["buttons"], "", 0)

    return num_presses


def main():
    filename = sys.argv[1]
    #result = part1(filename)
    result = part2(filename)
    print(f"Result: {result}")


main()
#cProfile.run('main()')
