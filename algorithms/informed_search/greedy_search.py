import heapq
import time
from Core.Action import get_actions, apply_action
from Core.Node import Node
from Core.Result import solution
from Core.Utils import is_goal, state_to_tuple, heuristic


def greedy_search(initial_state, max_expanded=100000):
    start_time = time.time()
    start = Node(initial_state, cost=heuristic(initial_state))

    # Frontier chi chua Node. Voi Greedy, Node.cost la h(n).
    frontier = []
    heapq.heappush(frontier, start)
    frontier_keys = {state_to_tuple(initial_state)}
    reached = set()
    expanded_nodes = 0
    generated_nodes = 1
    node = start

    while frontier and expanded_nodes < max_expanded:
        node = heapq.heappop(frontier)
        key = state_to_tuple(node.state)
        frontier_keys.discard(key)

        if key in reached:
            continue

        if is_goal(node.state):
            return solution(node, expanded_nodes, generated_nodes, start_time)

        reached.add(key)
        expanded_nodes += 1

        for action in get_actions(node.state):
            child_state = apply_action(node.state, action)
            child_key = state_to_tuple(child_state)
            if child_key in reached or child_key in frontier_keys:
                continue

            child = Node(
                state=child_state,
                parent=node,
                action=action,
                cost=heuristic(child_state)
            )
            heapq.heappush(frontier, child)
            frontier_keys.add(child_key)
            generated_nodes += 1

    return solution(node, expanded_nodes, generated_nodes, start_time)
