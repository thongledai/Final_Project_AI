# Số lượng phần tử tối đa trong một lọ và số lọ
CAPACITY = 4
NUM_BOTTLES = 6


# Sao chép trạng thái
def copy_state(state):
    return [row[:] for row in state]

# Chuyển trạng thái từ list sang tuple
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

# Lấy vị trí của phần tử trên cùng của một lọ
def get_top_index(state, bottle):
    for i in range(CAPACITY-1,-1,-1):
        if state[bottle][i] is not None:
            return i
    return -1

# Lấy màu của phần tử trên cùng của một lọ
def get_top_color(state,bottle):
    top=get_top_index(state,bottle)
    if top==-1:
        return None
    return state[bottle][top]

# Kiểm tra xem một lọ có rỗng không
def is_empty(state,bottle):
    return get_top_index(state,bottle)==-1

# Kiểm tra xem một lọ có đầy không
def is_full(state,bottle):
    return None not in state[bottle]

# Đếm số lượng phần tử rỗng trong một lọ
def empty_slots(state,bottle):
    return state[bottle].count(None)

# Đếm số lượng phần tử cùng màu ở trên cùng của một lọ
def get_count_same_top(state,bottle):
    top=get_top_index(state,bottle)
    if top==-1:
        return 0
    color=state[bottle][top]
    count=0
    while top>=0 and state[bottle][top]==color:
        count+=1
        top-=1
    return count

# Kiểm tra xem có thể đổ nước từ lọ src sang lọ dst không
def can_pour(state,src,dst):
    if src==dst:
        return False
    if is_empty(state,src):
        return False
    if is_full(state,dst):
        return False
    src_color=get_top_color(state,src)
    dst_color=get_top_color(state,dst)
    if dst_color is None:
        return True
    return src_color==dst_color

def pour(state,src,dst):
    if not can_pour(state,src,dst):
        return None
    new_state=copy_state(state)
    color=top_color(new_state,src)
    count=count_same_top(new_state,src)
    empty=empty_slots(new_state,dst)
    move=min(count,empty)
    for _ in range(move):
        src_top=get_top(new_state,src)
        dst_top=get_top(new_state,dst)
        new_state[src][src_top]=None
        if dst_top==-1:
            pos=0
        else:
            pos=dst_top+1
        new_state[dst][pos]=color
    return new_state

def goal_test(state,goal):
    return state==goal

def solution(node):
    path=[]
    actions=[]
    while node is not None:
        path.append(node.state)
        actions.append(node.action)
        node=node.parent
    path.reverse()
    actions.reverse()
    actions=actions[1:]
    return path,actions

