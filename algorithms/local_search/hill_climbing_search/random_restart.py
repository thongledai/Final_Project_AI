import random
import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def random_restart_hill_climbing_search(START, restarts=20):
    start_time = time.time()
    current = Node(START, cost=heuristic(START))
    explored_nodes = 0
    generated_nodes = 1

    for _ in range(restarts):
        current = Node(START, cost=heuristic(START))
        current, expanded, generated = _hill_climb(current)
        explored_nodes += expanded
        generated_nodes += generated

        if is_goal(current.state):
            return solution(current, explored_nodes, generated_nodes, start_time)

    return solution(current, explored_nodes, generated_nodes, start_time)



def _hill_climb(START):
    current = START
    explored = 0
    generated = 0
    visited = {state_to_tuple(current.state)}

    for _ in range(MAX_STEPS):
        if is_goal(current.state):
            break

        children = child_nodes(current)
        explored += 1
        generated += len(children)

        better_neighbors = [child for child in children
                            if child.cost <= current.cost
                            and state_to_tuple(child.state) not in visited]

        if not better_neighbors:
            break

        current = random.choice(better_neighbors)
        visited.add(state_to_tuple(current.state))

    return current, explored, generated




