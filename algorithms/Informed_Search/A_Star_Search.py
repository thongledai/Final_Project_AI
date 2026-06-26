import heapq
import itertools
import time
from Core.Action import Get_Actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, State_To_Tuple, Heuristic


def A_Star_Search(initial_state, max_expanded=100000):
    start_time = time.time()
    start = Node(initial_state)
    counter = itertools.count()

    # FRONTIER chứa các node đang chờ xét.
    # Mỗi phần tử có dạng: (f, g, thứ_tự, node)
    # f = g + h, trong đó g là node.cost và h là Heuristic(node.state).
    frontier = [(Heuristic(initial_state), 0, next(counter), start)]

    # best_cost lưu g(n) tốt nhất đã biết của mỗi trạng thái.
    # Key phải dùng tuple vì list không thể làm key trong dict.
    best_cost = {State_To_Tuple(initial_state): 0}

    # REACHED chứa các trạng thái đã được lấy khỏi FRONTIER và mở rộng.
    reached = set()

    expanded_nodes = 0
    generated_nodes = 1

    while frontier and expanded_nodes < max_expanded:
        # Lấy node có f(n) nhỏ nhất ra khỏi FRONTIER.
        _, _, _, node = heapq.heappop(frontier)
        node_key = State_To_Tuple(node.state)

        # Nếu node này không còn mang cost tốt nhất thì bỏ qua.
        # Trường hợp này xảy ra khi cùng một trạng thái đã được tìm thấy lại
        # bằng đường đi rẻ hơn và bản cũ vẫn còn nằm trong heap.
        if node.cost != best_cost.get(node_key):
            continue

        # Nếu trạng thái này đã mở rộng rồi và không có cost tốt hơn thì bỏ qua.
        if node_key in reached:
            continue

        if Is_Goal(node.state):
            return Solution(node, expanded_nodes, generated_nodes, start_time)

        # Loại n khỏi FRONTIER và thêm n vào REACHED.
        reached.add(node_key)
        expanded_nodes += 1

        for action in Get_Actions(node.state):
            child = node.Expand(action)
            child_key = State_To_Tuple(child.state)

            # g_new(m) = g(n) + cost(action).
            # Trong Node.Expand(), mỗi bước đổ mặc định tăng cost thêm 1.
            new_cost = child.cost
            old_cost = best_cost.get(child_key, float("inf"))

            # Nếu đã có đường đi tới m tốt hơn hoặc bằng thì bỏ qua m.
            if new_cost >= old_cost:
                continue

            # Nếu m đã nằm trong REACHED nhưng tìm được đường tốt hơn,
            # xóa m khỏi REACHED để cho phép xét lại theo cost mới.
            if child_key in reached:
                reached.remove(child_key)

            # Cập nhật lại g(m), f(m), cha của m đã nằm trong child.parent.
            best_cost[child_key] = new_cost
            priority = new_cost + Heuristic(child.state)
            heapq.heappush(frontier, (priority, new_cost, next(counter), child))
            generated_nodes += 1

    best_node = min((item[3] for item in frontier), key=lambda n: Heuristic(n.state), default=start)
    return Solution(best_node, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_expanded=100000):
    return A_Star_Search(initial_state, max_expanded)
