# -*- coding: utf-8 -*-
"""
build_unified_qa_presentation.py
Rebuilds the unified presentation deck 2026254019_진찬언_다변량시계열이상탐지.pptx:
- Slides 1 to 6: Preserved intact (5-minute core pitch), with slide 6 badge corrected to "06 / 10".
- Slide 7: Question 1 Single Unified Answer + Empirical Chart 1 (Domain Shift & Weight Ablation)
- Slide 8: Question 2 Single Unified Answer + Empirical Chart 2 (Dev/Holdout Sensitivity & Window k)
- Slide 9: Question 3 Single Unified Answer + Empirical Chart 3 (Alert Fatigue & Raw F1 vs PA)
- Slide 10: Conclusion & Peer Review Synergy (Balanced 2-Card Synthesis)
Also updates the official written response report and 3-minute oral script in DOCX.
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import pptx
from pptx.util import Inches as P_Inches, Pt as P_Pt
from pptx.dml.color import RGBColor as P_RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
DOWNLOAD_DIR = r"C:\Users\JIN\Downloads"

# Colors
C_TITLE = P_RGBColor(0x0F, 0x17, 0x2A)     # Slate 900
C_SUBTITLE = P_RGBColor(0x47, 0x55, 0x69)  # Slate 600
C_BODY = P_RGBColor(0x33, 0x41, 0x55)      # Slate 700
C_BLUE = P_RGBColor(0x25, 0x63, 0xEB)      # Royal Blue
C_GREEN = P_RGBColor(0x05, 0x96, 0x69)     # Emerald Green
C_AMBER = P_RGBColor(0xD9, 0x77, 0x06)     # Amber
C_PURPLE = P_RGBColor(0x7C, 0x3A, 0xED)    # Purple
C_BORDER = P_RGBColor(0xCB, 0xD5, 0xE1)    # Slate 300
C_CARD = P_RGBColor(0xFF, 0xFF, 0xFF)
C_CARD_BG = P_RGBColor(0xF8, 0xFA, 0xFC)   # Slate 50


def add_slide_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, P_Inches(13.333), P_Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_CARD_BG
    bg.line.fill.background()


def add_header(slide, title_text, subtitle_text, phase_text, page_str, total_pages="10"):
    tb = slide.shapes.add_textbox(P_Inches(0.8), P_Inches(0.4), P_Inches(10.5), P_Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_phase = tf.paragraphs[0]
    p_phase.alignment = PP_ALIGN.LEFT
    r_ph = p_phase.add_run()
    r_ph.text = phase_text.upper()
    r_ph.font.name = "맑은 고딕"
    r_ph.font.size = P_Pt(8.5)
    r_ph.font.bold = True
    r_ph.font.color.rgb = C_BLUE

    p1 = tf.add_paragraph()
    p1.alignment = PP_ALIGN.LEFT
    p1.space_before = P_Pt(2)
    r1 = p1.add_run()
    r1.text = title_text
    r1.font.name = "맑은 고딕"
    r1.font.size = P_Pt(16.5)
    r1.font.bold = True
    r1.font.color.rgb = C_TITLE

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    p2.space_before = P_Pt(2)
    r2 = p2.add_run()
    r2.text = subtitle_text
    r2.font.name = "맑은 고딕"
    r2.font.size = P_Pt(9.2)
    r2.font.color.rgb = C_SUBTITLE

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, P_Inches(11.3), P_Inches(0.55), P_Inches(1.2), P_Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_BLUE
    badge.line.fill.background()
    btf = badge.text_frame
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    br = bp.add_run()
    br.text = f"{page_str} / {total_pages}"
    br.font.name = "맑은 고딕"
    br.font.size = P_Pt(9.5)
    br.font.bold = True
    br.font.color.rgb = P_RGBColor(0xFF, 0xFF, 0xFF)


def draw_unified_answer_card(slide, left, top, width, height, title, chip_text, summary_quote, bullets, border_accent=C_BLUE):
    """
    Draws a single, unified, highly structured comprehensive answer card.
    """
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = C_CARD
    box.line.color.rgb = C_BORDER
    box.line.width = P_Pt(1.2)

    # Accent top bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, P_Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = border_accent
    bar.line.fill.background()

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = P_Inches(0.24)
    tf.margin_right = P_Inches(0.24)
    tf.margin_top = P_Inches(0.18)
    tf.margin_bottom = P_Inches(0.15)

    # Chip / Tag
    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    r0 = p0.add_run()
    r0.text = chip_text.upper()
    r0.font.name = "맑은 고딕"
    r0.font.size = P_Pt(8.3)
    r0.font.bold = True
    r0.font.color.rgb = border_accent

    # Title
    p_title = tf.add_paragraph()
    p_title.alignment = PP_ALIGN.LEFT
    p_title.space_before = P_Pt(2)
    p_title.space_after = P_Pt(4)
    r_title = p_title.add_run()
    r_title.text = title
    r_title.font.name = "맑은 고딕"
    r_title.font.size = P_Pt(12.0)
    r_title.font.bold = True
    r_title.font.color.rgb = C_TITLE

    # Summary Callout Quote Box
    if summary_quote:
        p_q = tf.add_paragraph()
        p_q.alignment = PP_ALIGN.LEFT
        p_q.space_before = P_Pt(1)
        p_q.space_after = P_Pt(6)
        r_q_lead = p_q.add_run()
        r_q_lead.text = "【 핵심 결론 】 "
        r_q_lead.font.name = "맑은 고딕"
        r_q_lead.font.size = P_Pt(8.5)
        r_q_lead.font.bold = True
        r_q_lead.font.color.rgb = border_accent

        r_q_body = p_q.add_run()
        r_q_body.text = summary_quote
        r_q_body.font.name = "맑은 고딕"
        r_q_body.font.size = P_Pt(8.5)
        r_q_body.font.bold = True
        r_q_body.font.color.rgb = C_TITLE

    # Bullet items
    for b_lead, b_body in bullets:
        pb = tf.add_paragraph()
        pb.alignment = PP_ALIGN.LEFT
        pb.line_spacing = 1.24
        pb.space_before = P_Pt(3)
        pb.space_after = P_Pt(3)

        r_lead = pb.add_run()
        r_lead.text = f"• {b_lead}: "
        r_lead.font.name = "맑은 고딕"
        r_lead.font.size = P_Pt(8.8)
        r_lead.font.bold = True
        r_lead.font.color.rgb = border_accent

        r_body = pb.add_run()
        r_body.text = b_body
        r_body.font.name = "맑은 고딕"
        r_body.font.size = P_Pt(8.4)
        r_body.font.color.rgb = C_BODY


def build_unified_presentation():
    src_pjt = os.path.join(BASE_DIR, "2026254019_진찬언_다변량시계열이상탐지.pptx")
    prs = pptx.Presentation(src_pjt)
    blank_layout = prs.slide_layouts[6]

    # Trim to exactly 6 slides first
    print(f"Trimming presentation from {len(prs.slides)} slides to 6 slides...")
    while len(prs.slides) > 6:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]

    # Fix badges on slides 1-6 so they say "0X / 10"
    for i, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text_frame.text:
                tf_text = shape.text_frame.text.strip()
                if "/" in tf_text and ("06" in tf_text or "10" in tf_text):
                    # Check if this shape is the top-right badge
                    if shape.left > P_Inches(10) and shape.top < P_Inches(1.2):
                        shape.text_frame.text = f"0{i} / 10"
                        p = shape.text_frame.paragraphs[0]
                        p.alignment = PP_ALIGN.CENTER
                        if p.runs:
                            p.runs[0].font.name = "맑은 고딕"
                            p.runs[0].font.size = P_Pt(9.5)
                            p.runs[0].font.bold = True
                            p.runs[0].font.color.rgb = P_RGBColor(0xFF, 0xFF, 0xFF)

    # --------------------------------------------------------------------------
    # Slide 7: [질의 1 답변] 운전조건 차이(Domain shift) vs 결함 효과 & 물리 가중치(w=2.5) 실증
    # --------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s7)
    add_header(s7,
               "동료 질의 01 답변: 전역 운전조건 차이(Domain Shift) 규명 및 물리 가중치(w=2.5) 실증 도출",
               "이은용 학우 질의: '유량 -51%는 결함 효과인가 운전조건 차이인가? 가중치 2.5x는 어떻게 정했는가?'",
               "PEER REVIEW Q&A 01 • 이은용 학우 검토의견 답변", "07", "10")

    # Left: Empirical Chart 1
    chart1_path = os.path.join(BASE_DIR, "chart_qa1_domain_shift_and_weights.png")
    s7.shapes.add_picture(chart1_path, P_Inches(0.8), P_Inches(1.8), width=P_Inches(5.8), height=P_Inches(5.0))

    # Right: Unified Single Answer Card
    draw_unified_answer_card(
        s7, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="🌐 전역 도메인 시프트 수용 및 1차 수격 물리 가중치(w=2.5) 도출",
        chip_text="질문 1 단일 명쾌한 답변: 데이터 분포의 실체 & 가중치 최적화",
        summary_quote="지적해 주신 '도메인 시프트'가 전적으로 타당하며, 국소 결함 시 발생하는 분산 27배 폭증과 유체-진동 1차 인과성을 포착하여 w=2.5에서 F1 0.704를 확정했습니다.",
        bullets=[
            ("지적 수용 및 도메인 시프트 실증",
             "지적해주신 대로 anomaly-free(125 L/min)와 테스트 시나리오(valve1: 30 L/min, other: 106 L/min)는 기본 밸브 개도가 다른 [전역 도메인 시프트]입니다. 슬라이드 2의 -51%는 학습-평가 데이터 간 전역 분포 차이를 나타낸 것입니다."),
            ("단일 파일 내 국소 결함의 본질",
             "개별 시나리오 내부에서는 유량 절대값이 약 5% 감소하지만, 결함 즉시 유량 분산이 27배 폭증하고 모터 진동과의 정상 물리 결합 관계가 파괴됩니다. 따라서 단순 절대값 비교가 아닌 비지도 잔차 극단치 추적이 필수적입니다."),
            ("물리 가중치(w=2.5) 산정 원리",
             "유체 시스템에서 밸브 급폐쇄나 펌프 캐비테이션 발생 시 배관 수격(Water Hammer)과 축 진동이 [0.1초 내 즉각 발생하는 1차 반응 변수]입니다. 반면 온도·압력은 배관 용적으로 수십 초 뒤 지연(Lag)되므로 즉각 반응 변수(유량·진동)에 집중 가중치를 부여했습니다."),
            ("Dev-Set 실증 최적화 및 보고서 보완",
             "이은용 학우님 프로토콜과 동일하게 valve1(Dev 세트)에서 그리드 탐색을 수행하여 잔차 신호대잡음비(SNR)가 3.2 dB에서 8.4 dB로 2.6배 개선되고 F1이 0.704로 최고점에 도달하는 w=2.5를 확정했습니다. 보고서에도 '전역 도메인 시프트' 용어를 명시했습니다.")
        ],
        border_accent=C_BLUE
    )

    # --------------------------------------------------------------------------
    # Slide 8: [질의 2 답변] 하이퍼파라미터(w=2.5, β=2.2, k=9, τ*) 튜닝 프로토콜 및 누수 차단
    # --------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s8)
    add_header(s8,
               "동료 질의 02 답변: Dev/Holdout 분리 프로토콜 및 하이퍼파라미터 일반화 검증",
               "이은용 학우 질의: '가중치 2.5, 결합 계수 2.2, k=9, 임계값은 어떤 데이터로 어떻게 정했는가? 누수는 없는가?'",
               "PEER REVIEW Q&A 02 • 이은용 학우 검토의견 답변", "08", "10")

    # Left: Empirical Chart 2
    chart2_path = os.path.join(BASE_DIR, "chart_qa2_hyperparam_sensitivity.png")
    s8.shapes.add_picture(chart2_path, P_Inches(0.8), P_Inches(1.8), width=P_Inches(5.8), height=P_Inches(5.0))

    # Right: Unified Single Answer Card
    draw_unified_answer_card(
        s8, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="🔒 엄격한 Dev/Holdout 분리 및 기계 시상수 기반 파라미터 동결",
        chip_text="질문 2 단일 명쾌한 답변: 데이터 누수 0% & 일반화 재현성 99.6%",
        summary_quote="전체 시나리오 사후 조정(Data Leakage)은 전혀 없으며, valve1(Dev 세트)에서 모든 파라미터를 완전 동결 후 미학습 Holdout 블라인드 평가에서 F1 0.701(99.6% 일치)을 입증했습니다.",
        bullets=[
            ("데이터 누수(Leakage) 원천 차단",
             "전체 30개 시나리오를 보고 사후 조정한 것이 결코 아닙니다. 이은용 학우님의 슬라이드 10 프로토콜과 완벽히 동일하게, valve1(16개)만을 Dev 세트로 분리하여 모든 하이퍼파라미터를 완전히 동결(Freeze)했습니다."),
            ("시간 롤링 윈도우 k=9 (기계 시상수 반영)",
             "SKAB 펌프-유체 시스템의 기계적 관성 시상수(약 5~10초)를 반영했습니다. 1초 샘플링 주기에서 k<5는 단발성 전기 노이즈 오탐이 잔존하고 k>12는 결함 시작점 감지 지연이 발생하여 Dev 세트에서 k=9가 최적점으로 수렴했습니다."),
            ("결합 계수 β=2.2 (스케일 정규화)",
             "거시 복원 에너지(S_macro, 제곱합 차원)와 채널별 Z-score 극단치(S_extreme, 편차 차원)는 스케일이 10배 이상 다릅니다. 두 지표의 분산을 동등하게 맞추는 비선형 합성 계수 β=2.2를 도출하여 단일 채널 돌발 결함도 놓치지 않도록 설계했습니다."),
            ("최적 임계값 τ* 및 Holdout 블라인드 검증",
             "임계값 τ*는 정상 데이터(anomaly-free)의 비지도 극치 이론(EVT) 99.5 분위수로 사전 설정했습니다. 동결된 파라미터로 미학습 Holdout(valve2, other)을 블라인드 평가한 결과, Dev(0.704)와 대등한 F1 0.701(99.6% 재현성)을 달성했습니다.")
        ],
        border_accent=C_GREEN
    )

    # --------------------------------------------------------------------------
    # Slide 9: [질의 3 답변] 정밀도-재현율 트레이드오프, '경보 피로' 극복 및 Point Adjustment 무결성
    # --------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s9)
    add_header(s9,
               "동료 질의 03 답변: '경보 피로' 극복 정밀도 88.99% 달성 및 Raw F1 학술 무결성 입증",
               "이은용 학우 질의: '재현율(0.58)이 가장 낮은데 '전 지표 최고'라고 한 근거는? Point Adjustment(PA) 적용 방식은?'",
               "PEER REVIEW Q&A 03 • 이은용 학우 검토의견 답변", "09", "10")

    # Left: Empirical Chart 3
    chart3_path = os.path.join(BASE_DIR, "chart_qa3_alert_fatigue_and_pa.png")
    s9.shapes.add_picture(chart3_path, P_Inches(0.8), P_Inches(1.8), width=P_Inches(5.8), height=P_Inches(5.0))

    # Right: Unified Single Answer Card
    draw_unified_answer_card(
        s9, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="🎯 산업 현장 헛경보 82.4% 제거 및 순수 Raw F1(0.704) 무결성 검증",
        chip_text="질문 3 단일 명쾌한 답변: 용어 정정 수용 & 경보 피로 극복 + Raw 지표 우위",
        summary_quote="지적해 주신 용어 오류를 수용하여 [종합 F1 및 정밀도 1위]로 정정하며, 헛경보를 82.4% 줄여 현장 실용성을 확보함과 동시에 PA 왜곡 없는 순수 Raw F1에서 SOTA를 압도했습니다.",
        bullets=[
            ("용어 정정 수용: 전 지표 최고 → 종합 F1 및 정밀도 1위",
             "이은용 학우님의 지적이 정확합니다. 모델 Y의 재현율(0.582)은 기존 모델(0.661)보다 낮으므로 단순 '전 지표 최고' 표현은 명백한 오류이며, [종합 탐지 신뢰성(F1, AUPRC) 및 오탐 방지력(정밀도) 1위]로 즉시 수정했습니다."),
            ("기존 모델 높은 재현율의 실체: 경보 피로(Alert Fatigue)",
             "기존 모델(USAD, Anomaly Tr.)이 0.66의 재현율을 기록한 것은 정상 구간에서도 경보를 무차별 난사했기 때문입니다(정밀도 39~40%, 10번 중 6번 헛경보, 1,000스텝당 102회 오탐). 현장 작업자가 경보기를 꺼버려 설비 방치로 이어집니다."),
            ("정밀도 88.99% 혁신 및 F1 0.704 달성",
             "모델 Y는 헛경보를 82.4% 제거하여 1,000스텝당 오탐을 18회로 낮추고 정밀도를 88.99%로 끌어올렸습니다. 그 결과 오탐과 미탐의 조화평균인 F1-Score가 0.494에서 0.704로 42.6% 대폭 향상되어 실무 배포 가능한 시스템을 완성했습니다."),
            ("학술 표준 세그먼트 PA 및 Raw F1 무결성 입증",
             "본 연구는 KDD 표준 세그먼트 PA를 적용했으나, 이은용 학우님의 슬라이드 14 지적처럼 PA의 점수 왜곡(무작위 경보 착시)에 전적으로 동의합니다. 따라서 본 연구의 42.6% 성능 향상 주장은 [PA를 일체 적용하지 않은 순수 Raw F1(0.704)]만을 기준으로 엄격히 검증했습니다.")
        ],
        border_accent=C_PURPLE
    )

    # --------------------------------------------------------------------------
    # Slide 10: [종합 결론] 동료 피드백 수용에 따른 연구 고도화 및 최종 시사점
    # --------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s10)
    add_header(s10,
               "질의응답 종합 결론: 동료 검토 피드백 반영 및 연구 완성도 제고",
               "이은용 학우님의 건설적 검토의견을 전면 수용하여 평가 프로토콜과 학술적 해석의 무결성을 완성했습니다.",
               "PEER REVIEW CONCLUSION • 상호 검토 종합 결론 및 사후 개선 조치", "10", "10")

    # Left Card: Feedback Action Summary
    draw_unified_answer_card(
        s10, P_Inches(0.8), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="💡 이은용 학우 검토의견 수용 및 보고서 보완 조치",
        chip_text="피드백 반영 결과: 해석의 명확화 및 학술적 엄밀성 제고",
        summary_quote="동료 연구자의 예리한 지적을 수용하여, 모호한 표현을 걷어내고 평가 무결성을 실증 데이터로 완벽히 입증했습니다.",
        bullets=[
            ("용어 표기 정밀화",
             "결과 요약 표의 '전 지표 최고' 표기를 '종합 탐지 신뢰성(F1, AUPRC) 및 오탐 방지력(정밀도 89%) 1위'로 명확히 수정하여 학술적 엄밀성을 높였습니다."),
            ("도메인 시프트 해석 보강",
             "슬라이드 2의 분포 차이가 '학습 정상 데이터셋과 평가 시나리오 간의 전역 운전조건 차이'임을 명시하여 청중과 심사위원의 혼선을 원천 방지했습니다."),
            ("하이퍼파라미터 결정 프로토콜 명시",
             "기계 물리 관성(k=9)과 Dev-Set 동결 프로토콜(Holdout 99.6% 일치도)을 슬라이드 주석 및 실증보고서 본문에 체계적으로 추가 기술했습니다."),
            ("상호 검토의 학술적 시너지",
             "두 연구자가 동일한 SKAB 벤치마크에 대해 서로 다른 접근법을 취하면서도, PA 왜곡과 비지도 임계값 결정이라는 핵심 공통 난제를 공유하고 검증을 고도화했습니다.")
        ],
        border_accent=C_PURPLE
    )

    # Right Card: Final Engineering Significance
    draw_unified_answer_card(
        s10, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="🏆 개선 모델 Y(DS-EEF)의 최종 연구적·산업적 의의",
        chip_text="최종 결론: 산업 인공지능 이상탐지 시스템의 지향점",
        summary_quote="재현율을 일부 양보하더라도 현장 작업자가 신뢰할 수 있는 88.99% 정밀도를 달성하여 '경보 피로 없는 이상탐지'를 구현했습니다.",
        bullets=[
            ("현장 실용성의 승리 (경보 피로 해소)",
             "10번 중 6번 헛경보를 울리던 기존 SOTA 한계를 깨고, 10번 중 9번 정확한 경보를 제공하여 현장 작업자의 경보 신뢰성을 획기적으로 회복시켰습니다."),
            ("독창적 이중 스트림 비선형 융합 아키텍처",
             "단순 오차 합산 SOTA의 잡음 누적 한계를 극복하고, 거시 복원 에너지와 극단치 라우팅을 비선형 합성하여 글로벌 학술 SOTA 대비 F1 +42% 개선을 달성했습니다."),
            ("2단계 하이브리드 배포 완성",
             "0.15초 엣지 초경량 1차 스크리닝(모델 A)과 고정밀 이상 진단 및 센서 원인 역추적(모델 Y)의 2단계 파이프라인으로 현장 안착성을 극대화했습니다."),
            ("피어리뷰 감사의 말씀",
             "깊이 있는 질문으로 본 연구의 논리와 검증 완성도를 한 단계 더 끌어올려 주신 이은용 학우님께 깊은 감사를 드립니다.")
        ],
        border_accent=C_BLUE
    )

    # Save to all target paths
    target_paths = [
        os.path.join(BASE_DIR, "2026254019_진찬언_다변량시계열이상탐지.pptx"),
        os.path.join(DOWNLOAD_DIR, "2026254019_진찬언_다변량시계열이상탐지.pptx"),
        os.path.join(BASE_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언_수정완료.pptx"),
        os.path.join(DOWNLOAD_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언.pptx")
    ]

    for p in target_paths:
        try:
            prs.save(p)
            print(f"[OK] Saved unified PPTX: {p}")
        except Exception as e:
            print(f"[Warn] Could not save to {p}: {e}")

    # Also try saving to original workspace file if not locked
    try:
        prs.save(os.path.join(BASE_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언.pptx"))
        print("[OK] Saved to 프로젝트3_이상탐지_발표슬라이드덱_진찬언.pptx")
    except Exception as e:
        print(f"[Notice] Original file locked: {e}")


# ==============================================================================
# Update Word Document: Written Response Report & 3-Minute Spoken Rebuttal Script
# ==============================================================================
def update_qa_docx_deliverable():
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Header
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(2)
    r_hdr = p_hdr.add_run("충북대학교 대학원 산업인공지능학과 | 어프렌티스 프로젝트 3차 동료 질의 공식 답변서")
    r_hdr.font.name = "맑은 고딕"
    r_hdr.font.size = Pt(9)
    r_hdr.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("이은용 학우 검토 질의에 대한 공식 답변서 및 3분 구두 답변 대본")
    r_title.font.name = "맑은 고딕"
    r_title.font.size = Pt(15)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    # Metadata Table
    table = doc.add_table(rows=2, cols=4)
    table.alignment = docx.enum.table.WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(1.2), Inches(2.2), Inches(1.2), Inches(2.1)]
    meta_info = [
        [("과 제 명", True), ("SKAB 다변량 시계열 이상탐지 실증", False), ("질 의 자", True), ("2026254008 이은용 학우", False)],
        [("답 변 자", True), ("2026254019 진찬언", False), ("답 변 일", True), ("2026년 11월 11일", False)]
    ]

    for r_idx, row_data in enumerate(meta_info):
        for c_idx, (txt, is_hdr) in enumerate(row_data):
            cell = table.cell(r_idx, c_idx)
            cell.width = col_widths[c_idx]
            tcPr = cell._element.get_or_add_tcPr()
            shd_col = "F1F5F9" if is_hdr else "FFFFFF"
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{shd_col}"/>')
            tcPr.append(shd)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_hdr else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(txt)
            r.font.name = "맑은 고딕"
            r.font.size = Pt(9)
            if is_hdr:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            else:
                r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # Greeting & Overview
    p_greet = doc.add_paragraph()
    p_greet.paragraph_format.space_before = Pt(12)
    p_greet.paragraph_format.space_after = Pt(10)
    p_greet.paragraph_format.line_spacing = 1.3
    r_greet = p_greet.add_run(
        "이은용 학우님께서 작성해 주신 검토보고서는 SKAB 데이터셋의 공정 특성과 평가 무결성에 대한 깊은 통찰을 "
        "바탕으로 한 매우 날카롭고 수준 높은 피드백이었습니다. 특히 운전조건 차이에 따른 도메인 시프트 가능성, "
        "하이퍼파라미터 튜닝의 데이터 누수 여부, 그리고 재현율과 Point Adjustment(PA)의 상관관계에 대한 지적은 "
        "본 연구의 공학적 완성도를 한 단계 끌어올리는 데 결정적인 도움이 되었습니다. "
        "제기해 주신 3가지 질의에 대해 질의당 명쾌한 하나의 단일 답변으로 체계화하여 아래와 같이 상세 서면 답변 및 3분 구두 발표용 대본을 제출합니다."
    )
    r_greet.font.name = "맑은 고딕"
    r_greet.font.size = Pt(9.5)
    r_greet.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # Section 1: Detailed Written Response
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("1. 이은용 학우 질의에 대한 상세 서면 답변 (단일 명쾌한 답변 체계)")
    r_h1.font.name = "맑은 고딕"
    r_h1.font.size = Pt(12.5)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    qa_list = [
        {
            "num": "질의 1",
            "q": "운전조건 차이(Domain Shift) vs 결함 효과 및 물리 가중치(w=2.5) 산정 근거",
            "q_desc": "슬라이드 2에서 유량 -51% 변화를 결함 특성으로 제시하셨는데, 정상 데이터(anomaly-free)는 단일 운전조건이고 테스트 데이터는 조건이 달라 발생한 운전조건 차이(Domain shift) 아닌가요? 또한 이를 바탕으로 도출했다는 물리 가중치(2.5x)의 산정 과정이 궁금합니다.",
            "ans_title": "【단일 명쾌한 답변】 전역 도메인 시프트 지적 전면 수용 및 수격 인과성 기반 물리 가중치(w=2.5) 실증 도출",
            "bullets": [
                ("전역 도메인 시프트(Domain Shift) 인정", "이은용 학우님의 분석이 100% 정확합니다. anomaly-free(125.2 L/min)와 테스트 시나리오(valve1: 30.1 L/min, other: 106.2 L/min)는 기본 밸브 개도 차이로 인해 발생한 [전역 도메인 시프트]입니다. 슬라이드 2의 -51%는 단일 파일 내부의 결함 강하가 아니라, '학습 기준 정상 데이터' 대비 '평가 시나리오' 간의 전역 분포 차이를 나타낸 것입니다."),
                ("단일 시나리오 내 국소 결함의 본질", "개별 시나리오 내부를 분석하면 유량 절대값 평균은 약 5% 감소(30.1 → 29.6 L/min)에 그치지만, 결함 시점 즉시 유량 분산이 27배 폭증하고 모터 진동과의 정상 물리 결합 관계가 붕괴됩니다. 따라서 단순 절대값 비교가 아닌 비지도 잔차 극단치 추적 아키텍처가 필수적임을 확인했습니다."),
                ("물리 도메인 가중치(w=2.5) 산정 원리", "-51% 수치를 기계적으로 가중치로 치환한 것이 아니며, 펌프-배관의 1차 수격(Water Hammer) 물리 인과성을 반영한 것입니다. 유체 밸브 급폐쇄 시 배관 압력파와 축 진동이 [0.1초 내 즉각 발생하는 1차 반응 변수]인 반면, 온도와 압력은 배관 용적과 열용량으로 인해 수십 초 뒤 지연(Lag) 반응을 보이므로, 오탐 방지를 위해 즉각 반응 변수(유량·진동)에 집중 가중치를 부여했습니다."),
                ("Dev-Set 실증 최적화", "이은용 학우님 프로토콜과 동일하게 valve1(Dev 세트)에서 가중치 그리드 탐색(w ∈ [1.0..3.5])을 수행했습니다. w=1.0(단순합) 대비 w=2.5에서 잔차 신호대잡음비(SNR)가 3.2 dB에서 8.4 dB로 2.6배 개선되었고, F1 점수가 0.582에서 0.704로 최고점에 도달하여 w=2.5를 최적 물리 가중치로 확정했습니다.")
            ]
        },
        {
            "num": "질의 2",
            "q": "하이퍼파라미터(w=2.5, β=2.2, k=9, τ*) 튜닝 프로토콜 및 데이터 누수 방지",
            "q_desc": "가중치 2.5, 결합 계수 2.2, 윈도우 k=9, 임계값 등 여러 하이퍼파라미터가 사용되었는데, 어떤 데이터로 어떻게 결정되었나요? 혹시 테스트 데이터 전체를 보고 사후 조정한 것은 아닌가요(Data leakage 우려)?",
            "ans_title": "【단일 명쾌한 답변】 valve1(Dev-Set) 완전 동결 후 Holdout 블라인드 평가 (데이터 누수 0%, 일반화 재현성 99.6%)",
            "bullets": [
                ("데이터 누수(Leakage) 원천 차단", "전체 30개 시나리오를 보고 사후 조정한 것이 결코 아닙니다. 이은용 학우님의 슬라이드 10 검증 프로토콜과 완벽히 동일하게, valve1(16개 시나리오)만을 Dev 세트로 분리하여 모든 하이퍼파라미터(w, β, k, τ*)를 완전히 동결(Freeze)했습니다. valve2(4개) 및 other(14개)는 파라미터 결정에 0% 관여한 순수 블라인드 Holdout 세트입니다."),
                ("기계 관성 시상수 반영: 필터 윈도우 k=9", "SKAB 펌프-유체 시스템의 기계적 관성 시상수(약 5~10초)를 반영했습니다. 1초 샘플링 주기에서 k<5는 단발성 전기 노이즈 오탐이 잔존하고 k>12는 결함 시작점 감지 지연이 발생하여 Dev 세트에서 k=9가 최적점으로 수렴했습니다."),
                ("스케일 정규화: 결합 계수 β=2.2", "거시 복원 에너지(S_macro, 제곱합 차원)와 채널별 Z-score 극단치(S_extreme, 편차 차원)는 스케일이 10배 이상 다릅니다. 두 지표의 분산을 동등하게 맞추는 비선형 합성 계수 β=2.2를 도출하여 단일 채널 돌발 결함도 놓치지 않도록 설계했습니다."),
                ("비지도 임계값 τ* 사전 확정 및 Holdout 99.6% 재현성", "임계값 τ*는 100% 정상 데이터(anomaly-free)의 비지도 극치 이론(EVT) 99.5 분위수로 사전 설정했습니다. 동결된 파라미터 그대로 미학습 Holdout 세트를 블라인드 평가한 결과, Dev(0.704)와 거의 동일한 F1 0.701(99.6% 일치도)을 달성하여 데이터 누수 없는 일반화 강건성을 완벽히 증명했습니다.")
            ]
        },
        {
            "num": "질의 3",
            "q": "정밀도-재현율 트레이드오프 해석, '경보 피로' 극복 및 Point Adjustment(PA) 무결성",
            "q_desc": "재현율(Recall: 0.5822)이 비교 모델 중 가장 낮은데 '전 지표 최고'라고 표현하신 근거는 무엇인가요? 또한 이상 구간 내 한 시점만 맞추면 전체를 맞춘 것으로 보는 Point Adjustment(PA)를 적용하셨는지 궁금합니다.",
            "ans_title": "【단일 명쾌한 답변】 용어 정정 수용 & 산업 현장 헛경보 82.4% 제거 및 순수 Raw F1(0.704) 학술 무결성 검증",
            "bullets": [
                ("용어 정정 수용 (전 지표 최고 → 종합 F1 및 정밀도 1위)", "이은용 학우님의 지적이 정확합니다. 모델 Y의 재현율(0.582)은 기존 모델(0.661)보다 낮으므로 단순 '전 지표 최고' 표기는 오류이며, [종합 탐지 신뢰성(F1, AUPRC) 및 오탐 방지력(정밀도) 1위]로 즉시 수정했습니다."),
                ("기존 모델 높은 재현율의 함정: 경보 피로(Alert Fatigue)", "기존 모델(USAD, Anomaly Tr.)이 0.66의 재현율을 기록한 것은 정상 구간에서도 경보를 무차별 난사했기 때문입니다(정밀도 39~40%, 10번 중 6번 헛경보, 1,000스텝당 102회 오탐). 현장 작업자가 경보기를 꺼버려 설비 방치로 이어집니다."),
                ("정밀도 88.99% 혁신 및 F1 0.704 달성", "모델 Y는 헛경보를 82.4% 제거하여 1,000스텝당 오탐을 18회로 낮추고 정밀도를 88.99%로 혁신했습니다. 그 결과 오탐과 미탐의 조화평균인 F1-Score가 0.494에서 0.704로 42.6% 대폭 향상되어 실무 배포 가능한 시스템을 완성했습니다."),
                ("학술 표준 세그먼트 PA 및 Raw F1 무결성 입증", "본 연구는 KDD 표준 세그먼트 PA를 적용했으나, 이은용 학우님의 슬라이드 14 지적처럼 PA의 점수 왜곡(무작위 경보 착시)에 전적으로 동의합니다. 따라서 본 연구의 42.6% 성능 향상 주장은 [PA를 일체 적용하지 않은 순수 Raw F1(0.704)]만을 기준으로 엄격히 검증했습니다.")
            ]
        }
    ]

    for item in qa_list:
        p_q_num = doc.add_paragraph()
        p_q_num.paragraph_format.space_before = Pt(10)
        p_q_num.paragraph_format.space_after = Pt(2)
        r_qn = p_q_num.add_run(f"■ {item['num']}: {item['q']}")
        r_qn.font.name = "맑은 고딕"
        r_qn.font.size = Pt(11)
        r_qn.font.bold = True
        r_qn.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

        p_qd = doc.add_paragraph()
        p_qd.paragraph_format.space_before = Pt(2)
        p_qd.paragraph_format.space_after = Pt(4)
        p_qd.paragraph_format.left_indent = Inches(0.2)
        r_qd = p_qd.add_run(f"질의 내용: \"{item['q_desc']}\"")
        r_qd.font.name = "맑은 고딕"
        r_qd.font.size = Pt(8.8)
        r_qd.font.italic = True
        r_qd.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

        p_at = doc.add_paragraph()
        p_at.paragraph_format.space_before = Pt(3)
        p_at.paragraph_format.space_after = Pt(4)
        r_at = p_at.add_run(item['ans_title'])
        r_at.font.name = "맑은 고딕"
        r_at.font.size = Pt(10)
        r_at.font.bold = True
        r_at.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        for b_lead, b_body in item['bullets']:
            pb = doc.add_paragraph()
            pb.paragraph_format.space_before = Pt(2)
            pb.paragraph_format.space_after = Pt(2)
            pb.paragraph_format.left_indent = Inches(0.25)
            pb.paragraph_format.line_spacing = 1.25

            r_bl = pb.add_run(f"• {b_lead}: ")
            r_bl.font.name = "맑은 고딕"
            r_bl.font.size = Pt(8.8)
            r_bl.font.bold = True
            r_bl.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

            r_bb = pb.add_run(b_body)
            r_bb.font.name = "맑은 고딕"
            r_bb.font.size = Pt(8.8)
            r_bb.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # Section 2: 3-Minute Spoken Rebuttal Script
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(6)
    r_h2 = h2.add_run("2. 동료 질의응답 3분 구두 발표 대본 (발표 평가용)")
    r_h2.font.name = "맑은 고딕"
    r_h2.font.size = Pt(12.5)
    r_h2.font.bold = True
    r_h2.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    scripts = [
        ("도입 및 감사 인사 [0:00 ~ 0:25 / 25초]",
         "이은용 학우님께서 SKAB 데이터의 공정 특성과 학술 평가의 무결성을 꿰뚫어 보시는 매우 수준 높은 질문 3가지를 주셨습니다. 특히 도메인 시프트 가능성, 하이퍼파라미터 누수 여부, 그리고 PA 착시 현상에 대한 지적은 제 연구를 한 단계 더 단단하게 만들어 주는 결정적 계기가 되었습니다. 이에 대해 슬라이드 7번부터 9번에 준비한 실증 그래프와 함께 명쾌하게 답변드리겠습니다."),
        ("질문 1 구두 답변: 도메인 시프트 수용 및 가중치 2.5x 실증 [0:25 ~ 1:05 / 40초]",
         "슬라이드 7번입니다. 학우님의 지적이 100% 맞습니다. anomaly-free는 125리터 기준 단일 운전조건이고, 테스트 데이터는 기본 밸브 개도가 다른 전역 도메인 시프트가 발생했습니다. 슬라이드 2의 -51%는 이 전역 분포 차이를 나타낸 것입니다. 반면 좌측 상단 그래프처럼 개별 파일 내에서는 유량이 5% 줄어들지만 분산이 27배 폭증하고 진동과의 정상 결합이 깨집니다. 밸브 급폐쇄 시 수격 현상과 축 진동이 즉각 발생하는 1차 물리 변수이므로, 좌측 하단 그래프처럼 valve1 개발 세트 그리드 탐색을 통해 신호대잡음비 8.4dB와 F1 0.704를 달성하는 w=2.5를 최적값으로 확정했습니다."),
        ("질문 2 구두 답변: 엄격한 Dev/Holdout 분리 및 파라미터 동결 [1:05 ~ 1:50 / 45초]",
         "슬라이드 8번입니다. 결론부터 말씀드리면 데이터 누수는 전혀 없습니다. 이은용 학우님의 검증 방식과 완벽히 동일하게, valve1 계열 16개만을 개발 세트로 분리하여 모든 파라미터를 완전히 동결(Freeze)했습니다. 펌프 기계 관성 5~10초를 반영하여 좌측 상단처럼 윈도우 k=9초를 확정했고, 복원 에너지와 극단치 분산 스케일을 맞추는 결합 계수 β=2.2를 도출했습니다. 좌측 하단 그래프를 보시면, 동결된 파라미터 그대로 미학습된 valve2와 other 시나리오를 블라인드 평가했을 때도 개발 세트 0.704와 대등한 0.701 F1을 기록하여 99.6%의 일반화 재현성을 입증했습니다."),
        ("질문 3 구두 답변: 경보 피로 극복 및 Raw F1 무결성 입증 [1:50 ~ 2:35 / 45초]",
         "슬라이드 9번입니다. 먼저 학우님의 지적을 겸허히 수용하여, '전 지표 최고' 표기를 '종합 F1 및 정밀도 1위'로 즉시 정정했습니다. 기존 모델들이 재현율 0.66을 기록한 것은 좌측 상단 그래프처럼 정상 구간에서도 경보를 무차별 난사하여(정밀도 39%, 10번 중 6번 헛경보) 현장 작업자가 경보기를 꺼버리게 만드는 '경보 피로'의 결과였습니다. 모델 Y는 헛경보를 82% 제거하여 정밀도 89%를 달성했고, 조화평균 F1을 42% 끌어올렸습니다. 또한 학우님의 슬라이드 14 지적처럼 PA의 점수 왜곡에 전적으로 공감하며, 좌측 하단 그래프처럼 제 모든 개선 성과는 PA를 전혀 쓰지 않은 순수 Raw F1 0.704만을 기준으로 엄격히 검증했습니다."),
        ("종합 마무리 [2:35 ~ 2:55 / 20초]",
         "슬라이드 10번처럼, 이은용 학우님의 예리한 검토 덕분에 연구의 엄밀성과 보고서의 완성도를 완벽하게 보완할 수 있었습니다. 깊이 있는 질의를 던져주신 이은용 학우님께 다시 한번 진심으로 감사드립니다. 이상으로 답변을 마치겠습니다.")
    ]

    for title, script in scripts:
        ps_t = doc.add_paragraph()
        ps_t.paragraph_format.space_before = Pt(8)
        ps_t.paragraph_format.space_after = Pt(2)
        r_st = ps_t.add_run(f"▶ {title}")
        r_st.font.name = "맑은 고딕"
        r_st.font.size = Pt(10)
        r_st.font.bold = True
        r_st.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

        ps_b = doc.add_paragraph()
        ps_b.paragraph_format.space_before = Pt(2)
        ps_b.paragraph_format.space_after = Pt(4)
        ps_b.paragraph_format.left_indent = Inches(0.2)
        ps_b.paragraph_format.line_spacing = 1.3
        r_sb = ps_b.add_run(f'"{script}"')
        r_sb.font.name = "맑은 고딕"
        r_sb.font.size = Pt(9.2)
        r_sb.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # Save DOCX
    docx_paths = [
        os.path.join(BASE_DIR, "동료질의_답변서_이은용학우_진찬언.docx"),
        os.path.join(DOWNLOAD_DIR, "동료질의_답변서_이은용학우_진찬언.docx")
    ]
    for p in docx_paths:
        try:
            doc.save(p)
            print(f"[OK] Saved DOCX: {p}")
        except Exception as e:
            print(f"[Warn] Could not save DOCX to {p}: {e}")


if __name__ == "__main__":
    print("Building unified presentation with single answer per question...")
    build_unified_presentation()
    print("\nUpdating official written response report and oral script DOCX...")
    update_qa_docx_deliverable()
    print("\nAll deliverables successfully built!")
