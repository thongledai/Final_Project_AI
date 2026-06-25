from collections import deque
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *

# Thuật toán tìm kiếm theo chiều sâu dần
def IDS(START):
    global start_time
    start_time= time.time()
    depth=0
    while True:
        result = DLS(START, depth)
        if result != "cutoff":
            result.runtime = time.time() - start_time
            return result
        

# Depth Limited Search
def DLS(START, limit):
    node = Node(START)
    frontier = deque([node])
    explored = []

    result = Solution(node, len(explored), len(explored) + len(frontier), start_time)
    while frontier:
        node=frontier.pop()
        explored.append(node.state)

        if Is_Goal(node.state):
            return Solution(node, len(explored), len(explored) + len(frontier), start_time)
        
        if node.Get_Depth() >=limit:
            result = "cutoff"
        else:
            actions = Get_Actions(node.state)
            for action in actions:
                child = node.Expand(action)
                
                if not child.Is_Cycle():
                    frontier.append(child)

    return result
