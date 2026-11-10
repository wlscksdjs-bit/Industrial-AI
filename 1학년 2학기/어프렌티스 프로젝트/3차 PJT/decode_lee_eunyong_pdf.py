# -*- coding: utf-8 -*-
"""
decode_lee_eunyong_pdf.py
Decodes hex-encoded TJ arrays using the ToUnicode CMaps in the PDF.
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
import pypdf

def parse_all_cmaps(reader):
    cmaps = {}
    for p_idx, page in enumerate(reader.pages):
        fonts = page.get('/Resources', {}).get('/Font', {})
        for fname, fref in fonts.items():
            if fname in cmaps:
                continue
            fobj = fref.get_object()
            if '/ToUnicode' in fobj:
                raw_cmap = fobj['/ToUnicode'].get_data().decode('latin1', errors='ignore')
                mapping = {}
                # parse beginbfchar
                for block in re.findall(r'beginbfchar(.*?)endbfchar', raw_cmap, re.DOTALL):
                    pairs = re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', block)
                    for src, dst in pairs:
                        code = int(src, 16)
                        # dst could be 4 or 8 hex digits
                        chars = ''.join([chr(int(dst[i:i+4], 16)) for i in range(0, len(dst), 4)])
                        mapping[code] = chars
                # parse beginbfrange
                for block in re.findall(r'beginbfrange(.*?)endbfrange', raw_cmap, re.DOTALL):
                    ranges = re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', block)
                    for start_hex, end_hex, dst_hex in ranges:
                        s_code = int(start_hex, 16)
                        e_code = int(end_hex, 16)
                        d_code = int(dst_hex, 16)
                        for c in range(s_code, e_code + 1):
                            mapping[c] = chr(d_code + (c - s_code))
                cmaps[fname] = mapping
    return cmaps

def decode_page_content(page, cmaps):
    contents = page.get_contents()
    if not contents:
        return ""
    if isinstance(contents, list):
        raw = b''.join([c.get_data() for c in contents]).decode('latin1', errors='ignore')
    else:
        raw = contents.get_data().decode('latin1', errors='ignore')
    
    # Process text operations
    # Track current font: /F1 12 Tf
    lines = []
    current_font = None
    
    # Split by operators
    tokens = re.split(r'(\s+)', raw)
    
    # Simpler regex approach: find /F[0-9]+ [0-9.]+ Tf and [ ... ] TJ
    text_chunks = []
    
    # Split stream into command sequences
    ops = re.findall(r'(/F\d+)\s+[\d\.]+\s+Tf|\[(.*?)\]\s*TJ|<([0-9a-fA-F]+)>\s*Tj', raw, re.DOTALL)
    
    cur_font = None
    for f_match, tj_match, single_tj in ops:
        if f_match:
            cur_font = f_match
        elif tj_match and cur_font in cmaps:
            cmap = cmaps[cur_font]
            # extract <hex> tokens
            hexes = re.findall(r'<([0-9a-fA-F]+)>', tj_match)
            chunk = []
            for h in hexes:
                # 4 hex chars per code
                for i in range(0, len(h), 4):
                    code = int(h[i:i+4], 16)
                    chunk.append(cmap.get(code, f'[?{h[i:i+4]}]'))
            text_chunks.append(''.join(chunk))
        elif single_tj and cur_font in cmaps:
            cmap = cmaps[cur_font]
            chunk = []
            for i in range(0, len(single_tj), 4):
                code = int(single_tj[i:i+4], 16)
                chunk.append(cmap.get(code, f'[?{single_tj[i:i+4]}]'))
            text_chunks.append(''.join(chunk))
            
    return '\n'.join(text_chunks)

def main():
    pdf_path = r'3차 PJT\2026254008_이은용_SKAB 데이터셋 산업 설비 이상감지_v4.pdf'
    reader = pypdf.PdfReader(pdf_path)
    cmaps = parse_all_cmaps(reader)
    print(f'Parsed {len(cmaps)} font CMaps.')
    
    out_file = r'3차 PJT\lee_eunyong_fully_decoded.txt'
    with open(out_file, 'w', encoding='utf-8') as f:
        for p_idx, page in enumerate(reader.pages):
            f.write(f'============================== PAGE {p_idx+1} ==============================\n')
            decoded = decode_page_content(page, cmaps)
            f.write(decoded + '\n\n')
            
    print(f'Successfully wrote fully decoded text to {out_file}!')

if __name__ == '__main__':
    main()
