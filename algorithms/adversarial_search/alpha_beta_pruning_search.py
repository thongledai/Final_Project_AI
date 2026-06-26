from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


def alpha_beta_pruning_search(node, maximizing_player, alpha=-1, beta=1):
    actions = get_actions(node.state)
    if is_goal(node.state):
        if maximizing_player:  # toi luot may -> May thua
            return -1
        else:  # toi luot nguoi -> May thang
            return 1

    elif len(actions) == 0 or node.is_cycle():  # Hoa
        return 0

    if maximizing_player:  # True: May di
        value = -1
        for action in actions:
            child = node.expand(action)
            value = max(value, alpha_beta_pruning_search(child, False, alpha, beta))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value

    else:  # False: Nguoi di
        value = 1
        for action in actions:
            child = node.expand(action)
            value = min(value, alpha_beta_pruning_search(child, True, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value
