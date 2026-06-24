import time
from Core.Action import get_actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import is_goal, state_to_tuple,heuristic


FOUND = object()


def IDASS(initial_state, max_depth=80):
    start_time = time.time()
    start = Node(initial_state)
    bound = heuristic(initial_state)
    expanded_nodes = 0
    generated_nodes = 1
    best_node = start

    def dfs(node, limit, path_keys):
        nonlocal expanded_nodes, generated_nodes, best_node

        f_score = node.cost + heuristic(node.state)
        if f_score > limit:
            return f_score, None

        if heuristic(node.state) < heuristic(best_node.state):
            best_node = node

        if is_goal(node.state):
            return FOUND, node

        if node.get_depth() >= max_depth:
            return float("inf"), None

        expanded_nodes += 1
        next_limit = float("inf")

        children = [node.expand(action) for action in get_actions(node.state)]
        generated_nodes += len(children)
        children.sort(key=lambda child: heuristic(child.state))

        for child in children:
            key = state_to_tuple(child.state)
            if key in path_keys:
                continue

            path_keys.add(key)
            result, found_node = dfs(child, limit, path_keys)
            path_keys.remove(key)

            if result is FOUND:
                return FOUND, found_node
            next_limit = min(next_limit, result)

        return next_limit, None

    while bound < float("inf"):
        result, found_node = dfs(start, bound, {state_to_tuple(initial_state)})
        if result is FOUND:
            return Solution(found_node, expanded_nodes, generated_nodes, start_time)
        bound = result

    return Solution(best_node, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_depth=80):
    return IDASS(initial_state, max_depth)
