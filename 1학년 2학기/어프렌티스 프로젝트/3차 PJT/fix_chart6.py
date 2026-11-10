# -*- coding: utf-8 -*-
"""
fix_chart6.py
Fixes text clipping in create_chart_slide6_root_cause()
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

C_WHITE = "#FFFFFF"
C_TEXT = "#0F172A"
C_SUBTEXT = "#475569"
C_GRID = "#E2E8F0"
C_GREEN = "#059669"
C_GREEN_LIGHT = "#ECFDF5"

plt.rcParams['font.sans-serif'] = ['Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_chart_slide6_root_cause():
    fig, ax = plt.subplots(figsize=(5.6, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_WHITE)
    ax.grid(True, axis='x', linestyle=':', alpha=0.5, color=C_GRID)

    # Top Suptitle
    fig.suptitle("결함 원인 센서 역추적 (Root Cause Attribution)",
                 fontsize=11.5, fontweight='bold', color=C_TEXT, y=0.98)

    sensors = [
        "기타 센서 4종 (합산)",
        "Temperature (온도)",
        "Internal Pressure (내부 압력)",
        "Motor Vibration (모터 진동)",
        "Volume Flow Rate (유량)"
    ]
    contributions = [1.8, 3.2, 15.3, 31.2, 48.5]
    colors = ["#CBD5E1", "#94A3B8", "#38BDF8", "#34D399", C_GREEN]

    y_pos = np.arange(len(sensors))
    bars = ax.barh(y_pos, contributions, color=colors, height=0.55, edgecolor=C_TEXT, linewidth=0.5)

    # Value labels to the right of each bar
    for bar, val in zip(bars, contributions):
        w = bar.get_width()
        ax.text(w + 1.2, bar.get_y() + bar.get_height() / 2.0, f"{val:.1f}%",
                va='center', ha='left', fontsize=7.5, fontweight='bold', color=C_TEXT)

    # Dedicated Explanation Card in the EMPTY RIGHT HALF (Anchored safely on the right)
    # Using ha='right' at x=0.97 prevents any overflow past the right boundary
    card_text = (
        "■ 상위 3개 센서 기여도 95.0% 독점\n\n"
        "• 유체 밸브 폐쇄 및 모터 진동 즉시 특정\n"
        "• 단순 감지 넘어 '정비 타깃' 1초 내 식별\n"
        "• 불필요한 전수 분해 방지 (정비 비용 절감)\n"
        "• 엣지 경량화 연계 실시간 2단계 배포 완성"
    )
    ax.text(0.97, 0.42, card_text, transform=ax.transAxes,
            ha='right', va='center', fontsize=7.1, color="#065F46", linespacing=1.35,
            bbox=dict(facecolor=C_GREEN_LIGHT, edgecolor="#10B981", boxstyle='round,pad=0.45', linewidth=1.2))

    ax.set_xlabel("결함 기여도 비율 (% Contribution)", fontsize=8.0, fontweight='bold', color=C_TEXT)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sensors, fontsize=8.0, fontweight='bold', color=C_TEXT)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.tick_params(axis='both', labelsize=7.5, colors=C_SUBTEXT)

    plt.subplots_adjust(top=0.90, bottom=0.12, left=0.33, right=0.96)
    return fig

if __name__ == "__main__":
    out_dir = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
    fig = create_chart_slide6_root_cause()
    test_path = os.path.join(out_dir, "test_chart6_fixed.png")
    fig.savefig(test_path, dpi=300, facecolor=C_WHITE)
    plt.close(fig)
    print("Successfully generated:", test_path)
