# Lưu trạng thái dữ liệu
import random
from Core.Utils import copy_state, START, CAPACITY


# Tạo trạng thái ban đầu ngẫu nhiên
def generate_random_start():
    nums = [1]*4 + [2]*4 + [3]*4
    random.shuffle(nums)
    return [nums[0:4], nums[4:8], nums[8:12], []]


class Model:
    def __init__(self):
        self.start_state = copy_state(START)      # Trạng thái ban đầu
        self.current_state = copy_state(START)     # Trạng thái hiện tại hiển thị
        self.result = None                         # Result sau khi chạy thuật toán
        self.current_step = 0                      # Bước hiện tại (index trong states)
        self.category = ""                         # Nhóm thuật toán đang chọn
        self.algorithm_name = ""                   # Tên thuật toán đang chọn
        self.algorithm_func = None                 # Hàm thuật toán
        self.mode = "normal"                       # "normal" | "partial" | "adversarial"
        self.is_random = False                     # Đang dùng START hay START_RANDOM
        self.animating = False                     # Đang chạy animation
        # Adversarial
        self.adversarial_turn = False              # True=máy đi trước, False=người đi trước
        self.adversarial_source = None             # Lọ nguồn người đã chọn (int hoặc None)
        self.game_status = "idle"                  # "idle" | "playing" | "human_win" | "machine_win" | "draw"
        self.game_controller = None                # GameController instance

    # Xóa toàn bộ trạng thái, path và kết quả
    def reset(self):
        self.current_state = copy_state(self.start_state)
        self.result = None
        self.current_step = 0
        self.animating = False
        self.adversarial_source = None
        self.game_status = "idle"
        self.game_controller = None

    # Đặt trạng thái mặc định (START từ Core/Utils)
    def set_default_start(self):
        self.is_random = False
        self.start_state = copy_state(START)
        self.reset()

    # Đặt trạng thái ngẫu nhiên (sinh mới mỗi lần)
    def set_random_start(self):
        self.is_random = True
        self.start_state = generate_random_start()
        self.reset()

    # Lấy tổng số bước trong path
    def get_total_steps(self):
        if self.result and self.result.states:
            return len(self.result.states) - 1
        return 0

    def get_current_display_state(self):
        if self.result and self.result.states:
            if self.current_step < len(self.result.states):
                return self.result.states[self.current_step]
                
        if self.mode == "partial":
            from algorithms.search_complex_environments.partially_observable_search import generate_belief_states
            known_colors = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
            return generate_belief_states(self.current_state, known_colors)
            
        return self.current_state

    # Lấy action tại bước hiện tại
    def get_current_action(self):
        if self.result and self.result.path:
            if 0 < self.current_step <= len(self.result.path):
                return self.result.path[self.current_step - 1]
        return None