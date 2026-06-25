import random
import time
from Core.Result import Solution
from Core.Node import Node
from Core.Utils import Is_Goal, State_To_Tuple,Child_Nodes, Heuristic


def Stochastic_Hill_Climbing_Search(initial_state, max_steps=1000, seed=None):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state)
    seen = {State_To_Tuple(initial_state)}
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        if Is_Goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

        children = Child_Nodes(current)
        expanded_nodes += 1
        generated_nodes += len(children)
        improving = [
            child
            for child in children
            if Heuristic(child.state) < Heuristic(current.state)
            and State_To_Tuple(child.state) not in seen
        ]

        if not improving:
            break

        weights = [Heuristic(current.state) - Heuristic(child.state) for child in improving]
        current = rng.choices(improving, weights=weights, k=1)[0]
        seen.add(State_To_Tuple(current.state))

    return Solution(current, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_steps=1000, seed=None):
    return Stochastic_Hill_Climbing_Search(initial_state, max_steps, seed)
