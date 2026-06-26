# Xử lý sự kiện, nút bấm
# Điều phối View ↔ Model
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

from Core.Utils import copy_state

# ── Algorithm imports ──
from algorithms.uninformed_search.breadth_first_search import breadth_first_search
from algorithms.uninformed_search.depth_first_search import depth_first_search
from algorithms.uninformed_search.iterative_deepening_search import iterative_deepening_search
from algorithms.uninformed_search.uniform_cost_search import uniform_cost_search

from algorithms.informed_search.a_star_search import a_star_search
from algorithms.informed_search.greedy_search import greedy_search
from algorithms.informed_search.ida_star_search import ida_star_search

from algorithms.local_search.hill_climbing_search.simple import simple_hill_climbing
from algorithms.local_search.hill_climbing_search.stochastic import stochastic_hill_climbing_search
from algorithms.local_search.hill_climbing_search.steepest_ascent import steepest_ascent_hill_climbing_search
from algorithms.local_search.hill_climbing_search.random_restart import random_restart_hill_climbing_search
from algorithms.local_search.local_beam_search import local_beam_search
from algorithms.local_search.simulated_annealing_search import simulated_annealing_search

from algorithms.search_complex_environments.and_or_graph_search import and_or_graph_search
from algorithms.search_complex_environments.partially_observable_search import partial_search

from algorithms.constraint_satisfaction_search.backtracking_search import backtracking_search
from algorithms.constraint_satisfaction_search.forward_checking_search import forward_checking_search

from algorithms.adversarial_search.minimax_search import minimax_search
from algorithms.adversarial_search.alpha_beta_pruning_search import alpha_beta_pruning_search
from algorithms.adversarial_search.expectimax_search import expectimax_search
from algorithms.adversarial_search.game import GameController as AdvGameController

from GUI.Model import Model
from GUI.View import View

# ── Registry ──
ALGORITHM_REGISTRY = {
    "uninformed_search": {
        "Breadth First Search": breadth_first_search,
        "Depth First Search": depth_first_search,
        "Iterative Deepening Search": iterative_deepening_search,
        "Uniform Cost Search": uniform_cost_search,
    },
    "informed_search": {
        "A* Search": a_star_search,
        "Greedy Search": greedy_search,
        "IDA* Search": ida_star_search,
    },
    "local_search": {
        "Simple Hill Climbing": simple_hill_climbing,
        "Stochastic Hill Climbing": stochastic_hill_climbing_search,
        "Steepest Ascent Hill Climbing": steepest_ascent_hill_climbing_search,
        "Random Restart Hill Climbing": random_restart_hill_climbing_search,
        "Local Beam Search": local_beam_search,
        "Simulated Annealing": simulated_annealing_search,
    },
    "search_complex_environments": {
        "And-Or Graph Search": and_or_graph_search,
        "Partially Observable Search": partial_search,
    },
    "constraint_satisfaction_search": {
        "Backtracking Search": backtracking_search,
        "Forward Checking Search": forward_checking_search,
    },
    "adversarial_search": {
        "Minimax Search": minimax_search,
        "Alpha-Beta Pruning": alpha_beta_pruning_search,
        "Expectimax Search": expectimax_search,
    },
}

CATEGORY_DISPLAY = {
    "uninformed_search": "1. Uninformed Search",
    "informed_search": "2. Informed Search",
    "local_search": "3. Local Search",
    "search_complex_environments": "4. Complex Environments",
    "constraint_satisfaction_search": "5. Constraint Satisfaction",
    "adversarial_search": "6. Adversarial Search",
}

# Reverse lookup
DISPLAY_TO_CATEGORY = {v: k for k, v in CATEGORY_DISPLAY.items()}


class Worker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, func, state):
        super().__init__()
        self.func = func
        self.state = state

    def run(self):
        try:
            result = self.func(self.state)
            self.finished.emit(result)
        except Exception as e:
            print(f"Error in background thread: {e}")
            self.finished.emit(None)


class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.model = Model()
        self.view = View(self)

        self.worker = None

        self._setup_combos()
        self._bind_events()

        self.view.show()
        
        # Vẽ trạng thái ban đầu sau khi show
        QTimer.singleShot(100, self._initial_draw)

        sys.exit(self.app.exec())

    # ══════════════════════════════════════
    # SETUP
    # ══════════════════════════════════════

    def _setup_combos(self):
        categories = list(CATEGORY_DISPLAY.values())
        self.view.combo_category.addItems(categories)
        self.view.combo_category.currentTextChanged.connect(self._on_category_changed)
        self.view.combo_algo.currentTextChanged.connect(self._on_algorithm_changed)
        
        # Gọi thủ công lần đầu để cập nhật combo_algo vì addItems đã đặt index=0
        if self.view.combo_category.count() > 0:
            self._on_category_changed(self.view.combo_category.currentText())
        
    def _bind_events(self):
        self.view.btn_start.clicked.connect(self._on_default)
        self.view.btn_random.clicked.connect(self._on_random)
        self.view.btn_execute.clicked.connect(self._on_execute)
        self.view.btn_next.clicked.connect(self._on_next)
        self.view.btn_last.clicked.connect(self._on_last)
        self.view.btn_remove.clicked.connect(self._on_remove)
        
        # Tương tác click lọ
        self.view.puzzle_view.click_callback = self._on_canvas_click
        
        # Tương tác đổi lượt chơi adversarial
        self.view.combo_turn.currentIndexChanged.connect(self._on_turn_changed)

    def _initial_draw(self):
        self.view.draw_state(self.model.start_state)

    # ══════════════════════════════════════
    # COMBOBOX EVENTS
    # ══════════════════════════════════════

    def _on_category_changed(self, display_name):
        category = DISPLAY_TO_CATEGORY.get(display_name, "")
        self.model.category = category

        # Cập nhật danh sách thuật toán
        algos = ALGORITHM_REGISTRY.get(category, {})
        algo_names = list(algos.keys())
        
        self.view.combo_algo.blockSignals(True)
        self.view.combo_algo.clear()
        self.view.combo_algo.addItems(algo_names)
        self.view.combo_algo.blockSignals(False)
        
        if category == "adversarial_search":
            self.view.show_adversarial_ui()
        else:
            self.view.hide_adversarial_ui()
            
        if algo_names:
            self.view.combo_algo.setCurrentIndex(0)
            self._on_algorithm_changed(algo_names[0])

    def _on_algorithm_changed(self, algo_name):
        if not algo_name:
            return
            
        category = self.model.category
        algos = ALGORITHM_REGISTRY.get(category, {})
        self.model.algorithm_name = algo_name
        self.model.algorithm_func = algos.get(algo_name)

        old_mode = self.model.mode

        if algo_name == "Partially Observable Search":
            self.model.mode = "partial"
            self._setup_partial_state()
        elif category == "adversarial_search":
            self.model.mode = "adversarial"
        else:
            self.model.mode = "normal"
            
        # Nếu vừa chuyển từ partial sang mode khác, phải khôi phục trạng thái ban đầu
        if old_mode == "partial" and self.model.mode != "partial":
            if self.model.is_random:
                self.model.set_random_start()
            else:
                self.model.set_default_start()
            
        self._on_remove()

    # ══════════════════════════════════════
    # BUTTON EVENTS
    # ══════════════════════════════════════

    def _on_default(self):
        self.model.set_default_start()
        if self.model.mode == "partial":
            self._setup_partial_state()
        self.view.clear_result_fields()
        self.view.show_step_info(0, 0)
        self._draw_current()

        if self.model.mode == "adversarial":
            self._start_adversarial_game()

    def _on_random(self):
        self.model.set_random_start()
        if self.model.mode == "partial":
            self._setup_partial_state()
        self.view.clear_result_fields()
        self.view.show_step_info(0, 0)
        self._draw_current()

        if self.model.mode == "adversarial":
            self._start_adversarial_game()

    def _setup_partial_state(self):
        """Tạo trạng thái partial (-1) từ start_state hiện tại."""
        # Cố gắng ẩn 2 ô có màu khác nhau để luôn tạo ra 2 trạng thái niềm tin
        hidden = 0
        first_color = None
        for i in range(len(self.model.start_state)):
            for j in range(len(self.model.start_state[i])):
                color = self.model.start_state[i][j]
                if color != -1 and (first_color is None or color != first_color):
                    if first_color is None:
                        first_color = color
                    self.model.start_state[i][j] = -1
                    hidden += 1
                    if hidden == 2:
                        break
            if hidden == 2:
                break
                
        self.model.current_state = copy_state(self.model.start_state)

    def _on_execute(self):
        if self.model.algorithm_func is None:
            self.view.lbl_success.setText("Success: Chưa chọn thuật toán")
            return
        if self.model.mode == "adversarial":
            return

        self.view.btn_execute.setEnabled(False)
        self.view.btn_execute.setText("Đang chạy...")
        
        self.worker = Worker(self.model.algorithm_func, self.model.start_state)
        self.worker.finished.connect(self._on_algo_done)
        self.worker.start()

    def _on_algo_done(self, result):
        self.view.btn_execute.setEnabled(True)
        self.view.btn_execute.setText("Execute")
        
        if result:
            self.model.result = result
            self.model.current_step = 0
            self.view.set_result_fields(result)
            self._draw_current()
            self.view.show_step_info(0, self.model.get_total_steps())
        else:
            self.view.lbl_success.setText("Success: Lỗi khi chạy thuật toán")

    def _on_next(self):
        if self.model.result is None or self.view.puzzle_view.is_animating:
            return

        total = self.model.get_total_steps()
        if self.model.current_step >= total:
            return

        state_before = self.model.get_current_display_state()
        self.model.current_step += 1
        state_after = self.model.get_current_display_state()
        action = self.model.get_current_action()

        self.view.show_step_info(self.model.current_step, total, action)

        def after_anim():
            self._draw_current()

        if action is None:
            self._draw_current()
        else:
            self.view.animate_pour(state_before, state_after, action, after_anim)

    def _on_last(self):
        if self.model.result is None or self.view.puzzle_view.is_animating:
            return

        if self.model.current_step <= 0:
            return

        self.model.current_step -= 1
        total = self.model.get_total_steps()
        action = self.model.get_current_action()
        self.view.show_step_info(self.model.current_step, total, action)
        self._draw_current()

    def _on_remove(self):
        self.model.result = None
        self.model.current_step = 0
        self.view.clear_result_fields()
        self.view.show_step_info(0, 0)
        self._draw_current()

    # ══════════════════════════════════════
    # ADVERSARIAL MODE
    # ══════════════════════════════════════

    def _on_turn_changed(self, index):
        if self.model.mode == "adversarial":
            self._start_adversarial_game()

    def _start_adversarial_game(self):
        turn_str = self.view.combo_turn.currentText()
        first_player = "human" if "Người" in turn_str else "machine"

        algo_func = self.model.algorithm_func
        if not algo_func:
            algo_func = expectimax_search 

        self.game_controller = AdvGameController(
            copy_state(self.model.start_state), 
            first_player=first_player,
            algo=algo_func
        )
        self.model.source_tube = None
        
        if first_player == "machine":
            self.view.update_adv_bottom("Agent")
            self._machine_turn()
        else:
            self.view.update_adv_bottom("Human")
            self._draw_current()

    def _on_canvas_click(self, tube_idx):
        if self.model.mode != "adversarial" or not hasattr(self, 'game_controller'):
            return

        gc = self.game_controller
        if gc.status != "playing" or gc.turn != "human":
            return

        if self.model.source_tube is None:
            # Chọn lọ nguồn
            if not gc.is_valid_source(tube_idx):
                return
            self.model.source_tube = tube_idx
            self._draw_current(highlight_tube=tube_idx)
        else:
            # Chọn lọ đích
            src = self.model.source_tube
            dst = tube_idx
            
            if src == dst:
                self.model.source_tube = None
                self._draw_current()
                return

            if gc.is_valid_move(src, dst):
                self.view.update_adv_bottom("Agent")
                state_before = copy_state(gc.state)
                gc.apply_move(src, dst)
                state_after = copy_state(gc.state)
                
                self.model.source_tube = None

                def on_done():
                    self._draw_current()
                    self._check_game_over()
                    if gc.status == "playing" and gc.turn == "machine":
                        self._machine_turn()

                self.view.animate_pour(state_before, state_after, (src, dst), on_done)
            else:
                self.model.source_tube = None
                self._draw_current()

    def _machine_turn(self):
        gc = self.game_controller
        QApplication.processEvents() # Cập nhật UI

        # Chạy máy ngầm hoặc đồng bộ tuỳ ý, ở đây chạy đồng bộ (hoặc QTimer delay nhẹ)
        QTimer.singleShot(500, self._do_machine_move)

    def _do_machine_move(self):
        gc = self.game_controller
        if gc.status != "playing" or gc.turn != "human": # máy
            state_before = copy_state(gc.state)
            
            # Gán lại thuật toán mới nhất
            if self.model.algorithm_func:
                gc.algo = self.model.algorithm_func

            gc.machine_move()
            
            state_after = copy_state(gc.state)
            action = None
            if gc.history:
                action = gc.history[-1]

            if action:
                self.view.update_adv_bottom("Human")
                
                def on_done():
                    self._draw_current()
                    self._check_game_over()
                    
                self.view.animate_pour(state_before, state_after, action, on_done)
            else:
                self._draw_current()
                self._check_game_over()

    def _check_game_over(self):
        gc = self.game_controller
        gc.check_winner()
        if gc.status != "playing":
            self._show_game_over()

    def _show_game_over(self):
        gc = self.game_controller
        status_map = {
            "human_win": "Human Win",
            "machine_win": "Agent Win",
            "draw": "Draw",
        }
        text = status_map.get(gc.status, "Game Over")
        self.view.update_adv_bottom("None", text)

    # ══════════════════════════════════════
    # UTILS
    # ══════════════════════════════════════

    def _draw_current(self, highlight_tube=None):
        if self.model.mode == "partial":
            state = self.model.get_current_display_state()
            self.view.draw_partial_states(state)
        elif self.model.mode == "adversarial":
            if hasattr(self, 'game_controller') and self.game_controller:
                self.view.draw_state(self.game_controller.state, highlight_tube)
            else:
                self.view.draw_state(self.model.start_state, highlight_tube)
        else:
            state = self.model.get_current_display_state()
            self.view.draw_state(state, highlight_tube)
