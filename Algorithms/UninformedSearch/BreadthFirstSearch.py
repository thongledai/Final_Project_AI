from collections import deque
import time
from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


# Thuật toán tìm kiếm theo chiều rộng
def BFS(START):
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
    
    frontier = deque([node])
    explored = []
    
    while frontier:
        node = frontier.popleft()
        explored.append(node.state)

        actions = get_actions(node.state)
        for action in actions:
            child = Node(state=apply_action(node.state, action), 
                         parent=node, 
                         action=action, 
                         cost=node.get_cost() + 1)
            
            if child.state not in explored and child not in frontier:
                if is_goal(child.state):
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
                frontier.append(child)

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