from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


def Alpha_Beta_Pruning_Search(node, alpha, beta, maximizing_player):
    actions = get_actions(node.state)
    if is_goal(node.state):
        if maximizing_player:  # toi luot may -> May thua
            return -1
        else:  # toi luot nguoi -> May thang
            return 1

    elif len(actions) == 0 or node.Is_Cycle():  # Hoa
        return 0

    if maximizing_player:  # True: May di
        value = -1
        for action in actions:
            child = node.Expand(action)
            value = max(value, Alpha_Beta_Pruning_Search(child, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value

    else:  # False: Nguoi di
        value = 1
        for action in actions:
            child = node.Expand(action)
            value = min(value, Alpha_Beta_Pruning_Search(child, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value
