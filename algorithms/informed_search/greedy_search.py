import heapq
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


def greedy_search(initial_state, max_expanded=100000):
    start_time = time.time()
    node = Node(initial_state, cost=heuristic(initial_state))

    # Frontier chi chua Node. Voi Greedy, Node.cost la h(n).
    frontier = []
    heapq.heappush(frontier, node)
    frontier_keys = {state_to_tuple(initial_state)}
    explored = set()
    expanded_nodes = 0
    generated_nodes = 1

    while frontier and expanded_nodes < max_expanded:
        node = heapq.heappop(frontier)
        key = state_to_tuple(node.state)
        frontier_keys.discard(key)

        if key in explored:
            continue

        if is_goal(node.state):
            return solution(node, expanded_nodes, generated_nodes, start_time)

        explored.add(key)
        expanded_nodes += 1

        for action in get_actions(node.state):
            child = node.expand(action, "h(x)")
            child_key = state_to_tuple(child.state)
            if child_key in explored or child_key in frontier_keys:
                continue

            heapq.heappush(frontier, child)
            frontier_keys.add(child_key)
            generated_nodes += 1

    return solution(node, expanded_nodes, generated_nodes, start_time)