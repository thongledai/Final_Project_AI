import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *



def local_beam_search(initial_state, beam_width=3, max_steps=1000):
    start_time = time.time()
    current_set = [Node(initial_state, cost=heuristic(initial_state))]
    expanded_nodes = 0
    generated_nodes = 1
    visited = {state_to_tuple(initial_state)}

    for _ in range(max_steps):
        neighbor_states = []

        for state in current_set:
            children = child_nodes(state)
            
            expanded_nodes += 1
            generated_nodes += len(children)
            
            for child in children:
                if state_to_tuple(child.state) not in visited:
                    neighbor_states.append(child)
                    visited.add(state_to_tuple(child.state))

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