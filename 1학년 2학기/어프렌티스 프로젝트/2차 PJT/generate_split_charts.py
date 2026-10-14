#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import numpy as np
import matplotlib.pyplot as plt

with open('experiment_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

base = data['base_comparison']
ablation = data['ablation_lookback']

plt.style.use('dark_background')

# Chart 1: Predictions
fig, ax1 = plt.subplots(figsize=(8.2, 4.3), facecolor='#22252b')
ax1.set_facecolor('#22252b')
trues = base['lstm']['trues'][:120]
rnn_p = base['rnn']['preds'][:120]
lstm_p = base['lstm']['preds'][:120]
gru_p = base['gru']['preds'][:120]

ax1.plot(trues, label='Actual OT (°C)', color='#ffffff', linewidth=2.4, alpha=0.95)
ax1.plot(rnn_p, label='RNN (MSE: ' + str(base['rnn']['MSE']) + ')', color='#f87171', linestyle='--', linewidth=1.5)
ax1.plot(lstm_p, label='LSTM (MSE: ' + str(base['lstm']['MSE']) + ')', color='#38bdf8', linestyle='-', linewidth=1.8)
ax1.plot(gru_p, label='GRU (MSE: ' + str(base['gru']['MSE']) + ')', color='#4fd1c5', linestyle='-.', linewidth=1.8)
ax1.set_title('Test Set OT Forecasting Trajectory (120 Hours)', color='#5eead4', fontsize=12, fontweight='bold', pad=10)
ax1.set_xlabel('Time Steps (Hours)', color='#c8cdd6', fontsize=10)
ax1.set_ylabel('Oil Temperature (°C)', color='#c8cdd6', fontsize=10)
ax1.set_ylim(0, 15.0)
ax1.legend(loc='upper left', framealpha=0.85, facecolor='#15171b', edgecolor='#4fd1c5', fontsize=9.5)
ax1.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)
plt.tight_layout()
plt.savefig('chart_predictions.png', dpi=200, facecolor='#22252b')
plt.close()

# Chart 2: Ablation Bar
fig, ax2 = plt.subplots(figsize=(8.2, 4.3), facecolor='#22252b')
ax2.set_facecolor('#22252b')
lbs = ['12', '24', '48']
x = np.arange(len(lbs))
w = 0.25

rnn_m = [ablation[lb]['rnn']['MAE'] for lb in lbs]
lstm_m = [ablation[lb]['lstm']['MAE'] for lb in lbs]
gru_m = [ablation[lb]['gru']['MAE'] for lb in lbs]

ax2.bar(x - w, rnn_m, w, label='Vanilla RNN', color='#f87171', alpha=0.85)
ax2.bar(x, lstm_m, w, label='LSTM', color='#38bdf8', alpha=0.85)
ax2.bar(x + w, gru_m, w, label='GRU', color='#4fd1c5', alpha=0.85)

for i in range(len(lbs)):
    ax2.text(x[i] - w, rnn_m[i] + 0.006, f'{rnn_m[i]:.3f}', ha='center', va='bottom', color='#fca5a5', fontsize=8.5, fontweight='bold')
    ax2.text(x[i], lstm_m[i] + 0.006, f'{lstm_m[i]:.3f}', ha='center', va='bottom', color='#7dd3fc', fontsize=8.5, fontweight='bold')
    ax2.text(x[i] + w, gru_m[i] + 0.006, f'{gru_m[i]:.3f}', ha='center', va='bottom', color='#5eead4', fontsize=8.5, fontweight='bold')

ax2.set_xticks(x)
ax2.set_xticklabels([f'Lookback {lb}h' for lb in lbs], color='#c8cdd6', fontsize=10.5)
ax2.set_ylim(0.35, 0.60)
ax2.set_title('Ablation Study: Lookback Window vs MAE (Lower is Better)', color='#5eead4', fontsize=12, fontweight='bold', pad=10)
ax2.set_xlabel('Input Sequence Length (Lookback Window)', color='#c8cdd6', fontsize=10)
ax2.set_ylabel('Test MAE', color='#c8cdd6', fontsize=10)
ax2.legend(loc='upper left', framealpha=0.4, facecolor='#15171b', edgecolor='#4fd1c5', fontsize=9)
ax2.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)
plt.tight_layout()
plt.savefig('chart_ablation.png', dpi=200, facecolor='#22252b')
plt.close()
print('Individual charts generated successfully!')
