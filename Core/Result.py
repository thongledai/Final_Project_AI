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

def Solution(success, path, states, last_state, cost, generated_states, depth, runtime):
    return Result(
        success=success,
        path=path,
        states=states,
        last_state=last_state,
        cost=cost,
        generated_states=generated_states,
        depth=depth,
        runtime=runtime
    )
