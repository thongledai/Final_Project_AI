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
            runtime = time.time() - start_time
            return result
        depth+=1
# Deoth Limited Search
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
                generated_states=1,
                depth=node.get_depth(),
                runtime=time.time()-start_time
        )
        if node.get_depth() >=limit:
            result = "cutoff"
        else:
            actions = get_actions(node.state)
            for action in actions:
                child = Node(state=apply_action(node.state, action), 
                            parent=node, 
                            action=action, 
                            cost=node.get_cost() + 1)
            if child.state not in explored and child not in frontier:
                frontier.append(child)

    return result