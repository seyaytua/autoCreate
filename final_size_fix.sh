#!/bin/bash

echo "数式サイズの最終調整を開始します..."

# style_config.pyをさらに小さく調整
cat > src/core/style_config.py << 'FINAL_STYLE_EOF'
"""統一スタイル設定（最終調整版）"""

STYLE_CONFIG = {
    # 数式画像設定
    'math_dpi': 300,
    'math_font_size': 10,  # さらに小さく（10pt）
    'math_color': 'black',
    'math_background': 'transparent',
    
    # インライン数式の高さ設定（ポイント単位）
    'inline_math_height': 11,  # 本文と同じ高さ（11pt）
    'display_math_width': 2.5,  # インチ単位
    
    # テキストスタイル
    'title_font': 'MS Gothic',
    'title_size': 16,
    'title_bold': True,
    'body_font': 'MS Mincho',
    'body_size': 11,
    
    # レイアウト
    'problem_spacing': 1.5,
    'paragraph_spacing': 1.15,
    'page_margin': 2.54,  # cm
    
    # 選択肢スタイル
    'choice_font': 'MS Mincho',
    'choice_size': 11,
    'choice_indent': 1.0,  # cm
}

# テンプレート定義
TEMPLATES = {
    'standard': {
        'name': '標準問題集',
        'header': None,
        'footer': 'ページ {page}',
        'title_style': '見出し 1',
        'numbering': True,
    },
    'exam': {
        'name': '定期試験',
        'header': '{school_name} 数学テスト',
        'footer': '氏名:__________ 得点:____/100',
        'title_style': '見出し 2',
        'time_limit': True,
    },
    'homework': {
        'name': '宿題プリント',
        'header': '提出日: {date}',
        'footer': 'クラス:____ 番号:____ 氏名:__________',
        'answer_space': True,
    }
}
FINAL_STYLE_EOF

echo "✓ style_config.pyを最終調整しました"

# 既存のtest_size_adjust.htmlを使ってテスト
echo "✓ テストHTMLは既に作成済みです"

# 簡易テストスクリプト
cat > quick_test.py << 'QUICK_TEST_EOF'
"""簡易テスト"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

# 初期化
parser = HTMLParser()
math_converter = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, math_converter)

# テストファイル
test_file = 'data/input/test_size_adjust.html'
output_file = 'data/output/test_final_size.docx'

print(f"設定: インライン数式={STYLE_CONFIG['inline_math_height']}pt, フォント={STYLE_CONFIG['math_font_size']}pt")
print(f"変換中: {test_file} → {output_file}")

# HTMLを読み込み
with open(test_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 解析・変換
problems = parser.parse(html_content)
doc = generator.create_document(problems)
doc.save(output_file)

print(f"✓ 完了: {output_file}")
print("\n確認してください:")
print(f"  open {output_file}")
QUICK_TEST_EOF

echo "✓ 簡易テストスクリプトを作成しました"

echo ""
echo "============================================"
echo "数式サイズの最終調整完了"
echo "============================================"
echo ""
echo "新しい設定:"
echo "  - インライン数式の高さ: 11pt（本文と同じ）"
echo "  - 数式フォントサイズ: 10pt（より小さく）"
echo ""
echo "テストを実行:"
echo "  python quick_test.py"
echo ""
echo "確認:"
echo "  open data/output/test_final_size.docx"
echo ""
