from math import exp
import time
import random
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def simulated_annealing_search(initial_state, start_temperature=10.0, cooling_rate=0.995):
    start_time = time.time()
    current = Node(initial_state, cost=heuristic(initial_state))
    best = current
    explored_nodes = 0
    generated_nodes = 1
    temperature = start_temperature
    visited = {state_to_tuple(initial_state)}

    for _ in range(MAX_STEPS):
        if is_goal(current.state):
            return solution(current, explored_nodes, generated_nodes, start_time)

        children = child_nodes(current)
        explored_nodes += 1
        generated_nodes += len(children)

        valid_children = [child for child in children if state_to_tuple(child.state) not in visited]
        
        if not valid_children or temperature <= 0.000001:
            break

        next_node = random.choice(valid_children)
        delta = next_node.cost - current.cost

        if delta < 0:
            current = next_node
            visited.add(state_to_tuple(current.state))
        else:
            probability = exp(-delta / temperature)
            if random.random() < probability:
                current = next_node
                visited.add(state_to_tuple(current.state))

        if current.cost < best.cost:
            best = current

        temperature *= cooling_rate

    # Trả về node tốt nhất tìm được
    if is_goal(best.state):
        return solution(best, explored_nodes, generated_nodes, start_time)
    return solution(best, explored_nodes, generated_nodes, start_time)


