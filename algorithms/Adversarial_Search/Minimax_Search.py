from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


def Minimax_Search(node, maximizing_player):
    actions = Get_Actions(node.state)
    if Is_Goal(node.state):
        if maximizing_player:  # toi luot may -> May thua
            return -1
        else:  # toi luot nguoi -> May thang
            return 1

    elif len(actions) == 0 or node.Is_Cycle():  # Hoa
        return 0

    if maximizing_player:  # True: May di
        max_eval = -1
        for action in actions:
            child = node.Expand(action)
            eval = Minimax_Search(child, False)
            max_eval = max(max_eval, eval)
        return max_eval

    else:  # False: Nguoi di
        min_eval = 1
        for action in actions:
            child = node.Expand(action)
            eval = Minimax_Search(child, True)
            min_eval = min(min_eval, eval)
        return min_eval
