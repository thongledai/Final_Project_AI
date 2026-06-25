import time
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, State_To_Tuple, Child_Nodes, Heuristic


def Local_Beam_Search(initial_state, beam_width=3, max_steps=1000):
    start_time = time.time()
    start = Node(initial_state)
    beam = [start]
    visited = {State_To_Tuple(initial_state)}
    best = start
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        next_beam = []

        for node in beam:
            if Is_Goal(node.state):
                return Solution(node, expanded_nodes, generated_nodes, start_time)

            children = Child_Nodes(node)
            expanded_nodes += 1
            generated_nodes += len(children)

            for child in children:
                key = State_To_Tuple(child.state)
                if key in visited:
                    continue
                visited.add(key)
                next_beam.append(child)

        if not next_beam:
            break

        next_beam.sort(key=lambda node: (Heuristic(node.state), node.cost))
        beam = next_beam[:beam_width]

        if Heuristic(beam[0].state) < Heuristic(best.state):
            best = beam[0]

    return Solution(best, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, beam_width=3, max_steps=1000):
    return Local_Beam_Search(initial_state, beam_width, max_steps)

