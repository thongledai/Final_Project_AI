from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *


def ABPS(node, alpha, beta, maximizing_player):

    actions=get_actions(node.state)
    if is_goal(node.state):
        if maximizing_player: # tới lượt máy -> Máy thua
           return -1
        else:    # tới lượt người -> Máy thắng
           return 1
        
    elif len(actions)==0 or node.is_cycle(): # Hòa
        return 0
    
    if maximizing_player:  # True: Máy đi
        value = -1
        for action in actions:
            child = node.expand(action)
            value = max(value, ABPS(child, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break 
        return value
    
    else: # False: Người đi
        value = 1
        for action in actions:
            child = node.expand(action)
            value = min(value, ABPS(child, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value
   

