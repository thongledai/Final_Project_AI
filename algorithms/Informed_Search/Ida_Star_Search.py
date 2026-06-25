import time
from Core.Action import Get_Actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, State_To_Tuple,Heuristic


FOUND = object()


def Ida_Star_Search(initial_state, max_depth=80):
    start_time = time.time()
    start = Node(initial_state)
    bound = Heuristic(initial_state)
    expanded_nodes = 0
    generated_nodes = 1
    best_node = start

    def Dfs(node, limit, path_keys):
        nonlocal expanded_nodes, generated_nodes, best_node

        f_score = node.cost + Heuristic(node.state)
        if f_score > limit:
            return f_score, None

        if Heuristic(node.state) < Heuristic(best_node.state):
            best_node = node

        if Is_Goal(node.state):
            return FOUND, node

        if node.Get_Depth() >= max_depth:
            return float("inf"), None

        expanded_nodes += 1
        next_limit = float("inf")

        children = [node.Expand(action) for action in Get_Actions(node.state)]
        generated_nodes += len(children)
        children.sort(key=lambda child: Heuristic(child.state))

        for child in children:
            key = State_To_Tuple(child.state)
            if key in path_keys:
                continue

            path_keys.add(key)
            result, found_node = Dfs(child, limit, path_keys)
            path_keys.remove(key)

            if result is FOUND:
                return FOUND, found_node
            next_limit = min(next_limit, result)

        return next_limit, None

    while bound < float("inf"):
        result, found_node = Dfs(start, bound, {State_To_Tuple(initial_state)})
        if result is FOUND:
            return Solution(found_node, expanded_nodes, generated_nodes, start_time)
        bound = result

    return Solution(best_node, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_depth=80):
    return Ida_Star_Search(initial_state, max_depth)

