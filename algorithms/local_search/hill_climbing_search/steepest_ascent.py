import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def _child_nodes(node):
    children = []
    for action in get_actions(node.state):
        children.append(node.expand(action, cost_function="h(x)"))
    return children


def steepest_ascent_hill_climbing_search(initial_state, max_steps=1000):
    start_time = time.time()
    current = Node(initial_state, cost=heuristic(initial_state))
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        if is_goal(current.state):
            return solution(current, expanded_nodes, generated_nodes, start_time)

        children = _child_nodes(current)
        candidate = min(children, key=lambda child: child.cost) if children else None
        expanded_nodes += 1
        generated_nodes += len(children)

        if candidate is None:
            break

        if candidate.cost >= current.cost:
            break

        current = candidate

    return solution(current, expanded_nodes, generated_nodes, start_time)
