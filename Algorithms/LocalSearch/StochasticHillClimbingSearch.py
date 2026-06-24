import random
import time
from Core.Result import Solution
from Core.Node import Node
from Core.Utils import is_goal, state_to_tuple,child_nodes, heuristic


def SHCS(initial_state, max_steps=1000, seed=None):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state)
    seen = {state_to_tuple(initial_state)}
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        if is_goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

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

    return Solution(current, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_steps=1000, seed=None):
    return SHCS(initial_state, max_steps, seed)
