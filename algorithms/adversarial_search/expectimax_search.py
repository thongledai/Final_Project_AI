from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *
import time


def expectimax_search(node, maximizing_player=True):
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

    def ES(node, maximizing_player):
        nonlocal explored, generated
        explored += 1

        actions = get_actions(node.state)
        if is_goal(node.state):
            if maximizing_player:  # toi luot may -> May thua
                save_final_node(node)
                return -1
            else:  # toi luot nguoi -> May thang
                save_final_node(node)
                return 1

        elif len(actions) == 0 or node.is_cycle():  # Hoa
            save_final_node(node)
            return 0

        if maximizing_player:  # True: May di
            max_eval = -1
            for action in actions:
                child = node.expand(action)
                generated += 1
                eval = ES(child, False)
                max_eval = max(max_eval, eval)
            return max_eval

        else:  # False: Nguoi di
            chance_eval = 0
            for action in actions:
                child = node.expand(action)
                generated += 1
                eval = ES(child, True)
                chance_eval += eval
            return chance_eval / len(actions)

    score = ES(node, maximizing_player)
    return score, solution(final_node, explored, generated, start_time)