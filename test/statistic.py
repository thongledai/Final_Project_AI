import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
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

# ── Thứ tự thuật toán cố định ────────────────────────────────────────────────
ALGOS = ['BFS','DFS','UCS','IDS','Greedy','A*','IDA*',
         'Hill_Simple','Hill_Steepest','Hill_Stochastic',
         'Hill_RandomRestart','SimulatedAnnealing','LocalBeam',
         'AndOrGraph','PartiallyObservable',
         'Minimax','AlphaBeta','Expectimax',
         'Backtracking','ForwardChecking']

# ── Màu theo nhóm thuật toán ─────────────────────────────────────────────────
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

# ── Style chung ──────────────────────────────────────────────────────────────
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

def hbar(ax, values, algos, colors, xlabel, title, fmt=None):
    y = np.arange(len(algos))
    bars = ax.barh(y, values, color=colors, height=0.6, edgecolor='none')
    ax.set_yticks(y)
    ax.set_yticklabels(algos, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    ax.invert_yaxis()
    for bar, val in zip(bars, values):
        if val == 0:
            ax.text(0.5, bar.get_y() + bar.get_height()/2,
                    '0' if fmt is None else fmt(0),
                    va='center', ha='left', fontsize=8, color='#888')
        else:
            ax.text(val + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                    (fmt(val) if fmt else f'{val:.1f}'),
                    va='center', fontsize=8, color='#444')
    ax.set_xlim(0, max(values) * 1.15 if max(values) > 0 else 1)

# ════════════════════════════════════════════════════════════════════════════
# FIGURE 1: Tỉ lệ thành công + Runtime + Explored
# ════════════════════════════════════════════════════════════════════════════
fig1, axes = plt.subplots(1, 3, figsize=(18, 7))
fig1.suptitle('So sánh hiệu suất thuật toán tìm kiếm – Sort Water\n'
              f'({TOTAL_TC} test cases)', fontsize=13, fontweight='bold', y=1.01)

# 1a. Tỉ lệ thành công
success_rate = (df.groupby('algorithm')['success'].sum() / TOTAL_TC * 100).reindex(ALGOS).fillna(0)
hbar(axes[0], success_rate.values, ALGOS, COLORS, 'Tỉ lệ thành công (%)',
     '1. Tỉ lệ thành công', fmt=lambda v: f'{v:.0f}%')
axes[0].axvline(x=100, color='#ccc', linewidth=0.8, linestyle='--')

# 1b. Runtime median (ms) – chỉ ca thành công
runtime_med = (ok.groupby('algorithm')['runtime_s'].median() * 1000).reindex(ALGOS).fillna(0)
hbar(axes[1], runtime_med.values, ALGOS, COLORS, 'Thời gian (ms)',
     '2. Runtime trung vị (ca thành công)', fmt=lambda v: f'{v:.2f}ms')

# 1c. Node explored trung bình
explored_mean = ok.groupby('algorithm')['explored'].mean().reindex(ALGOS).fillna(0)
hbar(axes[2], explored_mean.values, ALGOS, COLORS, 'Số node',
     '3. Node explored (trung bình)', fmt=lambda v: f'{v:.0f}')

# Legend nhóm
patches = [
    mpatches.Patch(color='#2a78d6', label='Uninformed'),
    mpatches.Patch(color='#1baf7a', label='Informed / Constraint'),
    mpatches.Patch(color='#eda100', label='Local search'),
    mpatches.Patch(color='#e34948', label='Complex environment'),
    mpatches.Patch(color='#4a3aa7', label='Adversarial'),
]
fig1.legend(handles=patches, loc='lower center', ncol=5,
            fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.04))

plt.tight_layout()
fig1.savefig(OUT_DIR / 'fig1_overview.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig1")

# ════════════════════════════════════════════════════════════════════════════
# FIGURE 2: Chất lượng lời giải – Cost & Depth
# ════════════════════════════════════════════════════════════════════════════
fig2, axes = plt.subplots(1, 2, figsize=(14, 7))
fig2.suptitle('Chất lượng lời giải (chỉ tính ca thành công)',
              fontsize=13, fontweight='bold')

depth_med = ok.groupby('algorithm')['depth'].median().reindex(ALGOS).fillna(0)
cost_med  = ok.groupby('algorithm')['cost'].median().reindex(ALGOS).fillna(0)

hbar(axes[0], depth_med.values, ALGOS, COLORS, 'Depth (trung vị)',
     '4. Độ sâu lời giải (depth)', fmt=lambda v: f'{v:.0f}')
hbar(axes[1], cost_med.values, ALGOS, COLORS, 'Cost (trung vị)',
     '5. Chi phí lời giải (cost)', fmt=lambda v: f'{v:.0f}')

fig2.legend(handles=patches, loc='lower center', ncol=5,
            fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.04))
plt.tight_layout()
fig2.savefig(OUT_DIR / 'fig2_quality.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig2")

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

ax.set_xticks(range(1, len(ALGOS)+1))
ax.set_xticklabels(ALGOS, rotation=40, ha='right', fontsize=9)
ax.set_ylabel('Runtime (ms)', fontsize=10)
ax.set_title('6. Boxplot runtime – thấy median, IQR và outlier', fontsize=11, fontweight='bold')
ax.grid(axis='y', color='#e8e8e8', linewidth=0.6)
ax.grid(axis='x', visible=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig3.legend(handles=patches, loc='upper right', fontsize=9, frameon=False)
plt.tight_layout()
fig3.savefig(OUT_DIR / 'fig3_boxplot_runtime.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig3")

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
    ax.scatter(x, y, color=color, s=80, zorder=3, edgecolors='white', linewidth=0.8)
    ax.annotate(algo, (x, y), textcoords='offset points',
                xytext=(5, 3), fontsize=8, color='#333')

ax.set_xlabel('Runtime trung vị (ms)', fontsize=10)
ax.set_ylabel('Cost trung vị', fontsize=10)
ax.set_title('7. Góc trái-dưới = tốt nhất (nhanh + cost thấp)', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(color='#e8e8e8', linewidth=0.6)

# Vùng "tốt nhất"
ax.axvspan(0, runtime_med[runtime_med > 0].quantile(0.3),
           alpha=0.05, color='green', label='Vùng runtime tốt')
ax.legend(handles=patches + [mpatches.Patch(color='green', alpha=0.2, label='Vùng runtime tốt')],
          fontsize=8, frameon=False, loc='upper left')

plt.tight_layout()
fig4.savefig(OUT_DIR / 'fig4_tradeoff.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig4")

# ════════════════════════════════════════════════════════════════════════════
# FIGURE 5: Heatmap – normalized score tổng hợp
# ════════════════════════════════════════════════════════════════════════════
fig5, ax = plt.subplots(figsize=(12, 7))
fig5.suptitle('Heatmap tổng hợp – Normalized score (cao = tốt hơn)',
              fontsize=13, fontweight='bold')

metrics = {
    'Thành công (%)': success_rate,
    'Runtime\n(thấp=tốt)': 1 / (runtime_med + 0.01),
    'Explored\n(thấp=tốt)': 1 / (explored_mean + 1),
    'Cost\n(thấp=tốt)': 1 / (cost_med + 0.01),
    'Depth\n(thấp=tốt)': 1 / (depth_med + 0.01),
}

# Normalize mỗi cột về [0,1]
heat_data = pd.DataFrame(metrics, index=ALGOS)
heat_norm = (heat_data - heat_data.min()) / (heat_data.max() - heat_data.min() + 1e-9)

im = ax.imshow(heat_norm.values, aspect='auto', cmap='RdYlGn', vmin=0, vmax=1)
ax.set_xticks(range(len(metrics)))
ax.set_xticklabels(list(metrics.keys()), fontsize=10)
ax.set_yticks(range(len(ALGOS)))
ax.set_yticklabels(ALGOS, fontsize=9)

for i in range(len(ALGOS)):
    for j in range(len(metrics)):
        val = heat_norm.values[i, j]
        ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                fontsize=8, color='black' if 0.3 < val < 0.8 else ('white' if val < 0.3 else 'black'))

plt.colorbar(im, ax=ax, shrink=0.8, label='Score (0=tệ nhất, 1=tốt nhất)')
ax.set_title('8. Nhìn tổng thể: màu xanh = tốt, đỏ = kém', fontsize=10)
plt.tight_layout()
fig5.savefig(OUT_DIR / 'fig5_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved fig5")

print(f"\n✅ Đã lưu 5 biểu đồ vào: {OUT_DIR.resolve()}")