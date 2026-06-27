from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *
import time


def alpha_beta_pruning_search(node, maximizing_player=True, alpha=-1, beta=1):
    if isinstance(node, list):
        node = Node(node)
    
    explored = 0
    generated = 1
    start_time = time.time()

    final_node = node
    is_last_node = True
    def save_final_node(node):
        nonlocal final_node, is_last_node

        if is_last_node:
            final_node = node
            is_last_node = False

    def AB(node, maximizing_player, alpha, beta):
        nonlocal explored, generated
        explored += 1

        actions = get_actions(node.state)

        if is_goal(node.state):
            if maximizing_player:  # toi luot may -> May thua
                save_final_node(node)
                return -1
            else:                  # toi luot nguoi -> May thang
                save_final_node(node)
                return 1

        elif len(actions) == 0 or node.is_cycle():  # Hoa
            save_final_node(node)
            return 0

        if maximizing_player:  # True: May di
            value = -1
            for action in actions:
                child = node.expand(action)
                generated += 1
                value = max(value, AB(child, False, alpha, beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value

        else:  # False: Nguoi di
            value = 1
            for action in actions:
                child = node.expand(action)
                generated += 1
                value = min(value, AB(child, True, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    score = AB(node, maximizing_player, alpha, beta)
    return score, solution(final_node, explored, generated, start_time)