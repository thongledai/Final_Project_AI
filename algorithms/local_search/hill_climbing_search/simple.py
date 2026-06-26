import time
from Core.Action import get_actions, apply_action
from Core.Node import Node
from Core.Result import solution
from Core.Utils import is_goal, heuristic


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
            child_state = apply_action(current.state, action)
            child = Node(
                state=child_state,
                parent=current,
                action=action,
                cost=heuristic(child_state)
            )
            generated_nodes += 1

            if child.cost < current_value:
                next_node = child
                break

        if next_node is None:
            break

        current = next_node

    return solution(current, expanded_nodes, generated_nodes, start_time)

