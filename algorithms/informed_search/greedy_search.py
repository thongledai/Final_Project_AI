import heapq
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


def greedy_search(START):
    start_time = time.time()
    node = Node(START, cost=heuristic(START))

    frontier = []
    heapq.heappush(frontier, node)
    frontier_set = {state_to_tuple(START)}
    explored_set = set()

    while frontier and len(explored_set) < MAX_STEPS:
        node = heapq.heappop(frontier)
        node_tuple = state_to_tuple(node.state)
        frontier_set.discard(node_tuple)

        if node_tuple in explored_set:
            continue

        if is_goal(node.state):
            return solution(node, len(explored_set), len(explored_set) + len(frontier) , start_time)

        explored_set.add(node_tuple)

        for action in get_actions(node.state):
            child = node.expand(action, "h(x)")
            child_tuple = state_to_tuple(child.state)
            if child_tuple in explored_set or child_tuple in frontier_set:
                continue

            heapq.heappush(frontier, child)
            frontier_set.add(child_tuple)

    return solution(node, len(explored_set), len(explored_set) + len(frontier), start_time)