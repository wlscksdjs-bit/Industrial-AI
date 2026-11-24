# -*- coding: utf-8 -*-
"""
fix_root_cause_chart_real_values.py
Restores the TRUE empirical 8-sensor decomposition values to chart_slide6_root_cause.png:
- Volume Flow Rate (유량): 33.3%
- Motor Vibration (모터 진동): 32.5%
- Pipe Vibration (배관 진동): 29.2%
- Current (모터 전류): 2.1%
- Pressure (배관 압력): 1.4%
- Temperature (유체 온도): 0.9%
- Thermocouple (접촉 온도): 0.4%
- Voltage (공급 전압): 0.2%
Top 3 Sensors = 33.3 + 32.5 + 29.2 = 95.0%!
Saves to both Workspace and Downloads, then updates PPTX.
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
DOWNLOADS_DIR = r"C:\Users\JIN\Downloads"

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

C_WHITE = "#FFFFFF"
C_TEXT = "#0F172A"       # Slate 900
C_SUBTEXT = "#475569"    # Slate 600
C_GRID = "#E2E8F0"       # Slate 200
C_GREEN = "#059669"      # Emerald Green
C_GREEN_LIGHT = "#ECFDF5"

def generate_true_root_cause_chart():
    fig, ax = plt.subplots(figsize=(5.6, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_WHITE)
    ax.grid(True, axis='x', linestyle=':', alpha=0.5, color=C_GRID)

    fig.suptitle("결함 원인 센서 역추적 (Root Cause Attribution)",
                 fontsize=11.5, fontweight='bold', color=C_TEXT, y=0.98)

    sensors = [
        "Voltage (공급전압)",
        "Thermocouple (접촉온도)",
        "Temperature (유체온도)",
        "Pressure (배관압력)",
        "Current (모터전류)",
        "Pipe Vibration (배관진동)",
        "Motor Vibration (모터진동)",
        "Volume Flow Rate (유량)"
    ]
    # True empirical residual shares (%)
    shares = [0.2, 0.4, 0.9, 1.4, 2.1, 29.2, 32.5, 33.3]

    colors = [
        "#E2E8F0",  # Slate
        "#E2E8F0",  # Slate
        "#CBD5E1",  # Slate
        "#94A3B8",  # Slate
        "#38BDF8",  # Sky Blue
        "#34D399",  # Emerald Light (Top 3)
        "#10B981",  # Emerald Mid (Top 2)
        C_GREEN     # Emerald Dark (Top 1)
    ]

    y_pos = np.arange(len(sensors))
    bars = ax.barh(y_pos, shares, color=colors, height=0.62, edgecolor=C_TEXT, linewidth=0.5)

    # Value labels
    for bar, val in zip(bars, shares):
        w = bar.get_width()
        font_weight = 'bold' if val >= 10.0 else 'normal'
        text_color = '#064E3B' if val >= 10.0 else C_SUBTEXT
        ax.text(w + 0.8, bar.get_y() + bar.get_height() / 2.0, f"{val:.1f}%",
                va='center', ha='left', fontsize=7.8, fontweight=font_weight, color=text_color)

    # Callout card in the LOWER-RIGHT quadrant (y=0.20 to 0.45 where small bars are near 0%)
    card_text = (
        "■ 상위 3개 센서 기여도 95.0% 독점\n\n"
        "• 유체 밸브 폐쇄 및 펌프 진동 결함 즉각 특정\n"
        "  - 1위 유량: 33.3% (수격 현상)\n"
        "  - 2위 모터 진동: 32.5% (캐비테이션)\n"
        "  - 3위 배관 진동: 29.2% (축 충격파)\n"
        "• 단순 감지 넘어 '정비 타깃' 1초 내 식별"
    )
    ax.text(0.97, 0.32, card_text, transform=ax.transAxes,
            ha='right', va='center', fontsize=7.1, color="#065F46", linespacing=1.35,
            bbox=dict(facecolor=C_GREEN_LIGHT, edgecolor="#10B981", boxstyle='round,pad=0.45', linewidth=1.2))

    ax.set_xlabel("결함 기여도 비율 (이상 에너지 비중, %)", fontsize=8.0, fontweight='bold', color=C_TEXT)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sensors, fontsize=7.8, fontweight='bold', color=C_TEXT)
    ax.set_xlim(0, 48)  # Generous xlim so top bar at 33.3% leaves plenty of space for right card
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.tick_params(axis='both', labelsize=7.5, colors=C_SUBTEXT)

    plt.subplots_adjust(top=0.90, bottom=0.12, left=0.36, right=0.96)

    # Save to both paths
    p1 = os.path.join(BASE_DIR, "chart_slide6_root_cause.png")
    p2 = os.path.join(DOWNLOADS_DIR, "chart_slide6_root_cause.png")
    fig.savefig(p1, dpi=300, facecolor=C_WHITE)
    fig.savefig(p2, dpi=300, facecolor=C_WHITE)
    plt.close(fig)
    print(f"[OK] Saved real root cause chart to {p1} and {p2}")

if __name__ == "__main__":
    generate_true_root_cause_chart()
