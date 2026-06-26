import heapq
import time
from Core.Node import *
from Core.Action import get_actions
from Core.Utils import *
from Core.Result import *


def a_star_search(START):
    start_time = time.time()
    node = Node(START, cost=heuristic(START))
    frontier = []
    heapq.heappush(frontier, node)

    best_g = {state_to_tuple(START): 0}
    explored_set = set()

    while frontier and (len(explored_set) < MAX_STEPS):

        node = heapq.heappop(frontier)
        node_key = state_to_tuple(node.state)
        g_node = best_g[node_key]

        if node.get_cost() != (g_node + heuristic(node.state)):
            continue

        if node_key in explored_set:
            continue

        if is_goal(node.state):
            return solution(node, len(explored_set), len(explored_set) + len(frontier), start_time)

        explored_set.add(node_key)

        for action in get_actions(node.state):
            child = node.expand(action,"f(x)")
            child_key = state_to_tuple(child.state)

            # g_child = g(n) + step_cost(n,action).
            g_child = child.get_cost() - heuristic(child.state)
            old_g = best_g.get(child_key, float("inf"))

            if g_child >= old_g:
                continue

            if child_key in explored_set:
                explored_set.remove(child_key)

            best_g[child_key] = g_child
            heapq.heappush(frontier, child)

    return solution(node, len(explored_set), len(explored_set) + len(frontier), start_time)