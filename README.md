# 初中英語 2500 詞自學講義

> 依據中國初中英語課程標準 2500 詞大綱整理的自學講義（繁體中文版）

## 📁 專案結構

```
junior-high-2500-vocab/
├── source/                          # 原始素材
│   └── 中國初中2500_原始.pdf         #   使用者上傳的原始 PDF
├── data/                            # 結構化資料
│   └── 初中英語2500詞_自學講義.xlsx   #   三個分頁：單字表、學習指引、統計總覽
├── scripts/                         # 工具腳本
│   └── generate_vocab_pdf.py        #   從 xlsx 產生設計感 PDF
└── output/                          # 輸出成品
    ├── 初中英語2500詞_自學講義.pdf    #   50 頁設計版 PDF
    └── vocab_2500.html              #   轉 PDF 的中繼 HTML
```

## 📊 資料規模

| 項目 | 數量 |
|------|------|
| 單字數 | 553 |
| 字母章節 | A–Z 共 26 章 |
| 學習指引 | 6 則教學筆記 |
| PDF 頁數 | 50 頁 |

## 🔧 重新產生 PDF

```bash
cd /srv/projects/junior-high-2500-vocab
python3 scripts/generate_vocab_pdf.py
~/.hermes/venv/bin/python3 -c "
from weasyprint import HTML
HTML('/tmp/vocab_2500.html').write_pdf('output/初中英語2500詞_自學講義.pdf')
"
```

## 📖 資料欄位說明（單字表）

| 欄位 | 說明 |
|------|------|
| 編號 | 流水號 |
| 單字 | 英文單字 |
| KK音標 | 美式發音 |
| 詞性 | v./n./adj./adv. 等 |
| 中文釋義 | 繁體中文翻譯 |
| 例句 | 英文例句 |
| 例句中譯 | 繁體中文翻譯 |
| 字母 | 首字母（A–Z） |
| 學習筆記 | 教學備註 |
