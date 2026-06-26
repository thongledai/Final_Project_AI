import time
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
    explored: int = 0                    # Số node đã xét
    generated: int = 0                   # Số node đã sinh ra
    depth: int = 0                       # Độ sâu lời giải
    runtime: float = 0                   # Thời gian chạy

def solution(node, explored, generated, start_time):
     return Result(
        success=is_goal(node.get_state()),
        path=node.get_path(),
        states=node.get_states(),
        last_state=node.get_state(),
        cost=node.cost,
        explored=explored,
        generated=generated,
        depth=node.get_depth(),
        runtime=time.time() - start_time,
    )
