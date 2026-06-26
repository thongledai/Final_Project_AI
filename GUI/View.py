import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QComboBox, QPushButton, QFrame, QScrollArea, QGridLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from Core.Utils import CAPACITY

# ── MÔ PHỎNG MÀU SẮC ──
COLOR_MAP = {
    1: QColor("#FF2A2A"),   # Đỏ
    2: QColor("#FFCC00"),   # Vàng
    3: QColor("#00CCFF"),   # Xanh dương
}

BG_COLOR = "#f4f4f4"
PANEL_BG = "#ffffff"
TUBE_OUTLINE = QColor("#aaaaaa")

# Kích thước lọ
TUBE_WIDTH = 60
CELL_HEIGHT = 55
TUBE_HEIGHT = 220
TUBE_GAP = 30
TUBE_CORNER = 15

# Tốc độ Animation
ANIM_DURATION = 300 # ms
ANIM_FPS = 60


class PuzzleView(QWidget):
    # Custom QWidget dùng QPainter để vẽ các lọ nước 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state_data = [] # Lưu state (list of tubes) hoặc multi-state
        self.is_multi_state = False
        
        self.tube_w = TUBE_WIDTH
        self.cell_h = CELL_HEIGHT
        self.tube_h = TUBE_HEIGHT
        self.tube_gap = TUBE_GAP
        self.tube_corner = TUBE_CORNER
        
        # Animation data
        self.is_animating = False
        self.anim_progress = 0.0
        self.anim_action = None
        self.anim_state_before = None
        self.anim_state_after = None
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._anim_step)
        
        self.on_anim_done_callback = None
        
        # Lưu các rect của lọ để hỗ trợ click (cho adversarial)
        self.tube_rects = []
        self.highlight_tube = None
        self.click_callback = None
        
        self.setMinimumSize(800, 400)
        
    def update_dimensions(self):
        if self.is_multi_state:
            self.tube_w = 40
            self.cell_h = 35
            self.tube_h = 140
            self.tube_gap = 20
            self.tube_corner = 10
        else:
            self.tube_w = TUBE_WIDTH
            self.cell_h = CELL_HEIGHT
            self.tube_h = TUBE_HEIGHT
            self.tube_gap = TUBE_GAP
            self.tube_corner = TUBE_CORNER

    def set_state(self, state_data, highlight=None):
        self.state_data = state_data
        self.highlight_tube = highlight
        self.is_multi_state = False
        
        if state_data and isinstance(state_data, list) and len(state_data) > 0:
            if isinstance(state_data[0], list) and len(state_data[0]) > 0 and isinstance(state_data[0][0], list):
                self.is_multi_state = True
        self.state_data = state_data
        self.update_dimensions()
        self._update_min_size()
        self.update() # Gọi paintEvent

    def _update_min_size(self):
        if not self.state_data:
            return
            
        # Tính kích thước tối thiểu cần thiết để QScrollArea hoạt động
        if self.is_multi_state:
            num_states = len(self.state_data)
            max_tubes = max(len(s) for s in self.state_data) if num_states > 0 else 0
            w = max_tubes * self.tube_w + (max_tubes + 1) * self.tube_gap
            h = num_states * (self.tube_h + 100)
        else:
            num_tubes = len(self.state_data)
            w = num_tubes * self.tube_w + (num_tubes + 1) * self.tube_gap
            h = self.tube_h + 100
            
        self.setMinimumSize(max(800, w), max(400, h))

    def start_animation(self, state_before, state_after, action, on_done):
        if action is None:
            on_done()
            return
            
        self.anim_state_before = state_before
        self.anim_state_after = state_after
        self.anim_action = action
        self.on_anim_done_callback = on_done
        
        self.is_animating = True
        self.is_multi_state = False
        
        if state_before and isinstance(state_before, list) and len(state_before) > 0:
            if isinstance(state_before[0], list) and len(state_before[0]) > 0 and isinstance(state_before[0][0], list):
                self.is_multi_state = True
                
        self.update_dimensions()
        
        self.anim_progress = 0.0
        
        self._update_min_size()
        
        self.anim_timer.start(1000 // ANIM_FPS)

    def _anim_step(self):
        self.anim_progress += (1000 / ANIM_FPS) / ANIM_DURATION
        if self.anim_progress >= 1.0:
            self.anim_timer.stop()
            self.is_animating = False
            self.state_data = self.anim_state_after
            self.update()
            if self.on_anim_done_callback:
                self.on_anim_done_callback()
        else:
            self.update()

    def mousePressEvent(self, event):
        if self.click_callback:
            # Tìm lọ nào được click
            for (rect, idx) in self.tube_rects:
                if rect.contains(event.pos()):
                    self.click_callback(idx)
                    return

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.tube_rects.clear()
        
        if self.is_animating:
            self._draw_animation(painter)
            return

        if not self.state_data:
            return

        cw = self.width()
        
        if self.is_multi_state:
            num_states = len(self.state_data)
            section_h = max(TUBE_HEIGHT + 100, self.height() // num_states if num_states > 0 else 0)
            
            for idx, state in enumerate(self.state_data):
                y_start = idx * section_h
                y_end = y_start + section_h
                
                # Draw label
                painter.setPen(QColor("#333333"))
                painter.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
                text_rect = painter.boundingRect(0, y_start + 10, cw, 30, Qt.AlignmentFlag.AlignHCenter, f"Belief State {idx + 1}")
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignHCenter, f"Belief State {idx + 1}")
                
                self._draw_tubes(painter, state, cw, y_start + 40, y_end, highlight_tube=None)
                
                # Line separator
                if idx < num_states - 1:
                    pen = QPen(QColor("#cccccc"), 2, Qt.PenStyle.DashLine)
                    painter.setPen(pen)
                    painter.drawLine(50, y_end, cw - 50, y_end)
        else:
            self._draw_tubes(painter, self.state_data, cw, 0, self.height(), self.highlight_tube)

    def _draw_tubes(self, painter, state, cw, y_start, y_end, highlight_tube=None):
        num_tubes = len(state)
        total_w = num_tubes * self.tube_w + (num_tubes - 1) * self.tube_gap
        start_x = (cw - total_w) // 2
        
        tube_y = y_start + (y_end - y_start - self.tube_h) // 2
        
        for i, tube in enumerate(state):
            x = start_x + i * (self.tube_w + self.tube_gap)
            self._draw_single_tube(painter, x, tube_y, tube, i == highlight_tube)
            
            # Label
            painter.setPen(QColor("#333333"))
            painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            painter.drawText(int(x), int(tube_y + self.tube_h + 10), int(self.tube_w), 30, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, f"Lọ {i}")
            
            from PyQt6.QtCore import QRect
            self.tube_rects.append((QRect(int(x), int(tube_y), int(self.tube_w), int(self.tube_h)), i))

    def _draw_single_tube(self, painter, x, y, tube, is_highlight):
        r = self.tube_corner
        w = self.tube_w
        h = self.tube_h
        
        # Vẽ nền trắng của lọ
        path = QPainterPath()
        path.moveTo(x, y)
        path.lineTo(x, y + h - r)
        path.arcTo(x, y + h - 2*r, 2*r, 2*r, 180, 90)
        path.arcTo(x + w - 2*r, y + h - 2*r, 2*r, 2*r, 270, 90)
        path.lineTo(x + w, y)
        path.closeSubpath()
        
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        # Vẽ nước
        for slot in range(CAPACITY):
            if slot >= len(tube):
                continue
                
            color = COLOR_MAP.get(tube[slot], QColor("#ffffff"))
            cell_bot = y + h - slot * self.cell_h
            cell_top = cell_bot - self.cell_h
            
            painter.setBrush(QBrush(color))
            
            if slot == 0:
                water_path = QPainterPath()
                water_path.moveTo(x + 2, cell_top)
                water_path.lineTo(x + 2, cell_bot - r)
                water_path.arcTo(x + 2, cell_bot - 2*r + 2, 2*r - 4, 2*r - 4, 180, 90)
                water_path.arcTo(x + w - 2*r + 2, cell_bot - 2*r + 2, 2*r - 4, 2*r - 4, 270, 90)
                water_path.lineTo(x + w - 2, cell_top)
                water_path.closeSubpath()
                painter.drawPath(water_path)
            else:
                painter.drawRect(int(x + 2), int(cell_top), int(w - 4), int(self.cell_h))
                
            # Line phân cách mờ hoặc hiệu ứng 3D
            painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
            painter.drawLine(int(x + 2), int(cell_top), int(x + w - 2), int(cell_top))
            painter.setPen(Qt.PenStyle.NoPen)

        # Vẽ viền
        outline_color = QColor("#FF6B00") if is_highlight else TUBE_OUTLINE
        pen = QPen(outline_color, 3)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
        
        # Đường thẳng đóng miệng lọ
        painter.drawLine(int(x), int(y), int(x + w), int(y))

    def _draw_animation(self, painter):
        if self.is_multi_state:
            num_states = len(self.anim_state_before)
            section_h = self.height() // num_states if num_states > 0 else 0
            cw = self.width()
            for idx in range(num_states):
                y_start = idx * section_h
                y_end = y_start + section_h
                
                # Draw label exactly like in paintEvent
                painter.setPen(QColor("#333333"))
                painter.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
                text_rect = painter.boundingRect(0, y_start + 10, cw, 30, Qt.AlignmentFlag.AlignHCenter, f"Belief State {idx + 1}")
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignHCenter, f"Belief State {idx + 1}")

                state_before_idx = self.anim_state_before[idx]
                state_after_idx = self.anim_state_after[idx]
                self._draw_animation_single_state(painter, state_before_idx, state_after_idx, y_start + 40, y_end)
                
                if idx < num_states - 1:
                    pen = QPen(QColor("#cccccc"), 2, Qt.PenStyle.DashLine)
                    painter.setPen(pen)
                    painter.drawLine(50, y_end, cw - 50, y_end)
        else:
            self._draw_animation_single_state(painter, self.anim_state_before, self.anim_state_after, 0, self.height())

    def _draw_animation_single_state(self, painter, state_before, state_after, y_start, y_end):
        cw = self.width()
        src, dst = self.anim_action
        
        num_tubes = len(state_before)
        total_w = num_tubes * self.tube_w + (num_tubes - 1) * self.tube_gap
        start_x = (cw - total_w) // 2
        tube_y = y_start + (y_end - y_start - self.tube_h) // 2
        
        for i in range(num_tubes):
            if i != src and i != dst:
                self._draw_single_tube(painter, start_x + i * (self.tube_w + self.tube_gap), tube_y, state_before[i], False)
                
        src_tube = list(state_before[src])
        dst_tube = list(state_before[dst])
        
        color_val = src_tube[-1] if src_tube else 1
        p = self.anim_progress
        
        src_x = start_x + src * (self.tube_w + self.tube_gap)
        self._draw_single_tube_anim(painter, src_x, tube_y, src_tube, -p)
        
        dst_x = start_x + dst * (self.tube_w + self.tube_gap)
        dst_tube_draw = list(dst_tube) + [color_val]
        self._draw_single_tube_anim(painter, dst_x, tube_y, dst_tube_draw, -(1-p))

    def _draw_single_tube_anim(self, painter, x, y, tube, offset_slots):
        r = self.tube_corner
        w = self.tube_w
        h = self.tube_h
        
        path = QPainterPath()
        path.moveTo(x, y)
        path.lineTo(x, y + h - r)
        path.arcTo(x, y + h - 2*r, 2*r, 2*r, 180, 90)
        path.arcTo(x + w - 2*r, y + h - 2*r, 2*r, 2*r, 270, 90)
        path.lineTo(x + w, y)
        path.closeSubpath()
        
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        for slot in range(CAPACITY):
            if slot >= len(tube):
                continue
                
            color = COLOR_MAP.get(tube[slot], QColor("#ffffff"))
            cell_bot = y + h - slot * self.cell_h
            cell_top = cell_bot - self.cell_h
            
            # Offset ô trên cùng
            if slot == len(tube) - 1:
                cell_top -= offset_slots * self.cell_h
                if cell_top >= cell_bot:
                    continue # Nước bị rút hết
            
            painter.setBrush(QBrush(color))
            
            if slot == 0:
                water_path = QPainterPath()
                water_path.moveTo(x + 2, cell_top)
                water_path.lineTo(x + 2, cell_bot - r)
                water_path.arcTo(x + 2, cell_bot - 2*r + 2, 2*r - 4, 2*r - 4, 180, 90)
                water_path.arcTo(x + w - 2*r + 2, cell_bot - 2*r + 2, 2*r - 4, 2*r - 4, 270, 90)
                water_path.lineTo(x + w - 2, cell_top)
                water_path.closeSubpath()
                painter.drawPath(water_path)
            else:
                painter.drawRect(int(x + 2), int(cell_top), int(w - 4), int(cell_bot - cell_top))
                
        pen = QPen(TUBE_OUTLINE, 3)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
        painter.drawLine(int(x), int(y), int(x + w), int(y))


class View(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.setWindowTitle("Water Puzzle Sort")
        self.resize(1400, 850)
        self.showMaximized()
        
        # Main widget
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f"background-color: {BG_COLOR};")
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)
        
        self._init_top_bar()
        self._init_middle_area()
        self._init_bottom_bar()
        
    def _init_top_bar(self):
        # Vùng 1
        self.top_frame = QFrame()
        self.top_frame.setFixedHeight(70)
        self.top_frame.setStyleSheet("""
            QFrame { background-color: transparent; }
            QLabel { font-size: 14px; font-weight: bold; color: #333; }
            QComboBox { 
                font-size: 14px; padding: 5px; width: 250px; 
                background: white; border: 1px solid #ccc; border-radius: 5px;
            }
            QComboBox::drop-down { border: none; }
        """)
        top_layout = QHBoxLayout(self.top_frame)
        top_layout.setContentsMargins(10, 0, 10, 0)
        
        top_layout.addWidget(QLabel("Chọn loại thuật toán:"))
        self.combo_category = QComboBox()
        top_layout.addWidget(self.combo_category)
        
        top_layout.addSpacing(30)
        
        top_layout.addWidget(QLabel("Chọn thuật toán:"))
        self.combo_algo = QComboBox()
        top_layout.addWidget(self.combo_algo)
        
        top_layout.addSpacing(30)
        
        self.lbl_turn = QLabel("Lượt đầu:")
        self.combo_turn = QComboBox()
        self.combo_turn.addItems(["Người đi trước", "Máy đi trước"])
        self.combo_turn.setFixedWidth(150)
        
        top_layout.addWidget(self.lbl_turn)
        top_layout.addWidget(self.combo_turn)
        
        top_layout.addStretch()
        
        self.main_layout.addWidget(self.top_frame)

    def _init_middle_area(self):
        # Vùng 2 & 3
        mid_layout = QHBoxLayout()
        
        # Vùng 2 - Puzzle
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: white; border-radius: 10px; border: 1px solid #ddd;
            }
            QWidget#scroll_content { background-color: white; }
        """)
        
        # Thêm hiệu ứng shadow bằng Qt (nếu cần thiết có thể dùng QGraphicsDropShadowEffect)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 5)
        self.scroll_area.setGraphicsEffect(shadow)
        
        self.puzzle_view = PuzzleView()
        self.puzzle_view.setObjectName("scroll_content")
        self.scroll_area.setWidget(self.puzzle_view)
        
        mid_layout.addWidget(self.scroll_area, stretch=7) # Chiếm 70%
        
        # Vùng 3 - Bảng điều khiển
        self.panel_frame = QFrame()
        self.panel_frame.setStyleSheet(f"background-color: {PANEL_BG}; border-radius: 10px; border: 1px solid #ddd;")
        self.panel_frame.setFixedWidth(300)
        
        panel_shadow = QGraphicsDropShadowEffect()
        panel_shadow.setBlurRadius(15)
        panel_shadow.setColor(QColor(0, 0, 0, 30))
        panel_shadow.setOffset(0, 5)
        self.panel_frame.setGraphicsEffect(panel_shadow)
        
        panel_layout = QVBoxLayout(self.panel_frame)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(15)
        
        lbl_title = QLabel("BẢNG ĐIỀU KHIỂN")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; border: none; color: #333;")
        panel_layout.addWidget(lbl_title)
        
        btn_style = """
            QPushButton {
                background-color: #dfe4ea;
                color: #2f3542;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
                height: 55px;
            }
            QPushButton:hover {
                background-color: #c8d6e5;
            }
            QPushButton:pressed {
                background-color: #a4b0be;
            }
            QPushButton:disabled {
                background-color: #f1f2f6;
                color: #ced6e0;
            }
        """
        
        self.btn_start = QPushButton("Initial")
        self.btn_start.setStyleSheet(btn_style)
        
        self.btn_random = QPushButton("Random")
        self.btn_random.setStyleSheet(btn_style)
        
        self.btn_execute = QPushButton("Execute")
        self.btn_execute.setStyleSheet(btn_style)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.setStyleSheet(btn_style)
        
        self.btn_last = QPushButton("Last")
        self.btn_last.setStyleSheet(btn_style)
        
        self.btn_remove = QPushButton("Remove")
        self.btn_remove.setStyleSheet(btn_style)
        
        panel_layout.addWidget(self.btn_start)
        panel_layout.addWidget(self.btn_random)
        panel_layout.addWidget(self.btn_execute)
        panel_layout.addWidget(self.btn_next)
        panel_layout.addWidget(self.btn_last)
        panel_layout.addWidget(self.btn_remove)
        panel_layout.addStretch()
        
        mid_layout.addWidget(self.panel_frame, stretch=3)
        self.main_layout.addLayout(mid_layout)

    def _init_bottom_bar(self):
        # Vùng 4 - Kết quả
        self.bottom_frame = QFrame()
        self.bottom_frame.setStyleSheet(f"background-color: {PANEL_BG}; border-radius: 10px; border: 1px solid #ddd;")
        
        bottom_shadow = QGraphicsDropShadowEffect()
        bottom_shadow.setBlurRadius(15)
        bottom_shadow.setColor(QColor(0, 0, 0, 30))
        bottom_shadow.setOffset(0, 5)
        self.bottom_frame.setGraphicsEffect(bottom_shadow)
        
        bottom_layout = QGridLayout(self.bottom_frame)
        bottom_layout.setContentsMargins(20, 15, 20, 15)
        
        lbl_style = "font-size: 14px; color: #333;"
        val_style = "font-size: 14px; color: #2f3542;"
        
        self.lbl_path = QLabel("<b>Path:</b> ")
        self.lbl_path.setStyleSheet(lbl_style)
        self.lbl_path.setWordWrap(True)
        
        bottom_layout.addWidget(self.lbl_path, 0, 0, 1, 6) # Row 0, span 6 cols
        
        self.lbl_success = QLabel("Success:")
        self.lbl_cost = QLabel("Cost:")
        self.lbl_explored = QLabel("Explored:")
        self.lbl_generated = QLabel("Generated:")
        self.lbl_depth = QLabel("Depth:")
        self.lbl_runtime = QLabel("Runtime:")
        
        for lbl in [self.lbl_success, self.lbl_cost, self.lbl_explored, self.lbl_generated, self.lbl_depth, self.lbl_runtime]:
            lbl.setStyleSheet(val_style)
            
        bottom_layout.addWidget(self.lbl_success, 1, 0)
        bottom_layout.addWidget(self.lbl_cost, 1, 1)
        bottom_layout.addWidget(self.lbl_explored, 1, 2)
        bottom_layout.addWidget(self.lbl_generated, 1, 3)
        bottom_layout.addWidget(self.lbl_depth, 1, 4)
        bottom_layout.addWidget(self.lbl_runtime, 1, 5)
        
        self.main_layout.addWidget(self.bottom_frame)

    # ── CÁC HÀM API GIỮ NGUYÊN CHO CONTROLLER ──
    
    def clear_result_fields(self):
        self.lbl_path.setText("<b>Path:</b> ")
        self.lbl_success.setText("<b>Success:</b>")
        self.lbl_cost.setText("<b>Cost:</b>")
        self.lbl_explored.setText("<b>Explored:</b>")
        self.lbl_generated.setText("<b>Generated:</b>")
        self.lbl_depth.setText("<b>Depth:</b>")
        self.lbl_runtime.setText("<b>Runtime:</b>")

    def set_result_fields(self, result):
        if result is None:
            self.clear_result_fields()
            return
            
        self.lbl_success.setText(f"<b>Success:</b> {result.success}")
        self.lbl_cost.setText(f"<b>Cost:</b> {result.cost}")
        self.lbl_explored.setText(f"<b>Explored:</b> {result.explored}")
        self.lbl_generated.setText(f"<b>Generated:</b> {result.generated}")
        self.lbl_depth.setText(f"<b>Depth:</b> {result.depth}")
        self.lbl_runtime.setText(f"<b>Runtime:</b> {result.runtime:.6f}s")
        path_str = " ".join(str(p) for p in result.path) if result.path else "None"
        self.lbl_path.setText(f"<b>Path:</b> {path_str}")

    def show_step_info(self, step, total, action=None):
        pass # Có thể thiết kế thêm nhãn ở panel nếu cần

    def draw_state(self, state, highlight_tube=None):
        self.puzzle_view.set_state(state, highlight_tube)
        
    def draw_partial_states(self, state_list):
        self.puzzle_view.set_state(state_list)
        
    def animate_pour(self, state_before, state_after, action, on_done):
        self.puzzle_view.start_animation(state_before, state_after, action, on_done)
        
    def show_adversarial_ui(self):
        self.lbl_turn.show()
        self.combo_turn.show()
        
        self.bottom_frame.show()
        
        # Ẩn button Execute, Next, Last, Remove
        self.btn_execute.hide()
        self.btn_next.hide()
        self.btn_last.hide()
        self.btn_remove.hide()

        self.lbl_path.hide()
        self.lbl_explored.hide()
        self.lbl_generated.hide()
        self.lbl_depth.hide()
        self.lbl_runtime.hide()
        
        self.lbl_success.setText("<b>Turn:</b> Human")
        self.lbl_cost.setText("<b>Result:</b> ")
        
    def hide_adversarial_ui(self):
        self.lbl_turn.hide()
        self.combo_turn.hide()
        
        self.bottom_frame.show()
        
        self.btn_execute.show()
        self.btn_next.show()
        self.btn_last.show()
        self.btn_remove.show()

        self.lbl_path.show()
        self.lbl_explored.show()
        self.lbl_generated.show()
        self.lbl_depth.show()
        self.lbl_runtime.show()
        self.clear_result_fields()

    def update_adv_bottom(self, turn, result=""):
        self.lbl_success.setText(f"<b>Turn:</b> {turn}")
        if result:
            self.lbl_cost.setText(f"<b>Result:</b> {result}")
        else:
            self.lbl_cost.setText("<b>Result:</b> ")