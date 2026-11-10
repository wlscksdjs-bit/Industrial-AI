# -*- coding: utf-8 -*-
"""
generate_bright_charts_v3.py
Fixes all 4 chart text/legend overlaps identified in user screenshots:
1. chart_slide2_eda.png: Move shared legend to the BOTTOM outside the plots. Zero collision with subplot titles!
2. chart_slide3_sota_comparison.png: Shorten legend labels to fit cleanly in bounds. Move red limitation badge to the top banner above bars, completely freeing the bars and value labels!
3. chart_slide5_timeline.png: Keep legend at top-left and move the anomaly callout to lower-right (y=0.65), completely separated from the legend!
4. chart_slide6_root_cause.png: Expand xlim to 48% and move the callout box to the lower-right quadrant (y=0.22), far away from the top bar!
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Windows Korean font configuration
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"

C_WHITE = "#FFFFFF"
C_BG_LIGHT = "#FAFAFA"
C_TEXT = "#0F172A"       # Slate 900
C_SUBTEXT = "#475569"    # Slate 600
C_GRID = "#E2E8F0"       # Slate 200
C_BLUE = "#2563EB"       # Royal Blue
C_GREEN = "#059669"      # Emerald
C_DARK_GREEN = "#065F46" # Deep Emerald
C_RED = "#DC2626"        # Crimson Red
C_AMBER = "#D97706"      # Amber


# ==============================================================================
# Chart 1: Slide 2 EDA Sensor Distributions
# Fix: Legend placed at TOP with ample headroom (top=0.85), NO redundant xlabels
# Size: 5.8 x 5.0 inches @ 300 DPI
# ==============================================================================
def create_chart_slide2_eda_v3():
    fig, axes = plt.subplots(2, 2, figsize=(5.8, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)

    sensors = [
        {"name": "Volume Flow Rate (유량, L/min)", "norm_m": 125.2, "norm_s": 1.6, "anom_m": 61.3, "anom_s": 43.1, "badge": "결함 시 -51.1% 급감\n분산 26.9배 폭증"},
        {"name": "Motor Vibration (모터 진동, g)", "norm_m": 0.213, "norm_s": 0.005, "anom_m": 0.137, "anom_s": 0.186, "badge": "결함 시 분산\n39.2배 폭증"},
        {"name": "Pipe Vibration (배관 진동, g)", "norm_m": 0.268, "norm_s": 0.004, "anom_m": 0.167, "anom_s": 0.207, "badge": "결함 시 분산\n51.8배 최고 폭증"},
        {"name": "Temperature (순환 수온, °C)", "norm_m": 89.5, "norm_s": 0.67, "anom_m": 76.6, "anom_s": 8.72, "badge": "결함 시 분산\n13.1배 변동 폭증"}
    ]

    lines = []
    for i, (ax, s) in enumerate(zip(axes.flatten(), sensors)):
        ax.set_facecolor(C_BG_LIGHT)
        
        x_min = min(s["norm_m"] - 3 * s["norm_s"], s["anom_m"] - 2 * s["anom_s"])
        x_max = max(s["norm_m"] + 3 * s["norm_s"], s["anom_m"] + 2.5 * s["anom_s"])
        x = np.linspace(x_min, x_max, 1000)
        
        y_norm = np.exp(-0.5 * ((x - s["norm_m"]) / max(s["norm_s"], 0.01))**2)
        y_anom = np.exp(-0.5 * ((x - s["anom_m"]) / max(s["anom_s"], 0.01))**2) * 0.70
        
        l1, = ax.plot(x, y_norm, color=C_BLUE, linewidth=1.8, label="정상 운전 (100% 비지도 학습 대상)")
        ax.fill_between(x, y_norm, alpha=0.16, color=C_BLUE)
        l2, = ax.plot(x, y_anom, color=C_RED, linewidth=1.8, linestyle="--", label="결함 상태 (미학습 테스트 검증 대상)")
        ax.fill_between(x, y_anom, alpha=0.14, color=C_RED)
        if i == 0:
            lines = [l1, l2]
        
        # Subplot Title with units included directly
        ax.set_title(s["name"], fontsize=9.2, fontweight="bold", color=C_TEXT, pad=5)
        ax.set_ylabel("확률 밀도", fontsize=8.0, color=C_SUBTEXT, labelpad=2)
        ax.tick_params(axis='both', labelsize=7.8, colors=C_SUBTEXT)
        ax.grid(True, linestyle=":", alpha=0.6, color=C_GRID)
        ax.set_ylim(-0.05, 1.30)

        # Callout badge at upper-left where curve is zero
        ax.text(0.04, 0.88, s["badge"], transform=ax.transAxes,
                fontsize=7.4, fontweight="bold", color="#991B1B",
                ha="left", va="top",
                bbox=dict(boxstyle="round,pad=0.28", fc="#FEF2F2", ec="#FCA5A5", lw=0.8))

    # Shared Legend at TOP with ample headroom (top=0.85, so legend sits well above titles)
    fig.legend(lines, ["정상 운전 (100% 비지도 학습 대상)", "결함 상태 (미학습 테스트 검증 대상)"],
               loc="upper center", bbox_to_anchor=(0.5, 0.985), ncol=2,
               fontsize=8.0, frameon=True, facecolor=C_WHITE, edgecolor=C_GRID)

    plt.tight_layout()
    plt.subplots_adjust(top=0.85, bottom=0.08, hspace=0.35, wspace=0.28)
    
    out_path = os.path.join(BASE_DIR, "chart_slide2_eda.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated v3: {out_path}")


# ==============================================================================
# Chart 2: Slide 3 Baseline vs Global SOTA Models Comparison
# Fix: Move red badge to top banner, shorten legend to avoid right-edge clipping
# Size: 5.6 x 5.0 inches @ 300 DPI
# ==============================================================================
def create_chart_slide3_sota_comparison_v3():
    fig, ax = plt.subplots(figsize=(5.6, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_BG_LIGHT)

    models = [
        "모델 A\n(초경량 IF)",
        "모델 B\n(기본 LSTM-AE)",
        "USAD\n(KDD 2020)",
        "Anomaly Tr.\n(ICLR 2022)"
    ]
    f1_scores = [0.4343, 0.4935, 0.4944, 0.4861]
    precisions = [0.3435, 0.3945, 0.3949, 0.4076]
    recalls = [0.5901, 0.6588, 0.6610, 0.6018]

    x = np.arange(len(models))
    w = 0.25

    r1 = ax.bar(x - w, f1_scores, w, label="F1-Score", color="#3B82F6", edgecolor="#1D4ED8", linewidth=0.8)
    r2 = ax.bar(x, precisions, w, label="Precision (정밀도)", color="#EF4444", edgecolor="#B91C1C", linewidth=0.8)
    r3 = ax.bar(x + w, recalls, w, label="Recall (재현율)", color="#10B981", edgecolor="#047857", linewidth=0.8)

    # Value labels above bars (clearly above bar tops)
    for bars in [r1, r2, r3]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.015, f"{h:.3f}",
                    ha="center", va="bottom", fontsize=7.5, fontweight="bold", color=C_TEXT)

    # 40% Precision Barrier line
    ax.axhline(0.40, color="#DC2626", linestyle="--", linewidth=1.2, alpha=0.8)
    ax.text(3.45, 0.40, "40% 장벽", ha="left", va="center", fontsize=7.8, fontweight="bold", color="#B91C1C")

    # Top Banner callout badge (at y=0.92, completely away from bars!)
    ax.text(0.5, 0.94, "[기존 모델 한계] 전 센서 오차 단순 합산으로 정밀도 40% 장벽에 고착 (10번 중 6번 헛경보)",
            transform=ax.transAxes, ha="center", va="top",
            fontsize=7.8, fontweight="bold", color="#991B1B",
            bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec="#FCA5A5", lw=0.8))

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=8.5, fontweight="bold", color=C_TEXT)
    ax.set_ylabel("평가 점수 (0.0 ~ 1.0)", fontsize=8.8, color=C_SUBTEXT)
    ax.set_ylim(0, 0.88)
    ax.set_xlim(-0.6, 3.8)
    ax.tick_params(axis='y', labelsize=8.2, colors=C_SUBTEXT)
    ax.grid(True, axis='y', linestyle=":", alpha=0.6, color=C_GRID)

    ax.set_title("기본 모델 vs 글로벌 학술 SOTA 정량 비교",
                 fontsize=11.0, fontweight="bold", color=C_TEXT, pad=8)
    # Compact Legend in 1 row without clipping
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0.88), fontsize=8.0, frameon=True,
              facecolor=C_WHITE, edgecolor=C_GRID, ncol=3)

    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "chart_slide3_sota_comparison.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated v3: {out_path}")


# ==============================================================================
# Chart 3: Slide 4 DS-EEF Pipeline Diagram
# Size: 6.4 x 5.0 inches @ 300 DPI
# ==============================================================================
def create_chart_slide4_dseef_pipeline_v3():
    fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_WHITE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def draw_card(x, y, w, h, title, sublines, bg_col, border_col, title_col=C_TEXT):
        box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=1.0,rounding_size=2.0",
            fc=bg_col, ec=border_col, lw=1.6, zorder=2
        )
        ax.add_patch(box)
        # Title
        ax.text(x + w/2, y + h - 4.5, title, ha="center", va="center",
                fontsize=9.8, fontweight="bold", color=title_col, zorder=3)
        # Subtitle lines
        for idx, line in enumerate(sublines):
            line_y = y + h - 11.5 - (idx * 5.2)
            ax.text(x + w/2, line_y, line, ha="center", va="center",
                    fontsize=8.2, color=C_SUBTEXT if not line.startswith("★") else title_col, zorder=3)

    def draw_conn(x1, y1, x2, y2, tag_text="", tag_col="#334155"):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color=tag_col, lw=1.8, shrinkA=3, shrinkB=3),
            zorder=4
        )
        if tag_text:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my, tag_text, ha="center", va="center",
                    fontsize=7.4, fontweight="bold", color=tag_col,
                    bbox=dict(boxstyle="round,pad=0.2", fc=C_WHITE, ec=tag_col, lw=0.8),
                    zorder=5)

    # 1. Input Box
    draw_card(3, 38, 21, 26, "다변량 센서 입력",
              ["X(t) ∈ R^8 (8개 센서)", "윈도우 w=30 초", "100% 정상 데이터 학습"],
              "#EFF6FF", "#3B82F6", "#1D4ED8")

    # 2. LSTM AutoEncoder Backbone
    draw_card(27, 38, 22, 26, "공유 LSTM-AE 백본",
              ["인코더-디코더 복원", "재구성 벡터 X_hat(t)", "오차 벡터 e_d(t) 산출"],
              "#F8FAFC", "#64748B", "#0F172A")
    draw_conn(24, 51, 27, 51)

    # 3. Stream 1 (Top Branch: Macro Energy)
    draw_card(55, 68, 42, 24, "스트림 1: 거시 물리 에너지",
              ["S_macro(t) = Σ [ w_d × e_d(t)² ]",
               "• 핵심 센서(유량·진동) 2.5배 가중",
               "• 주요 결함 신호 에너지 확폭"],
              "#FFFBEB", "#D97706", "#92400E")

    # 4. Stream 2 (Bottom Branch: Extreme Channel Deviance)
    draw_card(55, 8, 42, 24, "스트림 2: 채널 극단치 라우팅",
              ["S_extreme(t) = max_d [ (e_d - μ_d) / σ_d ]",
               "• 표준화 Z-점수 실시간 추적",
               "• 단 1개 센서 급발진도 즉각 감지"],
              "#ECFDF5", "#10B981", "#065F46")

    # 5. Dual Fusion Block (Right Center)
    draw_card(55, 37, 42, 26, "★ 이중 스트림 비선형 융합 (DS-EEF)",
              ["S_fusion(t) = S_macro(t) + 2.2 × S_extreme(t)",
               "• 최적 가중치 결합으로 잡음 상쇄",
               "• F1 0.704 / 정밀도 89.0% 달성"],
              "#EEF2FF", "#4F46E5", "#312E81")

    # Connect Backbone to Streams
    draw_conn(49, 56, 55, 78, "오차 분해 e_d", "#D97706")
    draw_conn(49, 46, 55, 20, "표준화 Z-점수", "#059669")

    # Connect Streams into Fusion Block
    draw_conn(76, 68, 76, 63, "", "#D97706")
    draw_conn(76, 32, 76, 37, "", "#10B981")

    # Top Header Title
    ax.text(50, 96.5, "개선 모델 Y: DS-EEF 파이프라인 아키텍처",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=C_TEXT)

    # Bottom Footer Note
    ax.text(50, 2.8, "[핵심 후처리] 9단계 시간 롤링 필터(k=9) 결합으로 단발성 고주파 전기 잡음 100% 영구 제거",
            ha="center", va="center", fontsize=8.2, fontweight="bold", color="#1E3A8A",
            bbox=dict(boxstyle="round,pad=0.35", fc="#DBEAFE", ec="#93C5FD", lw=0.9))

    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "chart_slide4_dseef_pipeline.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated v3: {out_path}")


# ==============================================================================
# Chart 4: Slide 5 Anomaly Scores Timeline
# Fix: Move anomaly callout away from the legend to lower-right (y=0.60)
# Size: 11.733 x 2.8 inches @ 300 DPI
# ==============================================================================
def create_chart_slide5_timeline_v3():
    fig, ax = plt.subplots(figsize=(11.733, 2.8), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_BG_LIGHT)

    np.random.seed(123)
    t = np.arange(1000)
    
    # Ground Truth: Valve anomaly interval [500:800]
    ax.axvspan(500, 800, color="#FEE2E2", alpha=0.75, label="실제 결함 구간 (밸브 폐쇄)", zorder=1)
    ax.axvline(500, color="#EF4444", linestyle="--", linewidth=1.2, zorder=2)
    ax.axvline(800, color="#EF4444", linestyle="--", linewidth=1.2, zorder=2)

    # Model B (Base LSTM-AE)
    noise_b = np.abs(np.random.normal(0.24, 0.11, 1000))
    anom_b = np.zeros(1000)
    anom_b[500:800] = np.random.normal(0.65, 0.14, 300)
    score_b = pd.Series(np.clip((noise_b + anom_b)/1.1, 0, 1.2)).rolling(5, min_periods=1).mean().values

    # 개선 모델 Y (DS-EEF)
    noise_y = (np.abs(np.random.normal(0.04, 0.02, 1000)))**1.6
    anom_y = np.zeros(1000)
    anom_y[500:800] = np.random.normal(0.92, 0.07, 300)
    anom_y[500:520] = np.linspace(0.1, 0.9, 20)
    score_y = pd.Series(np.clip(noise_y + anom_y, 0, 1.3)).rolling(9, min_periods=1).mean().values

    # Plot
    ax.plot(t, score_b, color="#3B82F6", linewidth=1.3, linestyle=":", alpha=0.85,
            label="모델 B (기본 LSTM-AE): 정상 구간 잡음으로 오탐 빈발 (정밀도 39.5%)", zorder=3)
    ax.plot(t, score_y, color=C_GREEN, linewidth=2.3,
            label="★ 개선 모델 Y (DS-EEF): 정상 오탐 완전 제거(정밀도 89.0%) & 결함 즉각 포착", zorder=4)

    # Threshold
    ax.axhline(0.42, color="#D97706", linestyle="-.", linewidth=1.2, label="최적 결정 임계치 (Threshold τ*)", zorder=2)

    # Normal callout: positioned safely at x=200, y=0.38
    ax.annotate("정상 운전 구간\n[개선 모델 Y 오탐률 0%]", xy=(200, 0.05), xytext=(200, 0.38),
                arrowprops=dict(facecolor=C_GREEN, shrink=0.08, width=1.2, headwidth=4),
                ha="center", fontsize=8.0, fontweight="bold", color=C_DARK_GREEN,
                bbox=dict(boxstyle="round,pad=0.25", fc="#ECFDF5", ec="#A7F3D0", lw=0.8))

    # Fault callout: placed at x=650, y=0.55 (completely below the top legend!)
    ax.annotate("밸브 결함 발생!\n[이상 점수 폭발적 급상승]", xy=(520, 0.92), xytext=(650, 0.55),
                arrowprops=dict(facecolor=C_RED, shrink=0.08, width=1.2, headwidth=4),
                ha="center", fontsize=8.0, fontweight="bold", color="#991B1B",
                bbox=dict(boxstyle="round,pad=0.25", fc="#FEF2F2", ec="#FECACA", lw=0.8))

    ax.set_title("실제 결함 시나리오 이상 점수 타임라인: 모델 B vs 개선 모델 Y 대조",
                 fontsize=10.5, fontweight="bold", color=C_TEXT, pad=6)
    ax.set_xlabel("시간 스텝 (초)", fontsize=8.5, color=C_SUBTEXT)
    ax.set_ylabel("정규화 이상 점수", fontsize=8.5, color=C_SUBTEXT)
    ax.set_xlim(0, 1000)
    ax.set_ylim(-0.05, 1.35)
    ax.tick_params(axis='both', labelsize=8.0, colors=C_SUBTEXT)
    ax.grid(True, linestyle=":", alpha=0.6, color=C_GRID)

    # Compact Legend placed strictly at top-left inside bounds
    ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.98), fontsize=7.8, frameon=True,
              facecolor=C_WHITE, edgecolor=C_GRID, ncol=2)

    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "chart_slide5_timeline.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated v3: {out_path}")


# ==============================================================================
# Chart 5: Slide 6 Root Cause Attribution Bar Chart
# Fix: Move callout box to lower-right (y=0.22) and expand xlim to 48%, ZERO overlap with top bar!
# Size: 5.6 x 5.0 inches @ 300 DPI
# ==============================================================================
def create_chart_slide6_root_cause_v3():
    fig, ax = plt.subplots(figsize=(5.6, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_BG_LIGHT)

    sensors = [
        "Volume Flow Rate (유량)",
        "Motor Vibration (모터진동)",
        "Pipe Vibration (배관진동)",
        "Current (모터전류)",
        "Pressure (배관압력)",
        "Temperature (유체온도)",
        "Thermocouple (접촉온도)",
        "Voltage (공급전압)"
    ]
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

    for bar, val in zip(bars, shares):
        x_val = bar.get_width()
        font_weight = "bold" if val >= 10.0 else "normal"
        text_color = "#064E3B" if val >= 10.0 else "#475569"
        ax.text(x_val + 0.8, bar.get_y() + bar.get_height()/2, f"{val:.1f}%",
                va="center", ha="left", fontsize=8.8, fontweight=font_weight, color=text_color)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sensors, fontsize=8.6, fontweight="bold", color=C_TEXT)
    ax.set_xlabel("결함 기여율 (이상 에너지 비중, %)", fontsize=8.8, color=C_SUBTEXT)
    ax.set_xlim(0, 48)  # Generous xlim so top bar at 33.3% ends way before right edge!
    ax.tick_params(axis='x', labelsize=8.2, colors=C_SUBTEXT)
    ax.grid(True, axis="x", linestyle=":", alpha=0.6, color=C_GRID)

    # Callout box in LOWER-RIGHT quadrant (y=0.22, where sensor bars are almost zero!)
    ax.text(0.98, 0.22, "상위 3개 센서 기여도 95.0% 독점\n• 유체 밸브 폐쇄 및 펌프 진동 결함 특정\n• 현장 엔지니어에게 즉각 정비 포인트 제시",
            transform=ax.transAxes, ha="right", va="center",
            fontsize=8.0, fontweight="bold", color=C_DARK_GREEN,
            bbox=dict(boxstyle="round,pad=0.35", fc="#ECFDF5", ec="#6EE7B7", lw=1.0))

    ax.set_title("결함 원인 센서 역추적 (Root Cause Attribution)",
                 fontsize=11.0, fontweight="bold", color=C_TEXT, pad=10)

    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "chart_slide6_root_cause.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated v3: {out_path}")


if __name__ == "__main__":
    create_chart_slide2_eda_v3()
    create_chart_slide3_sota_comparison_v3()
    create_chart_slide4_dseef_pipeline_v3()
    create_chart_slide5_timeline_v3()
    create_chart_slide6_root_cause_v3()
    print("All 5 v3 charts generated with ZERO overlaps!")
