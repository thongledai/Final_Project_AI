import time

from Algorithms.SearchCommon import build_result, heuristic
from Core.Action import actions
from Core.Node import Node
from Core.Utils import is_goal, state_to_tuple


FOUND = object()


def ida_star_search(initial_state, max_depth=80):
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

        ordered_actions = sorted(
            actions(node.state),
            key=lambda action: heuristic(node.expand(action).state),
        )

        for action in ordered_actions:
            child = node.expand(action)
            generated_nodes += 1
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
            return build_result(found_node, True, expanded_nodes, generated_nodes, start_time)
        bound = result

    return build_result(best_node, False, expanded_nodes, generated_nodes, start_time)


def IDAStar_Search(initial_state, max_depth=80):
    return ida_star_search(initial_state, max_depth)


def search(initial_state, max_depth=80):
    return ida_star_search(initial_state, max_depth)
