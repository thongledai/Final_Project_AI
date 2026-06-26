import heapq
import itertools
import time
from Core.Action import Get_Actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, State_To_Tuple,Heuristic


def Greedy_Search(initial_state, max_expanded=100000):
    start_time = time.time()
    start = Node(initial_state)
    counter = itertools.count()
    frontier = [(Heuristic(initial_state), next(counter), start)]
    visited = set()
    expanded_nodes = 0
    generated_nodes = 1
    best_node = start

    while frontier and expanded_nodes < max_expanded:
        _, _, node = heapq.heappop(frontier)
        key = State_To_Tuple(node.state)
        if key in visited:
            continue
        visited.add(key)

        if Heuristic(node.state) < Heuristic(best_node.state):
            best_node = node

        if Is_Goal(node.state):
            return Solution(node, expanded_nodes, generated_nodes, start_time)

        expanded_nodes += 1
        
        for action in Get_Actions(node.state):
            child = node.Expand(action)
            if State_To_Tuple(child.state) in visited:
                continue
            heapq.heappush(frontier, (Heuristic(child.state), next(counter), child))
            generated_nodes += 1

    return Solution(best_node, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_expanded=100000):
    return Greedy_Search(initial_state, max_expanded)

