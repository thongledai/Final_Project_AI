from Core.Action import *
from Core.Result import *
from Core.Cost import *
from Core.Node import *
from Core.Utils import *

# Kiểm tra xem có thể đổ nước từ lọ i1 sang lọ i2 không
def check_action(state,i1, i2):
    if i1==i2 or is_empty(state,i1) or is_full(state,i2):
        return False
    else:
        i1_value=get_top_value(state,i1)
        i2_value=get_top_value(state,i2)
        return is_empty(state,i2) or i1_value==i2_value


# Lấy danh sách các hành động có thể thực hiện từ trạng thái hiện tại (tối đa: A(2,4)=12)
def get_actions(state):
    result=[]
    for i1 in range(QUANTITY):
        for i2 in range(QUANTITY):
            if check_action(state,i1, i2):
                result.append((i1, i2))
    return result
    # eg: [(0, 1), (3, 2), (2, 3)]


# Số phần tử nước có thể đổ
def get_steps(state, action):
    i1, i2 = action
    runs=get_count_same_top(state,i1)
    slots=empty_slots(state,i2)
    return min(runs,slots)


# Thực hiện hành động đổ nước từ lọ i1 sang lọ i2 và trả về trạng thái mới
def apply_action(state, action):
    new_state=copy_state(state)
    steps=get_steps(state, action)
    i1, i2 = action
    for _ in range(steps):
        value = new_state[i1].pop()
        new_state[i2].append(value)

    return new_state
