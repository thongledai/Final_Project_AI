from Core.Node import *
from Core.Action import *
from Core.Utils import *
from Core.Result import *

def ES(node, maximizing_player):

    actions=get_actions(node.state)
    if is_goal(node.state):
        if maximizing_player: # tới lượt máy -> Máy thua
           return -1
        else:    # tới lượt người -> Máy thắng
           return 1
        
    elif len(actions)==0 or node.is_cycle(): # Hòa
        return 0
    
    if maximizing_player: # True: Máy đi
        max_eval = -1
        for action in actions:
            child = node.expand(action)
            eval = ES(child, False)
            max_eval = max(max_eval, eval)
        return max_eval
       
    else: # False: Người đi
        chance_eval = 0
        for action in actions:
            child = node.expand(action)
            eval = ES(child, True)
            chance_eval += eval
        return chance_eval / len(actions)