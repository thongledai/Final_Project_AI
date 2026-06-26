import time
from Core.Action import get_actions, apply_action
from Core.Node import Node
from Core.Result import solution
from Core.Utils import is_goal, heuristic


def _child_nodes(node):
    children = []
    for action in get_actions(node.state):
        child_state = apply_action(node.state, action)
        children.append(Node(
            state=child_state,
            parent=node,
            action=action,
            cost=heuristic(child_state)
        ))
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
