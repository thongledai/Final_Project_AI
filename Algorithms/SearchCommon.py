import time

from Core.Action import actions
from Core.Node import Node
from Core.Result import SearchResult
from Core.Utils import CAPACITY, is_goal, state_to_tuple


def heuristic(state):
    """Lower is better. Counts disorder inside tubes and unfinished tubes."""
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
    if node is None:
        return SearchResult(
            success=False,
            path=[],
            states=[],
            final_state=None,
            cost=0,
            expanded_nodes=expanded_nodes,
            generated_nodes=generated_nodes,
            depth=0,
            runtime=time.time() - start_time,
        )

    return SearchResult(
        success=success,
        path=node.get_path(),
        states=node.get_states(),
        final_state=node.state,
        cost=node.cost,
        expanded_nodes=expanded_nodes,
        generated_nodes=generated_nodes,
        depth=node.get_depth(),
        runtime=time.time() - start_time,
    )


def child_nodes(node):
    return [node.expand(action) for action in actions(node.state)]


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
