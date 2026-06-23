from dataclasses import dataclass
from typing import List
from Core.Action import *
from Core.Utils import *

@dataclass
class SearchResult:
    success: bool                        # Tìm thấy lời giải không
    path: List[tuple] = None             # Danh sách hành động từ start đến end
    states: List[list] = None            # Danh sách trạng thái
    final_state: list = None             # Trạng thái cuối cùng
    cost: float = 0                      # Tổng cost
    expanded_nodes: int = 0              # Số node mở rộng
    generated_nodes: int = 0             # Số node sinh ra
    depth: int = 0                       # Độ sâu lời giải
    runtime: float = 0                   # Thời gian chạy


# eg: BFS (đủ thông tin)
# return SearchResult(
#     success=is_goal(node.current),
#     actions=node.get_actions(),
#     states=node.get_path(),
#     final_state=node.current,
#     cost=node.cost,
#     expanded_nodes=expanded,
#     generated_nodes=generated,
#     depth=node.get_depth(),
#     runtime=end-start
# )

# eg: Hill Climbing (không đủ thông tin)
# return SearchResult(
#     success=is_goal(current),
#     final_state=current,
#     cost=steps,
#     runtime=end-start
# )