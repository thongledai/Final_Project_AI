import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def steepest_ascent_hill_climbing_search(START):
    start_time = time.time()
    current = Node(START, cost=heuristic(START))
    explored_nodes = 0
    generated_nodes = 1

    for _ in range(MAX_STEPS):
        if is_goal(current.state):
            return solution(current, explored_nodes, generated_nodes, start_time)
        
        explored_nodes += 1
        children = child_nodes(current)
        generated_nodes += len(children)
        candidate = min(children, key=lambda child: child.cost) if children else None
        
        if (candidate is None) or ((candidate.get_cost()) >= current.get_cost()):
            break

        current = candidate

    return solution(current, explored_nodes, generated_nodes, start_time)
