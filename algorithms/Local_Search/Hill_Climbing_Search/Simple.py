import time
from Core.Action import Get_Actions, Apply_Action
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, Heuristic


def Simple_Hill_Climbing(initial_state, max_steps=1000):
    start_time = time.time()
    current = Node(initial_state, cost=Heuristic(initial_state))
    expanded_nodes = 1
    generated_nodes = 1

    for _ in range(max_steps):
        if Is_Goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

        expanded_nodes += 1
        current_value = Heuristic(current.state)
        next_node = None

        for action in Get_Actions(current.state):
            child_state = Apply_Action(current.state, action)
            child = Node(
                state=child_state,
                parent=current,
                action=action,
                cost=Heuristic(child_state)
            )
            generated_nodes += 1

            if child.cost < current_value:
                next_node = child
                break

        if next_node is None:
            break

        current = next_node

    return Solution(current, expanded_nodes, generated_nodes, start_time)

