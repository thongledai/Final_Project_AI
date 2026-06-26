from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


def Expectimax_Search(node, maximizing_player):
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
            eval = Expectimax_Search(child, False)
            max_eval = max(max_eval, eval)
        return max_eval

    else:  # False: Nguoi di
        chance_eval = 0
        for action in actions:
            child = node.Expand(action)
            eval = Expectimax_Search(child, True)
            chance_eval += eval
        return chance_eval / len(actions)
