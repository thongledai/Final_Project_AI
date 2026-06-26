import heapq
import time
import itertools

from Core.Utils import *
from Core.Action import get_actions
from Core.Node import Node
from Core.Result import solution
from Core.Utils import is_goal, state_to_tuple
from Core.Cost import heuristic
MAX_BELIEF_STATES = 2  # Số belief states tối đa suy ra từ partial obs


# Nhận vào partial_state là list 2D (list of lists).
# Trả về list các possible states, mỗi state cũng là list 2D.
def generate_belief_states(partial_state: list, known_colors: list[int],
                           max_beliefs: int = MAX_BELIEF_STATES) -> list[list]:
    observed = []
    unknown_positions = []  # (tube_idx, slot_idx)

    for ti, tube in enumerate(partial_state):
        for si, cell in enumerate(tube):
            if cell == -1:
                unknown_positions.append((ti, si))
            elif cell is not None:
                observed.append(cell)

    if not unknown_positions:
        # Deep copy để tránh mutation ngoài ý muốn
        return [[list(tube) for tube in partial_state]]

    remaining = list(known_colors)
    for c in observed:
        if c in remaining:
            remaining.remove(c)

    if len(remaining) != len(unknown_positions):
        return [[list(tube) for tube in partial_state]]

    belief_states = []
    # Dùng frozenset của tuple để dedup — chỉ dùng nội bộ, output vẫn là list
    seen = set()

    for perm in itertools.permutations(remaining):
        # Tạo deep copy của partial_state để điền vào
        candidate = [list(tube) for tube in partial_state]
        for idx, (ti, si) in enumerate(unknown_positions):
            candidate[ti][si] = perm[idx]

        # Key để dedup: convert sang tuple of tuples tạm thời
        key = tuple(tuple(tube) for tube in candidate)
        if key not in seen:
            seen.add(key)
            belief_states.append(candidate)

        if len(belief_states) >= max_beliefs:
            break

    return belief_states if belief_states else [[list(tube) for tube in partial_state]]


# Key duy nhất cho một belief set (list các Node).
# Dùng frozenset of tuples — tương đương State_To_Tuple() nhưng cho cả tập.
# frozenset vì thứ tự các belief states không quan trọng.
def belief_key(nodes: list) -> frozenset:
    return frozenset(state_to_tuple(n.state) for n in nodes)


# Heuristic cho belief set = max(h(s)) — pessimistic.
# Đảm bảo admissible: phải giải được state khó nhất thì mới xong.
def belief_h(nodes: list) -> int:
    return max(heuristic(n.state) for n in nodes)


def belief_is_goal(nodes: list) -> bool:
    return all(is_goal(n.state) for n in nodes)


def belief_a_star_search(initial_state, known_colors, max_expanded=100000):
    start_time = time.time()

    beliefs     = generate_belief_states(initial_state, known_colors)
    start_nodes = [Node(state) for state in beliefs]

    counter   = itertools.count()
    g0        = 0
    h0        = belief_h(start_nodes)

    frontier  = [(h0, g0, next(counter), start_nodes)]
    best_cost = {belief_key(start_nodes): g0}
    reached   = set()

    expanded_nodes  = 0
    generated_nodes = 1

    while frontier and expanded_nodes < max_expanded:
        _, g, _, nodes = heapq.heappop(frontier)
        key = belief_key(nodes)

        if nodes[0].cost != best_cost.get(key):
            continue
        if key in reached:
            continue

        # Goal: TẤT CẢ states phải là goal
        if belief_is_goal(nodes):
            return solution(nodes[0], expanded_nodes, generated_nodes, start_time)

        reached.add(key)
        expanded_nodes += 1

        # UNION actions trên TẤT CẢ states — kể cả state đã goal
        # vì state đó vẫn có thể nhận action valid
        all_actions = set()
        for n in nodes:
            for action in get_actions(n.state):
                all_actions.add(action)

        for action in all_actions:
            next_nodes   = []
            action_cost  = None   # cost sau khi expand

            for n in nodes:
                actions_for_n = list(get_actions(n.state))
                if action in actions_for_n:
                    child = n.expand(action)
                    next_nodes.append(child)
                    action_cost = child.cost   # lấy cost từ node được expand
                else:
                    next_nodes.append(n)

            # Nếu không node nào apply được → bỏ action này
            if action_cost is None:
                continue

            child_key = belief_key(next_nodes)
            new_cost  = action_cost            # ← dùng cost thực, không nodes[0].cost
            old_cost  = best_cost.get(child_key, float("inf"))

            if new_cost >= old_cost:
                continue
            if child_key in reached:
                reached.remove(child_key)

            best_cost[child_key] = new_cost
            priority = new_cost + belief_h(next_nodes)
            heapq.heappush(frontier, (priority, new_cost, next(counter), next_nodes))
            generated_nodes += 1

    best_nodes = min(
        (item[3] for item in frontier),
        key=belief_h,
        default=start_nodes
    )
    return solution(best_nodes[0], expanded_nodes, generated_nodes, start_time)

def partial_search(start):
    known_colors = [1, 1, 1, 1,
                    2, 2, 2, 2,
                    3, 3, 3, 3,
                    4, 4, 4, 4,
                    5, 5, 5, 5]
    
    return belief_a_star_search(start, known_colors)