from Core.Node import *
from Core.Utils import *
from Core.Action import *
from Algorithms.AdversarialSearch.MinimaxSearch import MS
from Algorithms.AdversarialSearch.AlphaBetaPruningSearch import ABPS
from Algorithms.AdversarialSearch.ExpectimaxSearch import ES


def Game(START, turn): # True: Máy, False: Người
    node = Node(START) 
    step=0

    while True:

        step+=1
        print(step)

        for i in node.state:
            print(i)
        print()

        actions = get_actions(node.state)
        if is_goal(node.state):
            if turn:    # tới lượt máy -> người đã win
                print("Human win")
                break
            else:       # tới lượt người -> máy đã win
                print("Machine win")
                break
        elif len(actions) == 0 or node.is_cycle(): # không thể đi tiếp hoặc lặp lại trạng thái cũ -> hòa
            print("Draw")
            break

        if turn:
            print("Machine turn")
            max_eval = -1
            best_action = actions[0]

            for action in actions:
                child = node.expand(action)
                #eval = MS(child, False)
                #eval = ABPS(child, -1, 1, False)
                eval = ES(child, False)
                if eval > max_eval:
                    max_eval = eval
                    best_action = action

            print("Move:", best_action)
            node = node.expand(best_action)

        else:
            print("Human turn")
            while True:
                i1, i2 = map(int, input("Move: ").split())

                if (i1, i2) in actions:
                    node = node.expand((i1, i2))
                    break
                else:
                    print("Invalid move")
        print()
        turn = not turn
