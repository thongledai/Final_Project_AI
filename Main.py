from GUI.Controller import Controller

from algorithms.adversarial_search.minimax_search import minimax_search

if __name__ == "__main__":

    START = [[1, 1, 2, 2],      # lọ 0
         [3, 3, 3, 1],      # lọ 1
         [2, 2, 1, 3],      # lọ 2
         [          ]]      # lọ 3
    
    [[1,2,3,1],[2,3,1,3],[3,1,2,2],[]]
    # [[3,1,2,2],[1,2,3,1],[2,3,1,3],[]]
    # [[2,3,1,3],[3,1,2,2],[1,2,3,1],[]]
    # [[1,3,2,2],[2,1,3,1],[3,2,1,3],[]]
    # [[3,2,1,3],[1,3,2,2],[2,1,3,1],[]]
    # [[2,1,3,1],[3,2,1,3],[1,3,2,2],[]]
    print(minimax_search([[1,2,3,1],[2,3,1,3],[3,1,2,2],[]]))
    # Controller()
