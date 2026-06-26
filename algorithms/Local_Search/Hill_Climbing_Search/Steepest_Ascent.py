import time
from Core.Action import Get_Actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal, Heuristic


def _Child_Nodes(node):
    children = []
    for action in Get_Actions(node.state):
        children.append(node.Expand(action, cost_function="h(x)"))
    return children


def Steepest_Ascent_Hill_Climbing_Search(initial_state, max_steps=1000):
    start_time = time.time()
    current = Node(initial_state, cost=Heuristic(initial_state))
    expanded_nodes = 0
    generated_nodes = 1

    for _ in range(max_steps):
        if Is_Goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

        children = _Child_Nodes(current)
        candidate = min(children, key=lambda child: child.cost) if children else None
        expanded_nodes += 1
        generated_nodes += len(children)

        if candidate is None:
            break

        if candidate.cost >= current.cost:
            break

        current = candidate

    return Solution(current, expanded_nodes, generated_nodes, start_time)
