from Core.Action import *
from Core.Cost import *

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state   # List
        self.parent = parent # Node
        self.action = action # Tuple
        self.cost = cost     # int


    # So sánh = theo trạng thái
    def __eq__(self, other):
        return self.state == other.state


    # So sánh < theo cost
    def __lt__(self, other):
        return self.cost < other.cost


    # Trả về trạng thái hiện tại
    def Get_State(self):
        return self.state
    

    # Trả về chi phí
    def Get_Cost(self):
        return self.cost
    
    
    #Trả về node cha
    def Get_Parent(self):
        return self.parent
    

    # Trả về state từ gốc đến node hiện tại
    def Get_States(self):
        path = []
        current = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        path.reverse()
        return path


    # Trả về độ sâu từ gốc đến node hiện tại
    def Get_Depth(self):
        depth = 0
        current = self
        while current.parent is not None:
            depth += 1
            current = current.parent
        return depth


    # Trả về chuỗi hành động từ gốc đến node hiện tại
    def Get_Path(self):
        actions = []
        current = self
        while current.parent is not None:
            actions.append(current.action)
            current = current.parent
        actions.reverse()
        return actions


    # Kiểm tra xem node hiện tại có phải là gốc không
    def Is_Root(self):
        return self.parent is None
    

    # Trả về node gốc
    def Get_Root(self):
        current = self
        while current.parent is not None:
            current = current.parent
        return current


    # Tạo bản sao của node
    def Copy(self):
        return Node(
            state=[row[:] for row in self.state],
            parent=self.parent,
            action=self.action,
            cost=self.cost
        )


    # Update node cha
    def Set_Parent(self, parent):
        self.parent = parent


    # Update action
    def Set_Action(self, action):
        self.action = action


    # Update path cost
    def Set_Cost(self, cost):
        self.cost = cost

    
    # Tạo node con từ node hiện tại và action
    def Expand(self, action, cost_function=None):
        next_state = Apply_Action(self.state, action)
        match cost_function:
            case None: # Chi phí di chuyển mặc định là 1
                return Node(
                    state=next_state,
                    parent=self,
                    action=action,
                    cost=self.cost + 1
                )
            case "g(x)": # Chi phí di chuyển dùng hàm
                return Node(
                    state=next_state,
                    parent=self,
                    action=action,
                    cost=self.cost + Step_Cost(self.state, action)
                )
            case "h(x)": pass
            case "f(x)": pass
    # eg: child = node.Expand(action)


    # Kiểm tra có lặp lại trạng thái cũ không
    def Is_Cycle(self):
        ancestor=self.parent
        while ancestor is not None:
            if self.state == ancestor.state:
                return True
            ancestor=ancestor.parent
        return False

