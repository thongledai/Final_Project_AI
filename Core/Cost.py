from Core.Utils import *
from Core.Action import *

# Chi phí di chuyển
# Hàm g(x) = g(x) + 4 + số lượng phần tử còn lại - số lượng phần tử đổ thành công
def Step_Cost(state, action):
    i1 = action[0]
    moved = Get_Steps(state, action)
    remain = Get_Count_Same_Top(state,i1) - moved
    return 4 + remain - moved
    

