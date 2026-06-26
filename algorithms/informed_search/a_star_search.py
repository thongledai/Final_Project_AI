import heapq
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


def a_star_search(initial_state, max_expanded=100000):
    start_time = time.time()
    start = Node(initial_state, cost=heuristic(initial_state))
    frontier = []
    heapq.heappush(frontier, start)

    best_g = {state_to_tuple(initial_state): 0}
    explored = set()

    expanded_nodes = 0
    generated_nodes = 1
    node = start

    while frontier and expanded_nodes < max_expanded:
        # Lấy node có f(n) nhỏ nhất ra khỏi FRONTIER.
        node = heapq.heappop(frontier)
        node_key = state_to_tuple(node.state)
        g_node = best_g[node_key]

        if node.cost != g_node + heuristic(node.state):
            continue

        if node_key in explored:
            continue

        if is_goal(node.state):
            return solution(node, expanded_nodes, generated_nodes, start_time)

        # Loại n khỏi FRONTIER và thêm n vào REACHED.
        explored.add(node_key)
        expanded_nodes += 1

        for action in get_actions(node.state):
            child = node.Expand(action, cost="f(x)")
            child_key = state_to_tuple(child.state)

            # g_child = g(n) + cost(action).
            g_child = child.cost - heuristic(child.state)
            old_g = best_g.get(child_key, float("inf"))

            # Nếu đã có đường đi tới m tốt hơn hoặc bằng thì bỏ qua m.
            if g_child >= old_g:
                continue

            if child_key in explored:
                explored.remove(child_key)

            # Tạo Node con với cost là f(child), vì heapq so sánh theo Node.cost.
            best_g[child_key] = g_child
            heapq.heappush(frontier, child)
            generated_nodes += 1

    return solution(node, expanded_nodes, generated_nodes, start_time)