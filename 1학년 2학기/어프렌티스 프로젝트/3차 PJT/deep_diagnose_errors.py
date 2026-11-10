import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve, auc
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"g:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
SKAB_DATA_DIR = os.path.join(BASE_DIR, "SKAB", "data")
NORMAL_PATH = os.path.join(SKAB_DATA_DIR, "anomaly-free", "anomaly-free.csv")
VALVE1_DIR = os.path.join(SKAB_DATA_DIR, "valve1")
VALVE2_DIR = os.path.join(SKAB_DATA_DIR, "valve2")
OTHER_DIR = os.path.join(SKAB_DATA_DIR, "other")

BASE_SENSOR_COLS = [
    'Accelerometer1RMS',
    'Accelerometer2RMS',
    'Current',
    'Pressure',
    'Temperature',
    'Thermocouple',
    'Voltage',
    'Volume Flow RateRMS'
]

def main():
    print("=== Diagnosing Error Modes by Scenario Type ===")
    df_normal = pd.read_csv(NORMAL_PATH, sep=';', parse_dates=['datetime'], index_col='datetime')
    scaler = RobustScaler().fit(df_normal[BASE_SENSOR_COLS])
    
    # Load all files individually
    categories = {'valve1': [], 'valve2': [], 'other': []}
    for i in range(4, 16):
        categories['valve1'].append((f"valve1_{i}", os.path.join(VALVE1_DIR, f"{i}.csv")))
    for f in sorted(os.listdir(VALVE2_DIR)):
        if f.endswith('.csv'):
            categories['valve2'].append((f"valve2_{f}", os.path.join(VALVE2_DIR, f)))
    for f in sorted(os.listdir(OTHER_DIR)):
        if f.endswith('.csv'):
            categories['other'].append((f"other_{f}", os.path.join(OTHER_DIR, f)))
            
    print(f"Test files: valve1={len(categories['valve1'])}, valve2={len(categories['valve2'])}, other={len(categories['other'])}")

    # Check anomaly distribution per category
    for cat, flist in categories.items():
        total_len = 0
        total_anom = 0
        for name, fp in flist:
            df = pd.read_csv(fp, sep=';')
            total_len += len(df)
            total_anom += df['anomaly'].sum()
        print(f"Category [{cat}]: Total Samples = {total_len}, Anomaly Ratio = {total_anom / total_len * 100:.2f}%")

if __name__ == '__main__':
    main()
