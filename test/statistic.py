import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ── Đường dẫn tự động theo vị trí file script ───────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / 'results.csv'
OUT_DIR  = BASE_DIR / 'charts'
OUT_DIR.mkdir(exist_ok=True)

# ── Đọc dữ liệu ─────────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH)
df['success'] = df['success'].map({'True': True, 'False': False, True: True, False: False})

TOTAL_TC = df['test_case_id'].nunique()
ok = df[df['success'] == True].copy()

# ── Thứ tự & nhãn thuật toán ─────────────────────────────────────────────────
ALGOS = ['BFS','DFS','UCS','IDS','Greedy','A*','IDA*',
         'Hill_Simple','Hill_Steepest','Hill_Stochastic',
         'Hill_RandomRestart','SimulatedAnnealing','LocalBeam',
         'AndOrGraph','PartiallyObservable',
         'Minimax','AlphaBeta','Expectimax',
         'Backtracking','ForwardChecking']

ALGO_LABELS = ['BFS','DFS','UCS','IDS','Greedy','A*','IDA*',
               'Hill Simple','Hill Steepest','Hill Stochastic',
               'Hill Rand.Restart','Sim. Annealing','Local Beam',
               'AndOr Graph','Part. Observable',
               'Minimax','AlphaBeta','Expectimax',
               'Backtracking','Fwd. Checking']

# ── Màu theo nhóm ────────────────────────────────────────────────────────────
GROUP_COLOR = {
    'BFS':'#2a78d6','DFS':'#2a78d6','UCS':'#2a78d6','IDS':'#2a78d6',
    'Greedy':'#1baf7a','A*':'#1baf7a','IDA*':'#1baf7a',
    'Hill_Simple':'#eda100','Hill_Steepest':'#eda100',
    'Hill_Stochastic':'#eda100','Hill_RandomRestart':'#eda100',
    'SimulatedAnnealing':'#eda100','LocalBeam':'#eda100',
    'AndOrGraph':'#e34948','PartiallyObservable':'#e34948',
    'Minimax':'#4a3aa7','AlphaBeta':'#4a3aa7','Expectimax':'#4a3aa7',
    'Backtracking':'#1baf7a','ForwardChecking':'#1baf7a',
}
COLORS = [GROUP_COLOR[a] for a in ALGOS]

# ── Legend nhóm (dùng chung cho tất cả figure) ───────────────────────────────
patches = [
    mpatches.Patch(color='#2a78d6', label='Uninformed'),
    mpatches.Patch(color='#1baf7a', label='Informed / Constraint'),
    mpatches.Patch(color='#eda100', label='Local search'),
    mpatches.Patch(color='#e34948', label='Complex environment'),
    mpatches.Patch(color='#4a3aa7', label='Adversarial'),
]

# ── Tính metric ───────────────────────────────────────────────────────────────
success_rate   = (df.groupby('algorithm')['success'].sum() / TOTAL_TC * 100).reindex(ALGOS).fillna(0)
runtime_med    = (ok.groupby('algorithm')['runtime_s'].median() * 1000).reindex(ALGOS).fillna(0)
explored_mean  = ok.groupby('algorithm')['explored'].mean().reindex(ALGOS).fillna(0)
generated_mean = ok.groupby('algorithm')['generated'].mean().reindex(ALGOS).fillna(0)
depth_med      = ok.groupby('algorithm')['depth'].median().reindex(ALGOS).fillna(0)
cost_med       = ok.groupby('algorithm')['cost'].median().reindex(ALGOS).fillna(0)

# ── Style chung ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'axes.grid.axis': 'x',
    'grid.color': '#e8e8e8',
    'grid.linewidth': 0.6,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

# ── Hàm vẽ horizontal bar ────────────────────────────────────────────────────
def hbar(ax, values, algos, colors, xlabel, title, fmt=None):
    y = np.arange(len(algos))
    bars = ax.barh(y, values, color=colors, height=0.6, edgecolor='none')
    ax.set_yticks(y)
    ax.set_yticklabels(algos, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    ax.invert_yaxis()
    max_val = max(values) if max(values) > 0 else 1
    for bar, val in zip(bars, values):
        label = (fmt(val) if fmt else f'{val:.1f}')
        if val == 0:
            ax.text(max_val * 0.01, bar.get_y() + bar.get_height() / 2,
                    label, va='center', ha='left', fontsize=8, color='#888')
        else:
            ax.text(val + max_val * 0.01, bar.get_y() + bar.get_height() / 2,
                    label, va='center', fontsize=8, color='#444')
    ax.set_xlim(0, max_val * 1.15)


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 1: Tỉ lệ thành công + Runtime + Explored
# ════════════════════════════════════════════════════════════════════════════
fig1, axes = plt.subplots(1, 3, figsize=(18, 7))
fig1.suptitle(f'So sánh hiệu suất thuật toán tìm kiếm – Sort Water\n({TOTAL_TC} test cases)',
              fontsize=13, fontweight='bold', y=1.01)

hbar(axes[0], success_rate.values, ALGO_LABELS, COLORS,
     'Tỉ lệ thành công (%)', '1. Tỉ lệ thành công',
     fmt=lambda v: f'{v:.1f}%')
axes[0].axvline(x=100, color='#ccc', linewidth=0.8, linestyle='--')

hbar(axes[1], runtime_med.values, ALGO_LABELS, COLORS,
     'Thời gian (ms)', '2. Runtime trung vị (ca thành công)',
     fmt=lambda v: f'{v:.2f}ms')

hbar(axes[2], explored_mean.values, ALGO_LABELS, COLORS,
     'Số node', '3. Node explored (trung bình)',
     fmt=lambda v: f'{v:.0f}')

fig1.legend(handles=patches, loc='lower center', ncol=5,
            fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.04))
plt.tight_layout()
fig1.savefig(OUT_DIR / 'fig1_overview.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved fig1_overview.png")


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 2: Chất lượng lời giải – Cost & Depth
# ════════════════════════════════════════════════════════════════════════════
fig2, axes = plt.subplots(1, 2, figsize=(14, 7))
fig2.suptitle('Chất lượng lời giải (chỉ tính ca thành công)',
              fontsize=13, fontweight='bold')

hbar(axes[0], depth_med.values, ALGO_LABELS, COLORS,
     'Depth (trung vị)', '4. Độ sâu lời giải (depth)',
     fmt=lambda v: f'{v:.0f}')

hbar(axes[1], cost_med.values, ALGO_LABELS, COLORS,
     'Cost (trung vị)', '5. Chi phí lời giải (cost)',
     fmt=lambda v: f'{v:.0f}')

fig2.legend(handles=patches, loc='lower center', ncol=5,
            fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.04))
plt.tight_layout()
fig2.savefig(OUT_DIR / 'fig2_quality.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved fig2_quality.png")


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 3: Boxplot Runtime – phân phối & outlier
# ════════════════════════════════════════════════════════════════════════════
fig3, ax = plt.subplots(figsize=(14, 6))
fig3.suptitle('Phân phối Runtime theo thuật toán (ca thành công)',
              fontsize=13, fontweight='bold')

box_data = [ok[ok['algorithm'] == a]['runtime_s'].values * 1000 for a in ALGOS]
bp = ax.boxplot(box_data, vert=True, patch_artist=True,
                medianprops=dict(color='black', linewidth=1.5),
                flierprops=dict(marker='o', markersize=2, alpha=0.4),
                whiskerprops=dict(linewidth=0.8),
                capprops=dict(linewidth=0.8),
                boxprops=dict(linewidth=0.8))

for patch, color in zip(bp['boxes'], COLORS):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xticks(range(1, len(ALGOS) + 1))
ax.set_xticklabels(ALGO_LABELS, rotation=40, ha='right', fontsize=9)
ax.set_ylabel('Runtime (ms)', fontsize=10)
ax.set_title('6. Boxplot runtime – median, IQR và outlier', fontsize=11, fontweight='bold')
ax.grid(axis='y', color='#e8e8e8', linewidth=0.6)
ax.grid(axis='x', visible=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig3.legend(handles=patches, loc='upper right', fontsize=9, frameon=False)
plt.tight_layout()
fig3.savefig(OUT_DIR / 'fig3_boxplot_runtime.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved fig3_boxplot_runtime.png")


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 4: Scatter – Trade-off Runtime vs Cost
# ════════════════════════════════════════════════════════════════════════════
fig4, ax = plt.subplots(figsize=(10, 7))
fig4.suptitle('Trade-off: Thời gian vs Chi phí lời giải',
              fontsize=13, fontweight='bold')

for algo, color in zip(ALGOS, COLORS):
    sub = ok[ok['algorithm'] == algo]
    if len(sub) == 0:
        continue
    x = sub['runtime_s'].median() * 1000
    y = sub['cost'].median()
    ax.scatter(x, y, color=color, s=90, zorder=3,
               edgecolors='white', linewidth=0.8)
    ax.annotate(algo, (x, y), textcoords='offset points',
                xytext=(6, 3), fontsize=8, color='#333')

ax.set_xlabel('Runtime trung vị (ms)', fontsize=10)
ax.set_ylabel('Cost trung vị', fontsize=10)
ax.set_title('7. Góc trái-dưới = tốt nhất (nhanh + cost thấp)', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(color='#e8e8e8', linewidth=0.6)

ax.axvspan(0, runtime_med[runtime_med > 0].quantile(0.3),
           alpha=0.05, color='green')
fig4.legend(
    handles=patches + [mpatches.Patch(color='green', alpha=0.2, label='Vùng runtime tốt')],
    fontsize=8, frameon=False, loc='upper left'
)
plt.tight_layout()
fig4.savefig(OUT_DIR / 'fig4_tradeoff.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved fig4_tradeoff.png")


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 5: Heatmap – màu = normalized score, số = giá trị thật
# ════════════════════════════════════════════════════════════════════════════

# Cấu hình từng metric: (tên cột, series, invert, format_fn)
# invert=True → metric thấp = tốt (runtime, explored, cost, depth)
METRICS = [
    ('Thành công\n(%)',    success_rate,    False, lambda v: f'{v:.1f}%'),
    ('Runtime\n(ms)',      runtime_med,     True,  lambda v: f'{v:.2f}'),
    ('Explored\n(nodes)',  explored_mean,   True,  lambda v: f'{v:.0f}'),
    ('Generated\n(nodes)', generated_mean,  True,  lambda v: f'{v:.0f}'),
    ('Cost\n(median)',     cost_med,        True,  lambda v: f'{v:.0f}'),
    ('Depth\n(median)',    depth_med,       True,  lambda v: f'{v:.0f}'),
]

def normalize(series, invert):
    s = 1.0 / (series + 1e-9) if invert else series.astype(float)
    mn, mx = s.min(), s.max()
    if mx == mn:
        return pd.Series(np.ones(len(s)), index=s.index)
    return (s - mn) / (mx - mn)

n_algos, n_metrics = len(ALGOS), len(METRICS)
color_mat = np.zeros((n_algos, n_metrics))
raw_mat   = np.zeros((n_algos, n_metrics))

for j, (_, series, invert, _) in enumerate(METRICS):
    color_mat[:, j] = normalize(series, invert).values
    raw_mat[:, j]   = series.values

fig5, ax = plt.subplots(figsize=(14, 9))
fig5.patch.set_facecolor('white')
ax.set_facecolor('white')

im = ax.imshow(color_mat, aspect='auto', cmap='RdYlGn',
               vmin=0, vmax=1, interpolation='nearest')

# Đường kẻ ô
for x in np.arange(-0.5, n_metrics, 1):
    ax.axvline(x, color='white', linewidth=2)
for y in np.arange(-0.5, n_algos, 1):
    ax.axhline(y, color='white', linewidth=2)

# Số liệu THẬT bên trong ô (không phải normalized)
for i in range(n_algos):
    for j, (_, _, _, fmt) in enumerate(METRICS):
        nv  = color_mat[i, j]
        txt = fmt(raw_mat[i, j])
        text_color = 'white' if nv < 0.2 or nv > 0.88 else '#1a1a1a'
        ax.text(j, i, txt, ha='center', va='center',
                fontsize=9, color=text_color, fontweight='500')

# Ticks
col_labels = [m[0] for m in METRICS]
ax.set_xticks(range(n_metrics))
ax.set_xticklabels(col_labels, fontsize=10, fontweight='500')
ax.set_yticks(range(n_algos))
ax.set_yticklabels(ALGO_LABELS, fontsize=9.5)
ax.tick_params(left=False, bottom=False)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

# Màu nhãn thuật toán theo nhóm
for tick, algo in zip(ax.get_yticklabels(), ALGOS):
    tick.set_color(GROUP_COLOR[algo])
    tick.set_fontweight('bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.55, pad=0.02, aspect=25)
cbar.set_label('Normalized score\n(0 = kém nhất  →  1 = tốt nhất)', fontsize=9)
cbar.ax.tick_params(labelsize=8)
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
cbar.set_ticklabels(['0\n(kém)', '0.25', '0.5', '0.75', '1.0\n(tốt)'])

fig5.legend(handles=patches, loc='lower center', ncol=5,
            fontsize=9, frameon=False, bbox_to_anchor=(0.45, -0.02))

ax.set_title(
    f'Heatmap so sánh hiệu suất các thuật toán tìm kiếm – Sort Water\n'
    f'({TOTAL_TC} test cases  |  màu = normalized score  |  số = giá trị thực)',
    fontsize=11, fontweight='bold', pad=14
)

plt.tight_layout()
fig5.savefig(OUT_DIR / 'fig5_heatmap.png', dpi=160, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Saved fig5_heatmap.png")

print(f"\n🎉 Hoàn thành! 5 biểu đồ đã lưu vào: {OUT_DIR.resolve()}")