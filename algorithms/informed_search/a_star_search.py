import heapq
import time
from Core.Node import *
from Core.Action import get_actions
from Core.Utils import *
from Core.Result import *


def _g_cost(node):
    return node.cost - heuristic(node.state)


def a_star_search(START):
    start_time = time.time()

    node = Node(START, cost=heuristic(START))
    node_tuple = state_to_tuple(node.state)

    frontier = []
    heapq.heappush(frontier, node)

    frontier_dic = {node_tuple: 0}
    reached = {}
    generated = 1

    while frontier and len(reached) < MAX_STEPS:
        node = heapq.heappop(frontier)
        node_tuple = state_to_tuple(node.state)
        g_node = _g_cost(node)
        if(node_tuple in reached ):
            continue

        if is_goal(node.state):
            return solution(node, len(reached), generated, start_time)

        reached[node_tuple] = g_node

        for action in get_actions(node.state):
            child = node.expand(action, "f(x)")
            child_key = state_to_tuple(child.state)
            g_new = _g_cost(child)

            if child.is_cycle():
                continue

            if child_key in reached:
                if g_new >= reached[child_key]:
                    continue
                reached.pop(child_key)
                

            if child_key in frontier_dic:
                if g_new >= frontier_dic[child_key]:
                    continue

            frontier_dic[child_key] = g_new
            heapq.heappush(frontier, child)
            generated += 1

    return solution(node, len(reached), generated, start_time)
