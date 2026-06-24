from Core.Utils import *
from Core.Action import *

# Chi phí di chuyển
# Hàm g(x) = g(x) + 4 + số lượng phần tử còn lại - số lượng phần tử đổ thành công
def step_cost(state, action):
    i1 = action[0]
    moved = get_steps(state, action)
    remain = get_count_same_top(state,i1) - moved
    return 4 + remain - moved
    

