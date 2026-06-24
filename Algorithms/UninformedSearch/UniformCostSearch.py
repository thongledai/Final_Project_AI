import heapq
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


# Thuật toán tìm kiếm chi phí đồng nhất
def UCS(START):
    start_time=time.time()
    node=Node(START)
    if is_goal(node.state):
        return Solution(
            success=True,
            path=node.get_path(),
            states=node.get_states(),
            last_state=node.get_state(),
            cost=node.get_cost(),
            generated_states=1,
            depth=node.get_depth(),
            runtime=time.time()-start_time
        )
    
    frontier = []
    explored = []
    heapq.heappush(frontier, node)

    while frontier:
        node = heapq.heappop(frontier)
        explored.append(node.state)
        if is_goal(node.state):
            return Solution(
                success=True,
                path=child.get_path(),
                states=child.get_states(),
                last_state=child.get_state(),
                cost=child.get_cost(),
                generated_states=len(explored) + len(frontier),
                depth=child.get_depth(),
                runtime=time.time()-start_time
            )
        
        actions = get_actions(node.state)
        for action1 in actions:
            child = node.expand(action=action1,cost_function="g(x)")
            if child.state not in explored and child not in frontier:
                heapq.heappush(frontier, child)

    # failure
    return Solution(
        success=False,
        path=node.get_path(),
        states=node.get_states(),
        last_state=node.get_state(),
        cost=node.get_cost(),
        generated_states=len(explored) + len(frontier),
        depth=node.get_depth(),
        runtime=time.time()-start_time
    )  