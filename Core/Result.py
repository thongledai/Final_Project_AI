import time
from dataclasses import dataclass
from typing import List
from Core.Node import *
from Core.Utils import is_goal


@dataclass
class Result:
    success: bool                        # Tìm thấy lời giải không
    path: List[tuple] = None             # Danh sách hành động từ start đến end
    states: List[list] = None            # Danh sách trạng thái
    last_state: list = None              # Trạng thái cuối cùng
    cost: float = 0                      # Tổng cost
    explored: int = 0                    # Số node đã xét
    generated: int = 0                   # Số node đã sinh ra
    depth: int = 0                       # Độ sâu lời giải
    runtime: float = 0                   # Thời gian chạy

def solution(node, explored, generated, start_time):
    if node is None:
        return Result(
            explored=explored,
            generated=generated,
            runtime=time.time() - start_time,
        )

    elif isinstance(node, Node):
        return Result(
            success=is_goal(node.get_state()),
            path=node.get_path(),
            states=node.get_states(),
            last_state=node.get_state(),
            cost=node.get_cost(),
            explored=explored,
            generated=generated,
            depth=node.get_depth(),
            runtime=time.time() - start_time,
        )
    else:

        # Chuẩn hóa nếu node là một đối tượng đơn lẻ
        if not isinstance(node, (list, tuple)):
            node = [node]
            
        # 1. Lấy danh sách states từ tất cả các node
        all_node_states = [n.get_states() for n in node]
        
        # 2. Gộp chúng lại theo từng bước (step-by-step)
        # Nếu node chỉ có 1 phần tử, zip(*) vẫn chạy đúng và trả về [[a], [b], [c]]
        zipped_states = [list(step) for step in zip(*all_node_states)]

        return Result(
            success=all(is_goal(n.get_state()) for n in node),
            path=node[0].get_path(),
            states= zipped_states,
            last_state=node[0].get_state(),
            cost=node[0].get_cost(),
            explored=explored,
            generated=generated,
            depth=node[0].get_depth(),
            runtime=time.time() - start_time,
        )
