import time

from Core.Node import *
from Core.Result import *

def Backtracking_search(start):
    start_time = time.time()

    node = Node(start)

    explored = set()
    stats = {
        "generated_node": 1,  # node gốc
        "explored_node": 0,
        "max_cost_node": node
    }

    node_final = search(node, explored, stats)

    return Solution(
        stats["max_cost_node"] if node_final is None else node_final,
        stats["explored_node"],
        stats["generated_node"],
        start_time
    )


def search(node, explored, stats):

    if state_to_tuple(node.state) in explored:
        return None

    if node.cost > stats["max_cost_node"].cost:
        stats["max_cost_node"] = node

    stats["explored_node"] += 1      # node đang được xét

    if is_goal(node.state):
        return node

    explored.add(state_to_tuple(node.state))

    for action in get_actions(node.state):

        child = node.expand(action)
        stats["generated_node"] += 1  # sinh ra node mới

        res = search(child, explored, stats)

        if res is not None:
            return res

    return None