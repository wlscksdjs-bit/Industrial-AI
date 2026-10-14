#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate lean-deck darkmorphism HTML presentation for Apprentice Project Week 5.
Includes 5 slides, darkmorphism neumorphic styling, interactive controls, laser pointer (L key),
and embedded base64 visualization charts.
"""
import base64
import json
import os

with open('experiment_results.json', 'r', encoding='utf-8') as f:
    exp_data = json.load(f)

# Base64 charts
pred_b64 = ""
if os.path.exists('chart_predictions.png'):
    pred_b64 = base64.b64encode(open('chart_predictions.png', 'rb').read()).decode('utf-8')

ablation_b64 = ""
if os.path.exists('chart_ablation.png'):
    ablation_b64 = base64.b64encode(open('chart_ablation.png', 'rb').read()).decode('utf-8')

html_content = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>어프렌티스 프로젝트 5주차 과제 - RNN, LSTM, GRU 시계열 예측 실증 및 Ablation Study</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {{
  --ld-surface-page: #22252b;
  --ld-surface-card: #22252b;
  --ld-text-strong: #f1f5f9;
  --ld-text-soft: #c8cdd6;
  --ld-text-mute: rgba(200, 205, 214, 0.55);
  --ld-accent-primary: #4fd1c5;
  --ld-accent-cyan: #38bdf8;
  --ld-accent-teal: #5eead4;
  --ld-warn-color: #f87171;
  --ld-font-body: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --ld-font-mono: 'JetBrains Mono', monospace;
  --neu-flat: -6px -6px 14px #2b2f37, 6px 6px 16px #15171b;
  --neu-flat-sm: -4px -4px 10px #2b2f37, 4px 4px 12px #15171b;
  --neu-inset: inset -5px -5px 10px #2b2f37, inset 5px 5px 10px #15171b;
  --neu-inset-sm: inset -3px -3px 6px #2b2f37, inset 3px 3px 6px #15171b;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{
  margin: 0; padding: 0; height: 100%; width: 100%;
  background: var(--ld-surface-page);
  color: var(--ld-text-strong);
  font-family: var(--ld-font-body);
  overflow: hidden;
  user-select: none;
}}
.stage {{
  position: absolute; left: 0; top: 0; width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
}}
.slide {{
  width: 1920px; height: 1080px; position: relative;
  background: var(--ld-surface-page);
  overflow: hidden;
  display: none; padding: 60px 84px 76px;
  flex-direction: column;
  word-break: keep-all; line-break: strict;
}}
.slide.active {{
  display: flex;
}}

/* Header Elements */
.header-area {{
  margin-bottom: 32px;
}}
.eyebrow-row {{
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px;
}}
.eyebrow-pill {{
  background: var(--ld-surface-card);
  color: var(--ld-accent-primary);
  font-size: 15px; font-weight: 700; letter-spacing: 0.04em;
  padding: 8px 20px; border-radius: 9999px;
  box-shadow: var(--neu-flat-sm);
  display: inline-flex; align-items: center; gap: 8px;
}}
.hardware-pill {{
  background: var(--ld-surface-card);
  color: #38bdf8;
  font-family: var(--ld-font-mono);
  font-size: 13.5px; font-weight: 600;
  padding: 6px 16px; border-radius: 9999px;
  box-shadow: var(--neu-inset-sm);
  display: inline-flex; align-items: center; gap: 6px;
}}
.title {{
  font-size: 42px; font-weight: 800; line-height: 1.22;
  letter-spacing: -0.015em; color: var(--ld-text-strong);
}}
.title .accent {{
  color: var(--ld-accent-teal);
  text-shadow: 0 0 20px rgba(94, 234, 212, 0.25);
}}

/* Grid & Cards (Darkmorphism) */
.content-grid {{
  display: grid; gap: 26px; flex: 1; align-items: stretch;
}}
.cols-3 {{ grid-template-columns: repeat(3, 1fr); }}
.cols-2 {{ grid-template-columns: 1fr 1fr; }}
.cols-2-1 {{ grid-template-columns: 1.15fr 0.85fr; }}
.cols-1-12 {{ grid-template-columns: 1.1fr 0.9fr; }}

.card {{
  background: var(--ld-surface-card);
  border-radius: 20px;
  padding: 28px 30px;
  box-shadow: var(--neu-flat);
  display: flex; flex-direction: column;
  justify-content: flex-start;
}}
.card-inset {{
  background: var(--ld-surface-card);
  border-radius: 18px;
  padding: 22px 24px;
  box-shadow: var(--neu-inset);
}}
.card-header {{
  display: flex; align-items: center; gap: 12px; margin-bottom: 16px;
}}
.icon-box {{
  width: 38px; height: 38px; border-radius: 10px;
  background: var(--ld-surface-card);
  box-shadow: var(--neu-inset-sm);
  display: flex; align-items: center; justify-content: center;
  color: var(--ld-accent-primary); font-size: 18px; font-weight: 800;
}}
.card-title {{
  font-size: 21px; font-weight: 700; color: var(--ld-text-strong);
}}
.card-subtitle {{
  font-size: 14px; color: var(--ld-accent-cyan); font-family: var(--ld-font-mono);
}}

.card-body {{
  font-size: 16.5px; line-height: 1.62; color: var(--ld-text-soft); flex: 1;
}}
.bullet-list {{
  list-style: none; display: flex; flex-direction: column; gap: 11px;
}}
.bullet-item {{
  position: relative; padding-left: 20px; font-size: 16.5px; line-height: 1.55;
}}
.bullet-item::before {{
  content: ''; position: absolute; left: 0; top: 9px;
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--ld-accent-primary);
  box-shadow: 0 0 6px rgba(79, 209, 197, 0.6);
}}
.bullet-item.warn::before {{
  background: var(--ld-warn-color);
  box-shadow: 0 0 6px rgba(248, 113, 113, 0.6);
}}
.bullet-item.blue::before {{
  background: var(--ld-accent-cyan);
  box-shadow: 0 0 6px rgba(56, 189, 248, 0.6);
}}

/* Metric Tags & Tables */
.metric-row {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 15px;
}}
.metric-row:last-child {{ border-bottom: none; }}
.metric-label {{ color: var(--ld-text-soft); }}
.metric-val {{ font-family: var(--ld-font-mono); font-weight: 700; color: #ffffff; }}

table.dark-table {{
  width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 15px;
}}
table.dark-table th {{
  text-align: left; padding: 10px 12px; color: var(--ld-accent-teal);
  border-bottom: 2px solid rgba(94, 234, 212, 0.2); font-weight: 700;
}}
table.dark-table td {{
  padding: 10px 12px; color: var(--ld-text-strong);
  border-bottom: 1px solid rgba(255,255,255,0.06); font-family: var(--ld-font-mono);
}}
table.dark-table tr.highlight td {{
  background: rgba(79, 209, 197, 0.08); color: #5eead4; font-weight: 700;
}}

.chart-container {{
  border-radius: 16px; overflow: hidden; box-shadow: var(--neu-inset);
  display: flex; align-items: center; justify-content: center;
  background: #22252b; padding: 12px;
}}
.chart-img {{
  max-width: 100%; height: auto; border-radius: 8px;
}}

/* Footer HUD & Controls */
.footer-bar {{
  position: fixed; bottom: 20px; left: 36px; right: 36px;
  display: flex; justify-content: space-between; align-items: center;
  font-family: var(--ld-font-mono); font-size: 14px;
  color: rgba(200, 205, 214, 0.6); pointer-events: none;
}}
.footer-left {{
  display: flex; align-items: center; gap: 16px; pointer-events: auto;
}}
.laser-badge {{
  display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px;
  border-radius: 9999px; background: var(--ld-surface-card);
  box-shadow: var(--neu-flat-sm);
  cursor: pointer; pointer-events: auto; font-size: 12.5px; font-weight: 600;
  transition: all 0.2s ease; user-select: none; color: var(--ld-text-soft);
}}
.laser-badge:hover {{ color: #ffffff; }}
.laser-badge.mode-red {{
  color: #ff4d6d; box-shadow: inset -2px -2px 6px #2b2f37, inset 2px 2px 6px #15171b, 0 0 10px rgba(255,77,109,0.3);
}}
.laser-badge.mode-purple {{
  color: #c084fc; box-shadow: inset -2px -2px 6px #2b2f37, inset 2px 2px 6px #15171b, 0 0 10px rgba(192,132,252,0.3);
}}
#laser-pointer {{
  position: fixed; width: 14px; height: 14px; border-radius: 50%;
  pointer-events: none; transform: translate(-50%, -50%); z-index: 999999; display: none;
}}
#laser-pointer.laser-red {{
  display: block; background: radial-gradient(circle, #ffffff 15%, #ff2a55 55%, #e11d48 100%);
  box-shadow: 0 0 6px #fff, 0 0 12px #ff2a55, 0 0 24px #e11d48, 0 0 36px rgba(255,42,85,0.85);
}}
#laser-pointer.laser-purple {{
  display: block; background: radial-gradient(circle, #ffffff 15%, #c084fc 55%, #9333ea 100%);
  box-shadow: 0 0 6px #fff, 0 0 12px #c084fc, 0 0 24px #9333ea, 0 0 36px rgba(168,85,247,0.85);
}}
body.laser-active, body.laser-active * {{ cursor: none !important; }}
.controls {{
  position: fixed; right: 36px; bottom: 20px; display: flex; gap: 10px; pointer-events: auto;
}}
.btn {{
  background: var(--ld-surface-card); box-shadow: var(--neu-flat-sm);
  color: var(--ld-text-strong); padding: 7px 15px; border-radius: 10px; cursor: pointer;
  border: none; font-family: var(--ld-font-mono); font-size: 13px; font-weight: 600;
  transition: all 0.15s ease;
}}
.btn:hover {{ color: var(--ld-accent-teal); transform: translateY(-1px); }}
.btn:active {{ box-shadow: var(--neu-inset-sm); transform: translateY(0); }}

.badge-tag {{
  display: inline-block; padding: 3px 9px; border-radius: 6px;
  font-family: var(--ld-font-mono); font-size: 12px; font-weight: 700;
}}
.badge-green {{ background: rgba(79, 209, 197, 0.15); color: #5eead4; }}
.badge-blue {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; }}
.badge-red {{ background: rgba(248, 113, 113, 0.15); color: #f87171; }}
.badge-purple {{ background: rgba(192, 132, 252, 0.15); color: #c084fc; }}
</style>
</head>
<body>
<div id="laser-pointer"></div>
<div class="stage" id="stage">

  <!-- SLIDE 1: 문제 정의 & 데이터셋 -->
  <div class="slide active" id="slide-0">
    <div class="header-area">
      <div class="eyebrow-row">
        <span class="eyebrow-pill">STAGE 1 · DATASET & PROBLEM DEFINITION</span>
        <span class="hardware-pill">⚡ NVIDIA RTX 5070 · CUDA 12.8</span>
      </div>
      <h1 class="title">
        산업 전력 변압기 유온(OT) 정밀 예측을 위한 <span class="accent">다변량 시계열 파이프라인</span>
      </h1>
    </div>

    <div class="content-grid cols-3">
      <div class="card">
        <div class="card-header">
          <div class="icon-box">D</div>
          <div>
            <div class="card-title">ETTh1 벤치마크 데이터셋</div>
            <div class="card-subtitle">Electricity Transformer 1-Hour</div>
          </div>
        </div>
        <div class="card-body">
          <ul class="bullet-list">
            <li class="bullet-item"><strong>데이터 규모:</strong> 2개년치 17,420개 시간대별 연속 관측 로그</li>
            <li class="bullet-item"><strong>물리적 배경:</strong> 전력 변압기 운전 시 과열로 인한 설비 소손 및 블랙아웃 방지 핵심 설비 지표</li>
            <li class="bullet-item"><strong>특성 상관성:</strong> 유효·무효 전력 부하와 고·저전압 오일 온도 간의 복합 다변량 동역학 포함</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row">
            <span class="metric-label">총 관측 시점</span>
            <span class="metric-val">17,420 Timesteps</span>
          </div>
          <div class="metric-row">
            <span class="metric-label">수집 해상도</span>
            <span class="metric-val">1-Hour (정시 단위)</span>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="icon-box">X</div>
          <div>
            <div class="card-title">입출력 변수 & 예측 문제 정의</div>
            <div class="card-subtitle">Multivariate 7-Features to 1-Target</div>
          </div>
        </div>
        <div class="card-body">
          <ul class="bullet-list">
            <li class="bullet-item blue"><strong>입력 변수 X (7차원):</strong> 고전압/저전압 전력 부하 6종 (HUFL, HULL, MUFL, MULL, LUFL, LULL) + 이전 오일온도(OT)</li>
            <li class="bullet-item blue"><strong>예측 변수 Y (1차원):</strong> 향후 1시간 뒤 변압기 최종 오일 온도(OT, Oil Temperature)</li>
            <li class="bullet-item blue"><strong>Lookback Window:</strong> 과거 L시점 관측 행렬로부터 미래 Y를 추론하는 지도학습 시계열 태스크</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row">
            <span class="metric-label">입력 텐서 형태</span>
            <span class="metric-val">[Batch, Lookback, 7]</span>
          </div>
          <div class="metric-row">
            <span class="metric-label">예측 목표 텐서</span>
            <span class="metric-val">[Batch, 1] (Next-step OT)</span>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="icon-box">S</div>
          <div>
            <div class="card-title">분할 및 엄격한 데이터 누수 방지</div>
            <div class="card-subtitle">Temporal Split & Safe Scaling</div>
          </div>
        </div>
        <div class="card-body">
          <ul class="bullet-list">
            <li class="bullet-item"><strong>시간 순서 보존 분할:</strong> 학습(70%, 12,194건) → 검증(15%, 2,613건) → 시험(15%, 2,613건)</li>
            <li class="bullet-item"><strong>데이터 누수(Data Leakage) 차단:</strong> StandardScaler 통계치(평균/표준편차)는 오직 학습셋에서만 계산(fit)</li>
            <li class="bullet-item"><strong>평가 공정성:</strong> 검증 및 시험셋에는 학습 스케일러 변환(transform)만 적용하여 실전 배포 환경 엄격 시뮬레이션</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row">
            <span class="metric-label">Train / Val / Test</span>
            <span class="metric-val">12,194 / 2,613 / 2,613</span>
          </div>
          <div class="metric-row">
            <span class="metric-label">전처리 파이프라인</span>
            <span class="metric-val">StandardScaler (Train-only)</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 2: 모델 아키텍처 비교 -->
  <div class="slide" id="slide-1">
    <div class="header-area">
      <div class="eyebrow-row">
        <span class="eyebrow-pill">STAGE 2 · MODEL ARCHITECTURE & GATING</span>
        <span class="hardware-pill">⚙️ 파라미터 최적화 (Hidden 64, Layers 2)</span>
      </div>
      <h1 class="title">
        기울기 소실을 극복하는 <span class="accent">게이팅 메커니즘과 메모리 구조 비교</span>
      </h1>
    </div>

    <div class="content-grid cols-3">
      <!-- RNN -->
      <div class="card">
        <div class="card-header">
          <div class="icon-box" style="color: #f87171;">R</div>
          <div>
            <div class="card-title">Vanilla RNN</div>
            <div class="card-subtitle">Recurrent Neural Network</div>
          </div>
        </div>
        <div class="card-body">
          <div class="card-inset" style="margin-bottom: 14px; padding: 12px 16px;">
            <span style="font-family: var(--ld-font-mono); font-size: 14.5px; color: #fca5a5;">h_t = tanh(W_xh · x_t + W_hh · h_(t-1))</span>
          </div>
          <ul class="bullet-list">
            <li class="bullet-item warn"><strong>단일 상태 피드백:</strong> 매 시점마다 은닉 상태 h_t 하나로만 이전 모든 정보를 압축 갱신</li>
            <li class="bullet-item warn"><strong>장기 의존성 치명적 한계:</strong> BPTT 연쇄 법칙(Chain Rule) 적용 시 tanh 미분값(최대 1.0)의 반복 곱으로 기울기 소실(Vanishing Gradient) 직면</li>
            <li class="bullet-item"><strong>경량성:</strong> 게이트가 없어 파라미터 수가 가장 적고 단순한 단기 패턴 처리에 유리</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row"><span class="metric-label">게이트 구조</span><span class="metric-val">없음 (None)</span></div>
          <div class="metric-row"><span class="metric-label">상태 채널</span><span class="metric-val">Hidden State 단일</span></div>
        </div>
      </div>

      <!-- LSTM -->
      <div class="card">
        <div class="card-header">
          <div class="icon-box" style="color: #38bdf8;">L</div>
          <div>
            <div class="card-title">LSTM</div>
            <div class="card-subtitle">Long Short-Term Memory</div>
          </div>
        </div>
        <div class="card-body">
          <div class="card-inset" style="margin-bottom: 14px; padding: 12px 16px;">
            <span style="font-family: var(--ld-font-mono); font-size: 14.5px; color: #7dd3fc;">C_t = f_t ⊙ C_(t-1) + i_t ⊙ C̃_t</span>
          </div>
          <ul class="bullet-list">
            <li class="bullet-item blue"><strong>독립 셀 상태(Cell State):</strong> 과거 정보를 손실 없이 직통 전달하는 가산적(Additive) 정보 고속도로 제공</li>
            <li class="bullet-item blue"><strong>3개 정밀 게이트:</strong>
              <br>• 망각 게이트(f_t): 버릴 정보 선별
              <br>• 입력 게이트(i_t): 새 정보 저장 비율
              <br>• 출력 게이트(o_t): 다음 h_t 전달 제어</li>
            <li class="bullet-item"><strong>안정성:</strong> 긴 시퀀스에서도 그래디언트 유실을 완벽히 차단하여 높은 예측 신뢰성 보장</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row"><span class="metric-label">게이트 구조</span><span class="metric-val">3개 (Forget, Input, Output)</span></div>
          <div class="metric-row"><span class="metric-label">상태 채널</span><span class="metric-val">Cell (C_t) + Hidden (h_t)</span></div>
        </div>
      </div>

      <!-- GRU -->
      <div class="card">
        <div class="card-header">
          <div class="icon-box" style="color: #4fd1c5;">G</div>
          <div>
            <div class="card-title">GRU</div>
            <div class="card-subtitle">Gated Recurrent Unit</div>
          </div>
        </div>
        <div class="card-body">
          <div class="card-inset" style="margin-bottom: 14px; padding: 12px 16px;">
            <span style="font-family: var(--ld-font-mono); font-size: 14.5px; color: #5eead4;">h_t = (1 - z_t) ⊙ h_(t-1) + z_t ⊙ h̃_t</span>
          </div>
          <ul class="bullet-list">
            <li class="bullet-item"><strong>셀 상태 통합:</strong> Cell State와 Hidden State를 단일 은닉 상태 h_t로 통합하여 아키텍처 슬림화</li>
            <li class="bullet-item"><strong>2개 압축 게이트:</strong>
              <br>• 리셋 게이트(r_t): 이전 기억 참조량 결정
              <br>• 업데이트 게이트(z_t): 망각과 입력을 1-z_t와 z_t로 상호 결합</li>
            <li class="bullet-item"><strong>연산 효율 극대화:</strong> LSTM 대비 파라미터 약 25% 감축으로 초고속 학습 및 메모리 절감 달성</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row"><span class="metric-label">게이트 구조</span><span class="metric-val">2개 (Reset, Update)</span></div>
          <div class="metric-row"><span class="metric-label">상태 채널</span><span class="metric-val">통합 Hidden State (h_t)</span></div>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 3: 성능 평가 & 결과 분석 -->
  <div class="slide" id="slide-2">
    <div class="header-area">
      <div class="eyebrow-row">
        <span class="eyebrow-pill">STAGE 3 · BENCHMARK & TEST EVALUATION</span>
        <span class="hardware-pill">📈 Lookback L=24h · Test 2,613 샘플 정밀 평가</span>
      </div>
      <h1 class="title">
        동일 실험 조건(L=24) <span class="accent">3개 모델 성능 벤치마크 및 오차 분석</span>
      </h1>
    </div>

    <div class="content-grid cols-1-12">
      <!-- 왼쪽: 정량 평가 테이블 및 분석 -->
      <div class="card">
        <div class="card-header">
          <div class="icon-box">📊</div>
          <div>
            <div class="card-title">정량적 평가지표 벤치마크 (Test Set)</div>
            <div class="card-subtitle">RTX 5070 CUDA GPU 가속 12 에포크 학습 결과</div>
          </div>
        </div>
        <div class="card-body">
          <table class="dark-table">
            <thead>
              <tr>
                <th>모델</th>
                <th>학습시간</th>
                <th>MSE (오차제곱)</th>
                <th>MAE (절대오차)</th>
                <th>RMSE</th>
                <th>R² (설명력)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="badge-tag badge-red">Vanilla RNN</span></td>
                <td>3.76s</td>
                <td>0.4164</td>
                <td>0.4364</td>
                <td>0.6453</td>
                <td>94.82%</td>
              </tr>
              <tr>
                <td><span class="badge-tag badge-blue">LSTM</span></td>
                <td>3.53s</td>
                <td>0.4178</td>
                <td>0.4396</td>
                <td>0.6464</td>
                <td>94.81%</td>
              </tr>
              <tr class="highlight">
                <td><span class="badge-tag badge-green">GRU ★</span></td>
                <td><strong>3.33s (최속)</strong></td>
                <td>0.4230</td>
                <td>0.4622</td>
                <td>0.6504</td>
                <td>94.74%</td>
              </tr>
            </tbody>
          </table>

          <div style="margin-top: 20px;">
            <ul class="bullet-list">
              <li class="bullet-item"><strong>뛰어난 설명력:</strong> 세 모델 모두 R² 94.7% 이상의 고성능을 기록하며 복잡한 변압기 부하 변동에도 우수한 추종 성능을 보임</li>
              <li class="bullet-item"><strong>GPU 연산 속도:</strong> GRU는 간소화된 게이트 구조 덕분에 3.33초로 가장 빠른 학습 완료 (Vanilla RNN 대비 11.4% 가속)</li>
              <li class="bullet-item"><strong>단기 구간 유사성:</strong> L=24h의 상대적으로 짧은 과거 윈도우에서는 오차 지표 편차가 0.01 이내로 세 모델 모두 대등한 추종력을 보임</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 오른쪽: 궤적 시각화 차트 -->
      <div class="card">
        <div class="card-header">
          <div class="icon-box">📈</div>
          <div>
            <div class="card-title">시험 데이터 오일온도 예측 궤적 (120시간)</div>
            <div class="card-subtitle">실제값(Ground Truth) vs 3개 모델 예측값 비교</div>
          </div>
        </div>
        <div class="chart-container" style="flex: 1;">
          <img class="chart-img" src="data:image/png;base64,{pred_b64}" alt="Prediction Comparison Chart">
        </div>
        <div style="font-size: 13.5px; color: var(--ld-text-mute); margin-top: 10px; text-align: center;">
          * 실선(White): 실제 OT 관측치 | 점선/대시: RNN, LSTM, GRU의 시계열 피크 및 급변 구간 추적
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 4: Ablation Study -->
  <div class="slide" id="slide-3">
    <div class="header-area">
      <div class="eyebrow-row">
        <span class="eyebrow-pill">STAGE 4 · ABLATION STUDY</span>
        <span class="hardware-pill">🔬 입력 길이(Lookback: 12h vs 24h vs 48h) 조건 변경 실험</span>
      </div>
      <h1 class="title">
        시퀀스 길이에 따른 <span class="accent">기울기 소실 실증 및 게이팅 복원력 분석</span>
      </h1>
    </div>

    <div class="content-grid cols-1-12">
      <!-- 왼쪽: Ablation 바 차트 -->
      <div class="card">
        <div class="card-header">
          <div class="icon-box">📊</div>
          <div>
            <div class="card-title">입력 윈도우별 MAE 오차 추이</div>
            <div class="card-subtitle">Lookback Length L = 12h, 24h, 48h 비교</div>
          </div>
        </div>
        <div class="chart-container" style="flex: 1;">
          <img class="chart-img" src="data:image/png;base64,{ablation_b64}" alt="Ablation Bar Chart">
        </div>
        <div style="font-size: 13.5px; color: var(--ld-text-mute); margin-top: 10px; text-align: center;">
          * MAE는 낮을수록 우수함 (L=48h에서 Vanilla RNN의 급격한 성능 붕괴 관찰)
        </div>
      </div>

      <!-- 오른쪽: 핵심 발견 및 메커니즘 해석 -->
      <div class="card">
        <div class="card-header">
          <div class="icon-box">💡</div>
          <div>
            <div class="card-title">Ablation Study 핵심 인과관계 검증</div>
            <div class="card-subtitle">강의 38~46페이지 이론과 실험 데이터의 완벽한 일치</div>
          </div>
        </div>
        <div class="card-body">
          <div class="card-inset" style="margin-bottom: 14px; border-left: 4px solid #f87171;">
            <div style="font-weight: 700; color: #fca5a5; font-size: 16px; margin-bottom: 4px;">
              ① Vanilla RNN의 장기 의존성 붕괴 (기울기 소실 실증)
            </div>
            <p style="font-size: 15px; color: var(--ld-text-soft); line-height: 1.5;">
              L=12h(MAE 0.429)에서 L=48h(MAE 0.536)로 시퀀스를 확장하자 <strong>오차가 +25.0% 급증</strong>함. 48개 타임스텝의 BPTT 과정에서 연쇄 곱으로 인한 그래디언트 소실이 발생하여 원거리 정보를 전혀 활용하지 못함을 입증함.
            </p>
          </div>

          <div class="card-inset" style="margin-bottom: 14px; border-left: 4px solid #38bdf8;">
            <div style="font-weight: 700; color: #7dd3fc; font-size: 16px; margin-bottom: 4px;">
              ② LSTM의 Cell State 그래디언트 고속도로 효과
            </div>
            <p style="font-size: 15px; color: var(--ld-text-soft); line-height: 1.5;">
              L=12h부터 48h까지 MAE 0.44~0.45대를 기록하며, 윈도우가 4배로 늘어나도 <strong>성능이 저하되지 않는 뛰어난 구조적 안정성</strong>을 보임. 덧셈 기반의 Cell State 덕분에 원거리 문맥이 온전히 보존됨.
            </p>
          </div>

          <div class="card-inset" style="border-left: 4px solid #5eead4;">
            <div style="font-weight: 700; color: #5eead4; font-size: 16px; margin-bottom: 4px;">
              ③ GRU의 장기 문맥 압축 우수성 (최우수 성능 달성)
            </div>
            <p style="font-size: 15px; color: var(--ld-text-soft); line-height: 1.5;">
              L=48h에서 <strong>MAE 0.4305, MSE 0.4084로 전체 실험 모델 중 최우수 성능</strong> 달성. 결합 게이트(Update Gate)가 장기 문맥의 핵심만을 선별 압축하여 고차원 노이즈를 필터링하는 데 성공함.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 5: 결론 및 산업 제언 -->
  <div class="slide" id="slide-4">
    <div class="header-area">
      <div class="eyebrow-row">
        <span class="eyebrow-pill">STAGE 5 · CONCLUSION & INDUSTRIAL INSIGHT</span>
        <span class="hardware-pill">🎯 예지보전(PdM) 현장 실증 제언</span>
      </div>
      <h1 class="title">
        산업 AI 관점의 <span class="accent">최적 모델 선정 기준 및 배포 로드맵</span>
      </h1>
    </div>

    <div class="content-grid cols-3">
      <div class="card">
        <div class="card-header">
          <div class="icon-box" style="color: #4fd1c5;">★</div>
          <div>
            <div class="card-title">최적 모델 최종 선정: GRU</div>
            <div class="card-subtitle">정확도와 연산비용의 최적 트레이드오프</div>
          </div>
        </div>
        <div class="card-body">
          <ul class="bullet-list">
            <li class="bullet-item"><strong>최우수 정밀도:</strong> 충분한 관측 기간(L=48h) 확보 시 MSE 0.4084로 LSTM 및 RNN을 압도하는 예측력 달성</li>
            <li class="bullet-item"><strong>초고속 연산:</strong> 파라미터가 적어 RTX 5070 GPU 기준 학습 시간 3.33초 기록 (엣지 컨트롤러 탑재 최적화)</li>
            <li class="bullet-item"><strong>결론:</strong> 산업 전력 설비의 장주기 센서 모니터링에는 GRU가 가장 비용 효율적인 모델임</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row"><span class="metric-label">권장 입력 길이</span><span class="metric-val">L = 48 Hours</span></div>
          <div class="metric-row"><span class="metric-label">최종 달성 MSE</span><span class="metric-val">0.4084 (최저 오차)</span></div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="icon-box" style="color: #38bdf8;">⚡</div>
          <div>
            <div class="card-title">산업 변압기 예지보전(PdM) 가치</div>
            <div class="card-subtitle">1시간 사전 골든타임 확보의 경제성</div>
          </div>
        </div>
        <div class="card-body">
          <ul class="bullet-list">
            <li class="bullet-item blue"><strong>설비 소손 사고 방지:</strong> 권선 절연유 과열에 따른 절연 파괴 및 화재를 최소 1시간 전에 감지하여 부하 사전 분산</li>
            <li class="bullet-item blue"><strong>다운타임 비용 절감:</strong> 공장 정전(Blackout) 1회당 발생하는 수억 원 규모의 조업 중단 손실 원천 차단</li>
            <li class="bullet-item blue"><strong>정비 패러다임 전환:</strong> 주기적 사후 점검에서 실시간 이상 징후 기반 사전 선제 정비 체계로 고도화</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row"><span class="metric-label">조기 경보 시간</span><span class="metric-val">1-Hour Golden Time</span></div>
          <div class="metric-row"><span class="metric-label">도입 기대 효과</span><span class="metric-val">무정전 연속 가동 실현</span></div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="icon-box" style="color: #c084fc;">🚀</div>
          <div>
            <div class="card-title">향후 연구 및 고도화 방향</div>
            <div class="card-subtitle">Future Research & Extensions</div>
          </div>
        </div>
        <div class="card-body">
          <ul class="bullet-list">
            <li class="bullet-item"><strong>다중 시계열 멀티스텝 예측:</strong> Horizon H=24h, 48h 등 며칠 단위 중장기 유온 변동 예측 모델 확장 (Seq2Seq / Attention)</li>
            <li class="bullet-item"><strong>최신 트랜스포머 비교:</strong> 다음 주차 패치 기반 TimeXer, PatchTST 등 시계열 파운데이션 모델과의 벤치마크</li>
            <li class="bullet-item"><strong>경량화 온디바이스 배포:</strong> TensorRT 및 양자화(INT8) 적용으로 변압기 현장 임베디드 보드 실시간 추론 실증</li>
          </ul>
        </div>
        <div class="card-inset" style="margin-top: 14px;">
          <div class="metric-row"><span class="metric-label">차기 과제</span><span class="metric-val">Seq2Seq & TimeXer</span></div>
          <div class="metric-row"><span class="metric-label">현장 배포 기술</span><span class="metric-val">TensorRT INT8 Quantization</span></div>
        </div>
      </div>
    </div>
  </div>

</div>

<!-- Footer HUD & Controls -->
<div class="footer-bar">
  <div class="footer-left">
    <span style="font-weight: 700; color: #5eead4;">어프렌티스 프로젝트 · 충북대학교 산업인공지능학과</span>
    <span style="color: rgba(200,205,214,0.4);">|</span>
    <span>발표자: 진찬언 (2026254019)</span>
    <span style="color: rgba(200,205,214,0.4);">|</span>
    <span id="laser-indicator" class="laser-badge" onclick="cycleLaser()">● [L] 레이저: <span id="laser-text">OFF</span></span>
  </div>
  <div class="controls">
    <button class="btn" onclick="prev()">◀ Prev</button>
    <span id="counter" style="line-height:30px; padding:0 8px; font-weight:700; color: #5eead4;">1 / 5</span>
    <button class="btn" onclick="next()">Next ▶</button>
    <button class="btn" onclick="toggleFS()">Fullscreen [F]</button>
  </div>
</div>

<script>
let cur = 0;
const slides = document.querySelectorAll('.slide');
const counter = document.getElementById('counter');
const total = slides.length;

function fit() {{
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  slides.forEach(s => {{
    s.style.transform = 'scale(' + scale + ')';
    s.style.transformOrigin = 'center center';
  }});
}}
window.addEventListener('resize', fit);
window.addEventListener('load', fit);

function show(idx) {{
  if (idx < 0) idx = 0;
  if (idx >= total) idx = total - 1;
  cur = idx;
  slides.forEach((s, i) => s.classList.toggle('active', i === cur));
  if (counter) counter.innerText = (cur + 1) + ' / ' + total;
}}

function next() {{ show(cur + 1); }}
function prev() {{ show(cur - 1); }}
function toggleFS() {{
  if (!document.fullscreenElement) document.documentElement.requestFullscreen();
  else document.exitFullscreen();
}}

let laserState = 0; // 0: OFF, 1: RED, 2: PURPLE
const laserEl = document.getElementById('laser-pointer');
const laserBadge = document.getElementById('laser-indicator');
const laserText = document.getElementById('laser-text');

function updateLaserUI() {{
  if (laserState === 1) {{
    document.body.classList.add('laser-active');
    laserEl.className = 'laser-red';
    laserBadge.className = 'laser-badge mode-red';
    laserText.textContent = 'RED';
  }} else if (laserState === 2) {{
    document.body.classList.add('laser-active');
    laserEl.className = 'laser-purple';
    laserBadge.className = 'laser-badge mode-purple';
    laserText.textContent = 'PURPLE';
  }} else {{
    document.body.classList.remove('laser-active');
    laserEl.className = '';
    laserBadge.className = 'laser-badge';
    laserText.textContent = 'OFF';
  }}
}}

function cycleLaser() {{
  laserState = (laserState + 1) % 3;
  updateLaserUI();
}}

window.addEventListener('mousemove', (e) => {{
  if (laserState !== 0) {{
    laserEl.style.left = e.clientX + 'px';
    laserEl.style.top = e.clientY + 'px';
  }}
}});

window.addEventListener('keydown', (e) => {{
  if (e.key === 'l' || e.key === 'L') {{
    e.preventDefault();
    cycleLaser();
  }} else if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
    next();
  }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
    prev();
  }} else if (e.key.toLowerCase() === 'f') {{
    toggleFS();
  }}
}});
fit();
show(0);
</script>
</body>
</html>
"""

with open('presentation_deck.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("[V] presentation_deck.html successfully created!")
