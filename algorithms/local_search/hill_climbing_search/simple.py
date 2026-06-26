import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def simple_hill_climbing(START):
    start_time = time.time()
    current = Node(START, cost=heuristic(START))
    explored_nodes = 0
    generated_nodes = 1

    for _ in range(MAX_STEPS):
        if is_goal(current.state):
            return solution(current, explored_nodes, generated_nodes, start_time)
        explored_nodes += 1
        next_node = None
        
        children = child_nodes(current)
        for child in children:         
            generated_nodes += 1

            if child.get_cost() < current.get_cost():
                next_node = child
                break

        if next_node is None:
            break
        current = next_node

    return solution(current, explored_nodes, generated_nodes, start_time)