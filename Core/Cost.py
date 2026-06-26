from Core.Action import *
from Core.Result import *
from Core.Cost import *
from Core.Node import *
from Core.Utils import *

# Chi phí di chuyển(thực tế)
# g(x) = g(x) + 4 + số lượng phần tử còn lại - số lượng phần tử đổ thành công
def step_cost(state, action):
    i1 = action[0]
    moved = get_steps(state, action)
    remain = get_count_same_top(state,i1) - moved
    return 4 + remain - moved


# Chi phí ước lượng 
# h(n) = số ô còn trống + số lần hai màu cạnh nhau khác nhau trong 1 lọ
def heuristic(state):
    score = 0
    for tube in state:
        if not tube or (len(tube) == CAPACITY and len(set(tube)) == 1): # không tính lọ rỗng hoặc lọ đã hoàn thành
            continue

        score += CAPACITY - len(tube) # số ô còn trống
        score += sum(1 for i in range(1, len(tube)) # số lần 2 màu cạnh nhau khác nhau
                    if tube[i] != tube[i - 1])

    return score