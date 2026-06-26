from collections import deque
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *

# Thuật toán tìm kiếm theo chiều sâu dần
def iterative_deepening_search(START):
    global start_time
    start_time= time.time()
    depth=0
    while True:
        result = depth_limited_search(START, depth)
        if result != "cutoff":
            result.runtime = time.time() - start_time
            return result
        

# Depth Limited Search
def depth_limited_search(START, limit):
    node = Node(START)
    frontier = deque([node])
    explored = []

    result = solution(node, len(explored), len(explored) + len(frontier), start_time)
    while frontier:
        node=frontier.pop()
        explored.append(node.state)

        if is_goal(node.state):
            return solution(node, len(explored), len(explored) + len(frontier), start_time)
        
        if node.get_depth() >=limit:
            result = "cutoff"
        else:
            actions = get_actions(node.state)
            for action in actions:
                child = node.expand(action)
                
                if not child.is_cycle():
                    frontier.append(child)

    return result
