import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
sys.stdout.reconfigure(encoding='utf-8')

# Paths
BASE_DIR = r"g:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
SKAB_DATA_DIR = os.path.join(BASE_DIR, "SKAB", "data")

NORMAL_PATH = os.path.join(SKAB_DATA_DIR, "anomaly-free", "anomaly-free.csv")
VALVE1_DIR = os.path.join(SKAB_DATA_DIR, "valve1")
VALVE2_DIR = os.path.join(SKAB_DATA_DIR, "valve2")
OTHER_DIR = os.path.join(SKAB_DATA_DIR, "other")

# 8 Sensor features
SENSOR_COLS = [
    'Accelerometer1RMS',
    'Accelerometer2RMS',
    'Current',
    'Pressure',
    'Temperature',
    'Thermocouple',
    'Voltage',
    'Volume Flow RateRMS'
]

# Set visual style (Dark Theme matching presentation)
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = ['Malgun Gothic', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

def run_eda():
    print("=" * 70)
    print(" [Step 1] SKAB 산업 시계열 데이터셋 탐색적 데이터 분석 (EDA)")
    print("=" * 70)

    # 1. Load Normal Data
    df_normal = pd.read_csv(NORMAL_PATH, sep=';', parse_dates=['datetime'], index_col='datetime')
    print(f"\n1. 정상 데이터(anomaly-free.csv) 로드 완료: {df_normal.shape[0]} 행, {df_normal.shape[1]} 개 센서")
    
    # 2. Load Anomaly Datasets (representative files from valve1, valve2, other)
    # We will combine all anomaly files to get full benchmark overview
    anomaly_files = []
    for d in [VALVE1_DIR, VALVE2_DIR, OTHER_DIR]:
        for f in sorted(os.listdir(d)):
            if f.endswith('.csv'):
                anomaly_files.append((os.path.basename(d), f, os.path.join(d, f)))

    print(f"2. 결함 시나리오 데이터셋 탐색: 총 {len(anomaly_files)}개 파일 식별 (valve1: 16개, valve2: 4개, other: 14개)")

    # Load and aggregate anomaly datasets
    anomaly_dfs = []
    total_samples = 0
    total_anomalies = 0

    for cat, fname, fpath in anomaly_files:
        df = pd.read_csv(fpath, sep=';', parse_dates=['datetime'], index_col='datetime')
        df['category'] = cat
        df['filename'] = fname
        anomaly_dfs.append(df)
        total_samples += len(df)
        total_anomalies += int(df['anomaly'].sum())

    df_all_anom = pd.concat(anomaly_dfs, axis=0)
    print(f"   - 총 결함 시나리오 샘플 수: {total_samples:,} 건")
    print(f"   - 실제 이상 라벨(anomaly=1.0) 샘플 수: {total_anomalies:,} 건 ({total_anomalies/total_samples*100:.2f}%)")
    print(f"   - 정상 라벨(anomaly=0.0) 샘플 수: {total_samples - total_anomalies:,} 건 ({(total_samples-total_anomalies)/total_samples*100:.2f}%)")

    # 3. Statistical summary of normal data
    stats_normal = df_normal[SENSOR_COLS].describe().T[['mean', 'std', 'min', '50%', 'max']]
    stats_normal['skew'] = df_normal[SENSOR_COLS].skew()
    stats_normal['kurt'] = df_normal[SENSOR_COLS].kurtosis()

    # Statistical summary of anomaly points in test data
    df_pure_anom = df_all_anom[df_all_anom['anomaly'] == 1.0]
    stats_anom = df_pure_anom[SENSOR_COLS].describe().T[['mean', 'std', 'min', '50%', 'max']]
    stats_anom['skew'] = df_pure_anom[SENSOR_COLS].skew()
    stats_anom['kurt'] = df_pure_anom[SENSOR_COLS].kurtosis()

    print("\n3. 정상 vs 이상 센서별 기초 통계량 비교:")
    comp_df = pd.DataFrame({
        'Normal Mean': stats_normal['mean'],
        'Anom Mean': stats_anom['mean'],
        'Mean Shift (%)': ((stats_anom['mean'] - stats_normal['mean']) / (stats_normal['mean'].abs() + 1e-8) * 100),
        'Normal Std': stats_normal['std'],
        'Anom Std': stats_anom['std'],
        'Std Ratio': (stats_anom['std'] / (stats_normal['std'] + 1e-8))
    })
    print(comp_df.to_string())

    # 4. Chart 1: Sensor Correlation Heatmap (Normal vs Anomaly)
    print("\n4. 상관관계 매트릭스 차트 생성 중...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='#15171b')
    ax1.set_facecolor('#1c1f24')
    ax2.set_facecolor('#1c1f24')

    corr_normal = df_normal[SENSOR_COLS].corr()
    corr_anom = df_pure_anom[SENSOR_COLS].corr()

    short_cols = ['Acc1', 'Acc2', 'Curr', 'Press', 'Temp', 'TCouple', 'Volt', 'Flow']

    sns.heatmap(corr_normal, ax=ax1, cmap='mako', annot=True, fmt='.2f', cbar=False,
                xticklabels=short_cols, yticklabels=short_cols,
                annot_kws={"size": 9, "color": "white"})
    ax1.set_title("[정상 상태] 8개 센서 간 상관관계 매트릭스", color='#5eead4', fontsize=14, fontweight='bold', pad=12)

    sns.heatmap(corr_anom, ax=ax2, cmap='rocket', annot=True, fmt='.2f', cbar=True,
                xticklabels=short_cols, yticklabels=short_cols,
                annot_kws={"size": 9, "color": "white"})
    ax2.set_title("[이상 발생 상태] 8개 센서 간 상관관계 붕괴", color='#f87171', fontsize=14, fontweight='bold', pad=12)

    plt.suptitle("SKAB 워터 루프 테스트베드 정상 vs 결함 발생 시 센서 상관관계 구조 변화", color='#f8fafc', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    chart1_path = os.path.join(BASE_DIR, "chart_eda_correlation.png")
    plt.savefig(chart1_path, dpi=200, facecolor='#15171b')
    plt.close()
    print(f"   -> 저장 완료: {chart1_path}")

    # 5. Chart 2: Normal Baseline Sensor Time-Series (First 1,000 seconds)
    print("\n5. 정상 상태 시계열 트렌드 차트 생성 중...")
    fig, axes = plt.subplots(4, 2, figsize=(16, 10), facecolor='#15171b')
    axes = axes.flatten()

    colors = ['#38bdf8', '#818cf8', '#fbbf24', '#34d399', '#f472b6', '#a78bfa', '#fb923c', '#4ade80']
    sample_normal = df_normal.iloc[:1000]

    for idx, col in enumerate(SENSOR_COLS):
        ax = axes[idx]
        ax.set_facecolor('#1c1f24')
        ax.plot(sample_normal[col].values, color=colors[idx], linewidth=1.2, alpha=0.9)
        ax.set_title(f"{col} (Normal Baseline)", color='#e2e8f0', fontsize=11, fontweight='bold', loc='left')
        ax.grid(True, color='#2b2f37', linestyle=':', alpha=0.6)
        ax.tick_params(colors='#94a3b8', labelsize=9)

    plt.suptitle("SKAB 정상 운전(anomaly-free) 8개 다변량 센서 베이스라인 시계열 (1,000초 관측)", color='#5eead4', fontsize=16, fontweight='bold')
    plt.tight_layout()
    chart2_path = os.path.join(BASE_DIR, "chart_eda_sensor_trends.png")
    plt.savefig(chart2_path, dpi=200, facecolor='#15171b')
    plt.close()
    print(f"   -> 저장 완료: {chart2_path}")

    # 6. Chart 3: Anomaly Breakdown Case Study (valve1/0.csv - Valve closure fault)
    print("\n6. 결함 시나리오 왜곡 분석 차트 (valve1/0.csv) 생성 중...")
    df_sample_fault = pd.read_csv(os.path.join(VALVE1_DIR, "0.csv"), sep=';')
    
    fig, axes = plt.subplots(4, 1, figsize=(15, 11), facecolor='#15171b', sharex=True)
    
    # Anomaly region mask
    anom_mask = df_sample_fault['anomaly'] == 1.0
    
    # Key sensors for valve closure: Pressure, Flow Rate, Accelerometer1RMS, Current
    key_plots = [
        ('Pressure', '#38bdf8', '배관 내부 압력 (Pressure, bar)'),
        ('Volume Flow RateRMS', '#34d399', '유체 유량 (Volume Flow Rate, L/min)'),
        ('Accelerometer1RMS', '#f87171', '모터 펌프 진동 가속도 (Accelerometer1RMS, g)'),
        ('Current', '#fbbf24', '인버터 공급 전류 (Current, A)')
    ]

    for ax, (sensor, color, label) in zip(axes, key_plots):
        ax.set_facecolor('#1c1f24')
        ax.plot(df_sample_fault[sensor], color=color, linewidth=1.5, label=label)
        
        # Shade anomaly regions
        ax.fill_between(range(len(df_sample_fault)), 
                        df_sample_fault[sensor].min(), 
                        df_sample_fault[sensor].max(), 
                        where=anom_mask, color='#dc2626', alpha=0.25, label='실제 결함 구간 (Anomaly=1)')
        
        # Mark changepoint
        cps = df_sample_fault[df_sample_fault['changepoint'] == 1.0].index
        for cp in cps:
            ax.axvline(x=cp, color='#facc15', linestyle='--', linewidth=1.8, alpha=0.9, label='결함 시작/전이 시점 (Changepoint)')
            
        ax.set_ylabel(sensor, color='#e2e8f0', fontsize=10, fontweight='bold')
        ax.grid(True, color='#2b2f37', linestyle=':', alpha=0.6)
        ax.tick_params(colors='#94a3b8', labelsize=9)
        
        # Avoid duplicate legend handles
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right', facecolor='#1e2228', edgecolor='#334155', fontsize=9, labelcolor='#e2e8f0')

    axes[-1].set_xlabel("시간 스텝 (초, Time Step)", color='#cbd5e1', fontsize=11)
    plt.suptitle("SKAB 밸브 폐쇄 결함 시나리오(valve1/0.csv) 센서 신호 왜곡 및 결함 구간 시각화", color='#f87171', fontsize=15, fontweight='bold')
    plt.tight_layout()
    chart3_path = os.path.join(BASE_DIR, "chart_eda_normal_vs_anomaly.png")
    plt.savefig(chart3_path, dpi=200, facecolor='#15171b')
    plt.close()
    print(f"   -> 저장 완료: {chart3_path}")

    # 7. Save EDA summary to JSON
    eda_summary = {
        "dataset_name": "SKAB (Skoltech Anomaly Benchmark)",
        "normal_samples": len(df_normal),
        "anomaly_benchmark_files": len(anomaly_files),
        "total_test_samples": total_samples,
        "total_anomaly_points": total_anomalies,
        "anomaly_rate_pct": round(total_anomalies / total_samples * 100, 2),
        "sensor_features": SENSOR_COLS,
        "normal_vs_anom_comparison": comp_df.to_dict()
    }
    
    json_path = os.path.join(BASE_DIR, "eda_summary.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(eda_summary, f, indent=4, ensure_ascii=False)
    print(f"\n7. EDA 요약 메타데이터 저장 완료: {json_path}")
    print("=" * 70)
    print(" [Step 1] EDA 성공적으로 완료되었습니다!")
    print("=" * 70)

if __name__ == '__main__':
    run_eda()
