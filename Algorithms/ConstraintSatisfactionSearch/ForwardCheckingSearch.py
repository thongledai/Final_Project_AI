
import time

from Core.Utils import *
from Core.Node import *
from Core.Result import *

def forward_checking_search(start):

    start_time = time.time()

    node = Node(start)

    explored = set()
    stats = {
        "generated": 1,
        "expanded": 0,
        "max_cost_node": node
    }

    node_final = search(node, explored, stats)

    return Solution(
        stats["max_cost_node"] if node_final is None else node_final,
        stats["expanded"],
        stats["generated"],
        start_time
    )


def search(node, explored, stats):

    if state_to_tuple(node.state) in explored:
        return None

    if node.cost > stats["max_cost_node"].cost:
        stats["max_cost_node"] = node
        
    stats["expanded"] += 1      # node đang được xét

    if is_goal(node.state):
        return node

    explored.add(state_to_tuple(node.state))

    for action in get_actions(node.state):

        if not is_valid_action(node.state, action):
            continue

        child = node.expand(action)
        stats["generated"] += 1  # sinh ra node mới

        res = search(child, explored, stats)

        if res is not None:
            return res

    return None

# Không đổ từ ống chỉ có 1 màu sang ống rổng
def is_valid_action(state, action):
    src, dst = action
    
    src_tube = state[src]
    dst_tube = state[dst] 

    # --- Forward Checking: Chặn đổ từ ống thuần nhất sang ống trống ---
    if len(dst_tube) == 0 and len(set(src_tube)) == 1:
        return False  # Trả về False để CHẶN hành động dư thừa này

    return True


        


