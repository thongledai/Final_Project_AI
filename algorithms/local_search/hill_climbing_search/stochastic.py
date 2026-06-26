import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def stochastic_hill_climbing_search(START):
    start_time = time.time()
    current = Node(START, cost=heuristic(START))
    explored_nodes = 0
    generated_nodes = 1
    visited = {state_to_tuple(START)}

    for _ in range(MAX_STEPS):
        if is_goal(current.state):
            return solution(current, explored_nodes, generated_nodes, start_time)

        children = child_nodes(current)
        explored_nodes += 1
        generated_nodes += len(children)
        better_neighbors = [child for child in children
                            if child.get_cost() <= current.get_cost()
                            and state_to_tuple(child.state) not in visited]

        if not better_neighbors:
            break

        current = random.choice(better_neighbors)
        visited.add(state_to_tuple(current.state))

    return solution(current, explored_nodes, generated_nodes, start_time)

