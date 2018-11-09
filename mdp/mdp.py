import copy
import random


def calc_new_utility(state, utility_grid):
    max_util, max_pos = get_max_utility(state, utility_grid)
    utility = reward[state] + gamma * max_util
    return utility, max_pos


def get_max_utility(state, utility_grid):
    up_util = get_up_util(state, utility_grid)
    down_util = get_down_util(state, utility_grid)
    left_util = get_left_util(state, utility_grid)
    right_util = get_right_util(state, utility_grid)

    util_list = [up_util, down_util, left_util, right_util]
    max_util = max(util_list)
    max_pos = util_list.index(max_util)
    return max_util, max_pos


def get_up_util(state, utility_grid):
    up_state = get_up_state(state)
    left_state = get_left_state(state)
    right_state = get_right_state(state)

    util = 0.8 * utility_grid[up_state] + 0.1 * utility_grid[left_state] + 0.1 * utility_grid[right_state]
    return util


def get_down_util(state, utility_grid):
    down_state = get_down_state(state)
    left_state = get_left_state(state)
    right_state = get_right_state(state)

    util = 0.8 * utility_grid[down_state] + 0.1 * utility_grid[left_state] + 0.1 * utility_grid[right_state]
    return util


def get_left_util(state, utility_grid):
    left_state = get_left_state(state)
    up_state = get_up_state(state)
    down_state = get_down_state(state)

    util = 0.8 * utility_grid[left_state] + 0.1 * utility_grid[up_state] + 0.1 * utility_grid[down_state]
    return util


def get_right_util(state, utility_grid):
    right_state = get_right_state(state)
    up_state = get_up_state(state)
    down_state = get_down_state(state)

    util = 0.8 * utility_grid[right_state] + 0.1 * utility_grid[up_state] + 0.1 * utility_grid[down_state]
    return util


def get_up_state(state):
    # Get location if going up
    if state >= 6:
        up_state = state
    else:
        up_state = state + 3
    return up_state


def get_down_state(state):
    # Get location if going down
    if state <= 2:
        down_state = state
    else:
        down_state = state - 3
    return down_state


def get_left_state(state):
    # Get location if going left
    if state % 3 == 0:
        left_state = state
    else:
        left_state = state - 1
    return left_state


def get_right_state(state):
    # Get location if going right
    if state % 3 == 2:
        right_state = state
    else:
        right_state = state + 1
    return right_state


def get_policy_list(utility_grid):
    policy_list = []
    for state in range(len(utility_grid) - 1):
        _, max_pos = get_max_utility(state, utility_grid)
        policy_list.append(max_pos)

    policy_list.append(4)
    return policy_list


def display_results(utility_grid, policy_list):
    print("Policy table calculated:")
    for state in range(len(utility_grid)):
        print(grid_labels[state] + ": " + action_list[policy_list[state]])

    print()

    print("Utilities:")
    for state in range(len(utility_grid)):
        print(grid_labels[state] + ": " + str(utility_grid[state]))

    print()


def init_policy_vector():
    policy_list = []
    for i in range(len(reward) - 1):
        policy_list.append(random.randint(0, 3))
    policy_list.append(4)
    return policy_list


def evaluate_policy(utility_grid, policy_list):
    new_grid = copy.deepcopy(utility_grid)

    for state in range(len(utility_grid) - 1):
        if policy_list[state] == 0:
            new_grid[state] = reward[state] + gamma * get_up_util(state, utility_grid)
        elif policy_list[state] == 1:
            new_grid[state] = reward[state] + gamma * get_down_util(state, utility_grid)
        elif policy_list[state] == 2:
            new_grid[state] = reward[state] + gamma * get_left_util(state, utility_grid)
        else:
            new_grid[state] = reward[state] + gamma + get_right_util(state, utility_grid)

    return new_grid


def value_iteration(new_utility_grid):
    while True:
        utility_grid = copy.deepcopy(new_utility_grid)
        max_change = 0

        for state in range(len(utility_grid) - 1):
            new_utility_grid[state], _ = calc_new_utility(state, utility_grid)
            change = new_utility_grid[state] - utility_grid[state]
            if change > max_change:
                max_change = change

        if max_change < convergence_threshold:
            break

    policy_list = get_policy_list(utility_grid)
    display_results(utility_grid, policy_list)


def policy_iteration(utility_grid):
    policy_list = init_policy_vector()
    while True:
        utility_grid = evaluate_policy(utility_grid, policy_list)
        unchanged = True

        for state in range(len(utility_grid) - 1):
            new_utility, max_pos = calc_new_utility(state, utility_grid)
            if new_utility > utility_grid[state]:
                policy_list[state] = max_pos
                unchanged = False

        if unchanged:
            break

    display_results(utility_grid, policy_list)


reward = [-1, -1, -1, -1, -1, -1, -1, -1, 10]
new_utility_grid = [0, 0, 0, 0, 0, 0, 0, 0, 10]
utility_grid = [0, 0, 0, 0, 0, 0, 0, 0, 10]
gamma = 0.9
epsilon = 0.001
convergence_threshold = epsilon * (1 - gamma) / gamma
grid_labels = ['(1, 1)', '(2, 1)', '(3, 1)', '(1, 2)', '(2, 2)', '(3, 2)', '(1, 3)', '(2, 3)', '(3, 3)']
action_list = [
    'UP',
    'DOWN',
    'LEFT',
    'RIGHT',
    'TERMINAL'
]

policy_list = []

r = int(input("Enter r: "))
reward[6] = r

while True:
    user_input = int(input("Enter 1 for Value Iteration, 2 for Policy Iteration, 3 to Exit: "))

    if user_input == 3:
        break
    elif user_input == 1:
        value_iteration(new_utility_grid)
    elif user_input == 2:
        policy_iteration(utility_grid)
