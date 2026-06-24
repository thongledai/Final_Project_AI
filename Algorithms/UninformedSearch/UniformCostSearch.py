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
        return Solution(node,1,1,start_time)
    
    frontier = []
    explored = []
    heapq.heappush(frontier, node)

    while frontier:
        node = heapq.heappop(frontier)
        explored.append(node.state)
        if is_goal(node.state):
            return Solution(node,len(explored), len(explored) + len(frontier), start_time)
        
        actions = get_actions(node.state)
        for action1 in actions:
            child = node.expand(action=action1,cost_function="g(x)")
            if child.state not in explored and child not in frontier:
                heapq.heappush(frontier, child)

    # failure
    return Solution(node, len(explored), len(explored) + len(frontier), start_time)