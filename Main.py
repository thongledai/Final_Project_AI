from Core.Utils import START

from algorithms.uninformed_search.breadth_first_search import breadth_first_search
from algorithms.uninformed_search.depth_first_search import depth_first_search
from algorithms.uninformed_search.iterative_deepening_search import iterative_deepening_search
from algorithms.uninformed_search.uniform_cost_search import uniform_cost_search
from algorithms.informed_search.a_star_search import *
if __name__ == "__main__":
    result = breadth_first_search(START)

    print("\n=== KET QUA TIM KIEM DFS ===")
    print(f"- Success          : {result.success}")
    print(f"- Path             : {result.path}")
    print(f"- States           : {result.states}")
    print(f"- Last state       : {result.last_state}")
    print(f"- Cost             : {result.cost}")
    print(f"- Generated states : {result.generated}")
    print(f"- Depth            : {result.depth}")
    print(f"- Runtime          : {result.runtime:.6f}s")


# if __name__ == "__main__":
#     Game(START, False)
