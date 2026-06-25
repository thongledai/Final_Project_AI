from Core.Utils import START
from algorithms.uninformed_search.Breadth_First_Search import Bfs
from algorithms.uninformed_search.Depth_First_Search import Dfs
from algorithms.uninformed_search.Iterative_Deepening_Search import Ids
from algorithms.uninformed_search.Uniform_Cost_Search import Ucs
from algorithms.adversarial_search.Game import Game


# if __name__ == "__main__":
#     result = Dfs(START)
#
#     print("\n=== KET QUA TIM KIEM DFS ===")
#     print(f"- Success          : {result.success}")
#     print(f"- Path             : {result.path}")
#     print(f"- States           : {result.states}")
#     print(f"- Last state       : {result.last_state}")
#     print(f"- Cost             : {result.cost}")
#     print(f"- Generated states : {result.generated}")
#     print(f"- Depth            : {result.depth}")
#     print(f"- Runtime          : {result.runtime:.6f}s")


if __name__ == "__main__":
    Game(START, False)