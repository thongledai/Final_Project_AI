import random
import time
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, Child_Nodes, Heuristic


def _Hill_Climb(start, max_steps, rng):
    current = start
    expanded = 0
    generated = 0

    for _ in range(max_steps):
        if Is_Goal(current.state):
            break

        children = Child_Nodes(current)
        expanded += 1
        generated += len(children)

        better_neighbors = [
            child
            for child in children
            if Heuristic(child.state) < Heuristic(current.state)
        ]

        if not better_neighbors:
            break

        next_state = rng.choice(better_neighbors)
        current = next_state

    return current, expanded, generated


def Random_Restart_Hill_Climbing_Search(
    initial_state,
    restarts=20,
    max_steps=500,
    random_walk_steps=10,
    seed=None,
):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state)
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(restarts):
        current = Node(initial_state)
        current, expanded, generated = _Hill_Climb(current, max_steps, rng)
        expanded_nodes += expanded
        generated_nodes += generated

        if Is_Goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

    return Solution(current, expanded_nodes, generated_nodes, start_time)


