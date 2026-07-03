#!/usr/bin/env python3
"""Generate a mobile-friendly responsive HTML from the 初中英語2500詞講義."""

import openpyxl
import json
import html as html_mod
from collections import defaultdict

# Load data
wb = openpyxl.load_workbook('/srv/projects/junior-high-2500-vocab/data/初中英語2500詞_自學講義.xlsx')

ws = wb['單字表']
words = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[1] is None:
        continue
    words.append({
        'id': row[0], 'word': str(row[1]), 'phonetic': str(row[2]) if row[2] else '',
        'pos': str(row[3]) if row[3] else '', 'meaning': str(row[4]) if row[4] else '',
        'example': str(row[5]) if row[5] else '', 'example_zh': str(row[6]) if row[6] else '',
        'letter': str(row[7]) if row[7] else '', 'note': str(row[8]) if row[8] else ''
    })

by_letter = defaultdict(list)
for w in words:
    by_letter[w['letter']].append(w)
letters = sorted(by_letter.keys())

# Build JSON data for embedding
words_json = json.dumps(words, ensure_ascii=False)
letters_json = json.dumps(letters, ensure_ascii=False)

total_words = len(words)
words_with_example = sum(1 for w in words if w['example'])

# Count per letter
letter_counts = {l: len(by_letter[l]) for l in letters}
letter_counts_json = json.dumps(letter_counts, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>初中英語 2500 詞自學講義</title>
<style>
  :root {{
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --text-dim: #8b949e;
    --accent: #58a6ff;
    --accent-dim: #1f6feb;
    --red: #f85149;
    --orange: #d2991d;
    --green: #3fb950;
    --radius: 8px;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", "Noto Sans CJK TC", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding-bottom: env(safe-area-inset-bottom, 20px);
  }}

  .container {{ max-width: 800px; margin: 0 auto; padding: 12px 14px; }}

  /* ── Header ── */
  .header {{
    text-align: center;
    padding: 24px 0 12px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
  }}
  .header h1 {{ font-size: 1.5rem; font-weight: 700; letter-spacing: 0.03em; }}
  .header .badges {{
    display: flex; justify-content: center; gap: 10px; margin-top: 8px;
    flex-wrap: wrap;
  }}
  .badge {{
    font-size: 0.75rem; color: var(--text-dim);
    background: var(--surface); border: 1px solid var(--border);
    padding: 3px 10px; border-radius: 20px;
  }}

  /* ── Search ── */
  .search-bar {{
    position: sticky; top: 0; z-index: 100;
    background: var(--bg); padding: 8px 0 12px;
  }}
  .search-bar input {{
    width: 100%; padding: 10px 16px;
    font-size: 1rem; border-radius: var(--radius);
    border: 1px solid var(--border); background: var(--surface); color: var(--text);
    outline: none;
  }}
  .search-bar input:focus {{ border-color: var(--accent); }}
  .search-info {{ font-size: 0.8rem; color: var(--text-dim); margin-top: 4px; text-align: center; }}

  /* ── Letter nav ── */
  .letter-nav {{
    display: flex; flex-wrap: wrap; gap: 4px;
    padding: 8px 0 14px; justify-content: center;
  }}
  .letter-nav a {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px; font-size: 0.75rem; font-weight: 600;
    color: var(--text-dim); background: var(--surface);
    border: 1px solid var(--border); border-radius: 6px;
    text-decoration: none;
  }}
  .letter-nav a:hover, .letter-nav a:active {{ color: var(--accent); border-color: var(--accent); }}

  /* ── Letter section ── */
  .letter-section {{ margin-bottom: 20px; }}
  .letter-head {{
    font-size: 1.2rem; font-weight: 700; color: var(--accent);
    padding: 6px 0; margin-bottom: 8px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: baseline; gap: 8px;
    position: sticky; top: 0; background: var(--bg); z-index: 50;
  }}
  .letter-count {{ font-size: 0.75rem; color: var(--text-dim); font-weight: 400; }}

  /* ── Word card ── */
  .word-card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 10px 12px; margin-bottom: 8px;
    transition: border-color 0.15s;
  }}
  .word-card.hidden {{ display: none; }}
  .word-head {{
    display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap;
    margin-bottom: 3px;
  }}
  .word-num {{ font-size: 0.65rem; color: var(--text-dim); min-width: 20px; }}
  .word-text {{ font-weight: 700; color: var(--text); font-size: 1.05rem; }}
  .phonetic {{ color: var(--text-dim); font-size: 0.8rem; }}
  .pos {{
    color: var(--red); font-size: 0.7rem; font-weight: 600;
    background: rgba(248,81,73,0.1); padding: 1px 6px; border-radius: 3px;
  }}
  .word-meaning {{ color: var(--text); font-weight: 600; font-size: 0.95rem; }}
  .word-example {{
    margin-top: 4px; padding: 6px 8px;
    background: rgba(88,166,255,0.05); border-left: 2px solid var(--accent-dim);
    border-radius: 0 4px 4px 0; font-size: 0.85rem;
  }}
  .example-en {{ color: var(--text); font-style: italic; display: block; }}
  .example-zh {{ color: var(--text-dim); font-size: 0.8rem; display: block; margin-top: 2px; }}
  .word-note {{ margin-top: 4px; font-size: 0.78rem; color: var(--orange); font-style: italic; }}

  /* ── No results ── */
  .no-results {{
    text-align: center; padding: 40px 20px; color: var(--text-dim);
    display: none;
  }}
  .no-results.show {{ display: block; }}
  .no-results .emoji {{ font-size: 2rem; display: block; margin-bottom: 8px; }}

  /* ── Footer ── */
  .footer {{
    text-align: center; padding: 30px 0; color: var(--text-dim);
    font-size: 0.75rem; border-top: 1px solid var(--border); margin-top: 20px;
  }}

  /* ── Desktop tweaks ── */
  @media (min-width: 768px) {{
    .container {{ padding: 20px 24px; }}
    .header h1 {{ font-size: 2rem; }}
    .word-grid {{
      display: grid; grid-template-columns: 1fr 1fr; gap: 6px 12px;
    }}
  }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>📚 初中英語 2500 詞</h1>
    <p style="color:var(--text-dim);font-size:0.9rem;margin-top:2px;">自學講義 · 繁體中文版</p>
    <div class="badges">
      <span class="badge">📝 {total_words} 單字</span>
      <span class="badge">📖 {words_with_example} 例句</span>
      <span class="badge">🔤 {len(letters)} 字母章節</span>
    </div>
  </div>

  <div class="search-bar">
    <input type="text" id="search" placeholder="🔍 搜尋單字、詞性、中文釋義…" autocomplete="off">
    <div class="search-info" id="searchInfo"></div>
  </div>

  <nav class="letter-nav">
    <a href="#" onclick="document.getElementById('search').value='';filterWords();return false" style="width:auto;padding:0 8px;font-size:0.7rem;">全部</a>
'''

for l in letters:
    html += f'    <a href="#letter-{l}">{l}</a>\n'

html += '''  </nav>

  <div class="no-results" id="noResults">
    <span class="emoji">🔍</span>找不到符合的單字
  </div>

  <div id="wordContainer">
'''

# Word sections
for letter in letters:
    group = by_letter[letter]
    html += f'''    <div class="letter-section" id="letter-{letter}">
      <div class="letter-head">{letter} <span class="letter-count">{len(group)} 字</span></div>
      <div class="word-grid">
'''
    for w in group:
        phonetic = f' <span class="phonetic">{html_mod.escape(w["phonetic"])}</span>' if w['phonetic'] else ''
        pos = f' <span class="pos">{html_mod.escape(w["pos"])}</span>' if w['pos'] else ''
        
        card = f'''        <div class="word-card" data-word="{html_mod.escape(w['word'])}" data-meaning="{html_mod.escape(w['meaning'])}" data-pos="{html_mod.escape(w['pos'])}" data-example="{html_mod.escape(w['example'])}" data-examplezh="{html_mod.escape(w['example_zh'])}">
          <div class="word-head">
            <span class="word-num">{w['id']}</span>
            <span class="word-text">{html_mod.escape(w['word'])}</span>{phonetic}{pos}
          </div>
          <div class="word-meaning">{html_mod.escape(w['meaning'])}</div>'''
        
        if w['example']:
            card += f'''
          <div class="word-example">
            <span class="example-en">📝 {html_mod.escape(w['example'])}</span>
            <span class="example-zh">{html_mod.escape(w['example_zh'])}</span>
          </div>'''
        
        if w['note'] and w['note'] != 'None':
            card += f'''
          <div class="word-note">💡 {html_mod.escape(w['note'])}</div>'''
        
        card += '\n        </div>'
        html += card + '\n'
    
    html += '      </div>\n    </div>\n'

html += '''  </div>

  <div class="footer">
    初中英語 2500 詞自學講義 · 依據中國初中英語課程標準整理
  </div>
</div>

<script>
const cards = document.querySelectorAll('.word-card');
const searchInput = document.getElementById('search');
const searchInfo = document.getElementById('searchInfo');
const noResults = document.getElementById('noResults');
const container = document.getElementById('wordContainer');
const letterSections = document.querySelectorAll('.letter-section');

function filterWords() {
  const q = searchInput.value.trim().toLowerCase();
  let visible = 0;

  cards.forEach(card => {
    const word = (card.dataset.word || '').toLowerCase();
    const meaning = (card.dataset.meaning || '').toLowerCase();
    const pos = (card.dataset.pos || '').toLowerCase();
    const example = (card.dataset.example || '').toLowerCase();
    const exampleZh = (card.dataset.examplezh || '').toLowerCase();

    const match = !q || word.includes(q) || meaning.includes(q) || pos.includes(q) || example.includes(q) || exampleZh.includes(q);
    card.classList.toggle('hidden', !match);
    if (match) visible++;
  });

  // Show/hide letter sections
  letterSections.forEach(section => {
    const visibleCards = section.querySelectorAll('.word-card:not(.hidden)');
    section.style.display = visibleCards.length > 0 ? '' : 'none';
  });

  // Update UI
  if (q) {
    searchInfo.textContent = `找到 ${visible} 筆結果`;
    noResults.classList.toggle('show', visible === 0);
  } else {
    searchInfo.textContent = '';
    noResults.classList.remove('show');
  }
}

searchInput.addEventListener('input', filterWords);

// Smooth scroll to letter
document.querySelectorAll('.letter-nav a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) target.scrollIntoView({{ behavior: 'smooth' }});
  });
});
</script>
</body>
</html>'''

# Write
out_path = '/srv/projects/junior-high-2500-vocab/docs/index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Mobile HTML written: {out_path}")
print(f"Words: {total_words}, Letters: {len(letters)}")
