import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *

# Tăng giới hạn đệ quy vì AND-OR Search hoạt động theo chiều sâu (DFS-based)
def and_or_graph_search(start):
    def or_search(node, path):
        if is_goal(node.state):
            return node
        
        # Kiểm tra chu trình (Cycle Checking): Tránh việc đổ nước qua lại giữa 2 ống vô tận
        if state_to_tuple(node.state) in path:
            return None
        
        if stats['max_depth_node'].cost < node.cost:
            stats['max_depth_node'] = node
        
        stats['explored_node'] += 1
        path.add(state_to_tuple(node.state)) # Đánh dấu state hiện tại vào đường đi
        
        actions = get_actions(node.state)
        for action in actions:
            child = node.expand(action)
            stats['generated_node'] += 1
            
            # --- MÔ PHỎNG NÚT AND ---
            # Trong môi trường nondeterministic, 1 action sinh ra NHIỀU trạng thái (outcomes).
            # Trong Water Sort, 1 action chỉ sinh ra 1 trạng thái (child). 
            # Ta đưa nó vào list để đưa cho AND_Search xử lý nhằm giữ đúng format thuật toán.
            outcomes = [child]
            
            # Gọi AND_Search cho các kết quả của hành động này
            goal_node = and_search(outcomes, path)
            
            if goal_node is not None:
                # Trả lại trạng thái set như cũ (backtracking) dù không bắt buộc trong Python nếu ta pass by value,
                # nhưng dùng set() reference thì cần remove để các nhánh khác không bị ảnh hưởng.
                path.remove(state_to_tuple(node.state))
                return goal_node 
                
        path.remove(state_to_tuple(node.state))
        return None # Thất bại trên nhánh này

    # --- HÀM AND-SEARCH ---
    # Nhiệm vụ: Phải giải quyết thành công TẤT CẢ các trạng thái trong outcomes.
    def and_search(outcomes, path):
        # Mặc dù outcomes ở bài này độ dài luôn = 1, ta vẫn dùng vòng lặp để 
        # thể hiện rõ tính chất của AND node (phải duyệt qua mọi outcome).
        for child_node in outcomes:
            # Gọi đệ quy lại OR_Search cho từng outcome
            result = or_search(child_node, path)
            
            # Nếu có BẤT KỲ outcome nào thất bại (không thể giải tiếp)
            # thì toàn bộ hành động (AND node) này coi như vứt đi.
            if result is None:
                return None 
                
        # Nếu qua được vòng lặp (nghĩa là mọi outcomes đều giải được), 
        # trả về node đích để trace ngược đường đi.
        return result 
    
    start_time = time.time()
    initial_node = Node(start)
    
    stats = {
        'explored_node': 0,
        'generated_node': 1,
        'max_depth_node': initial_node
    }
    
    goal_node = or_search(initial_node, set())
    
    if goal_node is not None:
        # Thành công
        return solution(goal_node, stats['explored_node'], stats['generated_node'], start_time)
    else:
        # Thất bại
        return solution(stats['max_depth_node'], stats['explored_node'], stats['generated_node'], start_time)