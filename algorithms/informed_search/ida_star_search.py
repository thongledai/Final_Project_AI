import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *

FOUND = object()


# Thuật toán IDA* (Iterative Deepening A*)
# Tìm kiếm bằng DFS với ngưỡng f = g + h tăng dần.
def ida_star_search(START):
    start_time = time.time()
    start = Node(START)
    bound = heuristic(START)
    explored_nodes = 0
    generated_nodes = 1


    # DFS có giới hạn bởi ngưỡng f = limit.
    # Nếu chưa tìm thấy lời giải sẽ trả về giá trị f nhỏ nhất vượt ngưỡng.
    def dfs(node, limit):
        explored_nodes = 0
        generated_nodes = 1

        f = node.cost

        # Nếu f vượt quá ngưỡng hiện tại thì không mở rộng node này.
        if f > limit:
            return f, None, explored_nodes, generated_nodes

        # Nếu đạt trạng thái mục tiêu thì kết thúc tìm kiếm.
        if is_goal(node.state):
            return FOUND, node, explored_nodes, generated_nodes

        # Nếu trạng thái đã xuất hiện trên đường đi thì bỏ qua để tránh lặp.
        if node.is_cycle():
            return float("inf"), None, explored_nodes, generated_nodes

        # Nếu vượt quá độ sâu cho phép thì dừng mở rộng.
        if node.get_depth() >= MAX_STEPS:
            return float("inf"), None, explored_nodes, generated_nodes

        explored_nodes += 1
        next_limit = float("inf")

        # Mở rộng tất cả các node con.
        for action in get_actions(node.state):
            child = node.expand(action, "f(x)")
            generated_nodes += 1

            result, found_node, child_explored, child_generated = dfs(child, limit)

            explored_nodes += child_explored
            generated_nodes += child_generated

            # Nếu một node con đã tìm được lời giải thì trả về ngay.
            if result is FOUND:
                return FOUND, found_node, explored_nodes, generated_nodes

            # Cập nhật giá trị f nhỏ nhất vượt quá limit.
            next_limit = min(next_limit, result)

        # Không tìm thấy lời giải trong lần DFS này.
        return next_limit, None, explored_nodes, generated_nodes


    # Lặp lại DFS với các ngưỡng f tăng dần.
    while bound < float("inf"):

        result, found_node, explored_nodes, generated_nodes = dfs(start, bound)

        # Nếu đã tìm thấy lời giải thì trả kết quả.
        if result is FOUND:
            return solution(found_node, explored_nodes, generated_nodes, start_time)

        # Tăng ngưỡng lên giá trị f nhỏ nhất vừa bị cắt.
        bound = result

    # Không tìm thấy lời giải.
    return solution(start, explored_nodes, generated_nodes, start_time)
