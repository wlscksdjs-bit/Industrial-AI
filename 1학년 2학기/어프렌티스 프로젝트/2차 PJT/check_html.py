import os
c = open('presentation_deck.html', 'r', encoding='utf-8').read()
slides = c.count('class="slide')
print(f"Presentation deck verified! File size: {len(c)} characters, Total slides: {slides}")
