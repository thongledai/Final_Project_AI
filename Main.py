from GUI.Controller import Controller

from algorithms.informed_search.ida_star_search import ida_star_search

if __name__ == "__main__":

    START = [[1, 1, 2, 2],      # lọ 0
         [3, 3, 3, 1],      # lọ 1
         [2, 2, 1, 3],      # lọ 2
         [          ]]      # lọ 3
    
    # [[1,2,3,1],[2,3,1,3],[3,1,2,2],[]]
    # [[3,1,2,2],[1,2,3,1],[2,3,1,3],[]]
    # [[2,3,1,3],[3,1,2,2],[1,2,3,1],[]]
    # [[1,3,2,2],[2,1,3,1],[3,2,1,3],[]]
    # [[3,2,1,3],[1,3,2,2],[2,1,3,1],[]]
    # [[2,1,3,1],[3,2,1,3],[1,3,2,2],[]]
    print(ida_star_search([[1,2,3,1],[2,3,1,3],[3,1,2,2],[]]))
    # Controller()
