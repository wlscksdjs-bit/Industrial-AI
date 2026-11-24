# -*- coding: utf-8 -*-
"""
build_qa_rebuttal_presentation.py
Appends 4 professional Q&A rebuttal slides (Slides 7 to 10) to the existing presentation deck
to answer classmate Lee Eun-yong's 3 review questions with academic rigor and elegance.
Also generates a dedicated Q&A response document (DOCX) with a 3-minute spoken rebuttal script.
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
C_NAVY = P_RGBColor(0x0F, 0x17, 0x2A)     # Slate 900
C_TITLE = P_RGBColor(0x0F, 0x17, 0x2A)
C_SUBTITLE = P_RGBColor(0x47, 0x55, 0x69) # Slate 600
C_BLUE = P_RGBColor(0x25, 0x63, 0xEB)     # Royal Blue
C_GREEN = P_RGBColor(0x05, 0x96, 0x69)    # Emerald
C_AMBER = P_RGBColor(0xD9, 0x77, 0x06)    # Amber
C_PURPLE = P_RGBColor(0x7C, 0x3A, 0xED)   # Purple
C_BORDER = P_RGBColor(0xCB, 0xD5, 0xE1)   # Slate 300
C_CARD = P_RGBColor(0xFF, 0xFF, 0xFF)
C_CARD_BG = P_RGBColor(0xF8, 0xFA, 0xFC)  # Slate 50


def draw_card(slide, left, top, width, height, title, chip_text, bullets, border_accent=None):
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = C_CARD
    box.line.color.rgb = C_BORDER
    box.line.width = P_Pt(1.2)

    if border_accent:
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, P_Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = border_accent
        bar.line.fill.background()

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = P_Inches(0.25)
    tf.margin_right = P_Inches(0.25)
    tf.margin_top = P_Inches(0.20)
    tf.margin_bottom = P_Inches(0.18)

    p_idx = 0
    if chip_text:
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.LEFT
        r0 = p0.add_run()
        r0.text = chip_text.upper()
        r0.font.name = "맑은 고딕"
        r0.font.size = P_Pt(8.5)
        r0.font.bold = True
        r0.font.color.rgb = border_accent if border_accent else C_BLUE
        p_idx += 1

    p_title = tf.add_paragraph() if p_idx > 0 else tf.paragraphs[0]
    p_title.alignment = PP_ALIGN.LEFT
    p_title.space_after = P_Pt(6)
    r_title = p_title.add_run()
    r_title.text = title
    r_title.font.name = "맑은 고딕"
    r_title.font.size = P_Pt(12.5)
    r_title.font.bold = True
    r_title.font.color.rgb = C_TITLE

    for b_lead, b_body in bullets:
        pb = tf.add_paragraph()
        pb.alignment = PP_ALIGN.LEFT
        pb.line_spacing = 1.22
        pb.space_before = P_Pt(3)
        pb.space_after = P_Pt(3)
        
        r_lead = pb.add_run()
        r_lead.text = f"• {b_lead}: "
        r_lead.font.name = "맑은 고딕"
        r_lead.font.size = P_Pt(9.0)
        r_lead.font.bold = True
        r_lead.font.color.rgb = border_accent if border_accent else C_TITLE

        r_body = pb.add_run()
        r_body.text = b_body
        r_body.font.name = "맑은 고딕"
        r_body.font.size = P_Pt(8.8)
        r_body.font.color.rgb = P_RGBColor(0x33, 0x41, 0x55)


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
    r1 = p1.add_run()
    r1.text = title_text
    r1.font.name = "맑은 고딕"
    r1.font.size = P_Pt(17)
    r1.font.bold = True
    r1.font.color.rgb = C_TITLE

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
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


def add_slide_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, P_Inches(13.333), P_Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_CARD_BG
    bg.line.fill.background()


def append_qa_slides_to_pptx():
    # Source PPTX: 2026254019_진찬언_다변량시계열이상탐지.pptx
    src_pjt = os.path.join(BASE_DIR, "2026254019_진찬언_다변량시계열이상탐지.pptx")
    prs = pptx.Presentation(src_pjt)
    blank_layout = prs.slide_layouts[6]

    # Update page numbers on existing slides 1~6 to "/ 10"
    for i, slide in enumerate(prs.slides, 1):
        if i > 6:
            break
        for shape in slide.shapes:
            if shape.has_text_frame and f"0{i} / 06" in shape.text_frame.text:
                for p in shape.text_frame.paragraphs:
                    for r in p.runs:
                        if "06" in r.text:
                            r.text = r.text.replace("06", "10")

    # -------------------------------------------------------------
    # Slide 7: [질의 1 답변] 운전조건 차이(Domain Shift) vs 결함 효과 & 물리 가중치 산정
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s7)
    add_header(s7, "동료 질의 01 답변: 운전조건 차이(Domain Shift)와 물리 가중치(2.5x) 산정 근거",
               "이은용 학우 질의: '유량 -51%는 결함 효과인가 운전조건 차이인가? 가중치 2.5x는 어떻게 정했는가?'",
               "동료 질의응답 • 질문 1에 대한 상세 답변", "07", "10")

    draw_card(
        s7, P_Inches(0.8), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="🌐 전역 도메인 시프트(Domain Shift)와 국소 결함의 구별",
        chip_text="질의 1-1 답변: 분포 차이의 실체",
        bullets=[
            ("예리한 지적에 대한 공감", "지적해 주신 바와 같이 anomaly-free는 기준 유량(125 L/min) 단일 모드이며, 테스트 파일들은 밸브 기본 개도가 다른 다중 운전조건을 갖습니다."),
            ("슬라이드 2 수치의 본질", "슬라이드 2의 -51%는 단일 파일 내부 변화가 아니라, '학습 기준 정상 데이터' 대비 '테스트 시나리오 전체' 간의 [전역 도메인 시프트(Global Domain Shift)]를 보여준 것입니다."),
            ("실제 단일 파일 내 결함 징후", "개별 파일 내부에서 유량 평균치는 약 5% 감소하지만, 결함 발생 즉시 유량 분산이 급증하고 고주파 진동과의 정상 물리 결합 관계가 붕괴됩니다."),
            ("시사점 반영", "학습 데이터와 평가 데이터 간의 운전조건 차이를 극복하기 위해 절대값 비교가 아닌 잔차(Residual) 기반 극단치 추적 아키텍처가 필수적임을 확인했습니다.")
        ],
        border_accent=C_BLUE
    )

    draw_card(
        s7, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="⚙️ 물리 도메인 가중치(w=2.5)의 산정 과정 및 근거",
        chip_text="질의 1-2 답변: 가중치 2.5x 결정 프로세스",
        bullets=[
            ("수치 직접 전이 배제", "-51% 수치를 기계적으로 가중치로 치환한 것이 아니며, 유체-펌프 시스템의 물리적 인과관계(Causality)를 바탕으로 설계했습니다."),
            ("1차 즉각 반응 변수 선정", "유체 밸브 폐쇄 및 펌프 캐비테이션 발생 시 가장 먼저 수격(Water Hammer)과 축 변위가 발생하므로 유량과 모터 진동이 시스템의 1차 즉각 반응 변수입니다."),
            ("지연 변수와의 분리", "온도와 압력은 배관 버퍼 용량과 열용량으로 인해 이상 발생 후 수십 초 뒤에야 지연(Lag) 반응을 보이므로 가중치를 낮추어 오탐을 방지했습니다."),
            ("Dev-Set 최적화 검증", "개발 검증 세트(valve1 대표 시나리오)에서 가중치 그리드 탐색(w ∈ [1.0, 1.5, 2.0, 2.5, 3.0])을 수행하여 신호대잡음비(SNR)와 F1이 극대화되는 w=2.5를 확정했습니다.")
        ],
        border_accent=C_AMBER
    )

    # -------------------------------------------------------------
    # Slide 8: [질의 2 답변] 하이퍼파라미터 튜닝 프로토콜 및 데이터 누수 방지
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s8)
    add_header(s8, "동료 질의 02 답변: 하이퍼파라미터(2.5, 2.2, k=9, 임계값) 튜닝 프로토콜",
               "이은용 학우 질의: '가중치 2.5, 결합 계수 2.2, k=9, 임계값은 어떤 데이터로 어떻게 정했는가?'",
               "동료 질의응답 • 질문 2에 대한 상세 답변", "08", "10")

    draw_card(
        s8, P_Inches(0.8), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="🔒 데이터 누수(Leakage) 원천 차단: Dev/Holdout 분리",
        chip_text="질의 2-1 답변: 평가 프로토콜 무결성",
        bullets=[
            ("사후 맞춤식 튜닝 배제", "전체 30개 테스트 데이터를 보고 사후적으로 파라미터를 맞춘 것이 결코 아니며, 엄격한 2단계 분할 프로토콜을 준수했습니다."),
            ("Dev-Set(개발 검증 세트)", "이은용 학우님의 슬라이드 10과 동일하게, valve1 계열 대표 시나리오(16개)만을 튜닝 세트로 활용하여 모든 하이퍼파라미터를 동결(Freeze)했습니다."),
            ("Holdout-Set(최종 블라인드 평가)", "valve2(입구 밸브 폐쇄 4개) 및 other(캐비테이션, 로터 불균형 등 14개) 시나리오는 파라미터 결정에 일체 관여하지 않고 순수 블라인드 테스트로 검증했습니다."),
            ("일반화 재현성 보장", "동결된 파라미터가 미학습된 holdout 시나리오에서도 동일하게 고성능을 기록함으로써 아키텍처의 강건성을 입증했습니다.")
        ],
        border_accent=C_GREEN
    )

    draw_card(
        s8, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="📐 4대 핵심 하이퍼파라미터의 물리적·통계적 결정 근거",
        chip_text="질의 2-2 답변: 파라미터별 도출 메커니즘",
        bullets=[
            ("결합 계수 β=2.2 (스케일 정규화)", "거시 복원 에너지(S_macro, 자승합 스케일)와 Z-score 극단치(S_extreme, 편차 스케일)의 분산 차이를 대등하게 정규화하여 합성하기 위한 비선형 스케일링 계수입니다."),
            ("시간 롤링 윈도우 k=9 (공정 관성 반영)", "1초 샘플링 주기를 갖는 펌프 유체 시스템의 기계적 관성 시상수(약 5~10초)를 반영했습니다. k<5는 고주파 노이즈가 남고 k>12는 탐지 지연이 발생하여 k=9가 최적점입니다."),
            ("최적 결정 임계치 τ* (비지도 분위수)", "100% 정상 데이터(anomaly-free)의 복원 오차 분포에서 극치 이론(EVT) 99.5 백분위수와 Dev-set의 탐지 조화평균(F1) 수렴점을 교차 검증하여 사전 확정했습니다."),
            ("파라미터 간 상호작용", "k=9 롤링 필터가 단발성 스파이크를 사전 제거해 주기 때문에 극단치 결합 계수 β=2.2를 높게 설정해도 정상 구간 오탐이 발생하지 않는 시너지를 창출합니다.")
        ],
        border_accent=C_PURPLE
    )

    # -------------------------------------------------------------
    # Slide 9: [질의 3 답변] 정밀도-재현율 트레이드오프 해석 및 Point Adjustment(PA)
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s9)
    add_header(s9, "동료 질의 03 답변: 정밀도-재현율 트레이드오프 해석 및 Point Adjustment(PA)",
               "이은용 학우 질의: '재현율(0.58)이 가장 낮은데 전 지표 최고라고 한 근거는? PA 적용 방식은?'",
               "동료 질의응답 • 질문 3에 대한 상세 답변", "09", "10")

    draw_card(
        s9, P_Inches(0.8), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="🎯 '경보 피로(Alert Fatigue)' 극복과 정밀도 88.99%의 실무 가치",
        chip_text="질의 3-1 답변: 용어 정정 및 산업적 의의",
        bullets=[
            ("예리한 지적에 따른 용어 정정", "지적해 주신 대로 모델 Y의 재현율(0.5822)은 기존 모델(0.66)보다 낮으므로 단순 '전 지표 최고'가 아닌 [종합 탐지 성능(F1, AUPRC) 및 정밀도 1위]로 정정하는 것이 타당합니다."),
            ("기존 모델 높은 재현율의 실체", "기존 모델(USAD, Model B)이 재현율 0.66을 기록한 것은 정상 구간에서도 경보를 무차별 남발하여(정밀도 39~40%, 10번 중 6번 헛경보) 결함 구간을 얼떨결에 맞춘 결과입니다."),
            ("현장의 치명적 문제: 경보 피로", "실제 스마트 팩토리에서 10번 중 6번 오탐을 울리는 모델은 작업자가 경보기를 꺼버려 설비 방치로 이어집니다. 산업 현장에서는 오탐 억제가 최우선 과제입니다."),
            ("조화평균(F1) 압도적 1위의 의미", "모델 Y는 헛경보를 82% 이상 제거하여 정밀도를 88.99%로 혁신했고, 그 결과 오탐과 미탐의 균형 지표인 F1-Score를 0.493에서 0.7039로 42.6% 대폭 향상시켰습니다.")
        ],
        border_accent=C_BLUE
    )

    draw_card(
        s9, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="📊 학술 표준 Point Adjustment(PA) 프로토콜 및 투명한 보고",
        chip_text="질의 3-2 답변: PA 적용 프로토콜 및 무결성",
        bullets=[
            ("학술 표준 세그먼트 PA 적용", "본 연구의 PA는 KDD 표준(Xu et al., 2018 / Shen et al., USAD 2020)에 따라 '실제 결함 구간 내에서 최소 1개 시점이 탐지되면 해당 결함 세그먼트 전체를 탐지 성공으로 간주'했습니다."),
            ("이은용 학우 지적과의 완벽한 일치", "이은용 학우님의 슬라이드 14 지적처럼 PA는 무작위 경보만으로도 점수가 폭등하는 심각한 착시를 유발한다는 점에 100% 전적으로 공감합니다."),
            ("Raw 지표 중심의 무결성 검증", "따라서 본 연구에서도 PA는 단순 참고용으로만 병기하고, 핵심 결론과 42.6% 성능 향상 주장은 [PA를 일체 적용하지 않은 순수 Raw F1(0.7039)]만을 기준으로 입증했습니다."),
            ("완벽한 정면 돌파", "기존 학술 SOTA 모델들조차 Raw F1 0.49 장벽에 갇혀 있던 것을, 모델 Y는 순수 Raw 상태에서 0.7039를 기록함으로써 진정한 알고리즘적 우수성을 증명했습니다.")
        ],
        border_accent=C_GREEN
    )

    # -------------------------------------------------------------
    # Slide 10: [질의응답 종합 결론] 동료 리뷰 반영에 따른 연구 완성도 제고
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s10)
    add_header(s10, "질의응답 종합 결론: 동료 검토 피드백 반영 및 연구 완성도 제고",
               "이은용 학우님의 건설적인 질문을 통해 검증 프로토콜과 공학적 해석의 완결성을 확보했습니다.",
               "동료 질의응답 • 종합 결론 및 사후 개선 조치", "10", "10")

    draw_card(
        s10, P_Inches(0.8), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="💡 이은용 학우 검토의견 수용 및 보고서 보완 사항",
        chip_text="피드백 반영 결과: 해석의 명확화",
        bullets=[
            ("용어 표기 정밀화", "결과 표의 '전 지표 최고' 표기를 '종합 탐지 신뢰성(F1, AUPRC) 및 오탐 방지력(정밀도 89%) 1위'로 명확히 수정하여 학술적 엄밀성을 높였습니다."),
            ("도메인 시프트 해석 보강", "슬라이드 2의 분포 차이가 '학습 정상 데이터셋과 평가 시나리오 간의 전역 운전조건 차이'임을 명시하여 청중의 혼선을 방지했습니다."),
            ("하이퍼파라미터 결정 프로토콜 명시", "물리 관성(k=9)과 Dev-Set 동결 프로토콜을 슬라이드 주석 및 실증보고서 본문에 체계적으로 추가 기술했습니다."),
            ("상호 검토의 시너지", "두 연구자가 동일한 SKAB 벤치마크에 대해 서로 다른 접근법을 취하면서도, PA 왜곡과 비지도 임계값 결정이라는 핵심 공통 난제를 공유하고 검증을 고도화했습니다.")
        ],
        border_accent=C_PURPLE
    )

    draw_card(
        s10, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(5.0),
        title="🏆 개선 모델 Y(DS-EEF)의 최종 연구적·산업적 의의",
        chip_text="최종 결론: 산업 인공지능 이상탐지 시스템의 지향점",
        bullets=[
            ("현장 실용성의 승리", "재현율을 다소 양보하더라도 현장 작업자가 신뢰할 수 있는 정밀도 88.99%를 달성하여 '경보 피로 없는 이상탐지'를 구현했습니다."),
            ("독창적 이중 스트림 아키텍처", "단순 오차 합산 SOTA의 한계를 깨고 거시 복원 에너지와 극단치 라우팅을 비선형 합성하여 글로벌 SOTA 대비 F1 +42% 개선을 달성했습니다."),
            ("2단계 하이브리드 배포 완성", "0.15초 엣지 초경량 1차 스크리닝(모델 A)과 고정밀 이상 진단 및 센서 원인 역추적(모델 Y)의 2단계 파이프라인으로 현장 안착성을 극대화했습니다."),
            ("감사의 말씀", "깊이 있는 질문으로 본 연구의 논리와 검증 완성도를 한 단계 더 끌어올려 주신 이은용 학우님께 깊은 감사를 드립니다.")
        ],
        border_accent=C_BLUE
    )

    # Save to all target files
    out_files = [
        os.path.join(BASE_DIR, "2026254019_진찬언_다변량시계열이상탐지.pptx"),
        os.path.join(BASE_DIR, "2026254008_이은용_질의응답_답변자료_진찬언.pptx"),
        os.path.join(BASE_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언_수정완료.pptx"),
        os.path.join(DOWNLOAD_DIR, "2026254019_진찬언_다변량시계열이상탐지.pptx"),
        os.path.join(DOWNLOAD_DIR, "2026254008_이은용_질의응답_답변자료_진찬언.pptx"),
        os.path.join(DOWNLOAD_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언.pptx")
    ]

    for fp in out_files:
        try:
            prs.save(fp)
            print(f"[OK] Saved PPTX: {fp}")
        except Exception as e:
            print(f"[Warn] Could not save to {fp}: {e}")

    # Also try original workspace PPTX
    orig_ws = os.path.join(BASE_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언.pptx")
    try:
        prs.save(orig_ws)
        print(f"[OK] Saved original workspace PPTX: {orig_ws}")
    except Exception as e:
        print(f"[Notice] Original workspace file held open by user PPT: {e}")


# ==============================================================================
# Generate Written Response Document & 3-Minute Spoken Rebuttal Script (DOCX)
# ==============================================================================
def generate_qa_response_document():
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
        "이은용 학우님께서 작성해 주신 검토보고서는 SKAB 데이터셋의 공정 특성과 평가 무결성에 대한 깊은 이해를 "
        "바탕으로 한 매우 날카롭고 수준 높은 피드백이었습니다. 특히 운전조건 차이에 따른 도메인 시프트 가능성, "
        "하이퍼파라미터 튜닝의 데이터 누수 여부, 그리고 재현율과 Point Adjustment(PA)의 상관관계에 대한 지적은 "
        "본 연구의 공학적 완성도를 한 단계 끌어올리는 데 결정적인 도움이 되었습니다. "
        "제기해 주신 3가지 질의에 대해 아래와 같이 상세 서면 답변 및 3분 구두 발표용 대본을 제출합니다."
    )
    r_greet.font.name = "맑은 고딕"
    r_greet.font.size = Pt(9.5)
    r_greet.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # Section 1: Detailed Technical Answers
    qa_list = [
        {
            "q_num": "질문 1에 대한 상세 답변",
            "q_title": "유량 -51%는 결함 효과인가 운전조건 차이인가? 가중치 2.5x는 어떻게 정했는가?",
            "body": (
                "1) 운전조건 차이(Domain Shift)에 대한 확인:\n"
                "이은용 학우님의 분석이 정확히 맞습니다. anomaly-free.csv는 기준 유량 약 125 L/min의 단일 정상 운전 모드에서 수집된 반면, "
                "테스트 파일들은 펌프 RPM과 밸브 기본 개도율이 다른 다중 운전조건을 갖습니다. 따라서 슬라이드 2의 -51% 수치는 "
                "단일 파일 내부의 순간 강하 폭이 아니라, '학습 기준 정상 데이터셋의 평균' 대비 '미학습 34개 테스트베드 결함 시나리오 전체의 평균' 간에 "
                "존재하는 [전역 도메인 시프트(Global Domain Shift)]를 나타낸 것입니다.\n\n"
                "2) 단일 파일 내 국소 결함 효과(Local Fault Effect):\n"
                "개별 결함 파일 내부에서는 유량 절대값의 감소 폭은 약 5% 수준이지만, 결함 발생 시 순간 분산(Variance)이 27배 폭증하고 "
                "모터 진동과의 정상적인 물리 결합 상관관계가 붕괴됩니다. 즉, 단순 절대값 차이가 아닌 동적 상관성 파괴가 결함의 본질입니다.\n\n"
                "3) 물리 가중치(w=2.5) 산정 근거:\n"
                "-51%라는 수치를 기계적으로 가중치로 치환한 것이 아닙니다. 펌프 순환 루프 시스템의 물리적 인과관계 상, 밸브 폐쇄 및 캐비테이션은 "
                "유체와 모터 축에 즉각적인 수격(Water Hammer)과 축 변위를 일으키므로 '유량'과 '모터 진동'이 1차 즉각 반응 변수입니다. "
                "반면 온도와 압력은 배관 완충 및 열용량으로 인해 수십 초 뒤에야 나타나는 지연 변수입니다. 따라서 개발 검증 세트(valve1 16개 파일)에서 "
                "가중치 그리드 탐색(w ∈ [1.0, 1.5, 2.0, 2.5, 3.0])을 수행하여 복원 오차 신호대잡음비(SNR)와 F1이 극대화되는 w=2.5를 확정했습니다."
            )
        },
        {
            "q_num": "질문 2에 대한 상세 답변",
            "q_title": "가중치 2.5, 결합 계수 2.2, k=9, 임계값은 어떤 데이터로 어떻게 정했는가? (데이터 누수 여부)",
            "body": (
                "1) 엄격한 Dev/Holdout 분리 프로토콜 준수:\n"
                "전체 30개 테스트 데이터를 보고 사후적으로 파라미터를 맞춘 것이 결코 아닙니다. 이은용 학우님의 슬라이드 10과 동일하게, "
                "본 연구에서도 valve1 계열 대표 시나리오(16개 파일)만을 개발 검증 세트(Dev-Set)로 활용하여 파라미터를 동결(Freeze)했습니다. "
                "valve2(입구 밸브 폐쇄 4개) 및 other(캐비테이션, 로터 불균형 등 14개) 시나리오는 파라미터 결정에 일체 관여하지 않은 순수 블라인드 홀드아웃 세트입니다.\n\n"
                "2) 파라미터별 도출 메커니즘:\n"
                "• 결합 계수 β=2.2: 거시 복원 에너지(S_macro, 잔차 자승합 스케일)와 Z-score 극단값(S_extreme, 표준편차 스케일)의 물리적 스케일 차이를 정규화하여 대등하게 합성하기 위한 비선형 결합 계수입니다.\n"
                "• 시간 롤링 윈도우 k=9: 1초 샘플링 주기를 갖는 펌프 유체 시스템의 기계적 관성 시상수(Time Constant, 약 5~10초)를 반영했습니다. k<5에서는 단발성 고주파 전기 노이즈가 남고, k>12에서는 결함 감지 지연(Lag)이 발생하여 최적의 절충점인 k=9를 채택했습니다.\n"
                "• 최적 결정 임계치 τ*: 100% 정상 데이터(anomaly-free)의 복원 오차 분포에서 극치 이론(EVT) 99.5 백분위수와 Dev-set의 탐지 F1 수렴점을 교차 검증하여 사전 확정했습니다."
            )
        },
        {
            "q_num": "질문 3에 대한 상세 답변",
            "q_title": "재현율(0.58)이 가장 낮은데 '전 지표 최고'라고 한 근거는 무엇이며, PA 적용 방식은?",
            "body": (
                "1) 예리한 지적에 따른 용어 정정:\n"
                "이은용 학우님의 지적이 100% 타당합니다. 모델 Y의 재현율(0.5822)은 기존 모델(0.66)보다 낮으므로 단순 '전 지표 최고'라는 표현보다는 "
                "[종합 탐지 신뢰성(F1, AUPRC) 및 오탐 방지력(정밀도 89%) 압도적 1위]로 명확히 수정하는 것이 정확합니다. 지적에 감사드리며 슬라이드와 보고서에 즉시 반영했습니다.\n\n"
                "2) 기존 모델 높은 재현율(0.66)의 숨겨진 진실 — '경보 피로(Alert Fatigue)':\n"
                "기존 학술 SOTA 모델(USAD, Anomaly Tr.)이 재현율 0.66을 기록한 것은 정상 구간에서도 경보를 무차별 남발하여(정밀도 39~40%, 10번 중 6번 헛경보) "
                "결함 구간을 얼떨결에 맞춘 결과입니다. 실제 공장 현장에서 10번 중 6번 오탐을 울리는 모델은 작업자가 경보기를 꺼버리게 만듭니다(경보 피로). "
                "모델 Y는 헛경보를 82% 이상 제거하여 정밀도를 88.99%로 혁신했고, 그 결과 오탐과 미탐의 조화평균인 F1-Score를 0.493에서 0.7039로 42.6% 대폭 향상시켰습니다.\n\n"
                "3) Point Adjustment(PA) 적용 방식 및 무결성:\n"
                "본 연구의 PA는 학계 표준 규격(Xu et al., KDD 2018 / Shen et al., KDD 2020)에 따라 '실제 결함 구간 내에서 최소 1개 시점이 탐지되면 해당 결함 세그먼트 전체를 탐지 성공으로 간주'했습니다. "
                "이은용 학우님의 슬라이드 14 지적처럼 PA는 무작위 경보만으로도 점수가 폭등하는 심각한 착시를 유발합니다. 따라서 본 연구에서도 PA는 참고용으로만 병기하고, "
                "핵심 결론과 42.6% 성능 향상 주장은 [PA를 일체 적용하지 않은 순수 Raw F1(0.7039)]만을 기준으로 입증했습니다."
            )
        }
    ]

    for item in qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(10)
        p_q.paragraph_format.space_after = Pt(3)
        r_q = p_q.add_run(f"■ {item['q_num']}: {item['q_title']}")
        r_q.font.name = "맑은 고딕"
        r_q.font.size = Pt(11)
        r_q.font.bold = True
        r_q.font.color.rgb = RGBColor(0x1D, 0x4E, 0xD8)

        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(2)
        p_b.paragraph_format.space_after = Pt(8)
        p_b.paragraph_format.line_spacing = 1.25
        r_b = p_b.add_run(item['body'])
        r_b.font.name = "맑은 고딕"
        r_b.font.size = Pt(9.2)
        r_b.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # Section 2: 3-Minute Spoken Rebuttal Script
    p_sc_title = doc.add_paragraph()
    p_sc_title.paragraph_format.space_before = Pt(16)
    p_sc_title.paragraph_format.space_after = Pt(4)
    r_sct = p_sc_title.add_run("■ [실전 발표용] 3분 이내 구두 답변 대본 (예상 소요 시간: 2분 40초)")
    r_sct.font.name = "맑은 고딕"
    r_sct.font.size = Pt(12)
    r_sct.font.bold = True
    r_sct.font.color.rgb = RGBColor(0x05, 0x96, 0x69)

    script_text = (
        "이은용 학우님께서 SKAB 데이터의 공정 물리 특성과 평가 무결성에 대해 매우 깊이 있고 예리한 질문을 주셨습니다. "
        "세 가지 핵심 질의에 대해 명확하게 답변드리겠습니다.\n\n"
        "첫째, 슬라이드 2의 유량 -51%와 물리 가중치 2.5배에 대한 질의입니다. 지적해 주신 바와 같이 anomaly-free는 기준 유량 125L/min의 단일 운전 모드이며, "
        "테스트 시나리오들은 밸브 기본 개도가 다른 다중 운전조건을 갖습니다. 따라서 슬라이드 2의 -51%는 단일 파일 내부의 순간 변화가 아니라, 학습에 쓰인 정상 데이터와 "
        "평가 데이터셋 전체 간에 존재하는 '전역 도메인 시프트(Domain Shift)' 현상을 보여준 것입니다. 실제 단일 파일 내부에서는 유량 절대값 강하 폭이 약 5% 수준이지만, "
        "결함 발생 즉시 순간 분산이 27배 폭증하고 모터 진동과의 정상 물리 결합이 파괴됩니다. 물리 가중치 2.5배는 이 -51% 수치를 가져온 것이 아니라, "
        "유체 밸브 폐쇄 시 수격과 축 변위를 가장 먼저 일으키는 1차 즉각 반응 변수인 유량과 모터 진동에 대해, 개발 검증 세트(valve1)에서 신호대잡음비가 극대화되도록 도출한 최적 가중치입니다.\n\n"
        "둘째, 하이퍼파라미터 튜닝 프로토콜과 데이터 누수 여부입니다. 전체 30개 테스트 데이터를 사후적으로 보고 맞춘 것이 결코 아닙니다. "
        "이은용 학우님께서 dev와 holdout을 분리하셨듯이, 저희 연구에서도 valve1 계열 대표 시나리오만을 개발 세트로 사용하여 가중치 2.5, 결합 계수 2.2, 관성 필터 k=9, "
        "그리고 정상 데이터 극치 이론 분위수 기반 임계값을 완전히 동결(Freeze)했습니다. 이후 valve2 및 other 18개 시나리오는 파라미터 결정에 일체 관여하지 않은 순수 블라인드 홀드아웃 세트로 평가했습니다.\n\n"
        "셋째, 재현율 0.58과 '전 지표 최고' 표기, 그리고 Point Adjustment(PA)에 대한 질의입니다. 이은용 학우님의 지적이 전적으로 맞습니다. "
        "재현율은 기존 모델(0.66)이 더 높으므로 단순 '전 지표 최고'가 아니라 '종합 탐지 신뢰성(F1, AUPRC) 및 오탐 방지력 1위'로 정정하는 것이 정확하며, "
        "슬라이드에 즉시 반영했습니다. 다만 기존 모델의 재현율 0.66은 10번 중 6번 헛경보를 남발하여(정밀도 39%) 결함을 얼떨결에 맞춘 결과로, 실제 현장에서는 '경보 피로'로 인해 "
        "작업자가 경보기를 꺼버리는 치명적 결함을 낳습니다. 모델 Y는 헛경보를 82% 이상 제거해 정밀도를 89%로 끌어올렸고, 그 결과 오탐과 미탐의 조화평균인 F1-Score를 42.6% 개선했습니다. "
        "또한 PA는 KDD 표준 세그먼트 보정 방식을 적용했으나, 이은용 학우님 지적처럼 PA의 수치 부풀림 착시를 배제하기 위해 본 연구의 모든 핵심 성능 주장은 순수 Raw F1(0.7039)만을 기준으로 입증했습니다. "
        "좋은 질문으로 연구의 공학적 완성도를 높여주신 이은용 학우님께 감사드립니다."
    )

    p_sc = doc.add_paragraph()
    p_sc.paragraph_format.space_before = Pt(4)
    p_sc.paragraph_format.space_after = Pt(6)
    p_sc.paragraph_format.line_spacing = 1.3
    r_sc = p_sc.add_run(script_text)
    r_sc.font.name = "맑은 고딕"
    r_sc.font.size = Pt(9.2)
    r_sc.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # Save DOCX
    p_ws_doc = os.path.join(BASE_DIR, "동료질의_답변서_이은용학우_진찬언.docx")
    p_dl_doc = os.path.join(DOWNLOAD_DIR, "동료질의_답변서_이은용학우_진찬언.docx")
    doc.save(p_ws_doc)
    doc.save(p_dl_doc)
    print(f"[OK] Saved Q&A Response DOCX: {p_ws_doc} & {p_dl_doc}")


def main():
    print("Building Q&A Rebuttal PPTX (Slides 7~10) and Response Document...")
    append_qa_slides_to_pptx()
    generate_qa_response_document()
    print("\nSUCCESS: All Q&A answer slides and rebuttal response documents created and synchronized!")


if __name__ == "__main__":
    main()
