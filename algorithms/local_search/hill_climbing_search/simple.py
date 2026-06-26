import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def simple_hill_climbing(initial_state, max_steps=1000):
    start_time = time.time()
    current = Node(initial_state, cost=heuristic(initial_state))
    expanded_nodes = 1
    generated_nodes = 1

    for _ in range(max_steps):
        if is_goal(current.state):
            return solution(current, expanded_nodes, generated_nodes, start_time)

        expanded_nodes += 1
        current_value = heuristic(current.state)
        next_node = None

        for action in get_actions(current.state):
            child = current.expand(action, cost="h(x)")           
            generated_nodes += 1

            if child.cost < current_value:
                next_node = child
                break

        if next_node is None:
            break

        current = next_node

    return solution(current, expanded_nodes, generated_nodes, start_time)

