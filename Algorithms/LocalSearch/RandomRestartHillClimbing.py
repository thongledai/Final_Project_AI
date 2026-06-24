import random
import time

from Algorithms.SearchCommon import best_child, build_result, child_nodes, heuristic
from Core.Node import Node
from Core.Utils import is_goal, state_to_tuple


def _Random_walk(start, steps, rng):
    current = start
    seen = {state_to_tuple(current.state)}
    generated = 1

    for _ in range(steps):
        candidates = [
            child
            for child in child_nodes(current)
            if state_to_tuple(child.state) not in seen
        ]
        generated += len(candidates)
        if not candidates:
            break
        current = rng.choice(candidates)
        seen.add(state_to_tuple(current.state))

    return current, generated


def _Hill_climb(start, max_steps):
    current = start
    seen = {state_to_tuple(current.state)}
    expanded = 0
    generated = 0

    for _ in range(max_steps):
        if is_goal(current.state):
            break

        candidate, children = best_child(current)
        expanded += 1
        generated += len(children)

        if candidate is None or heuristic(candidate.state) >= heuristic(current.state):
            break

        key = state_to_tuple(candidate.state)
        if key in seen:
            break
        seen.add(key)
        current = candidate

    return current, expanded, generated


def Random_restart_hill_climbing(
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
    generated_nodes = 1

    for restart in range(restarts + 1):
        if restart == 0:
            start = root
        else:
            start, generated = _Random_walk(root, random_walk_steps, rng)
            generated_nodes += generated

        candidate, expanded, generated = _Hill_climb(start, max_steps)
        expanded_nodes += expanded
        generated_nodes += generated

        if heuristic(candidate.state) < heuristic(best.state):
            best = candidate

        if is_goal(candidate.state):
            return build_result(candidate, True, expanded_nodes, generated_nodes, start_time)

    return build_result(best, False, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, restarts=20, max_steps=500, random_walk_steps=10, seed=None):
    return Random_restart_hill_climbing(
        initial_state,
        restarts,
        max_steps,
        random_walk_steps,
        seed,
    )
