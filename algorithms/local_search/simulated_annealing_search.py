import math
import time
from Core.Action import *
from Core.Node import *
from Core.Result import *
from Core.Utils import *


def _child_nodes(node):
    children = []
    for action in get_actions(node.state):
        children.append(node.expand(action, "h(x)"))
    return children


def simulated_annealing_search(
    initial_state,
    max_steps=5000,
    start_temperature=10.0,
    cooling_rate=0.995,
    seed=None,
):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state, cost=heuristic(initial_state))
    expanded_nodes = 0
    generated_nodes = 1
    temperature = start_temperature

    for _ in range(max_steps):
        if is_goal(current.state):
            return solution(current, expanded_nodes, generated_nodes, start_time)

        children = _child_nodes(current)
        expanded_nodes += 1
        generated_nodes += len(children)

        if not children or temperature <= 0.000001:
            break

        next_state = rng.choice(children)
        delta = next_state.cost - current.cost

        if delta < 0:
            current = next_state
        else:
            probability = math.exp(-delta / temperature)
            if rng.random() < probability:
                current = next_state

        temperature *= cooling_rate

    return solution(current, expanded_nodes, generated_nodes, start_time)


