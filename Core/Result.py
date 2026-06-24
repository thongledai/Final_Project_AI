from dataclasses import dataclass
from typing import List
from Core.Action import *
from Core.Utils import *

@dataclass
class Result:
    success: bool                        # Tìm thấy lời giải không
    path: List[tuple] = None             # Danh sách hành động từ start đến end
    states: List[list] = None            # Danh sách trạng thái
    last_state: list = None              # Trạng thái cuối cùng
    cost: float = 0                      # Tổng cost
    generated_states: int = 0            # Số node sinh ra
    depth: int = 0                       # Độ sâu lời giải
    runtime: float = 0                   # Thời gian chạy

def Solution(node, success, expanded_nodes, generated_nodes, start_time):
     return Result(
        success=success,
        path=node.get_path(),
        states=node.get_states(),
        last_state=node.get_state(),
        cost=node.cost,
        generated_states=generated_nodes,
        depth=node.get_depth(),
        runtime=time.time() - start_time,
    )
