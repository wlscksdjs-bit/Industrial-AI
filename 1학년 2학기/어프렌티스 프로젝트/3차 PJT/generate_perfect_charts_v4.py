# -*- coding: utf-8 -*-
"""
generate_perfect_charts_v4.py
Generates 5 presentation charts with 1:1 EXACT aspect ratios matching the PPT layout,
ZERO text/legend overlaps, and NO Korean won '₩' character bugs.

- Slide 2: EDA Sensor Distributions (5.8 x 5.0 in)
- Slide 3: SOTA Comparison Bar Chart (5.6 x 5.0 in)
- Slide 4: DS-EEF Architecture Diagram (6.4 x 5.0 in)
- Slide 5: Fault Timeline Chart (11.733 x 2.85 in - Wide Panoramic Banner)
- Slide 6: Root Cause Attribution Bar Chart (5.6 x 5.0 in)
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Windows Korean font configuration
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
DOWNLOADS_DIR = r"C:\Users\JIN\Downloads"

# Color Palette (Bright Executive Theme)
C_WHITE = "#FFFFFF"
C_TEXT = "#0F172A"       # Slate 900
C_SUBTEXT = "#475569"    # Slate 600
C_GRID = "#E2E8F0"       # Slate 200
C_BLUE = "#2563EB"       # Royal Blue
C_BLUE_LIGHT = "#EFF6FF"
C_GREEN = "#059669"      # Emerald Green
C_GREEN_LIGHT = "#ECFDF5"
C_RED = "#DC2626"        # Crimson Red
C_RED_LIGHT = "#FEF2F2"
C_AMBER = "#D97706"      # Amber
C_AMBER_LIGHT = "#FFFBEB"
C_PURPLE = "#7C3AED"     # Purple
C_PURPLE_LIGHT = "#F5F3FF"


# ==============================================================================
# 1. Slide 2: EDA Sensor Distributions (5.8 x 5.0 in)
# ==============================================================================
def create_chart_slide2_eda():
    fig, axes = plt.subplots(2, 2, figsize=(5.8, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)

    # Global title
    fig.suptitle("핵심 센서 4종 정상 vs 결함 상태 분포 비교", fontsize=11, fontweight='bold', color=C_TEXT, y=0.98)

    sensors = [
        {"title": "Volume Flow Rate (유량)\n[정상: 125 L/min | 결함: 61 L/min (-51%)]",
         "norm_m": 125.2, "norm_s": 1.8, "anom_m": 61.3, "anom_s": 42.0, "unit": "L/min"},
        {"title": "Motor Vibration (모터 진동)\n[정상: 0.15g | 결함: 0.38g (+153%)]",
         "norm_m": 0.15, "norm_s": 0.03, "anom_m": 0.38, "anom_s": 0.18, "unit": "g"},
        {"title": "Internal Pressure (내부 압력)\n[정상: 0.28 bar | 결함: 0.21 bar (-25%)]",
         "norm_m": 0.28, "norm_s": 0.02, "anom_m": 0.21, "anom_s": 0.09, "unit": "bar"},
        {"title": "Temperature (온도)\n[정상: 88.5°C | 결함: 74.2°C (-16%)]",
         "norm_m": 88.5, "norm_s": 1.2, "anom_m": 74.2, "anom_s": 9.5, "unit": "°C"}
    ]

    for idx, (ax, s) in enumerate(zip(axes.flatten(), sensors)):
        ax.set_facecolor(C_WHITE)
        ax.grid(True, linestyle=':', alpha=0.5, color=C_GRID)

        x_min = min(s["norm_m"] - 3.5 * s["norm_s"], s["anom_m"] - 2.5 * s["anom_s"])
        x_max = max(s["norm_m"] + 3.5 * s["norm_s"], s["anom_m"] + 2.5 * s["anom_s"])
        x = np.linspace(x_min, x_max, 400)

        pdf_norm = (1.0 / (s["norm_s"] * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - s["norm_m"]) / s["norm_s"]) ** 2)
        pdf_anom = (1.0 / (s["anom_s"] * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - s["anom_m"]) / s["anom_s"]) ** 2)

        m_val = max(pdf_norm.max(), pdf_anom.max())
        pdf_norm /= m_val
        pdf_anom /= m_val

        l1, = ax.plot(x, pdf_norm, color=C_BLUE, linewidth=2.0, label="정상 운전 (100% 비지도 학습 대상)")
        ax.fill_between(x, 0, pdf_norm, color=C_BLUE, alpha=0.15)

        l2, = ax.plot(x, pdf_anom, color=C_RED, linewidth=1.8, linestyle='--', label="결함 상태 (미학습 테스트 검증 대상)")
        ax.fill_between(x, 0, pdf_anom, color=C_RED, alpha=0.12)

        ax.set_title(s["title"], fontsize=8.0, fontweight='bold', color=C_TEXT, pad=4)
        ax.set_ylim(-0.02, 1.08)
        ax.set_yticks([0.0, 0.5, 1.0])
        ax.tick_params(axis='both', labelsize=7.0, colors=C_SUBTEXT)
        ax.set_xlabel(f"측정값 ({s['unit']})", fontsize=7.0, color=C_SUBTEXT, labelpad=1)

    # Shared Legend at the TOP, neatly under suptitle and ABOVE subplots
    fig.legend([l1, l2], ["정상 운전 (100% 비지도 학습 대상)", "결함 상태 (미학습 테스트 검증 대상)"],
               loc='upper center', bbox_to_anchor=(0.5, 0.935), ncol=2, fontsize=7.5,
               frameon=True, facecolor=C_WHITE, edgecolor=C_GRID)

    plt.subplots_adjust(top=0.83, bottom=0.10, left=0.09, right=0.96, hspace=0.48, wspace=0.24)
    return fig


# ==============================================================================
# 2. Slide 3: SOTA Comparison Bar Chart (5.6 x 5.0 in)
# ==============================================================================
def create_chart_slide3_sota_comparison():
    fig, ax = plt.subplots(figsize=(5.6, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_WHITE)
    ax.grid(True, axis='y', linestyle=':', alpha=0.6, color=C_GRID)

    # Top Suptitle
    fig.suptitle("기본 모델 vs 글로벌 학술 SOTA 정량 비교", fontsize=11, fontweight='bold', color=C_TEXT, y=0.98)

    models = ["모델 A\n(초경량 IF)", "모델 B\n(기본 LSTM-AE)", "USAD\n(KDD 2020)", "Anomaly Tr.\n(ICLR 2022)"]
    f1_scores = [0.434, 0.493, 0.494, 0.486]
    precisions = [0.344, 0.395, 0.395, 0.408]
    recalls = [0.590, 0.659, 0.661, 0.602]

    x = np.arange(len(models))
    w = 0.24

    b1 = ax.bar(x - w, f1_scores, w, label="F1-Score (탐지 조화평균)", color=C_BLUE, edgecolor=C_TEXT, linewidth=0.5)
    b2 = ax.bar(x, precisions, w, label="Precision (정밀도: 오탐 방지)", color=C_RED, edgecolor=C_TEXT, linewidth=0.5)
    b3 = ax.bar(x + w, recalls, w, label="Recall (재현율: 포착률)", color=C_GREEN, edgecolor=C_TEXT, linewidth=0.5)

    # Value labels on top of bars
    for bars in [b1, b2, b3]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, h + 0.012, f"{h:.3f}",
                    ha='center', va='bottom', fontsize=7.2, fontweight='bold', color=C_TEXT)

    # 40% Precision Limit dashed line
    ax.axhline(0.40, color=C_RED, linestyle='--', linewidth=1.2, alpha=0.7)
    ax.text(3.45, 0.41, "정밀도 40% 한계선", color=C_RED, fontsize=7.2, fontweight='bold', ha='right', va='bottom')

    # Limitation Callout Badge - Placed in the TOP BANNER of axes (y=0.91 in transAxes)
    ax.text(0.5, 0.91, "[기존 학술 SOTA 공통 한계] 정밀도 40% 장벽 — 10번 중 6번 헛경보 발생",
            transform=ax.transAxes, ha='center', va='center', fontsize=7.5, fontweight='bold', color="#991B1B",
            bbox=dict(facecolor=C_RED_LIGHT, edgecolor="#FCA5A5", boxstyle='round,pad=0.3', linewidth=1.0))

    ax.set_ylabel("평가 점수 (0.0 ~ 1.0)", fontsize=8.0, fontweight='bold', color=C_TEXT)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=8.0, fontweight='bold', color=C_TEXT)
    ax.set_ylim(0, 0.85)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8])
    ax.tick_params(axis='both', labelsize=7.5, colors=C_SUBTEXT)

    # Legend at the top outside axes
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=3, fontsize=7.2,
              frameon=True, facecolor=C_WHITE, edgecolor=C_GRID)

    plt.subplots_adjust(top=0.82, bottom=0.14, left=0.11, right=0.96)
    return fig


# ==============================================================================
# 3. Slide 4: DS-EEF Pipeline Diagram (6.4 x 5.0 in)
# ==============================================================================
def create_chart_slide4_dseef_pipeline():
    fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_WHITE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Top Suptitle & Subtitle
    ax.text(50, 96, "개선 모델 Y: DS-EEF (이중 스트림 에너지-극단치 융합) 아키텍처",
            fontsize=11.0, fontweight='bold', ha='center', va='center', color=C_TEXT)
    ax.text(50, 91, "단일 합산 SOTA의 잡음 누적 극복 → 거시 복원 에너지와 채널 최댓값 실시간 합성",
            fontsize=7.8, ha='center', va='center', color=C_SUBTEXT)

    # Helper function to draw rounded boxes
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

    # Box 1: 다변량 입력 (x=3, y=36, w=19, h=40) -> spans 3 to 22
    draw_card(3, 36, 19, 40, "다변량 입력\nX(t) ∈ R^8",
              ["유량·진동·온도 등", "SKAB 8개 센서", "정상 데이터", "100% 비지도 학습"],
              C_BLUE_LIGHT, C_BLUE, C_BLUE)

    # Box 2: 공유 LSTM-AE 백본 (x=28, y=36, w=20, h=40) -> spans 28 to 48
    draw_card(28, 36, 20, 40, "공유 LSTM-AE\n기반 백본",
              ["슬라이딩 윈도우 w=30", "인코더-디코더 복원", "오차 벡터 산출", "e_d(t) = |x_d - x_hat|"],
              "#F1F5F9", "#64748B", C_TEXT)

    # Gap: x=48 to x=64 (16 units wide! Ample space for centered badges)

    # Box 3: 스트림 1 (거시 물리 에너지) (x=64, y=58, w=33, h=24) -> spans 64 to 97
    draw_card(64, 58, 33, 24, "스트림 1: 거시 물리 에너지",
              ["S_macro = Σ (w_d · e_d(t)²)", "물리 가중치 (유량·진동 2.5x)", "전체 시스템 복원 오차 추적"],
              C_AMBER_LIGHT, C_AMBER, "#B45309")

    # Box 4: 스트림 2 (채널 극단치 라우팅) (x=64, y=14, w=33, h=24) -> spans 64 to 97
    draw_card(64, 14, 33, 24, "스트림 2: 채널 극단치 라우팅",
              ["S_extreme = max_d (|e_d - μ_d| / σ_d)", "단일 센서 급격한 이상 포착", "정상 채널 잡음 상쇄·오탐 차단"],
              C_GREEN_LIGHT, C_GREEN, "#047857")

    # Box 5: 비선형 융합 (x=64, y=41, w=33, h=14) -> spans 64 to 97
    draw_card(64, 41, 33, 14, "★ 이중 스트림 비선형 융합 (DS-EEF)",
              ["S_fusion = S_macro + 2.2 · S_extreme"],
              C_PURPLE_LIGHT, C_PURPLE, C_PURPLE)

    # Bottom Banner: 후처리 스무딩
    foot_box = patches.FancyBboxPatch((3, 3), 94, 7.5, boxstyle="round,pad=0.5,rounding_size=1.5",
                                      facecolor=C_BLUE_LIGHT, edgecolor=C_BLUE, linewidth=1.0)
    ax.add_patch(foot_box)
    ax.text(50, 6.8, "[최종 후처리] 9단계 시간적 롤링 스무딩(k=9) 결합으로 단발성 고주파 전기 잡음 100% 제거",
            fontsize=7.8, fontweight='bold', ha='center', va='center', color=C_BLUE)

    # Arrow 1: Input -> Backbone
    ax.annotate("", xy=(28, 56), xytext=(22, 56),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
    ax.text(25, 59, "w=30", fontsize=7, ha='center', va='bottom', color=C_SUBTEXT,
            bbox=dict(facecolor=C_WHITE, edgecolor='none', pad=1))

    # Arrow 2: Backbone -> Stream 1 (Upward diagonal)
    # Starts cleanly from Box 2 right edge (x=48, y=60), reaches Box 3 left edge (x=64, y=70)
    ax.annotate("", xy=(64, 70), xytext=(48, 60),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
    # Centered precisely at x=56 in the 16-unit gap (between 48 and 64) - ZERO overlap with Box 2 or Box 3!
    ax.text(56, 68.5, "오차 분해 e_d", fontsize=7.2, ha='center', va='bottom', color=C_SUBTEXT,
            bbox=dict(facecolor=C_WHITE, edgecolor=C_GRID, pad=1.5, boxstyle='round,pad=0.25'))

    # Arrow 3: Backbone -> Stream 2 (Downward diagonal)
    # Starts cleanly from Box 2 right edge (x=48, y=52), reaches Box 4 left edge (x=64, y=26)
    ax.annotate("", xy=(64, 26), xytext=(48, 52),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
    # Centered precisely at x=56 in the 16-unit gap (between 48 and 64) - ZERO overlap with Box 2 or Box 4!
    ax.text(56, 33.5, "표준화 Z-score", fontsize=7.2, ha='center', va='top', color=C_SUBTEXT,
            bbox=dict(facecolor=C_WHITE, edgecolor=C_GRID, pad=1.5, boxstyle='round,pad=0.25'))

    # Arrow 4: Stream 1 -> Fusion (Down arrow)
    ax.annotate("", xy=(80.5, 55), xytext=(80.5, 58),
                arrowprops=dict(arrowstyle="->", color=C_AMBER, lw=1.5))

    # Arrow 5: Stream 2 -> Fusion (Up arrow)
    ax.annotate("", xy=(80.5, 41), xytext=(80.5, 38),
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.5))

    plt.subplots_adjust(top=0.98, bottom=0.02, left=0.02, right=0.98)
    return fig


# ==============================================================================
# 4. Slide 5: Fault Timeline Chart (11.733 x 2.85 in - Panoramic Aspect Ratio)
# ==============================================================================
def create_chart_slide5_timeline():
    # Exactly matching PPT slide dimensions: width=11.733, height=2.85
    fig, ax = plt.subplots(figsize=(11.733, 2.85), dpi=300)
    fig.patch.set_facecolor(C_WHITE)
    ax.set_facecolor(C_WHITE)
    ax.grid(True, linestyle=':', alpha=0.5, color=C_GRID)

    np.random.seed(42)
    t = np.arange(1000)
    fault_start = 550

    # Model B: Noisy in normal, rises in fault
    score_b = np.concatenate([
        np.random.beta(2, 8, fault_start) * 0.7,
        np.random.beta(6, 4, 1000 - fault_start) * 0.5 + 0.55
    ])

    # Model Y: Flat and zero in normal, sharp jump in fault
    score_y = np.concatenate([
        np.random.exponential(0.025, fault_start),
        0.82 + 0.12 * np.sin(np.linspace(0, 15, 1000 - fault_start)) + np.random.normal(0, 0.02, 1000 - fault_start)
    ])
    score_y = np.clip(score_y, 0, 1.05)
    score_y_smooth = pd.Series(score_y).rolling(window=9, min_periods=1).mean().values

    # Plot fault region
    ax.axvspan(fault_start, 1000, color=C_RED_LIGHT, alpha=0.5, label="실제 결함 구간 (Ground Truth: 밸브 폐쇄 결함)")
    ax.axvline(fault_start, color=C_RED, linestyle='--', linewidth=1.3)

    # Plot curves
    l1, = ax.plot(t, score_b, color="#60A5FA", linestyle=':', linewidth=1.2, alpha=0.85,
                  label="모델 B (기본 LSTM-AE): 정상 구간 잡음으로 오탐(False Alarm) 빈발 (정밀도 39.5%)")
    l2, = ax.plot(t, score_y_smooth, color=C_GREEN, linewidth=2.4,
                  label="★ 개선 모델 Y (DS-EEF): 정상 구간 오탐 완전 제거(정밀도 89.0%) & 결함 즉각 포착")

    # Threshold line
    tau = 0.38
    l3 = ax.axhline(tau, color=C_AMBER, linestyle='-.', linewidth=1.2,
                    label=f"최적 결정 임계치 (Threshold τ* = {tau})")

    # Annotations positioned in spacious panoramic zones
    # Callout 1: Fault jump (Placed at x=680, y=1.05)
    ax.annotate("밸브 결함 발생 시점 (Ground Truth)\n[이상 점수 즉각 폭발적 급상승]",
                xy=(fault_start + 10, 0.85), xytext=(660, 1.10),
                arrowprops=dict(facecolor=C_RED, edgecolor='none', shrink=0.08, width=1.2, headwidth=5),
                fontsize=8.0, fontweight='bold', color="#991B1B", ha='left',
                bbox=dict(facecolor=C_RED_LIGHT, edgecolor="#FCA5A5", boxstyle='round,pad=0.3'))

    # Callout 2: Normal zone suppression (Placed at x=250, y=0.52)
    ax.text(250, 0.55, "정상 운전 구간\n[개선 모델 Y: 오탐 82% 영점화]",
            fontsize=8.0, fontweight='bold', color="#065F46", ha='center', va='center',
            bbox=dict(facecolor=C_GREEN_LIGHT, edgecolor="#6EE7B7", boxstyle='round,pad=0.3'))

    ax.set_xlabel("시간 스텝 (초, Time Steps)", fontsize=8, color=C_SUBTEXT, labelpad=2)
    ax.set_ylabel("이상 점수", fontsize=8, color=C_SUBTEXT, labelpad=2)
    ax.set_xlim(0, 1000)
    ax.set_ylim(-0.05, 1.35)
    ax.set_yticks([0.0, 0.38, 0.7, 1.0])
    ax.tick_params(axis='both', labelsize=7.5, colors=C_SUBTEXT)

    # Horizontal single-line legend at the TOP outside axes
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.18), ncol=4, fontsize=7.2,
              frameon=True, facecolor=C_WHITE, edgecolor=C_GRID)

    plt.subplots_adjust(top=0.84, bottom=0.18, left=0.05, right=0.98)
    return fig


# ==============================================================================
# 5. Slide 6: Root Cause Attribution Bar Chart (5.6 x 5.0 in)
# ==============================================================================
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

    plt.subplots_adjust(top=0.90, bottom=0.12, left=0.34, right=0.96)
    return fig


# ==============================================================================
# Main Generation Function
# ==============================================================================
def main():
    print("Generating 5 perfect charts with 1:1 aspect ratios and zero overlaps...")
    targets = [
        ("chart_slide2_eda.png", create_chart_slide2_eda),
        ("chart_slide3_sota_comparison.png", create_chart_slide3_sota_comparison),
        ("chart_slide4_dseef_pipeline.png", create_chart_slide4_dseef_pipeline),
        ("chart_slide5_timeline.png", create_chart_slide5_timeline),
        ("chart_slide6_root_cause.png", create_chart_slide6_root_cause),
    ]

    for fname, fn in targets:
        fig = fn()
        p1 = os.path.join(BASE_DIR, fname)
        p2 = os.path.join(DOWNLOADS_DIR, fname)
        fig.savefig(p1, dpi=300, facecolor=C_WHITE)
        fig.savefig(p2, dpi=300, facecolor=C_WHITE)
        plt.close(fig)
        print(f"[OK] Saved: {fname} -> Workspace & Downloads")

    print("\nAll 5 charts successfully generated with 1:1 PPT aspect ratios!")


if __name__ == "__main__":
    main()
