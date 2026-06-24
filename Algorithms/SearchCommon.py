import time

from Core.Action import get_actions
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import CAPACITY, is_goal, state_to_tuple


def heuristic(state):
    # h(n) trong bài này là điểm đánh giá trạng thái còn lộn xộn bao nhiêu
    # Lọ rỗng -> +0
    # Lọ đầy 4 ô và cùng màu -> +0
    # Lọ chưa đúng -> cộng điểm phạt
    # Điểm phạt gồm:
    # +1 vì lọ chưa hoàn thành
    # + số ô còn trống
    # + số lần hai màu cạnh nhau khác nhau
    # + số màu khác nhau trong lọ - 1
    score = 0
    for tube in state:
        if not tube:
            continue

        if len(tube) == CAPACITY and len(set(tube)) == 1:
            continue

        score += 1
        score += CAPACITY - len(tube)
        score += sum(1 for i in range(1, len(tube)) if tube[i] != tube[i - 1])
        score += len(set(tube)) - 1

    return score


def build_result(node, success, expanded_nodes, generated_nodes, start_time):

    return Solution(
        success=success,
        path=node.get_path(),
        states=node.get_states(),
        last_state=node.get_state(),
        cost=node.cost,
        generated_states=generated_nodes,
        depth=node.get_depth(),
        runtime=time.time() - start_time,
    )


def child_nodes(node):
    return [node.expand(action) for action in get_actions(node.state)]


def best_child(node):
    children = child_nodes(node)
    if not children:
        return None, []
    return min(children, key=lambda child: (heuristic(child.state), child.cost)), children


def has_seen(node, seen):
    key = state_to_tuple(node.state)
    if key in seen:
        return True
    seen.add(key)
    return False
