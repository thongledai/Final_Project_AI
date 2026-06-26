import heapq
import time
from Core.Action import get_actions, apply_action
from Core.Cost import step_cost
from Core.Node import Node
from Core.Result import solution
from Core.Utils import is_goal, state_to_tuple, heuristic


def a_star_search(initial_state, max_expanded=100000):
    start_time = time.time()
    start = Node(initial_state, cost=heuristic(initial_state))

    # FRONTIER chỉ chứa Node.
    # Với A*, Node.cost là f(n) = g(n) + h(n).
    frontier = []
    heapq.heappush(frontier, start)

    # best_g lưu g(n) tốt nhất đã biết của mỗi trạng thái.
    # Key phải dùng tuple vì list không thể làm key trong dict.
    best_g = {state_to_tuple(initial_state): 0}

    # REACHED chứa các trạng thái đã được lấy khỏi FRONTIER và mở rộng.
    reached = set()

    expanded_nodes = 0
    generated_nodes = 1
    node = start

    while frontier and expanded_nodes < max_expanded:
        # Lấy node có f(n) nhỏ nhất ra khỏi FRONTIER.
        node = heapq.heappop(frontier)
        node_key = state_to_tuple(node.state)
        g_node = best_g.get(node_key)

        # Nếu node này không còn mang cost tốt nhất thì bỏ qua.
        # Trường hợp này xảy ra khi cùng một trạng thái đã được tìm thấy lại
        # bằng đường đi rẻ hơn và bản cũ vẫn còn nằm trong heap.
        if  node.cost != g_node + heuristic(node.state):
            continue

        # Nếu trạng thái này đã mở rộng rồi và không có cost tốt hơn thì bỏ qua.
        if node_key in reached:
            continue

        if is_goal(node.state):
            return solution(node, expanded_nodes, generated_nodes, start_time)

        # Loại n khỏi FRONTIER và thêm n vào REACHED.
        reached.add(node_key)
        expanded_nodes += 1

        for action in get_actions(node.state):
            child_state = apply_action(node.state, action)
            child_key = state_to_tuple(child_state)

            # g_child = g(n) + cost(action).
            g_child = g_node + step_cost(node.state, action)
            old_g = best_g.get(child_key, float("inf"))

            # Nếu đã có đường đi tới m tốt hơn hoặc bằng thì bỏ qua m.
            if g_child >= old_g:
                continue

            # Nếu m đã nằm trong REACHED nhưng tìm được đường tốt hơn,
            # xóa m khỏi REACHED để cho phép xét lại theo cost mới.
            if child_key in reached:
                reached.remove(child_key)

            # Tạo Node con với cost là f(child), vì heapq so sánh theo Node.cost.
            f_child = g_child + heuristic(child_state)
            best_g[child_key] = g_child
            child = Node(
                state=child_state,
                parent=node,
                action=action,
                cost=f_child
            )
            heapq.heappush(frontier, child)
            generated_nodes += 1

    return solution(node, expanded_nodes, generated_nodes, start_time)


