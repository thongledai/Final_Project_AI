import sys
import math

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QFrame, QScrollArea, QGridLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont,
    QPainterPath, QLinearGradient, QRadialGradient
)

from Core.Utils import CAPACITY

# ═══════════════════════════ COLORS ═══════════════════════════════
COLOR_MAP = {
    1: QColor("#FF2D55"),   # Bright Neon Red/Pink
    2: QColor("#FFCC00"),   # Sunny Golden Yellow
    3: QColor("#00C2FF"),   # Vivid Sky Blue
    4: QColor("#4CD964"),   # Vibrant Green
    5: QColor("#AF52DE"),   # Electric Purple
    6: QColor("#FF9500"),   # High-saturation Orange
    7: QColor("#FF4F00"),   # Intense Coral
}
COLOR_LIGHT = {
    1: QColor("#FF6B8B"),
    2: QColor("#FFE066"),
    3: QColor("#66DAFF"),
    4: QColor("#86F099"),
    5: QColor("#D08DFF"),
    6: QColor("#FFBE66"),
    7: QColor("#FF8566"),
}
COLOR_DARK = {
    1: QColor("#D81B60"),
    2: QColor("#F57F17"),
    3: QColor("#0077C2"),
    4: QColor("#00A935"),
    5: QColor("#7B1FA2"),
    6: QColor("#E65100"),
    7: QColor("#D84315"),
}

BG_COLOR        = "#D1D5DB"  # Darker light gray background
PANEL_BG        = "#FFFFFF"  # White panel
ACCENT_COLOR    = "#1E293B"  # Dark gray text


# ═══════════════════════ TUBE GEOMETRY ════════════════════════════
TUBE_WIDTH   = 62
CELL_HEIGHT  = 52
TUBE_HEIGHT  = CAPACITY * CELL_HEIGHT   # 208 px
TUBE_GAP     = 48
TUBE_BR      = TUBE_WIDTH // 2          # Full semicircle bottom

# ══════════════════════════ ANIMATION ═════════════════════════════
ANIM_DURATION  = 900    # ms  (total pour transition)
ANIM_FPS       = 60

WAVE_SPEED     = 2.6    # radians / second
WAVE_IDLE_AMP  = 2.2    # px  – gentle idle ripple
WAVE_POUR_AMP  = 14.0   # px  – active sloshing
WAVE_DECAY     = 0.055  # smoothing coefficient per frame

LIFT_HEIGHT    = 160    # px  – how high src tube lifts (way above others)
MAX_TILT       = 75     # deg – steep tilt like in reference image


# ═══════════════════════════════════════════════════════════════════
class PuzzleView(QWidget):
    """
    Custom widget that renders Water Sort Puzzle tubes.
    Features:
      • U-shaped (test-tube) glass appearance
      • Continuous water-wave animation on liquid surfaces
      • Animated pour-stream arc between tubes
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # ── Display state ─────────────────────────────────────────
        self.state_data     = []
        self.is_multi_state = False
        self.highlight_tube = None

        # ── Click interaction ─────────────────────────────────────
        self.tube_rects     = []
        self.click_callback = None

        # ── Pour animation ────────────────────────────────────────
        self.is_animating          = False
        self.anim_progress         = 0.0
        self.anim_action           = None
        self.anim_state_before     = None
        self.anim_state_after      = None
        self.on_anim_done_callback = None

        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._anim_step)

        # ── Wave animation (always running) ───────────────────────
        self.wave_phase      = 0.0
        self.wave_amplitude  = WAVE_IDLE_AMP
        self.wave_target_amp = WAVE_IDLE_AMP

        self.wave_timer = QTimer(self)
        self.wave_timer.timeout.connect(self._wave_step)
        self.wave_timer.start(1000 // ANIM_FPS)

        # ── Tube dimensions (may shrink in multi-state mode) ──────
        self._use_normal_dims()

        self.setMinimumSize(800, 450)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {PANEL_BG};")

    # ─────────────────────── Dimensions ───────────────────────────

    def _use_normal_dims(self):
        self.tube_w  = TUBE_WIDTH
        self.cell_h  = CELL_HEIGHT
        self.tube_h  = TUBE_HEIGHT
        self.tube_gap = TUBE_GAP
        self.tube_br = TUBE_BR

    def _use_small_dims(self):
        self.tube_w  = 40
        self.cell_h  = 33
        self.tube_h  = CAPACITY * 33
        self.tube_gap = 26
        self.tube_br = 20

    def update_dimensions(self):
        if self.is_multi_state:
            self._use_small_dims()
        else:
            self._use_normal_dims()

    def _update_min_size(self):
        if not self.state_data:
            return
        if self.is_multi_state:
            n  = len(self.state_data)
            mt = max((len(s) for s in self.state_data), default=0)
            w  = mt * self.tube_w + (mt + 1) * self.tube_gap
            h  = n * (self.tube_h + 120)
        else:
            n = len(self.state_data)
            w = n * self.tube_w + (n + 1) * self.tube_gap
            h = self.tube_h + 120
        self.setMinimumSize(max(800, w), max(450, h))

    # ─────────────────────── State ────────────────────────────────

    def set_state(self, state_data, highlight=None):
        self.state_data     = state_data
        self.highlight_tube = highlight
        self.is_multi_state = self._is_multi(state_data)
        self.update_dimensions()
        self._update_min_size()

    @staticmethod
    def _is_multi(data):
        return (data and isinstance(data, list) and len(data) > 0
                and isinstance(data[0], list) and len(data[0]) > 0
                and isinstance(data[0][0], list))

    # ─────────────────────── Wave ─────────────────────────────────

    def _wave_step(self):
        self.wave_phase = (self.wave_phase + WAVE_SPEED / ANIM_FPS) % (math.pi * 200)
        diff = self.wave_target_amp - self.wave_amplitude
        self.wave_amplitude += diff * WAVE_DECAY
        self.update()

    def _set_wave_active(self):
        self.wave_target_amp = WAVE_POUR_AMP
        self.wave_amplitude  = max(self.wave_amplitude, WAVE_POUR_AMP * 0.65)

    def _set_wave_idle(self):
        self.wave_target_amp = WAVE_IDLE_AMP

    # ─────────────────────── Pour animation ───────────────────────

    def start_animation(self, state_before, state_after, action, on_done):
        if action is None:
            on_done()
            return

        self.anim_state_before     = state_before
        self.anim_state_after      = state_after
        self.anim_action           = action
        self.on_anim_done_callback = on_done
        self.is_animating          = True
        self.is_multi_state        = self._is_multi(state_before)
        self.update_dimensions()
        self.anim_progress = 0.0
        self._update_min_size()
        self._set_wave_active()
        self.anim_timer.start(1000 // ANIM_FPS)

    def _anim_step(self):
        self.anim_progress += (1000.0 / ANIM_FPS) / ANIM_DURATION
        if self.anim_progress >= 1.0:
            self.anim_timer.stop()
            self.is_animating = False
            self.state_data   = self.anim_state_after
            self._set_wave_idle()
            if self.on_anim_done_callback:
                self.on_anim_done_callback()

    # ─────────────────────── Mouse ────────────────────────────────

    def mousePressEvent(self, event):
        if self.click_callback:
            for (rect, idx) in self.tube_rects:
                if rect.contains(event.pos()):
                    self.click_callback(idx)
                    return

    # ═══════════════════════ PAINT ════════════════════════════════

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.tube_rects.clear()

        if self.is_animating:
            self._paint_animation(painter)
            return

        if not self.state_data:
            return

        cw, ch = self.width(), self.height()

        if self.is_multi_state:
            n  = len(self.state_data)
            sh = max(self.tube_h + 120, ch // n if n > 0 else ch)
            for i, st in enumerate(self.state_data):
                ys, ye = i * sh, (i + 1) * sh
                painter.setPen(QColor("#333333"))
                painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
                painter.drawText(0, ys + 10, cw, 30,
                                 Qt.AlignmentFlag.AlignHCenter,
                                 f"Belief State {i + 1}")
                self._draw_tubes(painter, st, cw, ys + 40, ye, None)
                if i < n - 1:
                    painter.setPen(QPen(QColor("#CCCCCC"), 1, Qt.PenStyle.DashLine))
                    painter.drawLine(50, ye, cw - 50, ye)
        else:
            self._draw_tubes(painter, self.state_data, cw, 0, ch, self.highlight_tube)

    # ─────────────────────── Tubes layout ─────────────────────────

    def _draw_tubes(self, painter, state, cw, ys, ye, highlight):
        n       = len(state)
        total_w = n * self.tube_w + (n - 1) * self.tube_gap
        x0      = (cw - total_w) // 2
        ty      = ys + ((ye - ys) - self.tube_h) // 2

        for i, tube in enumerate(state):
            x = x0 + i * (self.tube_w + self.tube_gap)
            self._draw_tube(painter, x, ty, tube, i == highlight, i)

            painter.setPen(QColor("#1E293B"))
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            painter.drawText(
                int(x), int(ty + self.tube_h + 10),
                int(self.tube_w), 22,
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                f"Lọ {i}"
            )
            self.tube_rects.append(
                (QRect(int(x), int(ty), int(self.tube_w), int(self.tube_h)), i)
            )

    # ─────────────────────── Single tube ──────────────────────────

    def _tube_path(self, x, y):
        """U-shaped (test tube) clip path — open top, convex rounded bottom."""
        w, h, br = self.tube_w, self.tube_h, self.tube_br
        p = QPainterPath()
        p.moveTo(x, y)
        p.lineTo(x, y + h - br)
        # +180 (counter-clockwise in Qt) → passes through BOTTOM of ellipse
        # giving a convex U-shape. -180 would go through TOP (concave).
        p.arcTo(x, y + h - 2 * br, w, 2 * br, 180, 180)
        p.lineTo(x + w, y)
        return p

    def _draw_tube(self, painter, x, y, tube, is_highlight, tube_idx=0):
        w  = self.tube_w
        h  = self.tube_h
        tp = self._tube_path(x, y)

        painter.save()
        painter.setClipPath(tp)

        # 1. White glass interior (empty space)
        bg = QLinearGradient(x, y, x + w, y)
        bg.setColorAt(0.0, QColor(245, 245, 250, 255))
        bg.setColorAt(0.5, QColor(255, 255, 255, 255))
        bg.setColorAt(1.0, QColor(245, 245, 250, 255))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawPath(tp)

        # 2. Color blocks
        for slot in range(len(tube)):
            cv    = tube[slot]
            y_bot = y + h - slot * self.cell_h
            y_top = y_bot - self.cell_h

            if cv == -1:
                # Hidden color (partial-observable)
                painter.setBrush(QBrush(QColor(60, 60, 110, 100)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRect(int(x + 1), int(y_top), int(w - 2), int(self.cell_h))
                continue

            is_top = (slot == len(tube) - 1)
            if is_top:
                # Top slot drawn flat as requested
                self._draw_slot_solid(painter, x, y_top, y_bot, cv)
            else:
                self._draw_slot_solid(painter, x, y_top, y_bot, cv)

            # Separator between different colors
            if slot > 0 and tube[slot] != tube[slot - 1]:
                painter.setPen(QPen(QColor(0, 0, 0, 55), 1))
                painter.drawLine(int(x + 2), int(y_bot), int(x + w - 2), int(y_bot))
                painter.setPen(Qt.PenStyle.NoPen)

        # 3. Left glass highlight
        lh = QLinearGradient(x, y, x + w * 0.40, y)
        lh.setColorAt(0.0, QColor(255, 255, 255, 70))
        lh.setColorAt(0.5, QColor(255, 255, 255, 20))
        lh.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(lh))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(tp)

        # 4. Right edge shimmer
        rh = QLinearGradient(x + w * 0.70, y, x + w, y)
        rh.setColorAt(0.0, QColor(255, 255, 255, 0))
        rh.setColorAt(1.0, QColor(255, 255, 255, 25))
        painter.setBrush(QBrush(rh))
        painter.drawPath(tp)

        # 5. Bottom glow (reflects light through glass bottom)
        bg_glow = QRadialGradient(x + w / 2, y + h - self.tube_br * 0.6, self.tube_br)
        bg_glow.setColorAt(0.0, QColor(255, 255, 255, 18))
        bg_glow.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(bg_glow))
        painter.drawPath(tp)

        painter.restore()   # ← removes clip

        # 6. Tube outline
        if is_highlight:
            pen = QPen(QColor("#FFD700"), 3.5)
            # Gold glow
            glow_pen = QPen(QColor(255, 215, 0, 60), 9)
            glow_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(glow_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(tp)
        else:
            pen = QPen(QColor("#9CA3AF"), 2.5)

        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(tp)
        painter.drawLine(int(x), int(y), int(x + w), int(y))

    # ─────────────────────── Slot helpers ─────────────────────────

    def _draw_slot_solid(self, painter, x, y_top, y_bot, color_val):
        """Non-top liquid slot: horizontal gradient rectangle."""
        base  = COLOR_MAP.get(color_val,  QColor("#aaaaaa"))
        light = COLOR_LIGHT.get(color_val, base)
        dark  = COLOR_DARK.get(color_val,  base)

        grad = QLinearGradient(x, y_top, x + self.tube_w, y_top)
        grad.setColorAt(0.0,  light)
        grad.setColorAt(0.45, base)
        grad.setColorAt(1.0,  dark)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(grad))
        painter.drawRect(int(x + 1), int(y_top), int(self.tube_w - 2),
                         int(y_bot - y_top + 1))

    def _draw_slot_wave(self, painter, x, y_top, y_bot, color_val, tube_idx):
        """Draw top liquid slot: solid fill + wave ripple at surface."""
        if y_top >= y_bot:
            return

        base  = COLOR_MAP.get(color_val,  QColor("#aaaaaa"))
        light = COLOR_LIGHT.get(color_val, base)
        dark  = COLOR_DARK.get(color_val,  base)
        w     = self.tube_w
        amp   = self.wave_amplitude
        phase = self.wave_phase + tube_idx * 1.15
        n     = 34

        # ── 1. Solid gradient fill for the ENTIRE slot (guarantees no gap) ──
        grad = QLinearGradient(x, y_top, x + w, y_top)
        grad.setColorAt(0.0,  light)
        grad.setColorAt(0.45, base)
        grad.setColorAt(1.0,  dark)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(grad))
        painter.drawRect(int(x + 1), int(y_top), int(w - 2), int(y_bot - y_top + 1))

        # ── 2. Wave ripple overlay at the liquid surface ──
        # A closed shape from the sine wave down to y_top + amp*2
        wave = QPainterPath()
        wave.moveTo(x + 1, y_top + amp * math.sin(phase))
        for i in range(1, n + 1):
            t  = i / n
            px = x + 1 + t * (w - 2)
            py = y_top + amp * math.sin(phase + t * 4 * math.pi)
            wave.lineTo(px, py)
        wave.lineTo(x + w - 1, y_top + amp * 2 + 2)
        wave.lineTo(x + 1,     y_top + amp * 2 + 2)
        wave.closeSubpath()

        wg = QLinearGradient(x, y_top - amp, x, y_top + amp * 2)
        wg.setColorAt(0.0, light)
        wg.setColorAt(0.6, base)
        wg.setColorAt(1.0, base)
        painter.setBrush(QBrush(wg))
        painter.drawPath(wave)

        # ── 3. White crest highlight line ──
        crest = QPainterPath()
        crest.moveTo(x + 1, y_top + amp * math.sin(phase))
        for i in range(1, n + 1):
            t  = i / n
            crest.lineTo(x + 1 + t * (w - 2),
                         y_top + amp * math.sin(phase + t * 4 * math.pi))
        alpha = min(255, int(60 + amp * 10))
        painter.setPen(QPen(QColor(255, 255, 255, alpha), 1.6))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(crest)
        painter.setPen(Qt.PenStyle.NoPen)

    # ═══════════════════ ANIMATION PAINTING ═══════════════════════

    def _paint_animation(self, painter):
        if self.is_multi_state:
            n  = len(self.anim_state_before)
            sh = self.height() // n if n > 0 else self.height()
            cw = self.width()
            for i in range(n):
                ys, ye = i * sh, (i + 1) * sh
                painter.setPen(QColor("#333333"))
                painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
                painter.drawText(0, ys + 10, cw, 30,
                                 Qt.AlignmentFlag.AlignHCenter,
                                 f"Belief State {i + 1}")
                self._draw_anim_state(
                    painter,
                    self.anim_state_before[i],
                    self.anim_state_after[i],
                    ys + 40, ye
                )
                if i < n - 1:
                    painter.setPen(QPen(QColor("#CCCCCC"), 1, Qt.PenStyle.DashLine))
                    painter.drawLine(50, ye, cw - 50, ye)
        else:
            self._draw_anim_state(
                painter,
                self.anim_state_before,
                self.anim_state_after,
                0, self.height()
            )

    def _draw_anim_state(self, painter, state_before, state_after, ys, ye):
        cw       = self.width()
        src, dst = self.anim_action
        n        = len(state_before)
        total_w  = n * self.tube_w + (n - 1) * self.tube_gap
        x0       = (cw - total_w) // 2
        ty       = ys + ((ye - ys) - self.tube_h) // 2
        p        = self.anim_progress   # 0 → 1 overall

        lbl_color = QColor("#1E293B")
        lbl_font  = QFont("Segoe UI", 9, QFont.Weight.Bold)

        src_tube  = list(state_before[src])
        dst_tube  = list(state_before[dst])
        color_val = src_tube[-1] if src_tube else 1

        src_x = x0 + src * (self.tube_w + self.tube_gap)
        dst_x = x0 + dst * (self.tube_w + self.tube_gap)
        src_cx = src_x + self.tube_w / 2
        dst_cx = dst_x + self.tube_w / 2
        direction = 1.0 if dst_cx >= src_cx else -1.0

        # ── PHASED ANIMATION ──────────────────────────────────────
        # Phase 1: 0.00–0.20  Lift up + slide to hover position (vertical)
        # Phase 2: 0.20–0.40  Tilt to MAX_TILT (mouth stays anchored)
        # Phase 3: 0.40–0.70  Pouring (mouth stays anchored, liquid transfers)
        # Phase 4: 0.70–0.85  Un-tilt to 0 (mouth stays anchored)
        # Phase 5: 0.85–1.00  Lower back and slide to original position

        def ease(t):
            """Ease in-out (smoothstep)."""
            t = max(0.0, min(1.0, t))
            return t * t * (3.0 - 2.0 * t)

        # Tilt angle calculation
        if p < 0.20:
            tilt_t = 0.0
        elif p < 0.40:
            tilt_t = ease((p - 0.20) / 0.20)
        elif p < 0.70:
            tilt_t = 1.0
        elif p < 0.85:
            tilt_t = ease(1.0 - (p - 0.70) / 0.15)
        else:
            tilt_t = 0.0
        tilt_deg = tilt_t * MAX_TILT * direction
        tilt_rad = math.radians(tilt_deg)
        cos_t = math.cos(tilt_rad)
        sin_t = math.sin(tilt_rad)

        # Local mouth lip coords (where the pour happens)
        local_lx = self.tube_w / 2 * (-direction)
        local_ly = -self.tube_h + 12   # 12px inside mouth

        # Anchor coordinates for the exit mouth during pour (centered above dst mouth)
        target_exit_x = dst_x + self.tube_w / 2 - direction * 8
        target_exit_y = ty - 28

        # Position of the tube that keeps the mouth at target_exit
        anchor_x = target_exit_x - (local_lx * cos_t - local_ly * sin_t) - self.tube_w / 2
        anchor_lift = self.tube_h + (ty - target_exit_y) + (local_lx * sin_t + local_ly * cos_t)

        # Interpolate the tube's position based on active phase
        if p < 0.20:
            # Phase 1: Slide to vertical hover position next to dst
            slide_t = ease(p / 0.20)
            # Coordinates at tilt = 0
            anchor_x_0 = target_exit_x - local_lx - self.tube_w / 2
            anchor_lift_0 = self.tube_h + (ty - target_exit_y) + local_ly

            actual_src_x = src_x + (anchor_x_0 - src_x) * slide_t
            lift = anchor_lift_0 * slide_t
        elif p < 0.85:
            # Phases 2, 3, 4: Keep mouth perfectly anchored in space while tilting
            actual_src_x = anchor_x
            lift = anchor_lift
        else:
            # Phase 5: Slide back to start position
            slide_t = ease((p - 0.85) / 0.15)
            anchor_x_0 = target_exit_x - local_lx - self.tube_w / 2
            anchor_lift_0 = self.tube_h + (ty - target_exit_y) + local_ly

            actual_src_x = anchor_x_0 + (src_x - anchor_x_0) * slide_t
            lift = anchor_lift_0 * (1.0 - slide_t)

        # Liquid transfer progress (during phase 3)
        if p < 0.40:
            pour_t = 0.0
        elif p < 0.70:
            pour_t = ease((p - 0.40) / 0.30)
        else:
            pour_t = 1.0

        # ── Draw static tubes ──
        for i in range(n):
            if i in (src, dst):
                continue
            x = x0 + i * (self.tube_w + self.tube_gap)
            self._draw_tube(painter, x, ty, state_before[i], False, i)
            painter.setPen(lbl_color); painter.setFont(lbl_font)
            painter.drawText(int(x), int(ty + self.tube_h + 10),
                             int(self.tube_w), 22,
                             Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                             f"Lọ {i}")

        # ── Destination tube: liquid arriving ──
        state_after_src = list(state_after[src])
        state_after_dst = list(state_after[dst])
        K = len(src_tube) - len(state_after_src)
        if K <= 0:
            K = 1

        # Destination tube draws the final state, clipped to the current level:
        # dst_num_blocks starts at len(dst_tube) and grows to len(dst_tube) + K
        dst_num_blocks = len(dst_tube) + K * pour_t
        self._draw_tube_anim(painter, dst_x, ty, state_after_dst, dst_num_blocks, dst)
        painter.setPen(lbl_color); painter.setFont(lbl_font)
        painter.drawText(int(dst_x), int(ty + self.tube_h + 10),
                         int(self.tube_w), 22,
                         Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                         f"Lọ {dst}")

        # ── Source tube: lifted, slid horizontally, tilted ──
        # Source tube draws the initial state, clipped to the current level:
        # src_num_blocks starts at len(src_tube) and shrinks to len(src_tube) - K
        src_num_blocks = len(src_tube) - K * pour_t
        self._draw_tube_tilted(
            painter, actual_src_x, ty, src_tube,
            lift, tilt_deg, src, anim_num_blocks=src_num_blocks
        )
        # Label stays at original position
        painter.setPen(lbl_color); painter.setFont(lbl_font)
        painter.drawText(int(src_x), int(ty + self.tube_h + 10),
                         int(self.tube_w), 22,
                         Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                         f"Lọ {src}")

        # ── Pour stream (only while tilted and pouring) ──
        is_pouring = 0.25 < p < 0.80
        if src_tube and is_pouring:
            tilt_rad = math.radians(tilt_deg)
            cos_t    = math.cos(tilt_rad)
            sin_t    = math.sin(tilt_rad)

            # Pivot = bottom-centre of src tube at its current position
            piv_x = actual_src_x + self.tube_w / 2
            piv_y = ty + self.tube_h - lift

            # Start point: slightly inside the tube mouth along the tilted bottom wall
            local_lx = self.tube_w / 2 * (-direction)
            local_ly = -self.tube_h + 12   # 12 pixels inside the tube

            exit_x = piv_x + local_lx * cos_t - local_ly * sin_t
            exit_y = piv_y + local_lx * sin_t + local_ly * cos_t

            # Launch vector: shoots out of mouth along the longitudinal tube axis
            launch_dist = self.tube_w * 0.40
            vx = sin_t * launch_dist
            vy = -cos_t * launch_dist

            p0 = (exit_x, exit_y)
            p1 = (exit_x + vx, exit_y + vy)

            # Entry: top of current dst liquid level
            n_dst   = len(dst_tube)
            entry_x = dst_x + self.tube_w / 2
            entry_y = ty + self.tube_h - (n_dst + 1) * self.cell_h

            p3 = (entry_x, entry_y)
            
            # Control point 2: approach entry vertically from above
            drop = abs(entry_y - exit_y)
            p2 = (entry_x, entry_y - min(drop * 0.45, 65))

            # Stream fade based on tilt amount
            stream_fade = min(tilt_t * 3.0, 1.0)
            self._draw_pour_stream_gravity(
                painter, p0, p1, p2, p3,
                color_val, stream_fade
            )

    def _draw_tube_tilted(self, painter, cur_x, cur_y, tube,
                           lift, tilt_deg, tube_idx, anim_num_blocks=None):
        """
        Draw the source tube at (cur_x, cur_y) lifted by `lift` and
        rotated by `tilt_deg` around its bottom-centre pivot.
        """
        w, h = self.tube_w, self.tube_h

        # Pivot = bottom-centre, elevated
        piv_x = cur_x + w / 2
        piv_y = cur_y + h          # bottom-centre before lift

        painter.save()
        painter.translate(piv_x, piv_y - lift)
        painter.rotate(tilt_deg)
        
        if anim_num_blocks is None:
            anim_num_blocks = len(tube)
            
        self._draw_tube_anim(painter, -w / 2, -h, tube, anim_num_blocks, tube_idx)
        painter.restore()

    def _draw_tube_anim(self, painter, x, y, tube, num_blocks, tube_idx=0):
        """Draw tube with liquid clipped to a fractional number of blocks."""
        w  = self.tube_w
        h  = self.tube_h
        tp = self._tube_path(x, y)

        painter.save()
        painter.setClipPath(tp)

        # Interior
        bg = QLinearGradient(x, y, x + w, y)
        bg.setColorAt(0.0, QColor(245, 245, 250, 255))
        bg.setColorAt(0.5, QColor(255, 255, 255, 255))
        bg.setColorAt(1.0, QColor(245, 245, 250, 255))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawPath(tp)

        # ── Color blocks (Clipped dynamically by current liquid height) ──
        y_top_liquid = y + h - num_blocks * self.cell_h
        
        # Create rectangular path for the liquid height clip
        rect_path = QPainterPath()
        rect_path.addRect(x - 5, y_top_liquid, w + 10, h + 10)
        
        # Intersect with the U-shape tube path so the liquid remains inside the rounded bottom
        color_clip_path = tp.intersected(rect_path)
        
        painter.save()
        painter.setClipPath(color_clip_path)

        for slot in range(len(tube)):
            cv    = tube[slot]
            if cv == -1:
                continue
            y_bot = y + h - slot * self.cell_h
            y_top = y_bot - self.cell_h
            self._draw_slot_solid(painter, x, y_top, y_bot, cv)

        painter.restore()

        # Glass highlights
        lh = QLinearGradient(x, y, x + w * 0.40, y)
        lh.setColorAt(0.0, QColor(255, 255, 255, 70))
        lh.setColorAt(0.5, QColor(255, 255, 255, 20))
        lh.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(lh))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(tp)

        painter.restore()

        pen = QPen(QColor(160, 185, 255, 145), 2.5)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(tp)
        painter.drawLine(int(x), int(y), int(x + w), int(y))

    def _draw_pour_stream_gravity(self, painter, p0, p1, p2, p3, color_val, fade):
        """
        Draw a gravity-fed downward stream of liquid using cubic Bezier.
        The stream starts at p0 (inside the tilted tube mouth), flows along p1
        (pointing out of the tube), and curves smoothly to p2 and p3 (the destination).
        """
        if fade < 0.01:
            return

        base  = COLOR_MAP.get(color_val, QColor("#aaaaaa"))
        light = COLOR_LIGHT.get(color_val, base)

        # Made stream thicker to match reference image
        stream_w = max(5, self.tube_w * 0.24)

        p0x, p0y = p0
        p1x, p1y = p1
        p2x, p2y = p2
        p3x, p3y = p3

        def cbez(t, a, b, c, d):
            u = 1 - t
            return u*u*u*a + 3*u*u*t*b + 3*u*t*t*c + t*t*t*d

        n = 30
        lefts, rights = [], []

        for i in range(n + 1):
            t  = i / n
            bx = cbez(t, p0x, p1x, p2x, p3x)
            by = cbez(t, p0y, p1y, p2y, p3y)

            # Tangent via derivative of cubic bezier
            if i < n:
                tx = cbez((i+1)/n, p0x, p1x, p2x, p3x) - bx
                ty = cbez((i+1)/n, p0y, p1y, p2y, p3y) - by
            else:
                tx = bx - cbez((i-1)/n, p0x, p1x, p2x, p3x)
                ty = by - cbez((i-1)/n, p0y, p1y, p2y, p3y)

            L  = math.sqrt(tx*tx + ty*ty) or 1.0
            nx, ny = -ty / L, tx / L

            # Taper: thick at start, slightly thinner, then wider landing
            taper = 0.75 + 0.25 * (1.0 - t)
            sw = stream_w * taper

            lefts.append((bx - nx * sw, by - ny * sw))
            rights.append((bx + nx * sw, by + ny * sw))

        # ── Fill stream body ──
        stream = QPainterPath()
        stream.moveTo(*lefts[0])
        for pt in lefts[1:]:
            stream.lineTo(*pt)
        stream.lineTo(*rights[-1])
        for pt in reversed(rights[:-1]):
            stream.lineTo(*pt)
        stream.closeSubpath()

        sc = QColor(base)
        sc.setAlpha(int(230 * fade))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(sc))
        painter.drawPath(stream)

        # ── Highlight strip ──
        hl = QPainterPath()
        hl.moveTo(lefts[0][0] + (rights[0][0] - lefts[0][0]) * 0.28,
                  lefts[0][1] + (rights[0][1] - lefts[0][1]) * 0.28)
        for i in range(1, len(lefts)):
            px = lefts[i][0] + (rights[i][0] - lefts[i][0]) * 0.28
            py = lefts[i][1] + (rights[i][1] - lefts[i][1]) * 0.28
            hl.lineTo(px, py)
        lc = QColor(light)
        lc.setAlpha(int(110 * fade))
        painter.setPen(QPen(lc, 2.2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(hl)

        painter.setPen(Qt.PenStyle.NoPen)


# ═══════════════════════════════════════════════════════════════════
class View(QMainWindow):
    """Main window — dark game theme matching Water Sort Puzzle."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Water Sort Puzzle")
        self.resize(1400, 900)
        self.showMaximized()

        # Global white palette
        self.setStyleSheet(f"""
            QMainWindow  {{ background-color: {BG_COLOR}; }}
            QWidget      {{ background-color: transparent; color: #1E293B; font-family: 'Segoe UI'; }}
            QScrollBar:vertical {{
                background: #F1F5F9; width: 8px; border-radius: 4px; margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: #CBD5E1; border-radius: 4px; min-height: 24px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)

        central = QWidget()
        central.setStyleSheet(f"background-color: {BG_COLOR};")
        self.setCentralWidget(central)

        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(14, 14, 14, 14)
        self.main_layout.setSpacing(11)

        self._init_top_bar()
        self._init_middle()
        self._init_bottom_bar()

    # ─────────────────────── Top bar ──────────────────────────────

    def _init_top_bar(self):
        COMBO_STYLE = f"""
            QComboBox {{
                background-color: #FFFFFF;
                color: #1E293B;
                border: 1px solid #CBD5E1;
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 13px;
                min-width: 210px;
            }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox QAbstractItemView {{
                background-color: #FFFFFF;
                color: #1E293B;
                selection-background-color: #F1F5F9;
            }}
            QLabel {{
                color: #1E293B;
                font-size: 13px;
                font-weight: bold;
            }}
        """

        self.top_frame = QFrame()
        self.top_frame.setStyleSheet(
            f"QFrame {{ background-color: {PANEL_BG}; border-radius: 8px; border: 1px solid #94A3B8; }}" + COMBO_STYLE
        )

        lay = QHBoxLayout(self.top_frame)
        lay.setContentsMargins(15, 6, 15, 6)
        lay.setSpacing(14)

        lbl_cat  = QLabel("Chọn loại thuật toán:")
        self.combo_category = QComboBox()

        lbl_algo = QLabel("Chọn thuật toán:")
        self.combo_algo = QComboBox()

        self.lbl_turn  = QLabel("Lượt đầu:")
        self.combo_turn = QComboBox()
        self.combo_turn.addItems(["Người đi trước", "Máy đi trước"])
        self.combo_turn.setFixedWidth(165)
        self.combo_turn.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF; color: #1E293B;
                border: 1px solid #CBD5E1; border-radius: 4px;
                padding: 4px 10px; font-size: 13px;
            }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF; color: #1E293B;
                selection-background-color: #F1F5F9;
            }
        """)

        lay.addWidget(lbl_cat)
        lay.addWidget(self.combo_category)
        lay.addSpacing(18)
        lay.addWidget(lbl_algo)
        lay.addWidget(self.combo_algo)
        lay.addSpacing(18)
        lay.addWidget(self.lbl_turn)
        lay.addWidget(self.combo_turn)
        lay.addStretch()

        self.main_layout.addWidget(self.top_frame)

    # ─────────────────────── Middle area ──────────────────────────

    def _init_middle(self):
        mid = QHBoxLayout()
        mid.setSpacing(11)

        # ── Puzzle scroll area ──────────────────────────────────
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {PANEL_BG};
                border-radius: 8px;
                border: 1px solid #94A3B8;
            }}
        """)

        self.puzzle_view = PuzzleView()
        self.puzzle_view.setObjectName("puzzle_view")
        self.scroll_area.setWidget(self.puzzle_view)
        mid.addWidget(self.scroll_area, stretch=7)

        # ── Control panel ───────────────────────────────────────
        self.panel_frame = QFrame()
        self.panel_frame.setFixedWidth(280)
        self.panel_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {PANEL_BG};
                border-radius: 8px;
                border: 1px solid #94A3B8;
            }}
        """)

        pl = QVBoxLayout(self.panel_frame)
        pl.setContentsMargins(16, 22, 16, 22)
        pl.setSpacing(11)

        ptitle = QLabel("BẢNG ĐIỀU KHIỂN")
        ptitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ptitle.setStyleSheet(f"""
            font-size: 15px; font-weight: bold;
            color: #1E293B; border: none;
        """)
        pl.addWidget(ptitle)

        pl.addSpacing(4)

        def btn(text):
            b = QPushButton(text)
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: #78909C;
                    color: #FFFFFF;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 6px;
                    height: 40px;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: #90A4AE;
                }}
                QPushButton:pressed {{
                    background-color: #607D8B;
                }}
                QPushButton:disabled {{
                    background-color: #CFD8DC; color: #90A4AE;
                }}
            """)
            return b

        self.btn_start   = btn("Initial")
        self.btn_random  = btn("Random")
        self.btn_execute = btn("Execute")
        self.btn_auto    = btn("Auto")
        self.btn_pause   = btn("Pause")
        self.btn_next    = btn("Next")
        self.btn_last    = btn("Back")
        self.btn_remove  = btn("Remove")

        self.btn_pause.setEnabled(False)

        for b in (self.btn_start, self.btn_random, self.btn_execute,
                  self.btn_auto, self.btn_pause,
                  self.btn_next, self.btn_last, self.btn_remove):
            pl.addWidget(b)

        pl.addStretch()
        mid.addWidget(self.panel_frame, stretch=3)
        self.main_layout.addLayout(mid)

    # ─────────────────────── Bottom bar ───────────────────────────

    def _init_bottom_bar(self):
        self.bottom_frame = QFrame()
        self.bottom_frame.setMinimumHeight(75)
        self.bottom_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {PANEL_BG};
                border-radius: 8px;
                border: 1px solid #94A3B8;
            }}
            QLabel {{ 
                color: #1E293B; 
                font-size: 13px; 
                border: 1px solid #94A3B8; 
                border-radius: 4px; 
                padding: 4px;
                background-color: #F8FAFC;
            }}
        """)

        lay = QGridLayout(self.bottom_frame)
        lay.setContentsMargins(20, 8, 20, 8)
        lay.setHorizontalSpacing(28)

        self.lbl_path = QLabel(f"<b style='color:{ACCENT_COLOR}'>Path:</b> ")
        self.lbl_path.setWordWrap(True)
        lay.addWidget(self.lbl_path, 0, 0, 1, 6)

        self.lbl_success   = QLabel("Success:")
        self.lbl_cost      = QLabel("Cost:")
        self.lbl_explored  = QLabel("Explored:")
        self.lbl_generated = QLabel("Generated:")
        self.lbl_depth     = QLabel("Depth:")
        self.lbl_runtime   = QLabel("Runtime:")

        for col, lbl in enumerate([
            self.lbl_success,
            self.lbl_runtime,   
            self.lbl_cost,
            self.lbl_explored,
            self.lbl_generated,
            self.lbl_depth      
        ]):
            lbl.setFixedHeight(28)
            lay.addWidget(lbl, 1, col)

        self.main_layout.addWidget(self.bottom_frame)

    # ═══════════════════════ Public API ═══════════════════════════

    def clear_result_fields(self):
        ac = ACCENT_COLOR
        self.lbl_path.setText(f"<b style='color:{ac}'>Path:</b> ")
        self.lbl_success.setText(  f"<b style='color:{ac}'>Success:</b>")
        self.lbl_cost.setText(     f"<b style='color:{ac}'>Cost:</b>")
        self.lbl_explored.setText( f"<b style='color:{ac}'>Explored:</b>")
        self.lbl_generated.setText(f"<b style='color:{ac}'>Generated:</b>")
        self.lbl_depth.setText(    f"<b style='color:{ac}'>Depth:</b>")
        self.lbl_runtime.setText(  f"<b style='color:{ac}'>Runtime:</b>")

    def set_result_fields(self, result):
        if result is None:
            self.clear_result_fields()
            return

        ac = ACCENT_COLOR
        wc = "#000000"   # value color

        def f(label, val):
            return f"<b style='color:{ac}'>{label}:</b> <span style='color:{wc}'>{val}</span>"

        ok_txt = "True" if result.success else "False"
        self.lbl_success.setText(  f(  "Success",   ok_txt))
        self.lbl_cost.setText(     f(     "Cost",   result.cost))
        self.lbl_explored.setText( f( "Explored",   result.explored))
        self.lbl_generated.setText(f("Generated",   result.generated))
        self.lbl_depth.setText(    f(    "Depth",   result.depth))
        self.lbl_runtime.setText(  f(  "Runtime",   f"{result.runtime:.4f}s"))

        path_str = " -> ".join(str(p) for p in result.path) if result.path else "None"
        self.lbl_path.setText(
            f"<b style='color:{ac}'>Path:</b>"
            f" <span style='color:{wc}'>{path_str}</span>"
        )

    def show_step_info(self, step, total, action=None):
        pass  # Could extend with a step counter label if desired

    def draw_state(self, state, highlight_tube=None):
        self.puzzle_view.set_state(state, highlight_tube)

    def draw_partial_states(self, state_list):
        self.puzzle_view.set_state(state_list)

    def animate_pour(self, state_before, state_after, action, on_done):
        self.puzzle_view.start_animation(state_before, state_after, action, on_done)

    def show_adversarial_ui(self):
        self.bottom_frame.setMinimumHeight(45)
        self.lbl_turn.show()
        self.combo_turn.show()
        self.btn_execute.hide()
        self.btn_auto.hide()
        self.btn_pause.hide()
        self.btn_next.hide()
        self.btn_last.hide()
        self.btn_remove.hide()
        self.lbl_path.hide()
        self.lbl_explored.show()
        self.lbl_generated.show()
        self.lbl_depth.hide()
        self.lbl_runtime.show()
        ac = ACCENT_COLOR
        self.lbl_success.setText(f"<b style='color:{ac}'>Turn:</b> <span style='color:#000000'>Human</span>")
        self.lbl_cost.setText(   f"<b style='color:{ac}'>Result:</b> ")

    def hide_adversarial_ui(self):
        self.bottom_frame.setMinimumHeight(75)
        self.lbl_turn.hide()
        self.combo_turn.hide()
        self.btn_execute.show()
        self.btn_auto.show()
        self.btn_pause.show()
        self.btn_next.show()
        self.btn_last.show()
        self.btn_remove.show()
        self.lbl_path.show()
        self.lbl_explored.show()
        self.lbl_generated.show()
        self.lbl_depth.show()
        self.lbl_runtime.show()
        self.clear_result_fields()

    def update_adv_bottom(self, turn, result_text="", alg_result=None):
        ac = ACCENT_COLOR
        wc = "#1E293B"
        self.lbl_success.setText(
            f"<b style='color:{ac}'>Turn:</b> <span style='color:{wc}'>{turn}</span>"
        )
        if result_text:
            self.lbl_cost.setText(
                f"<b style='color:{ac}'>Result:</b> <span style='color:{wc}'>{result_text}</span>"
            )
        else:
            self.lbl_cost.setText(f"<b style='color:{ac}'>Result:</b> ")
            
        if alg_result:
            self.lbl_explored.setText(f"<b style='color:{ac}'>Explored:</b> <span style='color:{wc}'>{alg_result.explored}</span>")
            self.lbl_generated.setText(f"<b style='color:{ac}'>Generated:</b> <span style='color:{wc}'>{alg_result.generated}</span>")
            self.lbl_runtime.setText(f"<b style='color:{ac}'>Runtime:</b> <span style='color:{wc}'>{alg_result.runtime:.4f}s</span>")
        else:
            self.lbl_explored.setText(f"<b style='color:{ac}'>Explored:</b>")
            self.lbl_generated.setText(f"<b style='color:{ac}'>Generated:</b>")
            self.lbl_runtime.setText(f"<b style='color:{ac}'>Runtime:</b>")
