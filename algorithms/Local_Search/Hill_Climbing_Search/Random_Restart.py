import random
import time
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, State_To_Tuple,Best_Child, Child_Nodes, Heuristic


def _Random_Walk(start, steps, rng):
    current = start
    seen = {State_To_Tuple(current.state)}
    generated = 1

    for _ in range(steps):
        candidates = [
            child
            for child in Child_Nodes(current)
            if State_To_Tuple(child.state) not in seen
        ]
        generated += len(candidates)
        if not candidates:
            break
        current = rng.choice(candidates)
        seen.add(State_To_Tuple(current.state))

    return current, generated


def _Hill_Climb(start, max_steps):
    current = start
    seen = {State_To_Tuple(current.state)}
    expanded = 0
    generated = 0

    for _ in range(max_steps):
        if Is_Goal(current.state):
            break

        candidate, children = Best_Child(current)
        expanded += 1
        generated += len(children)

        if candidate is None or Heuristic(candidate.state) >= Heuristic(current.state):
            break

        key = State_To_Tuple(candidate.state)
        if key in seen:
            break
        seen.add(key)
        current = candidate

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
    root = Node(initial_state)
    best = root
    expanded_nodes = 0
    generated_nodes = 0

    for restart in range(restarts + 1):
        if restart == 0:
            start = root
        else:
            start, generated = _Random_Walk(root, random_walk_steps, rng)
            generated_nodes += generated

        candidate, expanded, generated = _Hill_Climb(start, max_steps)
        expanded_nodes += expanded
        generated_nodes += generated

        if Heuristic(candidate.state) < Heuristic(best.state):
            best = candidate

        if Is_Goal(candidate.state):
            return Solution(candidate, expanded_nodes, generated_nodes, start_time)

    return Solution(best, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, restarts=20, max_steps=500, random_walk_steps=10, seed=None):
    return Random_Restart_Hill_Climbing_Search(
        initial_state,
        restarts,
        max_steps,
        random_walk_steps,
        seed,
    )
