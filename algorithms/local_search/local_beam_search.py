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


def local_beam_search(initial_state, beam_width=3, max_steps=1000):
    start_time = time.time()
    current_set = [Node(initial_state, cost=heuristic(initial_state))]
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        neighbor_states = []

        for state in current_set:
            children = _child_nodes(state)
            neighbor_states.extend(children)

            expanded_nodes += 1
            generated_nodes += len(children)

        for neighbor in neighbor_states:
            if is_goal(neighbor.state):
                return solution(neighbor, expanded_nodes, generated_nodes, start_time)

        if not neighbor_states:
            break

        neighbor_states.sort(key=lambda state: state.cost)
        current_set = neighbor_states[:beam_width]

    current = min(
        current_set,
        key=lambda state: state.cost,
        default=Node(initial_state, cost=heuristic(initial_state)),
    )
    return solution(current, expanded_nodes, generated_nodes, start_time)


