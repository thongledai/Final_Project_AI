import time
from Core.Action import get_actions
from Core.Node import Node
from Core.Result import solution
from Core.Utils import is_goal,  heuristic

FOUND = object()

def ida_star_search(initial_state, max_depth=80):
    start_time = time.time()
    start = Node(initial_state)
    bound = heuristic(initial_state)
    expanded_nodes = 0
    generated_nodes = 1

    def Dfs(node, limit):
        nonlocal expanded_nodes, generated_nodes

        f = node.cost + heuristic(node.state)

        if f > limit:
            return f, None

        if is_goal(node.state):
            return FOUND, node

        if node.Get_Depth() >= max_depth:
            return float("inf"), None

        expanded_nodes += 1
        next_limit = float("inf")

        for action in get_actions(node.state):
            child = node.Expand(action)
            generated_nodes += 1
            result, found_node = Dfs(child, limit)

            if result is FOUND:
                return FOUND, found_node

            next_limit = min(next_limit, result)

        return next_limit, None

    while bound < float("inf"):
        result, found_node = Dfs(start, bound)
        if result is FOUND:
            return solution(found_node, expanded_nodes, generated_nodes, start_time)
        bound = result

    return solution(start, expanded_nodes, generated_nodes, start_time)