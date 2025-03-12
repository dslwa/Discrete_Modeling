import numpy as np
import pandas as pd


def border_handling(state, i, boundary):
    if boundary == "periodic":
        if i > 0:
            left = state[i - 1]
        else:
            left = state[-1]

        if i < len(state) - 1:
            right = state[i + 1]
        else:
            right = state[0]
    else:
        if i > 0:
            left = state[i - 1]
        else:
            left = 0

        if i < len(state) - 1:
            right = state[i + 1]
        else:
            right = 0

    return left, right


def rule_to_bin(rule_number):
    return np.array([int(x) for x in f"{rule_number:08b}"])


def compute_new_state(center, left, right, rule):
    index = 7 - (left * 4 + center * 2 + right)
    return rule[index]


def automaton(initial_state, rules, iterations, boundary="periodic"):
    if boundary == "periodic":
        print("periodic set")
    else:
        print("absorbing set")
    states = [initial_state.copy()]
    rule_sets = [rule_to_bin(r) for r in rules]

    for j in range(iterations):
        new_state = initial_state.copy()

        for i in range(len(initial_state)):
            left, right = border_handling(initial_state, i, boundary)

            rule = rule_sets[j % len(rule_sets)]
            new_state[i] = compute_new_state(initial_state[i], left, right, rule)

        initial_state = new_state
        states.append(new_state.copy())

    return states


def save_to_csv(states, filename="automaton_output.csv"):
    df = pd.DataFrame(states)
    df.to_csv(filename, index=False, header=False)
