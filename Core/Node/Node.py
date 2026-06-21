from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    state:list
    parent:Optional['Node']
    action:tuple
    cost:int

    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def show_state(self):
        for row in self.state:
            print(row)
        print()

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.cost < other.cost
    

