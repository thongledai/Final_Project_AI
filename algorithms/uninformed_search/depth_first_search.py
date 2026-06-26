from collections import deque
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


# Thuật toán tìm kiếm theo chiều sâu
def depth_first_search(START):
    start_time=time.time()
    node=Node(START)
    if is_goal(node.state):
        return solution(node,1,1, start_time)
    
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
                    return solution(child, len(explored), len(explored) + len(frontier), start_time)
                frontier.append(child)

    # failure
    return solution(node, len(explored), len(explored) + len(frontier), start_time)
