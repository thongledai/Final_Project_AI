from Core.Node import *
from Core.Utils import *
from Core.Action import *
from algorithms.adversarial_search.minimax_search import minimax_search
from algorithms.adversarial_search.alpha_beta_pruning_search import alpha_beta_pruning_search
from algorithms.adversarial_search.expectimax_search import expectimax_search

# turn: lượt đi: True: máy, False: người
# algorithm: minimax_search, alpha_beta_pruning_search, expectimax_search
def game(START, turn, algorithm):  
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
                eval = algorithm(child, False)
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
