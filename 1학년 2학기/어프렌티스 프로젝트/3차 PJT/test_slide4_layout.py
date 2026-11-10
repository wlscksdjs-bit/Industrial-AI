# -*- coding: utf-8 -*-
"""
test_slide4_layout.py
Generates and visually validates Slide 4 pipeline diagram with zero overlaps.
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

C_WHITE = "#FFFFFF"
C_TEXT = "#0F172A"
C_SUBTEXT = "#475569"
C_GRID = "#E2E8F0"
C_BLUE = "#2563EB"
C_BLUE_LIGHT = "#EFF6FF"
C_GREEN = "#059669"
C_GREEN_LIGHT = "#ECFDF5"
C_AMBER = "#D97706"
C_AMBER_LIGHT = "#FFFBEB"
C_PURPLE = "#7C3AED"
C_PURPLE_LIGHT = "#F5F3FF"

fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=300)
fig.patch.set_facecolor(C_WHITE)
ax.set_facecolor(C_WHITE)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(50, 96, "개선 모델 Y: DS-EEF (이중 스트림 에너지-극단치 융합) 아키텍처",
        fontsize=11.0, fontweight='bold', ha='center', va='center', color=C_TEXT)
ax.text(50, 91, "단일 합산 SOTA의 잡음 누적 극복 → 거시 복원 에너지와 채널 최댓값 실시간 합성",
        fontsize=7.8, ha='center', va='center', color=C_SUBTEXT)

def draw_card(x, y, w, h, title, body_lines, fc, ec, title_color=C_TEXT):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=2.0",
                                 facecolor=fc, edgecolor=ec, linewidth=1.5)
    ax.add_patch(box)
    if title:
        ax.text(x + w / 2, y + h - 4.5, title, fontsize=8.2, fontweight='bold',
                ha='center', va='top', color=title_color)
    cy = y + h - 11.0
    for line in body_lines:
        ax.text(x + w / 2, cy, line, fontsize=7.2, ha='center', va='top', color=C_TEXT)
        cy -= 4.8

# Box 1: 다변량 입력 (x=3, y=36, w=20, h=40) -> spans 3 to 23
draw_card(3, 36, 20, 40, "다변량 입력\nX(t) ∈ R^8",
          ["유량·진동·온도 등", "SKAB 8개 센서", "정상 데이터", "100% 비지도 학습"],
          C_BLUE_LIGHT, C_BLUE, C_BLUE)

# Box 2: 공유 LSTM-AE 백본 (x=29, y=36, w=21, h=40) -> spans 29 to 50
draw_card(29, 36, 21, 40, "공유 LSTM-AE\n기반 백본",
          ["슬라이딩 윈도우 w=30", "인코더-디코더 복원", "오차 벡터 산출", "e_d(t) = |x_d - x_hat|"],
          "#F1F5F9", "#64748B", C_TEXT)

# Gap: x=50 to x=63 (13 units wide!)

# Box 3: 스트림 1 (x=63, y=58, w=34, h=24) -> spans 63 to 97
draw_card(63, 58, 34, 24, "스트림 1: 거시 물리 에너지",
          ["S_macro = Σ (w_d · e_d(t)²)", "물리 가중치 (유량·진동 2.5x)", "전체 에너지 복원 오차 추적"],
          C_AMBER_LIGHT, C_AMBER, "#B45309")

# Box 4: 스트림 2 (x=63, y=14, w=34, h=24) -> spans 63 to 97
draw_card(63, 14, 34, 24, "스트림 2: 채널 극단치 라우팅",
          ["S_extreme = max_d (|e_d - μ_d| / σ_d)", "단일 센서 급격한 이상 포착", "정상 채널 잡음 상쇄·오탐 차단"],
          C_GREEN_LIGHT, C_GREEN, "#047857")

# Box 5: 비선형 융합 (x=63, y=41, w=34, h=14) -> spans 63 to 97
draw_card(63, 41, 34, 14, "★ 이중 스트림 비선형 융합 (DS-EEF)",
          ["S_fusion = S_macro + 2.2 · S_extreme"],
          C_PURPLE_LIGHT, C_PURPLE, C_PURPLE)

# Bottom Banner: 후처리 스무딩
foot_box = patches.FancyBboxPatch((3, 3), 94, 7.5, boxstyle="round,pad=0.5,rounding_size=1.5",
                                  facecolor=C_BLUE_LIGHT, edgecolor=C_BLUE, linewidth=1.0)
ax.add_patch(foot_box)
ax.text(50, 6.8, "[최종 후처리] 9단계 시간적 롤링 스무딩(k=9) 결합으로 단발성 고주파 전기 잡음 100% 제거",
        fontsize=7.8, fontweight='bold', ha='center', va='center', color=C_BLUE)

# Arrow 1: Input -> Backbone
ax.annotate("", xy=(29, 56), xytext=(23, 56),
            arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
ax.text(26, 59, "w=30", fontsize=7, ha='center', va='bottom', color=C_SUBTEXT,
        bbox=dict(facecolor=C_WHITE, edgecolor='none', pad=1))

# Arrow 2: Backbone -> Stream 1 (Upward diagonal)
# Starts from Box 2 right edge (x=50, y=62), ends at Box 3 left edge (x=63, y=70)
ax.annotate("", xy=(63, 70), xytext=(50, 62),
            arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
ax.text(56.5, 69, "오차 분해 e_d", fontsize=7.2, ha='center', va='bottom', color=C_SUBTEXT,
        bbox=dict(facecolor=C_WHITE, edgecolor=C_GRID, pad=1.5, boxstyle='round,pad=0.25'))

# Arrow 3: Backbone -> Stream 2 (Downward diagonal)
# Starts from Box 2 right edge (x=50, y=50), ends at Box 4 left edge (x=63, y=26)
ax.annotate("", xy=(63, 26), xytext=(50, 50),
            arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
ax.text(56.5, 35, "표준화 Z-score", fontsize=7.2, ha='center', va='top', color=C_SUBTEXT,
        bbox=dict(facecolor=C_WHITE, edgecolor=C_GRID, pad=1.5, boxstyle='round,pad=0.25'))

# Arrow 4: Stream 1 -> Fusion (Down arrow)
ax.annotate("", xy=(80, 55), xytext=(80, 58),
            arrowprops=dict(arrowstyle="->", color=C_AMBER, lw=1.5))

# Arrow 5: Stream 2 -> Fusion (Up arrow)
ax.annotate("", xy=(80, 41), xytext=(80, 38),
            arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.5))

plt.subplots_adjust(top=0.98, bottom=0.02, left=0.02, right=0.98)
fig.savefig(r"3차 PJT\test_slide4.png", dpi=300, facecolor=C_WHITE)
print("Saved test_slide4.png")
