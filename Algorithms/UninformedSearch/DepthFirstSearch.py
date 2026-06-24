from collections import deque
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


# Thuật toán tìm kiếm theo chiều sâu
def DFS(START):
    start_time=time.time()
    node=Node(START)
    if is_goal(node.state):
        return Solution(True, node.get_path(), node.get_states(), node.get_state(), node.get_cost(), 1, node.get_depth(), time.time()-start_time)
    
    frontier = deque([node])
    explored = []
    
    while frontier:
        node = frontier.pop()
        explored.append(node.state)

        actions = get_actions(node.state)
        for action in actions:
            child = node.expand(action)
            if child.state not in explored and child not in frontier:
                if is_goal(child.state):
                    return Solution(True, child.get_path(), child.get_states(), child.get_state(), child.get_cost(), len(explored) + len(frontier), child.get_depth(), time.time()-start_time)
                frontier.append(child)

    # failure
    return Solution(False, node.get_path(), node.get_states(), node.get_state(), node.get_cost(), len(explored) + len(frontier), node.get_depth(), time.time()-start_time)
