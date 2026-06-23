# Số phần tử tối đa trong một lọ
CAPACITY = 4
# Số lọ
QUANTITY = 4


# Sao chép trạng thái
def copy_state(state):
    return [row[:] for row in state]


# Chuyển trạng thái từ list sang tuple
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


# Lấy vị trí của phần tử trên cùng của lọ i
def get_top_index(state, i):
    return len(state[i]) - 1


# Lấy màu của phần tử trên cùng của lọ i
def get_top_value(state,i):
    if is_empty(state, i):
        return None
    return state[i][-1]


# Kiểm tra xem lọ i có rỗng không
def is_empty(state, i):
    return len(state[i])==0


# Kiểm tra xem lọ i có đầy không
def is_full(state,i):
    return len(state[i])==CAPACITY


# Đếm số lượng phần tử rỗng trong lọ i
def empty_slots(state,i):
    return CAPACITY-len(state[i])


# Đếm số phần tử cùng màu liên tiếp ở top của lọ i
def get_count_same_top(state,i):
    j=get_top_index(state,i)
    if j==-1:
        return 0
    else:
        top_value=state[i][j]
        count=0
        while j>=0 and state[i][j]==top_value:
            count+=1
            j-=1
        return count


# Kiểm tra xem trạng thái hiện tại có phải là trạng thái mục tiêu không
def is_goal(state):
    for i in state:
        if len(i) == 0:
            continue
        if len(i) != CAPACITY or len(set(i)) != 1:
            return False
    return True





