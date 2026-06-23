import random
import time

from Algorithms.SearchCommon import child_nodes, build_result, heuristic
from Core.Node import Node
from Core.Utils import is_goal, state_to_tuple


def stochastic_hill_climbing(initial_state, max_steps=1000, seed=None):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state)
    seen = {state_to_tuple(initial_state)}
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        if is_goal(current.state):
            return build_result(current, True, expanded_nodes, generated_nodes, start_time)

        children = child_nodes(current)
        expanded_nodes += 1
        generated_nodes += len(children)
        improving = [
            child
            for child in children
            if heuristic(child.state) < heuristic(current.state)
            and state_to_tuple(child.state) not in seen
        ]

        if not improving:
            break

        weights = [heuristic(current.state) - heuristic(child.state) for child in improving]
        current = rng.choices(improving, weights=weights, k=1)[0]
        seen.add(state_to_tuple(current.state))

    return build_result(current, is_goal(current.state), expanded_nodes, generated_nodes, start_time)


def Stochastic_Hill_Climbing(initial_state, max_steps=1000, seed=None):
    return stochastic_hill_climbing(initial_state, max_steps, seed)


def search(initial_state, max_steps=1000, seed=None):
    return stochastic_hill_climbing(initial_state, max_steps, seed)
