from Core.Utils import START

# from Algorithms.ConstraintSatisfactionSearch.AC_3 import *
from Algorithms.ConstraintSatisfactionSearch.BacktrackingSearch import *
# from Algorithms.ConstraintSatisfactionSearch.ForwardCheckingSearch import *

from Algorithms.Uninformed_Search.Breadth_First_Search import *
from Algorithms.Informed_Search.A_Star_Search import *
from Algorithms.SearchingInComplexEnvironments.PartiallyObservableSearch import *

if __name__ == "__main__":
    # Chạy thuật toán DFS
    x = [[2,3,2,1], [2,1,3,4], [1,1,4,5], [4,4,3,5], [2,5,3,5], [], []]
    
    partial_start = [
            [-1, -1, -1, 1],  # Ống 0: chỉ thấy top 2 là 3,1
            [-1, -1, -1, 1],  # Ống 1: chỉ thấy top 2 là 1,2
            [-1, -1, -1, 2],  # Ống 2: chỉ thấy top 2 là 2,3
            [-1, -1, -1, 3],
            [-1, -1, -1, 3],
            [],
            [],# Ống 3: rỗng hoàn toàn [đã biết]
        ]
    
    result = partial_search(partial_start)
    
    # result = A_Star_Search(x)

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

