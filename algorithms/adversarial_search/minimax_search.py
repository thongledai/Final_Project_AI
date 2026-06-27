from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *
import time


def minimax_search(node, maximizing_player=True):
    if isinstance(node, list):
        node = Node(node)
    explored = 0
    generated = 1
    start_time = time.time()

    def MS(node, maximizing_player):
        nonlocal explored, generated
        explored += 1

        actions = get_actions(node.state)
        if is_goal(node.state):
            if maximizing_player: # Lượt máy, máy thua
                return -1
            else: # Lượt người, máy thắng
                return 1

        elif len(actions) == 0 or node.is_cycle():
            return 0

        if maximizing_player:
            max_eval = -1
            for action in actions:
                child = node.expand(action)
                generated += 1
                eval = MS(child, False)
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = 1
            for action in actions:
                child = node.expand(action)
                generated += 1
                eval = MS(child, True)
                min_eval = min(min_eval, eval)
            return min_eval

    score = MS(node, maximizing_player)
    return score, solution(None, explored, generated, start_time)