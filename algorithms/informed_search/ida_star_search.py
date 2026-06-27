import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *

FOUND = object()

def ida_star_search(START):
    start_time = time.time()
    start = Node(START)
    bound = heuristic(START)
    expanded_nodes = 0
    generated_nodes = 1

    def dfs(node, limit):
        nonlocal expanded_nodes, generated_nodes

        f = node.cost + heuristic(node.state)

        if f > limit:
            return f, None

        if is_goal(node.state):
            return FOUND, node

        if node.is_cycle():
            return float("inf"), None

        if node.get_depth() >= MAX_STEPS:
            return float("inf"), None

        expanded_nodes += 1
        next_limit = float("inf")

        for action in get_actions(node.state):
            child = node.expand(action, "g(x)")
            generated_nodes += 1
            result, found_node = dfs(child, limit)

            if result is FOUND:
                return FOUND, found_node

            next_limit = min(next_limit, result)

        return next_limit, None

    while bound < float("inf"):
        result, found_node = dfs(start, bound)
        if result is FOUND:
            return solution(found_node, expanded_nodes, generated_nodes, start_time)
        bound = result

    return solution(start, expanded_nodes, generated_nodes, start_time)