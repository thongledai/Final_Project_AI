import heapq
import itertools
import time

from Algorithms.SearchCommon import build_result, heuristic
from Core.Action import get_actions
from Core.Node import Node
from Core.Utils import is_goal, state_to_tuple


def A_star_search(initial_state, max_expanded=100000):
    start_time = time.time()
    start = Node(initial_state)
    counter = itertools.count()
    frontier = [(heuristic(initial_state), 0, next(counter), start)]
    best_cost = {state_to_tuple(initial_state): 0}
    expanded_nodes = 0
    generated_nodes = 1

    while frontier and expanded_nodes < max_expanded:
        _, _, _, node = heapq.heappop(frontier)
        node_key = state_to_tuple(node.state)

        if node.cost != best_cost.get(node_key):
            continue

        if is_goal(node.state):
            return build_result(node, True, expanded_nodes, generated_nodes, start_time)

        expanded_nodes += 1
        for action in get_actions(node.state):
            child = node.expand(action)
            child_key = state_to_tuple(child.state)
            if child.cost >= best_cost.get(child_key, float("inf")):
                continue

            best_cost[child_key] = child.cost
            priority = child.cost + heuristic(child.state)
            heapq.heappush(frontier, (priority, child.cost, next(counter), child))
            generated_nodes += 1

    best_node = min((item[3] for item in frontier), key=lambda n: heuristic(n.state), default=start)
    return build_result(best_node, False, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_expanded=100000):
    return A_star_search(initial_state, max_expanded)
