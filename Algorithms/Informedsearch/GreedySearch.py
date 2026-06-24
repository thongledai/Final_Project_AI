import heapq
import itertools
import time

from Algorithms.SearchCommon import build_result, heuristic
from Core.Action import get_actions
from Core.Node import Node
from Core.Utils import is_goal, state_to_tuple


def Greedy_search(initial_state, max_expanded=100000):
    start_time = time.time()
    start = Node(initial_state)
    counter = itertools.count()
    frontier = [(heuristic(initial_state), next(counter), start)]
    visited = set()
    expanded_nodes = 0
    generated_nodes = 1
    best_node = start

    while frontier and expanded_nodes < max_expanded:
        _, _, node = heapq.heappop(frontier)
        key = state_to_tuple(node.state)
        if key in visited:
            continue
        visited.add(key)

        if heuristic(node.state) < heuristic(best_node.state):
            best_node = node

        if is_goal(node.state):
            return build_result(node, True, expanded_nodes, generated_nodes, start_time)

        expanded_nodes += 1
        
        for action in get_actions(node.state):
            child = node.expand(action)
            if state_to_tuple(child.state) in visited:
                continue
            heapq.heappush(frontier, (heuristic(child.state), next(counter), child))
            generated_nodes += 1

    return build_result(best_node, False, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_expanded=100000):
    return Greedy_search(initial_state, max_expanded)
