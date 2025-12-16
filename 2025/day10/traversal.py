import itertools
from button_ref import ButtonRef

class Traversal():
    def __init__(self, buttons):
        self.buttons = buttons
        self.groups = self.__get_button_permu_groups(buttons)

        print("Buttons:", self.buttons)
        print("Permutation groups:", self.groups)

    def get_button(self, button_ref):
        return self.buttons[self.groups[button_ref.group][button_ref.permu][button_ref.button]]

    def num_groups(self):
        return len(self.groups)

    def get_permutations(self, group_index):
        return [ButtonRef(group_index, permu_index, 0) for permu_index in range(len(self.groups[group_index]))]

    def get_button_index(self, button_ref):
        return self.groups[button_ref.group][button_ref.permu][button_ref.button]

    def next(self, button_ref):
        result = ButtonRef(button_ref.group, button_ref.permu, button_ref.button)
        result.button += 1
        if result.button >= len(self.groups[result.group][0]):
            result.button = 0
            result.permu = 0
            result.group += 1

        if result.group >= len(self.groups):
            return None

        return result

    def is_last_button(self, button_ref):
        return button_ref.group + 1 == len(self.groups) and button_ref.button + 1 == len(self.groups[-1][0])

    def is_last_button_in_group(self, button_ref):
        return button_ref.button + 1 == len(self.groups[button_ref.group][0])

    def next_group_index(self, button_ref):
        return self.next(button_ref).group

    def all_reachable_joltages(self, joltages, button_ref):
        for i, joltage in enumerate(joltages):
            if joltage > 0 and not self.__is_reachable_joltage_index(i, button_ref):
                return False
        return True

    def __is_reachable_joltage_index(self, joltage_index, button_ref):
        for group_index in range(button_ref.group, len(self.groups)):
            permu_index = button_ref.permu if group_index == button_ref.group else 0
            permu = self.groups[group_index][permu_index]
            low_permu_button_index = button_ref.button if group_index == button_ref.group else 0
            for permu_button_index in range(low_permu_button_index, len(permu)):
                button_index = permu[permu_button_index]
                button = self.buttons[button_index]
                if joltage_index in button:
                    return True
        return False

    def __get_button_permu_groups(self, buttons):
        groups = []
        largest_button = max(map(len, buttons))
        for i in range(largest_button, -1, -1):
            group = [j for j, button in enumerate(buttons) if len(button) == i + 1]
            if len(group) > 0:
                groups.append(group)

        permu_groups = []
        for group in groups:
            if len(group) > 1:
                permu_groups.append(list(itertools.permutations(group)))
            else:
                permu_groups.append([group])

        return permu_groups