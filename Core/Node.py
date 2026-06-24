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
    def get_state(self):
        return self.state
    

    # Trả về chi phí
    def get_cost(self):
        return self.cost
    

    #Trả về node cha
    def get_parent(self):
        return self.parent
    

    # Trả về state từ gốc đến node hiện tại
    def get_states(self):
        path = []
        current = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        path.reverse()
        return path


    # Trả về độ sâu từ gốc đến node hiện tại
    def get_depth(self):
        depth = 0
        current = self
        while current.parent is not None:
            depth += 1
            current = current.parent
        return depth


    # Trả về chuỗi hành động từ gốc đến node hiện tại
    def get_path(self):
        actions = []
        current = self
        while current.parent is not None:
            actions.append(current.action)
            current = current.parent
        actions.reverse()
        return actions


    # Kiểm tra xem node hiện tại có phải là gốc không
    def is_root(self):
        return self.parent is None
    

    # Trả về node gốc
    def get_root(self):
        current = self
        while current.parent is not None:
            current = current.parent
        return current


    # Tạo bản sao của node
    def copy(self):
        return Node(
            state=[row[:] for row in self.state],
            parent=self.parent,
            action=self.action,
            cost=self.cost
        )


    # Update node cha
    def set_parent(self, parent):
        self.parent = parent


    # Update action
    def set_action(self, action):
        self.action = action


    # Update path cost
    def set_cost(self, cost):
        self.cost = cost

    
    # Tạo node con từ node hiện tại và action
    def expand(self, action, cost_function=None):
        next_state = apply_action(self.state, action)
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
                    cost=self.cost + step_cost(self.state, action)
                )
            case "h(x)": pass
            case "f(x)": pass
    # eg: child = node.expand(action)


    # Kiểm tra có lặp lại trạng thái cũ không
    def is_cycle(self):
        ancestor=self.parent
        while ancestor is not None:
            if self.state == ancestor.state:
                return True
            ancestor=ancestor.parent
        return False

