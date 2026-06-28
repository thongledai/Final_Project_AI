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
    explored_nodes = 0
    generated_nodes = 1

    def dfs(node, limit):
        explored_nodes=0
        generated_nodes=1

        f = node.cost 

        if f > limit:
            return f, None, explored_nodes,generated_nodes

        if is_goal(node.state):
            return FOUND, node, explored_nodes,generated_nodes

        if node.is_cycle():
            return float("inf"), None,explored_nodes,generated_nodes

        if node.get_depth() >= MAX_STEPS:
            return float("inf"), None,explored_nodes,generated_nodes

        explored_nodes += 1
        next_limit = float("inf")

        for action in get_actions(node.state):
            child = node.expand(action, "f(x)")
            generated_nodes += 1
            result, found_node, child_explored, child_generated = dfs(child, limit)

            explored_nodes += child_explored
            generated_nodes += child_generated

            if result is FOUND:
                return FOUND, found_node,explored_nodes,generated_nodes

            next_limit = min(next_limit, result)

        return next_limit, None,explored_nodes,generated_nodes

    while bound < float("inf"):
        result, found_node,explored_nodes,generated_nodes = dfs(start, bound)
        if result is FOUND:
            return solution(found_node, explored_nodes, generated_nodes, start_time)
        bound = result

    return solution(start, explored_nodes, generated_nodes, start_time)