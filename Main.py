from Core.Utils import START
#from algorithms.local_search.hill_climbing_search.random_restart import random_restart_hill_climbing_search as random_restart
# 1. ADVERSARIAL SEARCH
# ==========================================

from algorithms.adversarial_search.game import *

# ==========================================
# 2. INFORMED SEARCH
# ==========================================
from algorithms.informed_search.a_star_search import a_star_search
from algorithms.informed_search.greedy_search import greedy_search
from algorithms.informed_search.ida_star_search import ida_star_search

# ==========================================
# 3. UNINFORMED SEARCH
# ==========================================
from algorithms.uninformed_search.breadth_first_search import breadth_first_search
from algorithms.uninformed_search.depth_first_search import depth_first_search
from algorithms.uninformed_search.iterative_deepening_search import iterative_deepening_search
from algorithms.uninformed_search.uniform_cost_search import uniform_cost_search

# ==========================================
# 4. LOCAL SEARCH
# ==========================================
from algorithms.local_search.hill_climbing_search.simple import simple_hill_climbing
from algorithms.local_search.hill_climbing_search.random_restart import random_restart_hill_climbing_search
from algorithms.local_search.hill_climbing_search.steepest_ascent import steepest_ascent_hill_climbing_search
from algorithms.local_search.hill_climbing_search.stochastic import stochastic_hill_climbing_search
# Các file ngang hàng trong local_search
from algorithms.local_search.local_beam_search import local_beam_search
from algorithms.local_search.simulated_annealing_search import simulated_annealing_search

# ==========================================
# 5. SEARCH COMPLEX ENVIRONMENTS
# ==========================================
from algorithms.search_complex_environments.and_or_graph_search import and_or_graph_search
from algorithms.search_complex_environments.partially_observable_search import partial_search

# 6
from algorithms.constraint_satisfaction_search.backtracking_search import backtracking_search
from algorithms.constraint_satisfaction_search.forward_checking_search import forward_checking_search


# if __name__ == "__main__":
#     result = forward_checking_search(START)

#     print("\n=== KET QUA TIM KIEM ===")
#     print(f"- Success          : {result.success}")
#     print(f"- Path             : {result.path}")
#     print(f"- States           : {result.states}")
#     print(f"- Last state       : {result.last_state}")
#     print(f"- Cost             : {result.cost}")
#     print(f"- Generated states : {result.generated}")
#     print(f"- Depth            : {result.depth}")
#     print(f"- Runtime          : {result.runtime:.6f}s")


if __name__ == "__main__":
    game(START, False, alpha_beta_pruning_search)
