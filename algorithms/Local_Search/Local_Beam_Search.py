import time
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, Child_Nodes, Heuristic


def Local_Beam_Search(initial_state, beam_width=3, max_steps=1000):
    start_time = time.time()
    current_set = [Node(initial_state)]
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        neighbor_states = []

        for state in current_set:
            children = Child_Nodes(state)
            neighbor_states.extend(children)

            expanded_nodes += 1
            generated_nodes += len(children)

        for neighbor in neighbor_states:
            if Is_Goal(neighbor.state):
                return Solution(neighbor, expanded_nodes, generated_nodes, start_time)

        if not neighbor_states:
            break

        neighbor_states.sort(key=lambda state: Heuristic(state.state))
        current_set = neighbor_states[:beam_width]

    current = min(
        current_set,
        key=lambda state: Heuristic(state.state),
        default=Node(initial_state),
    )
    return Solution(current, expanded_nodes, generated_nodes, start_time)


