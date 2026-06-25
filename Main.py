from Core.Utils import START
from Algorithms.UninformedSearch.BreadthFirstSearch import BFS 
from Algorithms.UninformedSearch.DepthFirstSearch import DFS 
from Algorithms.UninformedSearch.IterativeDeepeningSearch import IDS
from Algorithms.UninformedSearch.UniformCostSearch import UCS
from Algorithms.AdversarialSearch.Game import Game

from Algorithms.Informedsearch.AStarSearch import *
from Algorithms.ConstraintSatisfactionSearch.AC_3 import *
from Algorithms.ConstraintSatisfactionSearch.BacktrackingSearch import *
from Algorithms.ConstraintSatisfactionSearch.ForwardCheckingSearch import *

if __name__ == "__main__":
    # Chạy thuật toán DFS
    x = [[2,3,2,1], [2,1,3,4], [1,1,4,5], [4,4,3,5], [2,5,3,5], [], []] 
    # print(get_actions(x))
    result = forward_checking_search(x)
    
    # In kết quả chứa trong đối tượng Solution ra terminal
    print("\n=== KẾT QUẢ TÌM KIẾM ===")
    print(f"- Success          : {result.success}")
    print(f"- Path             : {result.path}")
    print(f"- States           : {result.states}")
    print(f"- Last state       : {result.last_state}")
    print(f"- Cost             : {result.cost}")
    print(f"- Generated states : {result.generated}")
    print(f"- Depth            : {result.depth}")
    print(f"- Runtime          : {result.runtime:.6f}s")

