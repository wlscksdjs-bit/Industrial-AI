# -*- coding: utf-8 -*-
import sys, re, pypdf
sys.stdout.reconfigure(encoding='utf-8')

def parse_cmap(raw_cmap):
    cmap = {}
    for src, dst in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', raw_cmap):
        if len(src) == 4 and len(dst) == 4:
            cmap[int(src, 16)] = chr(int(dst, 16))
        elif len(src) == 4 and len(dst) > 4:
            chars = ''.join([chr(int(dst[i:i+4], 16)) for i in range(0, len(dst), 4)])
            cmap[int(src, 16)] = chars
    return cmap

reader = pypdf.PdfReader(r'3차 PJT\2026254008_이은용_SKAB 데이터셋 산업 설비 이상감지_v4.pdf')

with open(r'3차 PJT\lee_eunyong_all_slides_clean.txt', 'w', encoding='utf-8') as out:
    for p_idx, page in enumerate(reader.pages):
        out.write(f'============================== SLIDE {p_idx+1} ==============================\n')
        res = page['/Resources'].get_object()
        fonts = res['/Font'].get_object()
        cmaps = {}
        for fname, fref in fonts.items():
            fobj = fref.get_object()
            if '/ToUnicode' in fobj:
                cmaps[str(fname)] = parse_cmap(fobj['/ToUnicode'].get_data().decode('latin1', errors='ignore'))
        
        c = page.get_contents()
        raw = c.get_data().decode('latin1', errors='ignore')
        bts = re.findall(r'BT\s*(.*?)\s*ET', raw, re.DOTALL)
        
        cur_font = None
        for bt in bts:
            f_m = re.findall(r'(/F\d+)\s+[\d\.]+\s+Tf', bt)
            if f_m:
                cur_font = f_m[-1]
            tjs = re.findall(r'\[(.*?)\]\s*TJ', bt, re.DOTALL)
            for tj in tjs:
                chars = []
                for h in re.findall(r'<([0-9a-fA-F]{4})>', tj):
                    code = int(h, 16)
                    chars.append(cmaps.get(cur_font, {}).get(code, ''))
                t = ''.join(chars).strip()
                if t:
                    out.write(t + '\n')
        out.write('\n')

print('Successfully extracted all 16 slides to lee_eunyong_all_slides_clean.txt!')
