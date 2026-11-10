# -*- coding: utf-8 -*-
"""
extract_lee_slides_fixed.py
Extracts and decodes all text from Lee Eun-yong's PDF slides.
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
import pypdf

def parse_cmap(raw_cmap):
    cmap = {}
    # bfchar
    for src, dst in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', raw_cmap):
        if len(src) == 4 and len(dst) == 4:
            cmap[int(src, 16)] = chr(int(dst, 16))
        elif len(src) == 4 and len(dst) > 4:
            chars = ''.join([chr(int(dst[i:i+4], 16)) for i in range(0, len(dst), 4)])
            cmap[int(src, 16)] = chars
    # bfrange
    for start_h, end_h, dst_h in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', raw_cmap):
        if len(start_h) == 4 and len(end_h) == 4 and len(dst_h) == 4:
            s = int(start_h, 16)
            e = int(end_h, 16)
            d = int(dst_h, 16)
            for code in range(s, e + 1):
                cmap[code] = chr(d + (code - s))
    return cmap

def decode_page(page):
    res = page['/Resources'].get_object()
    fonts = res['/Font'].get_object()
    cmaps = {}
    for fname, fref in fonts.items():
        fobj = fref.get_object()
        if '/ToUnicode' in fobj:
            cmaps[str(fname)] = parse_cmap(fobj['/ToUnicode'].get_data().decode('latin1', errors='ignore'))

    contents = page.get_contents()
    if not contents:
        return ""
    if isinstance(contents, list):
        raw = b''.join([c.get_data() for c in contents]).decode('latin1', errors='ignore')
    else:
        raw = contents.get_data().decode('latin1', errors='ignore')

    bt_blocks = re.findall(r'BT\s*(.*?)\s*ET', raw, re.DOTALL)
    page_texts = []
    for bt in bt_blocks:
        cur_font = None
        f_m = re.findall(r'(/F\d+)\s+[\d\.]+\s+Tf', bt)
        if f_m:
            cur_font = f_m[-1]

        tj_blocks = re.findall(r'\[(.*?)\]\s*TJ', bt, re.DOTALL)
        for tj in tj_blocks:
            line_chars = []
            for h in re.findall(r'<([0-9a-fA-F]{4})>', tj):
                code = int(h, 16)
                if cur_font and cur_font in cmaps:
                    ch = cmaps[cur_font].get(code, '')
                else:
                    ch = ''
                line_chars.append(ch)
            text_str = ''.join(line_chars).strip()
            if text_str:
                page_texts.append(text_str)

        tj_single = re.findall(r'<([0-9a-fA-F]{4})>\s*Tj', bt)
        if tj_single and cur_font and cur_font in cmaps:
            text_str = ''.join([cmaps[cur_font].get(int(h, 16), '') for h in tj_single]).strip()
            if text_str:
                page_texts.append(text_str)

    return '\n'.join(page_texts)

def main():
    reader = pypdf.PdfReader(r'3차 PJT\2026254008_이은용_SKAB 데이터셋 산업 설비 이상감지_v4.pdf')
    out_file = r'3차 PJT\lee_eunyong_clean_slides.txt'
    with open(out_file, 'w', encoding='utf-8') as f:
        for i, page in enumerate(reader.pages):
            f.write(f'============================== SLIDE {i+1} ==============================\n')
            txt = decode_page(page)
            f.write(txt + '\n\n')
    print('Extraction done! Saved to', out_file)

if __name__ == '__main__':
    main()
