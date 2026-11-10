# -*- coding: utf-8 -*-
import os, sys

target_path = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT\build_final_sota_deliverables.py"

with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Speech script replacements
content = content.replace(
    '"title": "다변량 산업 시계열 이상탐지 신규 SOTA 모델(DS-EEF) 설계 및 실증",',
    '"title": "다변량 산업 시계열 이상탐지 개선 모델 Y(DS-EEF) 설계 및 실증",'
)
content = content.replace(
    "기존 글로벌 SOTA 딥러닝 모델들의 구조적 한계를 규명하고 이를 뛰어넘는 새로운 모델인 '신규 발굴 SOTA: 이중 스트림 에너지-극단치 융합 신경망(DS-EEF)'을 설계·구현하였습니다.",
    "기존 글로벌 SOTA 딥러닝 모델들의 구조적 한계를 규명하고 이를 뛰어넘는 '개선 모델 Y: 이중 스트림 에너지-극단치 융합 신경망(DS-EEF)'을 설계·구현하였습니다."
)
content = content.replace(
    '"title": "2단계: 기존 SOTA의 구조적 한계 규명 및 신규 제안 DS-EEF 아키텍처",',
    '"title": "2단계: 기존 SOTA의 구조적 한계 규명 및 개선 모델 Y(DS-EEF) 아키텍처",'
)
content = content.replace(
    "이에 본 연구는 센서 간 이질성을 반영하는 독창적 아키텍처인 'DS-EEF'를 창안했습니다.",
    "이에 본 연구는 센서 간 물리적 이질성을 반영하는 독창적 아키텍처인 '개선 모델 Y(DS-EEF)'를 창안했습니다."
)
content = content.replace(
    '"action": "[레이저 포인터로 하단 벤치마크 표의 신규 SOTA 행과 타임라인 그래프 지목]",',
    '"action": "[레이저 포인터로 하단 벤치마크 표의 개선 모델 Y 행과 타임라인 그래프 지목]",'
)
content = content.replace(
    "[표의 신규 SOTA 행 지목] 본 연구가 독창적으로 설계한 신규 제안 SOTA 모델(DS-EEF)은",
    "[표의 개선 모델 Y 행 지목] 본 연구가 독창적으로 설계한 개선 모델 Y(DS-EEF)는"
)
content = content.replace(
    "신규 제안 모델의 초록색 실선은",
    "개선 모델 Y의 초록색 실선은"
)
content = content.replace(
    "이상 징후 포착 시에만 중앙 서버의 신규 SOTA(DS-EEF)가 2차 정밀 분석을",
    "이상 징후 포착 시에만 상위 서버의 개선 모델 Y(DS-EEF)가 2차 정밀 분석을"
)
content = content.replace(
    "기존 SOTA의 한계를 극복한 신규 DS-EEF 아키텍처를 통해",
    "기존 글로벌 SOTA의 한계를 극복한 개선 모델 Y(DS-EEF 아키텍처)를 통해"
)

# 2. PPTX replacements
content = content.replace(
    'r2.text = "다변량 산업 시계열 이상탐지 신규 SOTA 모델(DS-EEF) 설계 및 실증\\n"',
    'r2.text = "다변량 산업 시계열 이상탐지 개선 모델 Y(DS-EEF) 설계 및 실증\\n"'
)
content = content.replace(
    '("신규 SOTA 아키텍처 DS-EEF", "이중 스트림 에너지-극단치 융합"),',
    '("개선 모델 Y: DS-EEF 아키텍처", "이중 스트림 에너지-극단치 융합"),'
)
content = content.replace(
    '("Test F1-Score 0.7039 돌파", "기존 SOTA 대비 +42% 수직 상승"),',
    '("Test F1-Score 0.7039 돌파", "기존 글로벌 SOTA 대비 +42% 수직 상승"),'
)
content = content.replace(
    'add_header(s3, "2. 기존 SOTA의 한계 규명 및 신규 제안 DS-EEF 아키텍처",',
    'add_header(s3, "2. 기존 SOTA의 구조적 한계 규명 및 개선 모델 Y(DS-EEF) 아키텍처",'
)
content = content.replace(
    'r.text = "🔬 신규 DS-EEF 수리 모델"',
    'r.text = "🔬 개선 모델 Y(DS-EEF) 수리 모델"'
)
content = content.replace(
    '"32,857개 윈도우 평가: 신규 SOTA(DS-EEF)가 F1 0.704, 정밀도 89.0%, PA F1 81.0%로 전 지표 압도", "04")',
    '"32,857개 윈도우 평가: 개선 모델 Y(DS-EEF)가 F1 0.704, 정밀도 89.0%, PA F1 81.0%로 전 지표 압도", "04")'
)
content = content.replace(
    'table_shape = s4.shapes.add_table(rows=7, cols=7, left=P_Inches(0.8), top=P_Inches(1.9), width=P_Inches(11.733), height=P_Inches(2.1))',
    'table_shape = s4.shapes.add_table(rows=6, cols=7, left=P_Inches(0.8), top=P_Inches(1.9), width=P_Inches(11.733), height=P_Inches(2.1))'
)

old_pptx_table = """    table_data = [
        ["모델 A (Isolation Forest)", "0.4343", "0.3435", "0.5901", "0.3468", "0.4755", "초경량 엣지 (0.15초)"],
        ["모델 B (기본 LSTM-AE)", "0.4935", "0.3945", "0.6588", "0.7009", "0.5249", "시계열 복원 베이스라인"],
        ["SOTA 1: USAD (KDD 2020)", "0.4944", "0.3949", "0.6610", "0.6156", "0.5053", "2단계 적대적 오토인코더"],
        ["SOTA 2: Anomaly Tr. (ICLR 2022)", "0.4861", "0.4076", "0.6018", "0.6440", "0.5364", "연관 불일치도 어텐션"],
        ["기존 개선 모델 y (물리가중+k=5)", "0.5876", "0.5519", "0.6283", "0.7397", "0.6213", "도메인 가중치 결합"],
        ["★ 신규 제안 SOTA (DS-EEF, 본 연구)", "0.7039", "0.8899", "0.5822", "0.7557", "0.8104", "전 지표 1위 (+42.6% 도약)"]
    ]
    for r_i, row in enumerate(table_data):
        is_champion = (r_i == 5)"""

new_pptx_table = """    table_data = [
        ["모델 A (Isolation Forest)", "0.4343", "0.3435", "0.5901", "0.3468", "0.4755", "초경량 엣지 (0.15초)"],
        ["모델 B (기본 LSTM-AE)", "0.4935", "0.3945", "0.6588", "0.7009", "0.5249", "시계열 복원 베이스라인"],
        ["SOTA 1: USAD (KDD 2020)", "0.4944", "0.3949", "0.6610", "0.6156", "0.5053", "2단계 적대적 오토인코더"],
        ["SOTA 2: Anomaly Tr. (ICLR 2022)", "0.4861", "0.4076", "0.6018", "0.6440", "0.5364", "연관 불일치도 어텐션"],
        ["★ 개선 모델 Y (DS-EEF, 제안 모델)", "0.7039", "0.8899", "0.5822", "0.7557", "0.8104", "전 지표 1위 (+42.6% 도약)"]
    ]
    for r_i, row in enumerate(table_data):
        is_champion = (r_i == 4)"""

content = content.replace(old_pptx_table, new_pptx_table)

content = content.replace(
    '"이상 에너지 95% 주원인 센서 규명 및 초경량 엣지(IF) + 중앙 정밀진단(DS-EEF) 협력 파이프라인", "05")',
    '"이상 에너지 95% 주원인 센서 규명 및 초경량 엣지(IF) + 중앙 정밀진단(개선 모델 Y) 협력 파이프라인", "05")'
)
content = content.replace(
    '"• 2차 중앙 서버 (신규 SOTA DS-EEF): 이상 의심 신호만 수신하여 정밀 진단 및 센서 기여도 분해.\\n"',
    '"• 2차 중앙 서버 (개선 모델 Y): 이상 의심 신호만 수신하여 DS-EEF로 정밀 진단 및 센서 기여도 분해.\\n"'
)
content = content.replace(
    '("2. 기존 글로벌 SOTA 한계 극복 및 신규 아키텍처(DS-EEF) 창안",',
    '("2. 기존 글로벌 SOTA 한계 극복 및 개선 모델 Y(DS-EEF) 창안",'
)

# 3. HTML Deck replacements
content = content.replace(
    '<div class="slide-title">다변량 산업 시계열 이상탐지 신규 SOTA 모델(DS-EEF) 설계 및 실증</div>',
    '<div class="slide-title">다변량 산업 시계열 이상탐지 개선 모델 Y(DS-EEF) 설계 및 실증</div>'
)
content = content.replace(
    '<div class="metric-label">신규 SOTA 아키텍처 DS-EEF</div>',
    '<div class="metric-label">개선 모델 Y: DS-EEF 아키텍처</div>'
)
content = content.replace(
    '<div class="slide-title">2단계: 기존 SOTA의 구조적 한계 규명 및 신규 제안 DS-EEF 아키텍처</div>',
    '<div class="slide-title">2단계: 기존 SOTA의 구조적 한계 규명 및 개선 모델 Y(DS-EEF) 아키텍처</div>'
)
content = content.replace(
    '<div class="card-title">🔬 신규 제안 SOTA 아키텍처: DS-EEF 파이프라인</div>',
    '<div class="card-title">🔬 개선 모델 Y(DS-EEF) 파이프라인</div>'
)
content = content.replace(
    '<div class="slide-subtitle">32,857개 윈도우 평가: 신규 SOTA(DS-EEF)가 F1 0.704, 정밀도 89.0%, PA F1 81.0%로 전 지표 압도</div>',
    '<div class="slide-subtitle">32,857개 윈도우 평가: 개선 모델 Y(DS-EEF)가 F1 0.704, 정밀도 89.0%, PA F1 81.0%로 전 지표 압도</div>'
)

old_html_table = """                        <tr><td>기존 개선 모델 y (물리가중+k=5)</td><td>83.50초</td><td>0.5876</td><td>0.5519</td><td>0.6283</td><td>0.7397</td><td>0.6213</td><td>도메인 가중치 결합</td></tr>
                        <tr style="background:rgba(52, 211, 153, 0.15); font-weight:bold; color:var(--accent-green);">
                            <td>★ 신규 제안 SOTA (DS-EEF, 본 연구)</td><td>83.20초</td><td>0.7039</td><td>0.8899</td><td>0.5822</td><td>0.7557</td><td>0.8104</td><td>전 지표 최고 기록 (+42.6% 도약)</td>
                        </tr>"""

new_html_table = """                        <tr style="background:rgba(52, 211, 153, 0.15); font-weight:bold; color:var(--accent-green);">
                            <td>★ 개선 모델 Y (DS-EEF, 제안 모델)</td><td>83.20초</td><td>0.7039</td><td>0.8899</td><td>0.5822</td><td>0.7557</td><td>0.8104</td><td>전 지표 최고 기록 (+42.6% 도약)</td>
                        </tr>"""

content = content.replace(old_html_table, new_html_table)

content = content.replace(
    '<li><strong>2차 중앙 정밀 진단 서버 (신규 SOTA DS-EEF)</strong>:',
    '<li><strong>2차 중앙 정밀 진단 서버 (개선 모델 Y)</strong>:'
)
content = content.replace(
    '<div class="conclusion-title">2. 기존 글로벌 SOTA 한계 극복 및 신규 아키텍처(DS-EEF) 창안</div>',
    '<div class="conclusion-title">2. 기존 글로벌 SOTA 한계 극복 및 개선 모델 Y(DS-EEF) 창안</div>'
)

# 4. DOCX Report replacements
content = content.replace(
    '"2. [기존 글로벌 SOTA 한계 규명]: USAD(KDD 2020, F1 0.494) 및 Anomaly Transformer(ICLR 2022, F1 0.486)는 전 센서 단순 합산으로 정상 채널 잡음이 누적되는 한계가 있음. 이를 개선하기 위해 \'거시 물리 에너지 + 극단치 라우팅\' 이중 스트림 융합 신경망(DS-EEF)을 독창적으로 설계함.",',
    '"2. [기존 글로벌 SOTA 한계 극복 및 개선 모델 Y 창안]: USAD(KDD 2020, F1 0.494) 및 Anomaly Transformer(ICLR 2022, F1 0.486)는 전 센서 단순 합산으로 정상 채널 잡음이 누적되는 한계가 있음. 이를 개선하기 위해 \'거시 물리 에너지 + 극단치 라우팅\' 이중 스트림 융합 신경망(개선 모델 Y, DS-EEF)을 독창적으로 설계함.",'
)
content = content.replace(
    'add_h1("제3장. 성능 평가 및 신규 SOTA(DS-EEF) 최종 벤치마크 검증")',
    'add_h1("제3장. 성능 평가 및 개선 모델 Y(DS-EEF) 최종 벤치마크 검증")'
)
content = content.replace(
    'tbl_t2 = doc.add_table(rows=7, cols=7)',
    'tbl_t2 = doc.add_table(rows=6, cols=7)'
)

old_docx_table = """    t2_rows = [
        ["모델 A (Isolation Forest)", "0.4343", "0.3435", "0.5901", "0.3468", "0.4755", "초경량 엣지 (0.15초)"],
        ["모델 B (기본 LSTM-AE)", "0.4935", "0.3945", "0.6588", "0.7009", "0.5249", "시계열 복원 베이스라인"],
        ["SOTA 1: USAD (KDD 2020)", "0.4944", "0.3949", "0.6610", "0.6156", "0.5053", "2단계 적대적 오토인코더"],
        ["SOTA 2: Anomaly Tr. (ICLR 2022)", "0.4861", "0.4076", "0.6018", "0.6440", "0.5364", "연관 불일치도 어텐션"],
        ["기존 개선 모델 y (물리가중+k=5)", "0.5876", "0.5519", "0.6283", "0.7397", "0.6213", "도메인 가중치 결합"],
        ["★ 신규 제안 SOTA (DS-EEF, 본 연구)", "0.7039", "0.8899", "0.5822", "0.7557", "0.8104", "전 지표 최고 기록 (+42.6% 도약)"]
    ]
    for r_idx, row in enumerate(t2_rows):
        for c_idx, val in enumerate(row):
            c = tbl_t2.cell(r_idx + 1, c_idx)
            is_winner = (r_idx == 5)"""

new_docx_table = """    t2_rows = [
        ["모델 A (Isolation Forest)", "0.4343", "0.3435", "0.5901", "0.3468", "0.4755", "초경량 엣지 (0.15초)"],
        ["모델 B (기본 LSTM-AE)", "0.4935", "0.3945", "0.6588", "0.7009", "0.5249", "시계열 복원 베이스라인"],
        ["SOTA 1: USAD (KDD 2020)", "0.4944", "0.3949", "0.6610", "0.6156", "0.5053", "2단계 적대적 오토인코더"],
        ["SOTA 2: Anomaly Tr. (ICLR 2022)", "0.4861", "0.4076", "0.6018", "0.6440", "0.5364", "연관 불일치도 어텐션"],
        ["★ 개선 모델 Y (DS-EEF, 제안 모델)", "0.7039", "0.8899", "0.5822", "0.7557", "0.8104", "전 지표 최고 기록 (+42.6% 도약)"]
    ]
    for r_idx, row in enumerate(t2_rows):
        for c_idx, val in enumerate(row):
            c = tbl_t2.cell(r_idx + 1, c_idx)
            is_winner = (r_idx == 4)"""

content = content.replace(old_docx_table, new_docx_table)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully replaced and updated build_final_sota_deliverables.py!")
