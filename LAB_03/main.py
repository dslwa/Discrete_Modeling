from Lab_03 import *

if __name__ == '__main__':
    album_number = "415335"
    rules = [int(album_number[i:i + 2]) for i in range(0, len(album_number), 2)] + [190]
    initial_state = [1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]

    for r in rules:
        print(rule_to_bin(r))

    while True:
        try:
            iterations = int(input("Number of iterations: "))
            if iterations <= 0:
                raise ValueError("Number must be > 0.")
            break
        except ValueError as e:
            print(e)

    boundary_condition = input("(periodic/absorbing): ")
    while boundary_condition not in ["periodic", "absorbing"]:
        print("choose 'periodic' or 'absorbing'.")
        boundary_condition = input("(periodic/absorbing): ")

    states = automaton(initial_state, rules, iterations, boundary_condition)
    save_to_csv(states)
