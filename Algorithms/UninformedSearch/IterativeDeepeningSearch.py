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

    result = Solution(
            success=False,
            path=node.get_path(),
            states=node.get_states(),
            last_state=node.get_state(),
            cost=node.get_cost(),
            generated_states=len(explored) + len(frontier),
            depth=node.get_depth(),
        )
    while frontier:
        node=frontier.pop()
        explored.append(node.state)

        if is_goal(node.state):
            return Solution(
                success=True,
                path=node.get_path(),
                states=node.get_states(),
                last_state=node.get_state(),
                cost=node.get_cost(),
                generated_states=len(explored) + len(frontier),
                depth=node.get_depth(),
                runtime=time.time()-start_time
        )
        if node.get_depth() >=limit:
            result = "cutoff"
        else:
            actions = get_actions(node.state)
            for action in actions:
                child = node.expand(action)
                if not child.is_cycle():
                    frontier.append(child)

    return result
