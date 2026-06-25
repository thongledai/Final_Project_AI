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
    if Is_Goal(node.state):
        return Solution(node,1,1, start_time)
    
    frontier = deque([node])
    explored = []
    
    while frontier:
        node = frontier.pop()
        explored.append(node.state)

        actions = Get_Actions(node.state)
        for action in actions:
            child = node.Expand(action)
            
            if child.state not in explored and child not in frontier:
                if Is_Goal(child.state):
                    return Solution(child, len(explored), len(explored) + len(frontier), start_time)
                frontier.append(child)

    # failure
    return Solution(node, len(explored), len(explored) + len(frontier), start_time)
