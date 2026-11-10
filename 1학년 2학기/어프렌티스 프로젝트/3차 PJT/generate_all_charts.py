import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"g:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"

# Dark Theme styling
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = ['Malgun Gothic', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

def generate_comparison_chart():
    fig, ax = plt.subplots(figsize=(14.5, 6.8), facecolor='#15171b')
    ax.set_facecolor('#1c1f24')

    models = [
        '모델 A\n(Isolation Forest)',
        '모델 B\n(기본 LSTM-AE)',
        'SOTA 1: USAD\n(Audibert+ KDD 2020)',
        'SOTA 2: Anomaly Tr.\n(Xu+ ICLR 2022)',
        '★ 최종 개선 모델 y\n(도메인가중+롤링필터)'
    ]
    
    # Metrics
    f1_raw_vals = [0.4343, 0.4935, 0.4944, 0.4861, 0.5876]
    prec_raw_vals = [0.3435, 0.3945, 0.3949, 0.4076, 0.5519]
    rec_raw_vals = [0.5901, 0.6588, 0.6610, 0.6018, 0.6283]
    auprc_vals = [0.3468, 0.7009, 0.6156, 0.6440, 0.7397]
    f1_pa_vals = [0.4755, 0.5249, 0.5053, 0.5364, 0.6213]

    metrics = {
        'F1-Score (Raw)': f1_raw_vals,
        'Precision (Raw)': prec_raw_vals,
        'Recall (Raw)': rec_raw_vals,
        'AUPRC (핵심 지표)': auprc_vals,
        'F1-Score (PA)': f1_pa_vals
    }

    x = np.arange(len(models))
    width = 0.155
    colors_bar = ['#38bdf8', '#818cf8', '#34d399', '#fbbf24', '#f472b6']

    for i, (m_name, vals) in enumerate(metrics.items()):
        offset = (i - 2) * width
        rects = ax.bar(x + offset, vals, width, label=m_name, color=colors_bar[i], alpha=0.9, edgecolor='#2b2f37')
        for rect in rects:
            h = rect.get_height()
            ax.annotate(f'{h:.3f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                        fontsize=8.5, color='#e2e8f0', fontweight='bold')

    ax.set_title("SKAB Test 세트 이종 모델 및 최신 SOTA(USAD, Anomaly Transformer) 벤치마크 (개선 모델 y 최고 성능 입증)", color='#5eead4', fontsize=13, fontweight='bold', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(models, color='#f8fafc', fontsize=10.5, fontweight='bold')
    ax.set_ylabel("성능 점수 (Score, 0.0 ~ 1.0)", color='#cbd5e1', fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.grid(True, color='#2b2f37', linestyle=':', alpha=0.6)
    ax.legend(facecolor='#1e2228', edgecolor='#334155', fontsize=9.5, loc='upper left', labelcolor='#e2e8f0')

    chart_model_comp = os.path.join(BASE_DIR, "chart_pjt3_model_comparison.png")
    plt.tight_layout()
    plt.savefig(chart_model_comp, dpi=200, facecolor='#15171b')
    plt.close()
    print(f"Generated: {chart_model_comp}")

if __name__ == '__main__':
    generate_comparison_chart()
