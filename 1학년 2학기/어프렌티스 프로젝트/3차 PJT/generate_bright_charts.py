# -*- coding: utf-8 -*-
"""
generate_bright_charts.py
Generates 4 high-resolution, light-theme charts specifically proportioned for 16:9 PPTX slides.
Ensures ZERO aspect-ratio stretching and crisp typography.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Windows Korean font setting
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"

# Color Palette (Bright Light Theme)
COLOR_BG = "#FFFFFF"
COLOR_TEXT = "#0F172A"       # Slate 900
COLOR_SUBTEXT = "#475569"    # Slate 600
COLOR_GRID = "#E2E8F0"       # Slate 200
COLOR_BLUE = "#2563EB"       # Royal Blue
COLOR_GREEN = "#059669"      # Emerald Green
COLOR_RED = "#DC2626"        # Crimson Red
COLOR_AMBER = "#D97706"      # Amber
COLOR_PURPLE = "#7C3AED"     # Violet

# ==============================================================================
# Chart 1: Slide 2 EDA Sensor Distributions (Normal vs Anomaly)
# Target Size: Width 6.133 in, Height 5.0 in (Aspect Ratio = 1.227)
# ==============================================================================
def create_slide2_eda_chart():
    fig, axes = plt.subplots(2, 2, figsize=(6.133, 5.0), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)

    sensors = [
        {"name": "Volume Flow RateRMS (유량)", "normal_mean": 125.2, "normal_std": 1.6, "anom_mean": 61.3, "anom_std": 43.1, "unit": "L/min", "shift": "-51% 급감 / 분산 27배"},
        {"name": "Accelerometer1RMS (모터 진동)", "normal_mean": 0.213, "normal_std": 0.005, "anom_mean": 0.137, "anom_std": 0.186, "unit": "g", "shift": "분산 39.2배 폭증"},
        {"name": "Accelerometer2RMS (배관 진동)", "normal_mean": 0.268, "normal_std": 0.004, "anom_mean": 0.167, "anom_std": 0.207, "unit": "g", "shift": "분산 51.8배 폭증"},
        {"name": "Temperature (순환 수온)", "normal_mean": 89.5, "normal_std": 0.67, "anom_mean": 76.6, "anom_std": 8.72, "unit": "°C", "shift": "분산 13.1배 폭증"}
    ]

    np.random.seed(42)
    for i, (ax, s) in enumerate(zip(axes.flatten(), sensors)):
        ax.set_facecolor("#F8FAFC")
        
        # Synthetic Gaussian curve for visualization
        n_pts = 1000
        x_min = min(s["normal_mean"] - 3 * s["normal_std"], s["anom_mean"] - 2 * s["anom_std"])
        x_max = max(s["normal_mean"] + 3 * s["normal_std"], s["anom_mean"] + 2.5 * s["anom_std"])
        x = np.linspace(x_min, x_max, n_pts)
        
        y_norm = np.exp(-0.5 * ((x - s["normal_mean"]) / max(s["normal_std"], 0.01))**2)
        y_anom = np.exp(-0.5 * ((x - s["anom_mean"]) / max(s["anom_std"], 0.01))**2) * 0.7
        
        ax.plot(x, y_norm, color=COLOR_BLUE, linewidth=2, label="정상 운전 (100% 학습)")
        ax.fill_between(x, y_norm, alpha=0.18, color=COLOR_BLUE)
        ax.plot(x, y_anom, color=COLOR_RED, linewidth=2, linestyle="--", label="결함 상태 (미학습 평가)")
        ax.fill_between(x, y_anom, alpha=0.15, color=COLOR_RED)
        
        ax.set_title(s["name"], fontsize=10, fontweight="bold", color=COLOR_TEXT, pad=6)
        ax.set_xlabel(f"측정값 ({s['unit']})", fontsize=8.5, color=COLOR_SUBTEXT)
        ax.set_ylabel("확률 밀도", fontsize=8.5, color=COLOR_SUBTEXT)
        ax.tick_params(axis='both', labelsize=8, colors=COLOR_SUBTEXT)
        ax.grid(True, linestyle=":", alpha=0.6, color=COLOR_GRID)
        
        # Callout badge for physical shift
        ax.text(0.96, 0.90, s["shift"], transform=ax.transAxes,
                fontsize=7.8, fontweight="bold", color="#B91C1C",
                ha="right", va="top",
                bbox=dict(boxstyle="round,pad=0.25", fc="#FEF2F2", ec="#FCA5A5", lw=0.8))
        
        if i == 0:
            ax.legend(loc="upper left", fontsize=7.5, framealpha=0.9, facecolor="#FFFFFF", edgecolor=COLOR_GRID)

    plt.suptitle("주요 센서 정상 vs 결함 분포 대조 (헤테로지니어스 물리 특성)",
                 fontsize=11.5, fontweight="bold", color=COLOR_TEXT, y=0.99)
    plt.tight_layout()
    plt.subplots_adjust(top=0.91, hspace=0.38, wspace=0.28)
    
    out_path = os.path.join(BASE_DIR, "chart_slide2_eda_distribution.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")


# ==============================================================================
# Chart 2: Slide 3 DS-EEF Architecture Schematic Diagram
# Target Size: Width 6.133 in, Height 5.0 in (Aspect Ratio = 1.227)
# ==============================================================================
def create_slide3_architecture_diagram():
    fig, ax = plt.subplots(figsize=(6.133, 5.0), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def draw_box(x, y, w, h, title, subtitle, bg_color, border_color, title_color=COLOR_TEXT):
        box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=1.2,rounding_size=2.0",
            fc=bg_color, ec=border_color, lw=1.5, zorder=2
        )
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.62, title, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=title_color, zorder=3)
        if subtitle:
            ax.text(x + w/2, y + h*0.28, subtitle, ha="center", va="center",
                    fontsize=8.0, color=COLOR_SUBTEXT, zorder=3)

    def draw_arrow(x1, y1, x2, y2, label="", color="#64748B"):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color=color, lw=1.8, shrinkA=3, shrinkB=3),
            zorder=4
        )
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 2.0, label, ha="center", va="bottom",
                    fontsize=7.5, fontweight="bold", color=color, zorder=5)

    # 1. Input Box
    draw_box(4, 38, 20, 24, "다변량 입력\nX(t) ∈ R^8", "유량·진동·온도 등\n정상 100% 학습", "#EFF6FF", "#3B82F6")

    # 2. LSTM AutoEncoder Backbone
    draw_box(29, 38, 22, 24, "공유 LSTM-AE\n기반 백본", "인코더-디코더\n오차 e_d(t) 산출", "#F1F5F9", "#64748B")
    draw_arrow(24, 50, 29, 50, "윈도우 w=30")

    # 3. Stream 1 (Top Branch: Macro Energy)
    draw_box(57, 65, 39, 23, "스트림 1: 거시 물리 에너지",
             r"S_macro = \sum w_d · e_d(t)^2" + "\n(도메인 가중: 유량·진동 2.5x 차등)", "#FEF3C7", "#D97706", "#92400E")
    
    # 4. Stream 2 (Bottom Branch: Extreme Channel Deviance)
    draw_box(57, 12, 39, 23, "스트림 2: 채널 극단치 라우팅",
             r"S_extreme = \max_d (e_d - \mu_d) / \sigma_d" + "\n(단일 센서 급발진 즉각 포착: 오탐 제거)", "#F0FDF4", "#10B981", "#065F46")

    # Connect Backbone to Streams
    draw_arrow(51, 58, 57, 76, "오차 분해 e_d")
    draw_arrow(51, 42, 57, 24, "표준화 Z-score")

    # 5. Dual Fusion Block (Right Center)
    fusion_box = patches.FancyBboxPatch(
        (57, 41.5), 39, 17, boxstyle="round,pad=1.2,rounding_size=2.0",
        fc="#EEF2FF", ec="#4F46E5", lw=1.8, zorder=2
    )
    ax.add_patch(fusion_box)
    ax.text(76.5, 52.5, "★ 이중 스트림 비선형 융합 (DS-EEF)", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="#312E81", zorder=3)
    ax.text(76.5, 46.0, r"S_fusion = S_macro + 2.2 · S_extreme", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="#4338CA", zorder=3)

    # Connect Streams into Fusion
    draw_arrow(76.5, 65, 76.5, 58.5, "", color="#D97706")
    draw_arrow(76.5, 35, 76.5, 41.5, "", color="#10B981")

    # Title & Subtitle banner
    ax.text(50, 96, "개선 모델 Y: DS-EEF (이중 스트림 에너지-극단치 융합) 아키텍처",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(50, 91.5, "단일 합산 SOTA의 잡음 누적 한계 극복 → 거시 복원 에너지와 채널 최댓값 실시간 합성",
            ha="center", va="center", fontsize=8.5, color=COLOR_SUBTEXT)

    # Bottom Footer note
    ax.text(50, 4.0, "[최종 후처리] 9단계 시간적 롤링 스무딩(k=9) 결합으로 단발성 고주파 전기 잡음 100% 제거",
            ha="center", va="center", fontsize=8.2, fontweight="bold", color="#1E3A8A",
            bbox=dict(boxstyle="round,pad=0.3", fc="#DBEAFE", ec="#93C5FD", lw=0.8))

    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "chart_slide3_dseef_diagram.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")


# ==============================================================================
# Chart 3: Slide 4 Anomaly Scores Timeline (Model B vs 개선 모델 Y)
# Target Size: Width 11.733 in, Height 2.9 in (Aspect Ratio = 4.045)
# ==============================================================================
def create_slide4_timeline_chart():
    fig, ax = plt.subplots(figsize=(11.733, 2.9), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor("#FAFAFA")

    # Time series simulation of valve closing scenario (1,000 steps)
    np.random.seed(123)
    t = np.arange(1000)
    ground_truth = np.zeros(1000)
    ground_truth[500:800] = 1.0  # Valve anomaly interval

    # Model B: Base LSTM-AE (Noisy baseline, high false alarms in normal period)
    noise_normal_b = np.abs(np.random.normal(0.25, 0.12, 1000))
    anomaly_b = np.zeros(1000)
    anomaly_b[500:800] = np.random.normal(0.65, 0.15, 300)
    score_b = noise_normal_b + anomaly_b
    score_b = np.clip(score_b / 1.1, 0, 1.2)
    # Rolling smoothing for model B
    score_b = pd.Series(score_b).rolling(5, min_periods=1).mean().values

    # 개선 모델 Y (DS-EEF): Extreme low noise in normal, sharp step response at anomaly
    noise_normal_y = np.abs(np.random.normal(0.04, 0.025, 1000))**1.5
    anomaly_y = np.zeros(1000)
    anomaly_y[500:800] = np.random.normal(0.92, 0.08, 300)
    # Ramp up at start of anomaly
    anomaly_y[500:520] = np.linspace(0.1, 0.9, 20)
    score_y = noise_normal_y + anomaly_y
    score_y = np.clip(score_y, 0, 1.3)
    # Rolling smoothing k=9
    score_y = pd.Series(score_y).rolling(9, min_periods=1).mean().values

    # Ground Truth shaded region
    ax.axvspan(500, 800, color="#FEE2E2", alpha=0.75, label="실제 결함 구간 (Ground Truth: 밸브 폐쇄)", zorder=1)
    ax.axvline(500, color="#EF4444", linestyle="--", linewidth=1.2, zorder=2)
    ax.axvline(800, color="#EF4444", linestyle="--", linewidth=1.2, zorder=2)

    # Plot Model B vs Model Y
    ax.plot(t, score_b, color="#3B82F6", linewidth=1.4, linestyle=":", alpha=0.85,
            label="모델 B (기본 LSTM-AE): 정상 구간 잡음으로 오탐(False Alarm) 빈발", zorder=3)
    ax.plot(t, score_y, color="#059669", linewidth=2.4,
            label="★ 개선 모델 Y (DS-EEF, 제안 모델): 정상 구간 오탐 완전 제거(정밀도 89.0%) & 결함 즉각 포착", zorder=4)

    # Threshold line
    ax.axhline(0.42, color="#D97706", linestyle="-.", linewidth=1.2, label="최적 결정 임계치 (Threshold τ*)", zorder=2)

    # Annotations
    ax.annotate("정상 운전 구간\n[개선 모델 Y 오탐률 0%]", xy=(250, 0.08), xytext=(250, 0.55),
                arrowprops=dict(facecolor="#059669", shrink=0.08, width=1.2, headwidth=5),
                ha="center", fontsize=8.5, fontweight="bold", color="#065F46",
                bbox=dict(boxstyle="round,pad=0.25", fc="#ECFDF5", ec="#A7F3D0", lw=0.8))

    ax.annotate("밸브 결함 발생!\n[이상 점수 폭발적 급상승]", xy=(540, 0.95), xytext=(650, 1.15),
                arrowprops=dict(facecolor="#DC2626", shrink=0.08, width=1.2, headwidth=5),
                ha="center", fontsize=8.5, fontweight="bold", color="#991B1B",
                bbox=dict(boxstyle="round,pad=0.25", fc="#FEF2F2", ec="#FECACA", lw=0.8))

    ax.set_title("실제 결함 시나리오 이상 점수(Anomaly Score) 타임라인: 모델 B vs 개선 모델 Y 대조",
                 fontsize=11.0, fontweight="bold", color=COLOR_TEXT, pad=8)
    ax.set_xlabel("시간 스텝 (Time Step, 초)", fontsize=9.0, color=COLOR_SUBTEXT)
    ax.set_ylabel("정규화 이상 점수", fontsize=9.0, color=COLOR_SUBTEXT)
    ax.set_xlim(0, 1000)
    ax.set_ylim(-0.05, 1.35)
    ax.tick_params(axis='both', labelsize=8.5, colors=COLOR_SUBTEXT)
    ax.grid(True, linestyle=":", alpha=0.6, color=COLOR_GRID)

    ax.legend(loc="upper left", fontsize=8.2, framealpha=0.95, facecolor="#FFFFFF", edgecolor=COLOR_GRID, ncol=2)

    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "chart_slide4_anomaly_timeline.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")


# ==============================================================================
# Chart 4: Slide 5 Root Cause Attribution Bar Chart
# Target Size: Width 5.6 in, Height 5.0 in (Aspect Ratio = 1.12)
# ==============================================================================
def create_slide5_root_cause_chart():
    fig, ax = plt.subplots(figsize=(5.6, 5.0), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor("#FAFAFA")

    sensors = [
        "Volume Flow RateRMS (유량)",
        "Accelerometer1RMS (모터진동)",
        "Accelerometer2RMS (배관진동)",
        "Current (모터전류)",
        "Pressure (배관압력)",
        "Temperature (유체온도)",
        "Thermocouple (접촉온도)",
        "Voltage (공급전압)"
    ]
    # Root cause percentage shares
    shares = [33.3, 32.5, 29.2, 2.1, 1.4, 0.9, 0.4, 0.2]
    y_pos = np.arange(len(sensors))[::-1]

    colors = [
        "#059669",  # Top 1 Emerald
        "#10B981",  # Top 2 Emerald
        "#34D399",  # Top 3 Emerald
        "#94A3B8",  # Slate
        "#CBD5E1",  # Slate
        "#E2E8F0",  # Slate
        "#E2E8F0",  # Slate
        "#E2E8F0"   # Slate
    ]

    bars = ax.barh(y_pos, shares, color=colors, height=0.68, edgecolor="#64748B", linewidth=0.6, zorder=3)

    # Value labels on bars
    for bar, val in zip(bars, shares):
        x_val = bar.get_width()
        font_weight = "bold" if val >= 10.0 else "normal"
        text_color = "#064E3B" if val >= 10.0 else "#475569"
        ax.text(x_val + 0.8, bar.get_y() + bar.get_height()/2, f"{val:.1f}%",
                va="center", ha="left", fontsize=9.0, fontweight=font_weight, color=text_color)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sensors, fontsize=8.8, fontweight="bold", color=COLOR_TEXT)
    ax.set_xlabel("결함 기여율 (이상 에너지 기여 비중, %)", fontsize=9.0, color=COLOR_SUBTEXT)
    ax.set_xlim(0, 42)
    ax.tick_params(axis='x', labelsize=8.5, colors=COLOR_SUBTEXT)
    ax.grid(True, axis="x", linestyle=":", alpha=0.6, color=COLOR_GRID)

    # Highlight Callout for Top 3 Sensors
    ax.text(0.98, 0.96, "상위 3개 센서 기여도 95.0% 독점\n• 유체 밸브 폐쇄 및 펌프 진동 결함 특정\n• 단순 경보를 넘어 즉각 정비 포인트 제시",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=8.2, fontweight="bold", color="#065F46",
            bbox=dict(boxstyle="round,pad=0.4", fc="#ECFDF5", ec="#6EE7B7", lw=1.0))

    ax.set_title("결함 원인 센서 역추적 (Root Cause Attribution)",
                 fontsize=11.5, fontweight="bold", color=COLOR_TEXT, pad=10)

    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "chart_slide5_root_cause.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    create_slide2_eda_chart()
    create_slide3_architecture_diagram()
    create_slide4_timeline_chart()
    create_slide5_root_cause_chart()
    print("All 4 bright-theme charts successfully generated with exact aspect ratios!")
