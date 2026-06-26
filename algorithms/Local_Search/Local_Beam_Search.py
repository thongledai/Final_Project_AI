import time
from Core.Action import Get_Actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, Heuristic


def _Child_Nodes(node):
    children = []
    for action in Get_Actions(node.state):
        children.append(node.Expand(action, cost_function="h(x)"))
    return children


def Local_Beam_Search(initial_state, beam_width=3, max_steps=1000):
    start_time = time.time()
    current_set = [Node(initial_state, cost=Heuristic(initial_state))]
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        neighbor_states = []

        for state in current_set:
            children = _Child_Nodes(state)
            neighbor_states.extend(children)

            expanded_nodes += 1
            generated_nodes += len(children)

        for neighbor in neighbor_states:
            if Is_Goal(neighbor.state):
                return Solution(neighbor, expanded_nodes, generated_nodes, start_time)

        if not neighbor_states:
            break

        neighbor_states.sort(key=lambda state: state.cost)
        current_set = neighbor_states[:beam_width]

    current = min(
        current_set,
        key=lambda state: state.cost,
        default=Node(initial_state, cost=Heuristic(initial_state)),
    )
    return Solution(current, expanded_nodes, generated_nodes, start_time)


