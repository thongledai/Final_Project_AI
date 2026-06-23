import time

from Algorithms.SearchCommon import best_child, build_result, heuristic
from Core.Node import Node
from Core.Utils import is_goal, state_to_tuple


def steepest_ascent_hill_climbing(initial_state, max_steps=1000):
    start_time = time.time()
    current = Node(initial_state)
    seen = {state_to_tuple(initial_state)}
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        if is_goal(current.state):
            return build_result(current, True, expanded_nodes, generated_nodes, start_time)

        candidate, children = best_child(current)
        expanded_nodes += 1
        generated_nodes += len(children)

        if candidate is None:
            break

        if heuristic(candidate.state) >= heuristic(current.state):
            break

        key = state_to_tuple(candidate.state)
        if key in seen:
            break
        seen.add(key)
        current = candidate

    return build_result(current, is_goal(current.state), expanded_nodes, generated_nodes, start_time)


def Steepest_Ascent_Hill_Climbing(initial_state, max_steps=1000):
    return steepest_ascent_hill_climbing(initial_state, max_steps)


def search(initial_state, max_steps=1000):
    return steepest_ascent_hill_climbing(initial_state, max_steps)
