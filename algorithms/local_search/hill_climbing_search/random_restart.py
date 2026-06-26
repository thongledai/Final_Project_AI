import random
import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def _child_nodes(node):
    children = []
    for action in get_actions(node.state):
        children.append(node.expand(action, "h(x)"))
    return children


def _hill_climb(start, max_steps, rng):
    current = start
    expanded = 0
    generated = 0

    for _ in range(max_steps):
        if is_goal(current.state):
            break

        children = _child_nodes(current)
        expanded += 1
        generated += len(children)

        better_neighbors = [
            child
            for child in children
            if child.cost < current.cost
        ]

        if not better_neighbors:
            break

        next_state = rng.choice(better_neighbors)
        current = next_state

    return current, expanded, generated


def random_restart_hill_climbing_search(
    initial_state,
    restarts=20,
    max_steps=500,
    random_walk_steps=10,
    seed=None,
):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state, heuristic(initial_state))
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(restarts):
        current = Node(initial_state, heuristic(initial_state))
        current, expanded, generated = _hill_climb(current, max_steps, rng)
        expanded_nodes += expanded
        generated_nodes += generated

        if is_goal(current.state):
            return solution(current, expanded_nodes, generated_nodes, start_time)

    return solution(current, expanded_nodes, generated_nodes, start_time)


