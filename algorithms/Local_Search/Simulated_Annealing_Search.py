import math
import random
import time
from Core.Action import Get_Actions, Apply_Action
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, Heuristic


def _Child_Nodes(node):
    children = []
    for action in Get_Actions(node.state):
        child_state = Apply_Action(node.state, action)
        children.append(Node(
            state=child_state,
            parent=node,
            action=action,
            cost=Heuristic(child_state)
        ))
    return children


def Simulated_Annealing_Search(
    initial_state,
    max_steps=5000,
    start_temperature=10.0,
    cooling_rate=0.995,
    seed=None,
):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state, cost=Heuristic(initial_state))
    expanded_nodes = 0
    generated_nodes = 1
    temperature = start_temperature

    for _ in range(max_steps):
        if Is_Goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

        children = _Child_Nodes(current)
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

    return Solution(current, expanded_nodes, generated_nodes, start_time)


