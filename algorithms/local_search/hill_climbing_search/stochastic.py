import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *

def _child_nodes(node):
    children = []
    for action in get_actions(node.state):
        children.append(node.Expand(action, cost_function="h(x)"))
    return children


def stochastic_hill_climbing_search(initial_state, max_steps=1000, seed=None):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state, cost=heuristic(initial_state))
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        if is_goal(current.state):
            return solution(current, expanded_nodes, generated_nodes, start_time)

        children = _child_nodes(current)
        expanded_nodes += 1
        generated_nodes += len(children)
        better_neighbors = [
            child
            for child in children
            if child.cost < current.cost
        ]

        if not better_neighbors:
            break

        current = rng.choice(better_neighbors)

    return solution(current, expanded_nodes, generated_nodes, start_time)

