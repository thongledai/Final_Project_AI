import time
from Core.Action import Get_Actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, State_To_Tuple, Heuristic


def Simple_Hill_Climbing(initial_state, max_steps=1000):
    start_time = time.time()
    current = Node(initial_state)
    expanded_nodes = 1
    generated_nodes = 1

    for _ in range(max_steps):
        if Is_Goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

        expanded_nodes += 1
        current_value = Heuristic(current.state)
        next_state = None

        for action in Get_Actions(current.state):
            child = current.Expand(action)
            generated_nodes += 1

            if Heuristic(child.state) < current_value:
                next_state = child
                break

        if next_state is None:
            break

        current = next_state

    return Solution(current, expanded_nodes, generated_nodes, start_time)


def Search(initial_state, max_steps=1000):
    return Simple_Hill_Climbing(initial_state, max_steps)
