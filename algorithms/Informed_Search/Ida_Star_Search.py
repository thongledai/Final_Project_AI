import time
from Core.Action import Get_Actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal,  Heuristic

FOUND = object()

def Ida_Star_Search(initial_state, max_depth=80):
    start_time = time.time()
    start = Node(initial_state)
    bound = Heuristic(initial_state)
    expanded_nodes = 0
    generated_nodes = 1

    def Dfs(node, limit):
        nonlocal expanded_nodes, generated_nodes

        f = node.cost + Heuristic(node.state)

        if f > limit:
            return f, None

        if Is_Goal(node.state):
            return FOUND, node

        if node.Get_Depth() >= max_depth:
            return float("inf"), None

        expanded_nodes += 1
        next_limit = float("inf")

        for action in Get_Actions(node.state):
            child = node.Expand(action, cost_function="g(x)")
            generated_nodes += 1
            result, found_node = Dfs(child, limit)

            if result is FOUND:
                return FOUND, found_node

            next_limit = min(next_limit, result)

        return next_limit, None

    while bound < float("inf"):
        result, found_node = Dfs(start, bound)
        if result is FOUND:
            return Solution(found_node, expanded_nodes, generated_nodes, start_time)
        bound = result

    return Solution(start, expanded_nodes, generated_nodes, start_time)
