from Core.Utils import START
from Algorithms.UninformedSearch.DepthFirstSearch import DFS 
from Algorithms.UninformedSearch.IterativeDeepeningSearch import IDS
<<<<<<< HEAD

if __name__ == "__main__":
    # Chạy thuật toán DFS
    result = IDS(START)
    
    # In kết quả chứa trong đối tượng Solution ra terminal
    print("\n=== KẾT QUẢ TÌM KIẾM IDS ===")
=======
from Algorithms.UninformedSearch.UniformCostSearch import UCS

if __name__ == "__main__":
    # Chạy thuật toán DFS
    result = UCS(START)
    
    # In kết quả chứa trong đối tượng Solution ra terminal
    print("\n=== KẾT QUẢ TÌM KIẾM UCS ===")
>>>>>>> Thong
    print(f"- Success          : {result.success}")
    print(f"- Path             : {result.path}")
    print(f"- States           : {result.states}")
    print(f"- Last state       : {result.last_state}")
    print(f"- Cost             : {result.cost}")
    print(f"- Generated states : {result.generated_states}")
    print(f"- Depth            : {result.depth}")
    print(f"- Runtime          : {result.runtime:.6f}s")
