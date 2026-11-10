# -*- coding: utf-8 -*-
"""
build_peer_review_questions_docx.py
Generates a clean, simple, professional 1-page peer review question document
for classmate Lee Eun-yong (2026254008).
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = r"G:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
DOWNLOAD_DIR = r"C:\Users\JIN\Downloads"

DOC_NAME = "SKAB_산업설비이상감지_2026254008_이은용_검토질의서_2026254019_진찬언.docx"
DOC_NAME_ALT = "동료질의서_이은용학우_진찬언.docx"

C_NAVY = RGBColor(0x0F, 0x17, 0x2A)     # Slate 900
C_BLUE = RGBColor(0x1D, 0x4E, 0xD8)     # Blue 700
C_BODY = RGBColor(0x33, 0x41, 0x55)     # Slate 700
C_MUTED = RGBColor(0x64, 0x74, 0x8B)    # Slate 500


def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def create_peer_review_doc():
    doc = docx.Document()

    # Compact 1-Page A4 Margins
    for s in doc.sections:
        s.top_margin = Inches(0.45)
        s.bottom_margin = Inches(0.45)
        s.left_margin = Inches(0.55)
        s.right_margin = Inches(0.55)

    # Document Header / Category
    p_cat = doc.add_paragraph()
    p_cat.paragraph_format.space_before = Pt(0)
    p_cat.paragraph_format.space_after = Pt(1)
    r_cat = p_cat.add_run("충북대학교 대학원 산업인공지능학과 | 어프렌티스 프로젝트 3차 동료 검토 질의서")
    r_cat.font.name = "맑은 고딕"
    r_cat.font.size = Pt(8.0)
    r_cat.font.color.rgb = C_MUTED

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(1)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("SKAB 데이터셋 기반 산업 설비 이상감지 발표 질의서 (핵심 3선)")
    r_title.font.name = "맑은 고딕"
    r_title.font.size = Pt(13)
    r_title.font.bold = True
    r_title.font.color.rgb = C_NAVY

    # Metadata Table
    table = doc.add_table(rows=2, cols=4)
    table.alignment = docx.enum.table.WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(1.1), Inches(2.5), Inches(1.1), Inches(2.4)]
    meta_info = [
        [("과 제 명", True), ("SKAB 데이터셋 산업 설비 이상감지", False), ("발 표 자", True), ("2026254008 이은용 학우", False)],
        [("리 뷰 어", True), ("2026254019 진찬언", False), ("검 토 일", True), ("2026년 11월 10일", False)]
    ]

    for r_idx, row_data in enumerate(meta_info):
        for c_idx, (txt, is_hdr) in enumerate(row_data):
            cell = table.cell(r_idx, c_idx)
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=45, bottom=45, left=90, right=90)
            if is_hdr:
                set_cell_background(cell, "F1F5F9")
            else:
                set_cell_background(cell, "FFFFFF")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_hdr else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(txt)
            r.font.name = "맑은 고딕"
            r.font.size = Pt(8.2)
            if is_hdr:
                r.font.bold = True
                r.font.color.rgb = C_NAVY
            else:
                r.font.color.rgb = C_BODY

    # Brief Intro
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_before = Pt(6)
    p_intro.paragraph_format.space_after = Pt(6)
    p_intro.paragraph_format.line_spacing = 1.15
    r_intro = p_intro.add_run(
        "이은용 학우님의 발표 자료는 SKAB 34개 시나리오에 대해 dev/holdout을 엄격히 분리하고, "
        "Point Adjustment(PA)의 통계적 왜곡을 날카롭게 검증하며 비지도 이상탐지 프로토콜을 체계적으로 정립한 "
        "우수한 결과물입니다. 발표 내용을 더욱 발전적으로 공유받고자 발표자님의 연구 성과를 부각할 수 있는 "
        "핵심 질의 3가지를 드립니다."
    )
    r_intro.font.name = "맑은 고딕"
    r_intro.font.size = Pt(8.2)
    r_intro.font.color.rgb = C_BODY

    # 3 Core Questions Data
    questions = [
        {
            "num": "질문 1",
            "title": "[모델 최적화] Isolation Forest의 큰 폭 개선(+0.181)과 집단 이상(Collective Anomaly) 특성",
            "context": (
                "슬라이드 11~12에서 초경량 비시계열 모델인 Isolation Forest가 '점수 평활(E3)'과 '임계값 최적화(E4)' 결합 시 "
                "F1이 0.609에서 0.790으로 가장 큰 폭(+0.181)으로 상승하며 딥러닝(Conv-AE, 0.775)보다 우수한 최고 성능을 기록했습니다."
            ),
            "question": (
                "복잡한 딥러닝보다 단순한 Isolation Forest가 점수 평활과 결합했을 때 더 높은 일반화 성능을 낸 주된 이유가 "
                "슬라이드 4에서 짚어주신 SKAB 데이터셋의 '집단 이상(연속 구간 결함)' 특성과 어떤 연관이 있는지 발표자님의 견해가 궁금합니다."
            )
        },
        {
            "num": "질문 2",
            "title": "[평가 무결성] Point Adjustment(PA)의 왜곡 실증과 실제 산업 현장 알람 프로토콜",
            "context": (
                "슬라이드 14에서 '무작위 1% 경보 시 Without PA는 F1 0.02이나 With PA는 0.95까지 왜곡된다'는 강력한 실험 근거를 제시하시며, "
                "학계의 PA 과대평가 문제를 짚고 모든 판정을 엄격한 'Without PA' 기준으로 선언하신 점이 매우 훌륭했습니다."
            ),
            "question": (
                "실제 공정 현장에서는 순간 오탐 방지도 중요하지만 고장 확산 전 '구간 내 조기 감지'도 의미를 갖습니다. "
                "향후 현장 배포 시 연구용 기준인 '순수 Without PA'와 실무 운영용 '지속 감지 기준(예: k-step 롤링 경보)' 중 "
                "어떤 형태의 알람 프로토콜을 현장에 적용하는 것이 가장 현실적이라고 판단하시는지 의견을 여쭙고 싶습니다."
            )
        },
        {
            "num": "질문 3",
            "title": "[실전 배포 확장] 운전조건 변화(다중 정상 상태) 흡수 및 결함 원인 센서 역추적",
            "context": (
                "슬라이드 15의 한계 분석에서 '운전조건 변화에 따른 탐지 영향'과 '사후 분석(어느 센서가 결함을 유발했는지 "
                "원인을 규명하는 해석력)'의 필요성을 날카롭게 지적해 주셨습니다."
            ),
            "question": (
                "최종 선정된 우수 모델(Isolation Forest / PCA)을 실제 연속 펌프 공정에 상시 배포할 때, "
                "유량·압력 등의 '운전조건 변화에 의한 오경보'를 줄이고 작업자에게 '결함 원인 센서'를 직관적으로 제공하기 위해 "
                "염두에 두고 계신 보완 아이디어나 후속 연구 방향이 있으신지 궁금합니다."
            )
        }
    ]

    for q in questions:
        # Question Header Box
        p_q_hdr = doc.add_paragraph()
        p_q_hdr.paragraph_format.space_before = Pt(5)
        p_q_hdr.paragraph_format.space_after = Pt(2)
        
        r_q_badge = p_q_hdr.add_run(f"■ {q['num']}. ")
        r_q_badge.font.name = "맑은 고딕"
        r_q_badge.font.size = Pt(9.5)
        r_q_badge.font.bold = True
        r_q_badge.font.color.rgb = C_BLUE

        r_q_title = p_q_hdr.add_run(q['title'])
        r_q_title.font.name = "맑은 고딕"
        r_q_title.font.size = Pt(9.5)
        r_q_title.font.bold = True
        r_q_title.font.color.rgb = C_NAVY

        # Question Content Table (Single clean card)
        q_table = doc.add_table(rows=2, cols=1)
        q_table.alignment = docx.enum.table.WD_TABLE_ALIGNMENT.CENTER
        q_table.autofit = False

        # Row 1: Context
        c_ctx = q_table.cell(0, 0)
        c_ctx.width = Inches(7.1)
        set_cell_background(c_ctx, "F8FAFC")
        set_cell_margins(c_ctx, top=40, bottom=40, left=90, right=90)
        p_ctx = c_ctx.paragraphs[0]
        p_ctx.paragraph_format.line_spacing = 1.15
        
        r_ctx_lbl = p_ctx.add_run("[검토 배경 및 강점] ")
        r_ctx_lbl.font.name = "맑은 고딕"
        r_ctx_lbl.font.size = Pt(8.0)
        r_ctx_lbl.font.bold = True
        r_ctx_lbl.font.color.rgb = C_BLUE

        r_ctx_txt = p_ctx.add_run(q['context'])
        r_ctx_txt.font.name = "맑은 고딕"
        r_ctx_txt.font.size = Pt(8.0)
        r_ctx_txt.font.color.rgb = C_BODY

        # Row 2: Question
        c_q = q_table.cell(1, 0)
        c_q.width = Inches(7.1)
        set_cell_background(c_q, "EFF6FF")
        set_cell_margins(c_q, top=45, bottom=45, left=90, right=90)
        p_q = c_q.paragraphs[0]
        p_q.paragraph_format.line_spacing = 1.18

        r_q_lbl = p_q.add_run("[핵심 질의] ")
        r_q_lbl.font.name = "맑은 고딕"
        r_q_lbl.font.size = Pt(8.2)
        r_q_lbl.font.bold = True
        r_q_lbl.font.color.rgb = RGBColor(0x1E, 0x40, 0xAF)

        r_q_txt = p_q.add_run(q['question'])
        r_q_txt.font.name = "맑은 고딕"
        r_q_txt.font.size = Pt(8.2)
        r_q_txt.font.color.rgb = C_NAVY

    # Save to Workspace and Downloads
    p_ws = os.path.join(BASE_DIR, DOC_NAME)
    p_ws_alt = os.path.join(BASE_DIR, DOC_NAME_ALT)
    p_dl = os.path.join(DOWNLOAD_DIR, DOC_NAME)
    p_dl_alt = os.path.join(DOWNLOAD_DIR, DOC_NAME_ALT)

    doc.save(p_ws)
    doc.save(p_ws_alt)
    doc.save(p_dl)
    doc.save(p_dl_alt)
    print(f"[OK] 1-Page Peer review questions DOCX saved to:\n  - {p_ws}\n  - {p_dl}")


if __name__ == "__main__":
    create_peer_review_doc()
