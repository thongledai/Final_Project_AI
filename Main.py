from Core.Utils import START
from Algorithms.UninformedSearch.BreadthFirstSearch import BFS 

if __name__ == "__main__":
    # Chạy thuật toán BFS
    result = BFS(START)
    
    # In kết quả chứa trong đối tượng Solution ra terminal
    print("=== KẾT QUẢ TÌM KIẾM BFS ===")
    print(f"- Success          : {result.success}")
    print(f"- Path             : {result.path}")
    print(f"- States           : {result.states}")
    print(f"- Final state      : {result.final_state}")
    print(f"- Cost             : {result.cost}")
    print(f"- Generated states : {result.generated_states}")
    print(f"- Depth            : {result.depth}")
    print(f"- Runtime          : {result.runtime:.6f}s")