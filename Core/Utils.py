import time
import random

# Số phần tử tối đa trong một lọ
CAPACITY = 4
# Số lọ
QUANTITY = 4


# Trạng thái ban đầu
START = [[1, 3, 2, 2],      # lọ 0
         [3, 2, 1, 3],      # lọ 1
         [1, 3, 2, 1],      # lọ 2
         [          ]]      # lọ 3

# Trạng thái ban đầu random
nums = [1]*4 + [2]*4 + [3]*4
random.shuffle(nums)
START_RANDOM = [
    nums[0:4],
    nums[4:8],
    nums[8:12],
    []             
]

# Sao chép trạng thái
def Copy_State(state):
    return [row[:] for row in state]


# Chuyển trạng thái từ list sang tuple
def State_To_Tuple(state):
    return tuple(tuple(row) for row in state)


# Lấy vị trí của phần tử trên cùng của lọ i
def Get_Top_Index(state, i):
    return len(state[i]) - 1


# Lấy màu của phần tử trên cùng của lọ i
def Get_Top_Value(state,i):
    if Is_Empty(state, i):
        return None
    return state[i][-1]


# Kiểm tra xem lọ i có rỗng không
def Is_Empty(state, i):
    return len(state[i])==0


# Kiểm tra xem lọ i có đầy không
def Is_Full(state,i):
    return len(state[i])==CAPACITY


# Đếm số lượng phần tử rỗng trong lọ i
def Empty_Slots(state,i):
    return CAPACITY-len(state[i])


# Đếm số phần tử cùng màu liên tiếp ở top của lọ i
def Get_Count_Same_Top(state,i):
    j=Get_Top_Index(state,i)
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
def Is_Goal(state):
    for i in state:
        if len(i) == 0:
            continue
        if len(i) != CAPACITY or len(set(i)) != 1:
            return False
    return True
def Heuristic(state):
    # h(n) trong bài này là điểm đánh giá trạng thái còn lộn xộn bao nhiêu
    # Lọ rỗng -> +0
    # Lọ đầy 4 ô và cùng màu -> +0
    # Lọ chưa đúng -> cộng điểm phạt
    # Điểm phạt gồm:
    # +1 vì lọ chưa hoàn thành
    # + số ô còn trống
    # + số lần hai màu cạnh nhau khác nhau
    # + số màu khác nhau trong lọ - 1
    score = 0
    for tube in state:
        if not tube:
            continue

        if len(tube) == CAPACITY and len(set(tube)) == 1:
            continue

        score += 1
        score += CAPACITY - len(tube)
        score += sum(1 for i in range(1, len(tube)) if tube[i] != tube[i - 1])
        score += len(set(tube)) - 1

    return score

def Child_Nodes(node):
    from Core.Action import Get_Actions

    return [node.Expand(action) for action in Get_Actions(node.state)]


def Best_Child(node):
    children = Child_Nodes(node)
    if not children:
        return None, []
    return min(children, key=lambda child: (Heuristic(child.state), child.cost)), children


def Has_Seen(node, seen):
    key = State_To_Tuple(node.state)
    if key in seen:
        return True
    seen.add(key)
    return False




