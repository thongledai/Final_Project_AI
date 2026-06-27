from Core.Node import *
from Core.Utils import *
from Core.Action import *
from algorithms.adversarial_search.minimax_search import minimax_search
from algorithms.adversarial_search.alpha_beta_pruning_search import alpha_beta_pruning_search
from algorithms.adversarial_search.expectimax_search import expectimax_search

# turn: lượt đi: True: máy, False: người
# algorithm: minimax_search, alpha_beta_pruning_search, expectimax_search

class GameController:
    def __init__(self, start, first_player="machine", algo=None):
        self.node = Node(start)
        self.turn = first_player      # "machine" hoặc "human"
        self.algo = algo
        self.status = "playing"       # "playing" | "human_win" | "machine_win" | "draw"
        self.step = 0
        self.history = []

    @property
    def state(self):
        return self.node.state

    def is_valid_source(self, src):
        actions = get_actions(self.node.state)
        return any(a[0] == src for a in actions)

    def is_valid_move(self, src, dst):
        actions = get_actions(self.node.state)
        return (src, dst) in actions

    def apply_move(self, src, dst):
        if self.is_valid_move(src, dst):
            self.node = self.node.expand((src, dst))
            self.history.append((src, dst))
            self.step += 1
            self.turn = "machine" if self.turn == "human" else "human"
            self.check_winner()

    def check_winner(self):
        actions = get_actions(self.node.state)

        if is_goal(self.node.state):
            if self.turn == "machine":  
                self.status = "human_win"
            else:          
                self.status = "machine_win"
            return self.status

        if len(actions) == 0 or self.node.is_cycle():
            self.status = "draw"
            return self.status

        return "playing"

    def machine_move(self):
        if self.status != "playing" or self.turn != "machine":
            return None

        import time
        from Core.Result import solution
        start_time = time.time()

        actions = get_actions(self.node.state)
        if not actions:
            self.status = "draw"
            return None

        max_eval = -2
        best_action = actions[0]
        
        total_explored = 0
        total_generated = 1

        for action in actions:
            child = self.node.expand(action)
            res = self.algo(child, False)
            
            if isinstance(res, tuple):
                eval_score, alg_result = res
                if hasattr(alg_result, 'explored'):
                    total_explored += alg_result.explored
                if hasattr(alg_result, 'generated'):
                    total_generated += alg_result.generated
            else:
                eval_score = res
                
            if eval_score > max_eval:
                max_eval = eval_score
                best_action = action

        self.last_result = solution(None, total_explored, total_generated, start_time)
        self.apply_move(best_action[0], best_action[1])
        return best_action
