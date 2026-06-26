import heapq
import time
from Core.Action import Get_Actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, State_To_Tuple, Heuristic


def Greedy_Search(initial_state, max_expanded=100000):
    start_time = time.time()
    start = Node(initial_state, cost=Heuristic(initial_state))

    # Frontier chi chua Node. Voi Greedy, Node.cost la h(n).
    frontier = []
    heapq.heappush(frontier, start)
    frontier_keys = {State_To_Tuple(initial_state)}
    reached = set()
    expanded_nodes = 0
    generated_nodes = 1
    node = start

    while frontier and expanded_nodes < max_expanded:
        node = heapq.heappop(frontier)
        key = State_To_Tuple(node.state)
        frontier_keys.discard(key)

        if key in reached:
            continue

        if Is_Goal(node.state):
            return Solution(node, expanded_nodes, generated_nodes, start_time)

        reached.add(key)
        expanded_nodes += 1

        for action in Get_Actions(node.state):
            child = node.Expand(action, cost_function="h(x)")
            child_key = State_To_Tuple(child.state)
            if child_key in reached or child_key in frontier_keys:
                continue

            heapq.heappush(frontier, child)
            frontier_keys.add(child_key)
            generated_nodes += 1

    return Solution(node, expanded_nodes, generated_nodes, start_time)
