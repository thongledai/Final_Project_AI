from Core.Node import *
from Core.Utils import *
from Core.Action import *
from algorithms.adversarial_search.Minimax_Search import Minimax_Search
from algorithms.adversarial_search.Alpha_Beta_Pruning_Search import Alpha_Beta_Pruning_Search
from algorithms.adversarial_search.Expectimax_Search import Expectimax_Search


def game(START, turn):  # True: May, False: Nguoi
    node = Node(START)
    step = 0

    while True:
        step += 1
        print(step)

        for i in node.state:
            print(i)
        print()

        actions = get_actions(node.state)
        if is_goal(node.state):
            if turn:  # toi luot may -> nguoi da win
                print("Human win")
                break
            else:  # toi luot nguoi -> may da win
                print("Machine win")
                break
        elif len(actions) == 0 or node.is_cycle():  # khong the di tiep hoac lap lai trang thai cu -> hoa
            print("Draw")
            break

        if turn:
            print("Machine turn")
            max_eval = -1
            best_action = actions[0]

            for action in actions:
                child = node.expand(action)
                # eval = Minimax_Search(child, False)
                # eval = Alpha_Beta_Pruning_Search(child, -1, 1, False)
                eval = Expectimax_Search(child, False)
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
