# -*- coding: utf-8 -*-
with open(r'3차 PJT\build_qa_rebuttal_presentation.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'r_lead = pb.add_run(f"• {b_lead}: ")'
replacement = 'r_lead = pb.add_run()\n        r_lead.text = f"• {b_lead}: "'
text = text.replace(target, replacement)

target2 = 'r_body = pb.add_run(b_body)'
replacement2 = 'r_body = pb.add_run()\n        r_body.text = b_body'
text = text.replace(target2, replacement2)

with open(r'3차 PJT\build_qa_rebuttal_presentation.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Patch applied successfully!')
