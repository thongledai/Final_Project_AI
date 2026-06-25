from Core.Utils import *


# Kiểm tra xem có thể đổ nước từ lọ i1 sang lọ i2 không
def Check_Action(state,i1, i2):
    if i1==i2 or Is_Empty(state,i1) or Is_Full(state,i2):
        return False
    else:
        i1_value=Get_Top_Value(state,i1)
        i2_value=Get_Top_Value(state,i2)
        return Is_Empty(state,i2) or i1_value==i2_value


# Lấy danh sách các hành động có thể thực hiện từ trạng thái hiện tại (tối đa: A(2,4)=12)
def Get_Actions(state):
    result=[]
    for i1 in range(len(state)):
        for i2 in range(len(state)):
            if Check_Action(state,i1, i2):
                result.append((i1, i2))
    return result
    # eg: [(0, 1), (3, 2), (2, 3)]


# Số phần tử nước có thể đổ
def Get_Steps(state, action):
    i1, i2 = action
    runs=Get_Count_Same_Top(state,i1)
    slots=Empty_Slots(state,i2)
    return min(runs,slots)


# Thực hiện hành động đổ nước từ lọ i1 sang lọ i2 và trả về trạng thái mới
def Apply_Action(state, action):
    new_state=Copy_State(state)
    steps=Get_Steps(state, action)
    i1, i2 = action
    for _ in range(steps):
        value = new_state[i1].pop()
        new_state[i2].append(value)

    return new_state
