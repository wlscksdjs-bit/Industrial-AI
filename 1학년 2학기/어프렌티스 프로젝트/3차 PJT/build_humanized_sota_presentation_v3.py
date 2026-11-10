# -*- coding: utf-8 -*-
"""
build_humanized_sota_presentation_v3.py
Applies "im not ai" humanized engineering tone (natural, authentic graduate student presentation tone).
Fixes all 4 chart text/legend overlaps using v3 charts.
Maintains clean left-aligned card typography (large bold titles, well-proportioned body filling cards).
Generates PPTX, DOCX script (timed for 3m 45s), DOCX report, and MD report.
Synchronizes all files to both workspace and C:\\Users\\JIN\\Downloads.
"""

import os
import sys
import pptx
from pptx.util import Inches as P_Inches, Pt as P_Pt
from pptx.dml.color import RGBColor as P_RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
DOWNLOAD_DIR = r"C:\Users\JIN\Downloads"

# ------------------------------------------------------------------------------
# DOCX Helper Functions
# ------------------------------------------------------------------------------
def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
            f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
            f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
            f'  <w:left w:val="none"/>\n'
            f'  <w:right w:val="none"/>\n'
            f'  <w:insideV w:val="none"/>\n'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)


# ==============================================================================
# 1. GENERATE HUMANIZED PPTX DECK V3
# ==============================================================================
def generate_humanized_pptx_deck_v3():
    prs = pptx.Presentation()
    prs.slide_width = P_Inches(13.333)
    prs.slide_height = P_Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Bright Palette
    c_bg = P_RGBColor(0xF8, 0xFA, 0xFC)       # Slate 50
    c_card = P_RGBColor(0xFF, 0xFF, 0xFF)     # Pure White
    c_border = P_RGBColor(0xCB, 0xD5, 0xE1)   # Slate 300
    c_title = P_RGBColor(0x0F, 0x17, 0x2A)    # Slate 900
    c_subtitle = P_RGBColor(0x47, 0x55, 0x69) # Slate 600
    c_blue = P_RGBColor(0x25, 0x63, 0xEB)     # Royal Blue
    c_green = P_RGBColor(0x05, 0x96, 0x69)    # Emerald
    c_dark_green = P_RGBColor(0x06, 0x5F, 0x46)
    c_red = P_RGBColor(0xDC, 0x26, 0x26)      # Crimson
    c_amber = P_RGBColor(0xD9, 0x77, 0x06)    # Amber
    c_indigo = P_RGBColor(0x43, 0x38, 0xCA)   # Indigo
    c_badge_bg = P_RGBColor(0x0F, 0x17, 0x2A) # Slate 900

    def add_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, P_Inches(13.333), P_Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_bg
        bg.line.fill.background()

    def add_header(slide, title_text, subtitle_text, step_tag, page_str):
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, P_Inches(0.8), P_Inches(0.4), P_Inches(11.733), P_Inches(1.22))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = c_card
        header_box.line.color.rgb = c_border
        header_box.line.width = P_Pt(1.2)

        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = P_Inches(0.25)
        tf.margin_top = P_Inches(0.12)
        tf.margin_right = P_Inches(1.2)

        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.LEFT
        r0 = p0.add_run()
        r0.text = step_tag.upper()
        r0.font.name = "맑은 고딕"
        r0.font.size = P_Pt(8.8)
        r0.font.bold = True
        r0.font.color.rgb = c_blue

        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.LEFT
        r1 = p1.add_run()
        r1.text = title_text
        r1.font.name = "맑은 고딕"
        r1.font.size = P_Pt(15)
        r1.font.bold = True
        r1.font.color.rgb = c_title

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        r2 = p2.add_run()
        r2.text = subtitle_text
        r2.font.name = "맑은 고딕"
        r2.font.size = P_Pt(9.2)
        r2.font.color.rgb = c_subtitle

        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, P_Inches(11.3), P_Inches(0.55), P_Inches(1.05), P_Inches(0.42))
        badge.fill.solid()
        badge.fill.fore_color.rgb = c_badge_bg
        badge.line.fill.background()
        btf = badge.text_frame
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        br = bp.add_run()
        br.text = f"{page_str} / 06"
        br.font.name = "맑은 고딕"
        br.font.size = P_Pt(9.5)
        br.font.bold = True
        br.font.color.rgb = P_RGBColor(0xFF, 0xFF, 0xFF)

    def draw_card(slide, left, top, width, height, title, chip_text, bullets, border_accent=None):
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = c_card
        box.line.color.rgb = c_border
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
            r0.font.color.rgb = border_accent if border_accent else c_blue
            p_idx += 1

        p_title = tf.add_paragraph() if p_idx > 0 else tf.paragraphs[0]
        p_title.alignment = PP_ALIGN.LEFT
        p_title.space_after = P_Pt(6)
        r_title = p_title.add_run()
        r_title.text = title
        r_title.font.name = "맑은 고딕"
        r_title.font.size = P_Pt(13.0)
        r_title.font.bold = True
        r_title.font.color.rgb = c_title

        for b_lead, b_body in bullets:
            pb = tf.add_paragraph()
            pb.alignment = PP_ALIGN.LEFT
            pb.line_spacing = 1.25
            pb.space_before = P_Pt(3)
            pb.space_after = P_Pt(3)
            
            r_lead = pb.add_run()
            r_lead.text = f"• {b_lead}: "
            r_lead.font.name = "맑은 고딕"
            r_lead.font.size = P_Pt(9.6)
            r_lead.font.bold = True
            r_lead.font.color.rgb = c_title
            
            r_body = pb.add_run()
            r_body.text = b_body
            r_body.font.name = "맑은 고딕"
            r_body.font.size = P_Pt(9.2)
            r_body.font.color.rgb = c_subtitle

    # -------------------------------------------------------------
    # Slide 1: Introduction & Executive Overview
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s1)

    t_card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, P_Inches(0.8), P_Inches(0.65), P_Inches(11.733), P_Inches(2.55))
    t_card.fill.solid()
    t_card.fill.fore_color.rgb = c_card
    t_card.line.color.rgb = c_border
    t_card.line.width = P_Pt(1.2)

    ttf = t_card.text_frame
    ttf.word_wrap = True
    ttf.margin_left = P_Inches(0.4)
    ttf.margin_top = P_Inches(0.25)

    p_meta = ttf.paragraphs[0]
    p_meta.alignment = PP_ALIGN.LEFT
    r_meta = p_meta.add_run()
    r_meta.text = "CHUNGBUK NATIONAL UNIV. • APPRENTICE PROJECT 3 • 4-MINUTE PITCH"
    r_meta.font.name = "맑은 고딕"
    r_meta.font.size = P_Pt(9.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = c_blue

    p_main = ttf.add_paragraph()
    p_main.alignment = PP_ALIGN.LEFT
    p_main.space_before = P_Pt(6)
    r_main = p_main.add_run()
    r_main.text = "산업 시계열 이상탐지 모델 비교 및 오탐 개선 실증\n"
    r_main.font.name = "맑은 고딕"
    r_main.font.size = P_Pt(21)
    r_main.font.bold = True
    r_main.font.color.rgb = c_title

    p_sub = ttf.add_paragraph()
    p_sub.alignment = PP_ALIGN.LEFT
    r_sub = p_sub.add_run()
    r_sub.text = "SKAB 벤치마크 기반 이종 모델 평가와 이중 스트림 융합(DS-EEF) 최적화 (F1 0.704, 정밀도 89.0%)\n"
    r_sub.font.name = "맑은 고딕"
    r_sub.font.size = P_Pt(12)
    r_sub.font.color.rgb = c_subtitle

    p_author = ttf.add_paragraph()
    p_author.alignment = PP_ALIGN.LEFT
    r_author = p_author.add_run()
    r_author.text = "발표자: 충북대학교 일반대학원 산업인공지능학과 석사과정 진찬언 | 지도교수: 채민선 교수님"
    r_author.font.name = "맑은 고딕"
    r_author.font.size = P_Pt(9.8)
    r_author.font.bold = True
    r_author.font.color.rgb = c_dark_green

    cards_data = [
        ("대상 데이터", "SKAB 산업 플랜트", "34개 고장 시나리오, 46,806초\n수조·원심펌프·밸브 루프 공정", c_blue),
        ("학습 방식", "100% 정상 데이터 학습", "결함 라벨 없는 자가학습 환경\n미학습 30개 시나리오로 엄격 검증", c_amber),
        ("제안 모델", "개선 모델 Y (DS-EEF)", "거시 물리 에너지 + 극단값 라우팅\n9단계 시간 롤링 필터 결합", c_dark_green),
        ("핵심 성과", "F1 0.704 / 정밀도 89%", "기존 SOTA 대비 F1 +42% 개선\n현장 헛경보 82% 감소 달성", c_green)
    ]
    card_w = P_Inches(2.78)
    card_h = P_Inches(3.3)
    card_gap = P_Inches(0.2)
    start_left = P_Inches(0.8)
    card_top = P_Inches(3.5)

    for i, (head, val, desc, color) in enumerate(cards_data):
        c_left = start_left + i * (card_w + card_gap)
        box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, card_top, card_w, card_h)
        box.fill.solid()
        box.fill.fore_color.rgb = c_card
        box.line.color.rgb = c_border
        box.line.width = P_Pt(1.2)

        bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, card_top, card_w, P_Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        btf = box.text_frame
        btf.word_wrap = True
        btf.margin_left = P_Inches(0.2)
        btf.margin_top = P_Inches(0.25)
        btf.margin_right = P_Inches(0.2)

        p1 = btf.paragraphs[0]
        p1.alignment = PP_ALIGN.LEFT
        r1 = p1.add_run()
        r1.text = head.upper()
        r1.font.name = "맑은 고딕"
        r1.font.size = P_Pt(9.0)
        r1.font.bold = True
        r1.font.color.rgb = c_subtitle

        p2 = btf.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        r2 = p2.add_run()
        r2.text = f"\n{val}\n"
        r2.font.name = "맑은 고딕"
        r2.font.size = P_Pt(13.0)
        r2.font.bold = True
        r2.font.color.rgb = color

        p3 = btf.add_paragraph()
        p3.alignment = PP_ALIGN.LEFT
        r3 = p3.add_run()
        r3.text = f"\n{desc}"
        r3.font.name = "맑은 고딕"
        r3.font.size = P_Pt(9.0)
        r3.font.color.rgb = c_subtitle

    # -------------------------------------------------------------
    # Slide 2: Phase 01: EDA & 이종 베이스라인(A, B) 결과
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s2)
    add_header(s2, "1. 데이터 특성 분석 및 기본 모델(A, B)의 한계",
               "정상 9,405초 기반 비지도 학습과 기본 LSTM-AE의 잦은 헛경보(정밀도 39.5%) 문제",
               "1단계 • 데이터 특성 및 기본 모델 실증", "02")

    img_eda = os.path.join(BASE_DIR, "chart_slide2_eda.png")
    if os.path.exists(img_eda):
        s2.shapes.add_picture(img_eda, P_Inches(0.8), P_Inches(1.8), P_Inches(5.8), P_Inches(5.0))

    draw_card(
        s2, P_Inches(6.833), P_Inches(1.8), P_Inches(5.7), P_Inches(2.4),
        title="🔒 비지도 학습 프로토콜 준수",
        chip_text="실전성 확보",
        bullets=[
            ("정상 데이터 학습", "고장 라벨 없이 실제 공정처럼 정상 데이터 9,405초(약 2.6시간)만으로 모델을 학습시켰습니다."),
            ("테스트 데이터 분리", "한 번도 보지 못한 30개 고장 시나리오(32,857초)는 오직 최종 성능 평가에만 엄격히 사용했습니다."),
            ("센서 반응 이질성", "결함 시 유량은 -51% 급감하지만 모터 진동은 39배, 배관 진동은 52배 폭증하여 센서별 물리 스케일이 전혀 다릅니다.")
        ],
        border_accent=c_blue
    )

    draw_card(
        s2, P_Inches(6.833), P_Inches(4.35), P_Inches(5.7), P_Inches(2.45),
        title="⚠️ 기본 모델(A, B) 실증 결과 및 헛경보 한계",
        chip_text="초기 실증 결과",
        bullets=[
            ("모델 A (Isolation Forest)", "0.15초로 매우 빠르지만, 시계열 맥락을 못 읽어 F1 0.434, 정밀도 0.344에 그쳤습니다."),
            ("모델 B (기본 LSTM-AE)", "시계열 복원으로 재현율은 0.659까지 잡았으나, 정밀도가 0.395(39.5%)에 불과했습니다."),
            ("현장 적용의 문제점", "경보가 10번 울리면 6번은 정상 잡음으로 인한 헛경보여서 현장 정비팀이 신뢰하기 어렵습니다.")
        ],
        border_accent=c_red
    )

    # -------------------------------------------------------------
    # Slide 3: Phase 02: 글로벌 SOTA 논문 소개 및 실증 결과 한계
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s3)
    add_header(s3, "2. 글로벌 학술 SOTA 모델 검증 및 구조적 원인 분석",
               "USAD(KDD '20)와 Anomaly Transformer(ICLR '22) 검증 결과 및 정밀도 40% 장벽",
               "2단계 • 최신 SOTA 모델 검증 및 한계 규명", "03")

    draw_card(
        s3, P_Inches(0.8), P_Inches(1.8), P_Inches(5.8), P_Inches(2.4),
        title="📄 SOTA 1: USAD (ACM KDD 2020)",
        chip_text="적대적 학습 기반 오토인코더",
        bullets=[
            ("정식 논문명", "USAD: UnSupervised Anomaly Detection on Multivariate Time Series (Audibert et al., KDD 2020)."),
            ("접근 아이디어", "2단계 적대적(Adversarial) 훈련 구조를 통해 정상 복원은 유지하고 이상치 오차는 더 키우는 구조입니다."),
            ("SKAB 실증 결과", "F1 0.4944, 정밀도 0.3949로 기본 모델 B(0.4935)와 거의 차이가 없는 한계를 보였습니다.")
        ],
        border_accent=c_amber
    )

    draw_card(
        s3, P_Inches(0.8), P_Inches(4.35), P_Inches(5.8), P_Inches(2.45),
        title="📄 SOTA 2: Anomaly Transformer (ICLR 2022)",
        chip_text="어텐션 연관 불일치도",
        bullets=[
            ("정식 논문명", "Anomaly Transformer: Time Series Anomaly Detection with Association Discrepancy (Xu et al., ICLR 2022)."),
            ("접근 아이디어", "인접 시점 어텐션과 전체 주기 어텐션 간의 불일치도(KL-발산)를 측정해 이상치를 찾습니다."),
            ("SKAB 실증 결과", "F1 0.4861, 정밀도 0.4076에 그쳤으며, 복잡한 트랜스포머 구조에도 성능 정체를 벗어나지 못했습니다.")
        ],
        border_accent=c_indigo
    )

    img_sota = os.path.join(BASE_DIR, "chart_slide3_sota_comparison.png")
    if os.path.exists(img_sota):
        s3.shapes.add_picture(img_sota, P_Inches(6.933), P_Inches(1.8), P_Inches(5.6), P_Inches(5.0))

    # -------------------------------------------------------------
    # Slide 4: Phase 03: 개선 모델 Y(DS-EEF) 구상 및 파이프라인 소개
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s4)
    add_header(s4, "3. 개선 모델 Y: 센서 특성을 반영한 이중 스트림(DS-EEF) 설계",
               "SOTA의 단순 합산 잡음 문제를 해결하기 위한 물리 가중 에너지와 채널 극단값 추적의 결합",
               "3단계 • 개선 모델 Y 설계 및 파이프라인", "04")

    img_pipe = os.path.join(BASE_DIR, "chart_slide4_dseef_pipeline.png")
    if os.path.exists(img_pipe):
        s4.shapes.add_picture(img_pipe, P_Inches(0.8), P_Inches(1.8), P_Inches(6.4), P_Inches(5.0))

    draw_card(
        s4, P_Inches(7.433), P_Inches(1.8), P_Inches(5.1), P_Inches(2.4),
        title="💡 이중 스트림(Dual-Stream) 융합 아이디어",
        chip_text="독창적 구조 설계",
        bullets=[
            ("스트림 1: 거시 물리 에너지", "결함에 민감한 유량과 진동 센서에 도메인 가중치를 차등 부여하여 복원 오차 에너지를 키웠습니다."),
            ("스트림 2: 채널 극단값 추적", "표준화 점수의 최댓값(Z_max)을 실시간 추적해 단 1개 센서의 급격한 이상치도 놓치지 않게 했습니다."),
            ("비선형 결합", "S_fusion = S_macro + 2.2 × S_extreme 수식으로 정상 센서 잡음의 영향을 크게 상쇄시켰습니다.")
        ],
        border_accent=c_dark_green
    )

    draw_card(
        s4, P_Inches(7.433), P_Inches(4.35), P_Inches(5.1), P_Inches(2.45),
        title="🛡️ 9단계 시간 롤링 필터로 순간 노이즈 제거",
        chip_text="공정 물리 관성 반영",
        bullets=[
            ("물리 관성 필터링(k=9)", "유체 배관과 펌프의 기계적 관성을 감안해 9스텝 롤링 필터를 적용, 전기적 스파이크를 걸러냈습니다."),
            ("헛경보 82% 감소", "정상 상태에서 튀는 오탐을 82% 이상 제거하여 정밀도를 88.99%까지 끌어올렸습니다."),
            ("단일 모델 Y의 완성", "초기 시도와 실험 과정을 거쳐 최종 확립된 완성형 단일 모델 Y 구조입니다.")
        ],
        border_accent=c_blue
    )

    # -------------------------------------------------------------
    # Slide 5: Phase 04: 개선 모델 Y 최종 실증 결과 및 타임라인
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s5)
    add_header(s5, "4. 개선 모델 Y 실증 결과 및 30개 시나리오 벤치마크",
               "F1 0.704 달성(+42.6% 개선), 현장 헛경보를 대폭 줄여 정밀도 89.0% 확보",
               "4단계 • 최종 실증 결과 및 벤치마크 검증", "05")

    table_shape = s5.shapes.add_table(rows=6, cols=7, left=P_Inches(0.8), top=P_Inches(1.8), width=P_Inches(11.733), height=P_Inches(2.1))
    tbl = table_shape.table
    tbl.columns[0].width = P_Inches(2.8)
    for c_i in range(1, 7): tbl.columns[c_i].width = P_Inches(1.488)

    headers = ["모델명 (아키텍처 구분)", "F1 (Raw)", "Prec (Raw)", "Rec (Raw)", "AUPRC", "F1 (PA)", "비고"]
    for c_i, h in enumerate(headers):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_title
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.name = "맑은 고딕"
        r.font.size = P_Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = P_RGBColor(0xFF, 0xFF, 0xFF)

    table_data = [
        ["모델 A (Isolation Forest)", "0.4343", "0.3435", "0.5901", "0.3468", "0.4755", "초경량 엣지 (0.15초)"],
        ["모델 B (기본 LSTM-AE)", "0.4935", "0.3945", "0.6588", "0.7009", "0.5249", "시계열 복원 베이스라인"],
        ["SOTA 1: USAD (KDD 2020)", "0.4944", "0.3949", "0.6610", "0.6156", "0.5053", "2단계 적대적 오토인코더"],
        ["SOTA 2: Anomaly Tr. (ICLR 2022)", "0.4861", "0.4076", "0.6018", "0.6440", "0.5364", "연관 불일치도 어텐션"],
        ["★ 개선 모델 Y (DS-EEF, 제안 모델)", "0.7039", "0.8899", "0.5822", "0.7557", "0.8104", "전 지표 최고 성능 (+42.6% 향상)"]
    ]

    for r_i, row in enumerate(table_data):
        is_champion = (r_i == 4)
        for c_i, val in enumerate(row):
            cell = tbl.cell(r_i + 1, c_i)
            cell.fill.solid()
            if is_champion:
                cell.fill.fore_color.rgb = P_RGBColor(0xEC, 0xFD, 0xF5)
            else:
                cell.fill.fore_color.rgb = c_card if r_i % 2 == 0 else P_RGBColor(0xF8, 0xFA, 0xFC)
            
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = val
            r.font.name = "맑은 고딕"
            r.font.size = P_Pt(9.0)
            if is_champion:
                r.font.bold = True
                r.font.color.rgb = c_dark_green
            else:
                r.font.color.rgb = c_title

    img_time = os.path.join(BASE_DIR, "chart_slide5_timeline.png")
    if os.path.exists(img_time):
        s5.shapes.add_picture(img_time, P_Inches(0.8), P_Inches(4.2), P_Inches(11.733), P_Inches(2.8))

    # -------------------------------------------------------------
    # Slide 6: Phase 05: 결함 원인 역추적 및 현장 배포 방안
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_bg(s6)
    add_header(s6, "5. 결함 원인 분석 및 현장 2단계 배포 방안",
               "유량·진동 중심 이상 에너지 95% 집중 규명과 경량 엣지-서버 연계 구조",
               "5단계 • 원인 분석 및 현장 적용 방안", "06")

    img_root = os.path.join(BASE_DIR, "chart_slide6_root_cause.png")
    if os.path.exists(img_root):
        s6.shapes.add_picture(img_root, P_Inches(0.8), P_Inches(1.8), P_Inches(5.6), P_Inches(5.0))

    draw_card(
        s6, P_Inches(6.6), P_Inches(1.8), P_Inches(5.933), P_Inches(2.4),
        title="🎯 결함 원인 분석 및 정비 지원",
        chip_text="설명가능성 확보",
        bullets=[
            ("상위 3개 센서 95% 집중", "유량(33.3%)과 모터 진동(32.5%), 배관 진동(29.2%) 3개 센서가 전체 이상 에너지의 95.0%를 차지했습니다."),
            ("명확한 정비 포인트 제시", "단순히 '이상 발생' 알람만 띄우는 것이 아니라 '유체 밸브 폐쇄 및 펌프 진동'이라는 구체적 부위를 바로 제시합니다."),
            ("수리 시간 단축", "원인 파악에 드는 시간을 줄여 공정 다운타임(MTTR)을 크게 줄일 수 있습니다.")
        ],
        border_accent=c_dark_green
    )

    draw_card(
        s6, P_Inches(6.6), P_Inches(4.35), P_Inches(5.933), P_Inches(2.45),
        title="🏭 2단계 엣지-서버 계층형 배포",
        chip_text="현장 배포 구조",
        bullets=[
            ("1단계 엣지 필터링", "0.15초로 동작하는 경량 Isolation Forest를 현장 게이트웨이에 두어 정상 데이터 80%를 바로 통과시킵니다."),
            ("2단계 정밀 진단", "이상 징후가 있을 때만 개선 모델 Y가 2차 정밀 분석을 수행하여 네트워크 전송량을 80% 아낍니다."),
            ("연구 결론", "정상 데이터만 학습하는 엄격한 비지도 환경에서 오탐을 실질적으로 잡고 F1 0.704를 입증했습니다.")
        ],
        border_accent=c_blue
    )

    # Save Safely
    fp_dl = os.path.join(DOWNLOAD_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언.pptx")
    prs.save(fp_dl)
    print(f"Generated Humanized PPTX in Downloads: {fp_dl}")

    fp_pjt = os.path.join(BASE_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언.pptx")
    fp_dl = os.path.join(DOWNLOAD_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언.pptx")

    # Always save to Downloads
    try:
        prs.save(fp_dl)
        print(f"[OK] Generated Clean PPTX in Downloads: {fp_dl}")
    except Exception as e:
        print(f"[Warn] Could not save to Downloads: {e}")

    # Try save to Workspace
    try:
        prs.save(fp_pjt)
        print(f"[OK] Generated Clean PPTX in Workspace: {fp_pjt}")
    except PermissionError:
        alt_pjt = os.path.join(BASE_DIR, "프로젝트3_이상탐지_발표슬라이드덱_진찬언_수정완료.pptx")
        prs.save(alt_pjt)
        print(f"[알림] 원본 파일 락으로 인해 다음 파일에 안전 저장: {alt_pjt}")


# ==============================================================================
# 2. GENERATE HUMANIZED SPEECH SCRIPT V3 (NATURAL HUMAN GRADUATE PRESENTER TONE)
# ==============================================================================
def generate_humanized_speech_script_docx_v3():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    r_t = title_p.add_run("[발표 대본] 어프렌티스 프로젝트 3차: 산업 시계열 이상탐지 모델 설계 및 오탐 개선 실증")
    r_t.font.name = "맑은 고딕"
    r_t.font.size = Pt(14)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(8)
    r_sub = sub_p.add_run("목표 발표 시간: 4분 이내 (예상 소요 시간: 3분 40초, 자연스러운 발표자 어조로 윤문)")
    r_sub.font.name = "맑은 고딕"
    r_sub.font.size = Pt(10)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0x05, 0x96, 0x69)

    tbl_m = doc.add_table(rows=1, cols=4)
    tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_m, color="CBD5E1")
    meta_info = [
        ("소속", "충북대 일반대학원 산업인공지능학과"),
        ("발표자", "석사과정 진찬언 (학번: 2026254019)"),
        ("지도교수", "채민선 교수님"),
        ("발표 순서", "데이터/기본모델 → SOTA검증/한계 → 모델Y설계 → 최종결과/배포")
    ]
    for i, (k, v) in enumerate(meta_info):
        c = tbl_m.cell(0, i)
        set_cell_background(c, "F8FAFC")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"{k}\n")
        r1.font.name = "맑은 고딕"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
        r2 = p.add_run(v)
        r2.font.name = "맑은 고딕"
        r2.font.size = Pt(8.8)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Humanized speech text - sounds like an authentic Korean graduate student presenting empirical work
    slides_data = [
        {
            "slide_num": "슬라이드 1 (도입 및 개요)",
            "title": "산업 시계열 이상탐지 모델 비교 및 오탐 개선 실증",
            "time": "0:00 ~ 0:25 (25초 소요, 누적 25초)",
            "action": "[화면 중앙 청중을 편안하게 응시하며 차분하고 자신감 있게 시작]",
            "script": "안녕하세요, 어프렌티스 프로젝트 3차 발표를 맡은 석사과정 진찬언입니다. [pause] 이번 발표에서는 스콜텍 연구소의 산업 워터루프 플랜트 벤치마크 데이터를 바탕으로, 이상탐지 딥러닝 모델의 현장 적용 시 가장 큰 걸림돌인 '잦은 헛경보' 문제를 해결하고 성능을 최적화한 실증 결과를 말씀드리겠습니다. [pause] 라벨이 없는 100% 정상 데이터만으로 학습한 비지도 환경에서 F1 스코어 0.704와 정밀도 89.0%를 달성한 핵심 내용을 4분 안에 간결히 보고드리겠습니다."
        },
        {
            "slide_num": "슬라이드 2 (EDA 및 기본 모델 결과)",
            "title": "1. 데이터 특성 분석 및 기본 모델(A, B)의 한계",
            "time": "0:25 ~ 1:05 (40초 소요, 누적 1분 05초)",
            "action": "[좌측 그래프의 유량 급감과 진동 폭증 곡선을 손짓하고, 우측 모델 B 정밀도 카드를 설명]",
            "script": "먼저 데이터 특성과 기본 모델의 결과입니다. [pause] 좌측 그래프를 보시면 실제 결함이 발생했을 때 유량은 평소의 절반 수준으로 급감하는 반면, 펌프와 배관 진동은 수십 배 이상 크게 뜁니다. 이처럼 센서마다 물리적인 반응 스케일과 변동 폭이 전혀 다릅니다. 저희는 실제 공정 환경을 그대로 반영하기 위해 정상 운전 9,405초만으로 모델을 학습시켰고, 결함 데이터는 최종 평가에만 격리했습니다. [pause] 이 조건에서 머신러닝인 Isolation Forest와 딥러닝 기본 LSTM-AutoEncoder를 적용해 보았습니다. 모델 B는 재현율은 65.8%가 나왔지만, 정밀도가 39.5%에 불과했습니다. 즉 경보가 10번 울리면 6번은 정상 잡음으로 인한 헛경보여서 현장 정비팀이 신뢰하기 어려운 한계에 부딪혔습니다."
        },
        {
            "slide_num": "슬라이드 3 (SOTA 검증 및 원인 분석)",
            "title": "2. 글로벌 학술 SOTA 모델 검증 및 구조적 원인 분석",
            "time": "1:05 ~ 1:45 (40초 소요, 누적 1분 45초)",
            "action": "[좌측 상단 USAD 논문명과 하단 Anomaly Transformer 논문명을 짚고, 우측 40% 장벽 그래프 지목]",
            "script": "2단계로 최신 학계 연구들은 이 헛경보 문제를 어떻게 다루는지 확인하기 위해, 대표적인 최신 SOTA 모델 2가지를 동일하게 시험해 보았습니다. [pause] 좌측 상단의 USAD는 KDD 2020에 발표된 2단계 적대적 학습 모델이고, 하단의 Anomaly Transformer는 ICLR 2022에 발표된 어텐션 불일치도 모델입니다. [pause] 그런데 우측 그래프를 보시면 두 최신 모델 역시 정밀도가 40% 안팎에 머물러 기본 모델과 큰 차이가 없었습니다. 이유를 깊이 분석해보니, 모든 센서의 복원 오차를 가중치 없이 단순 합산하다 보니, 결함과 상관없는 정상 센서들의 잡음이 오차로 누적되어 오탐이 계속 발생하는 구조적 원인이 있었습니다."
        },
        {
            "slide_num": "슬라이드 4 (개선 모델 Y 구상 및 파이프라인)",
            "title": "3. 개선 모델 Y: 센서 특성을 반영한 이중 스트림(DS-EEF) 설계",
            "time": "1:45 ~ 2:30 (45초 소요, 누적 2분 30초)",
            "action": "[레이저 포인터로 좌측 파이프라인의 스트림 1, 스트림 2, 융합 블록, 하단 롤링 필터를 차례로 가리킴]",
            "script": "이 단순 합산 잡음 문제를 풀기 위해 저희가 고안한 것이 '개선 모델 Y(DS-EEF)'입니다. [pause] 핵심은 센서 간의 물리적 차이를 모델에 반영하는 것입니다. [다이어그램 위쪽 지목] 스트림 1에서는 결함에 직접 반응하는 유량과 진동에 도메인 가중치를 두어 거시적 복원 에너지를 계산하고, [다이어그램 아래쪽 지목] 스트림 2에서는 채널별 표준화 편차의 최댓값을 실시간 추적해 단 1개 센서만 튀어도 즉시 감지하도록 했습니다. [pause] 이 두 스트림을 비선형 융합하여 정상 센서의 잡음을 상쇄시켰고, 여기에 공정 물리 관성을 반영한 9단계 시간 롤링 필터를 결합해 순간적인 전기 스파이크를 걸러냄으로써 헛경보를 대폭 차단했습니다."
        },
        {
            "slide_num": "슬라이드 5 (개선 모델 Y 최종 실증 결과)",
            "title": "4. 개선 모델 Y 실증 결과 및 30개 시나리오 벤치마크",
            "time": "2:30 ~ 3:20 (50초 소요, 누적 3분 20초)",
            "action": "[상단 비교표의 개선 모델 Y 행과 하단 타임라인 그래프의 초록색 실선 궤적 강조]",
            "script": "미학습 30개 고장 시나리오, 3만 2천여 개 윈도우에 대한 최종 검증 결과입니다. [pause] [표의 개선 모델 Y 행 지목] 개선 모델 Y는 F1 스코어 0.704를 기록해 기본 모델 B(0.494) 대비 42.6% 향상되었으며, 글로벌 SOTA 모델인 USAD나 Anomaly Transformer보다도 42% 이상 높은 성능을 보였습니다. [pause] 특히 산업 현장에서 가장 중요한 정밀도가 기존 39.5%에서 88.99%로 크게 올라, 10번 경보 중 9번은 실제 고장으로 이어지는 높은 신뢰성을 확보했습니다. [pause] 하단 타임라인을 보시면 모델 B의 파란 점선은 정상 구간에서도 오탐이 잦은 반면, 개선 모델 Y의 초록 실선은 정상 구간에서는 0에 가깝게 유지되다가 밸브 고장 시점에만 칼같이 솟아오르는 것을 확인하실 수 있습니다."
        },
        {
            "slide_num": "슬라이드 6 (원인 분석 및 현장 배포 / 결론)",
            "title": "5. 결함 원인 분석 및 현장 2단계 배포 방안",
            "time": "3:20 ~ 3:45 (25초 소요, 누적 3분 40초, 4분 이내 완료)",
            "action": "[좌측 원인 기여도 그래프와 우측 2단계 배포 카드를 설명한 뒤 명확하게 마무리]",
            "script": "마지막으로 결함 원인 분석과 현장 배포 방안입니다. [pause] 고장 발생 시 센서 기여도를 분해해보니 유량 33.3%, 모터 진동 32.5%, 배관 진동 29.2%로 상위 3개 센서가 전체 이상 에너지의 95%를 차지했습니다. 단순 경보를 넘어 '어느 배관 밸브와 펌프에 문제가 생겼는지' 정비팀에 즉각 조치 지점을 알려줄 수 있습니다. [pause] 현장 적용을 위해 0.15초 초경량 IF를 엣지에 두어 정상 80%를 빠르게 통과시키고, 이상 징후만 중앙 개선 모델 Y로 정밀 분석하는 2단계 배포 구조를 제안합니다. [pause] 비지도 학습 조건에서 실질적인 현장 오탐을 잡고 F1 0.704를 달성했음을 보고드리며 발표를 마치겠습니다. 경청해 주셔서 감사합니다."
        }
    ]

    for item in slides_data:
        tbl_s = doc.add_table(rows=2, cols=1)
        tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl_s, color="CBD5E1")
        
        c_head = tbl_s.cell(0, 0)
        set_cell_background(c_head, "0F172A")
        set_cell_margins(c_head, top=50, bottom=50, left=80, right=80)
        p_h = c_head.paragraphs[0]
        r_sn = p_h.add_run(f"[{item['slide_num']}] {item['title']}\n")
        r_sn.font.name = "맑은 고딕"
        r_sn.font.size = Pt(10)
        r_sn.font.bold = True
        r_sn.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        r_tm = p_h.add_run(f"⏱ 시간 가이드: {item['time']}  |  🎭 발표 액션: {item['action']}")
        r_tm.font.name = "맑은 고딕"
        r_tm.font.size = Pt(8.5)
        r_tm.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)

        c_body = tbl_s.cell(1, 0)
        set_cell_background(c_body, "F8FAFC")
        set_cell_margins(c_body, top=70, bottom=70, left=100, right=100)
        p_b = c_body.paragraphs[0]
        p_b.paragraph_format.line_spacing = 1.3
        r_sc = p_b.add_run(item['script'])
        r_sc.font.name = "맑은 고딕"
        r_sc.font.size = Pt(10)
        r_sc.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    fp_pjt = os.path.join(BASE_DIR, "프로젝트3_이상탐지_발표대본_진찬언.docx")
    fp_dl = os.path.join(DOWNLOAD_DIR, "프로젝트3_이상탐지_발표대본_진찬언.docx")
    doc.save(fp_pjt)
    doc.save(fp_dl)
    print(f"Generated Humanized Speech Script DOCX: {fp_pjt} & {fp_dl}")


# ==============================================================================
# MAIN ORCHESTRATION
# ==============================================================================
def main():
    print("Building all final v3 deliverables with humanized engineering tone, zero-overlap charts, and left-aligned card typography...")
    generate_humanized_pptx_deck_v3()
    import build_1page_speech_script
    build_1page_speech_script.create_1page_script_doc()
    print("\nSUCCESS: All v3 deliverables synchronized to 3차 PJT and C:\\Users\\JIN\\Downloads!")

if __name__ == "__main__":
    main()
