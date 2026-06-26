import time
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, State_To_Tuple,Best_Child, Heuristic


def Steepest_Ascent_Hill_Climbing_Search(initial_state, max_steps=1000):
    start_time = time.time()
    current = Node(initial_state)
    seen = {State_To_Tuple(initial_state)}
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        if Is_Goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

        candidate, children = Best_Child(current)
        expanded_nodes += 1
        generated_nodes += len(children)

        if candidate is None:
            break

        if Heuristic(candidate.state) >= Heuristic(current.state):
            break

        key = State_To_Tuple(candidate.state)
        if key in seen:
            break
        seen.add(key)
        current = candidate

    return Solution(current, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_steps=1000):
    return Steepest_Ascent_Hill_Climbing_Search(initial_state, max_steps)
