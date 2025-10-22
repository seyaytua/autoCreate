#!/bin/bash

echo "数式サイズのバランス調整を開始します..."

# style_config.pyをバランス調整
cat > src/core/style_config.py << 'BALANCED_STYLE_EOF'
"""統一スタイル設定（バランス調整版）"""

STYLE_CONFIG = {
    # 数式画像設定
    'math_dpi': 300,
    'math_font_size': 11,  # 少し大きく（11pt）
    'math_color': 'black',
    'math_background': 'transparent',
    
    # インライン数式の高さ設定（ポイント単位）
    'inline_math_height': 12,  # 本文より少し大きく（12pt）
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
BALANCED_STYLE_EOF

echo "✓ style_config.pyをバランス調整しました"

# テストスクリプト
cat > test_balanced.py << 'TEST_BALANCED_EOF'
"""バランス調整テスト"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

print("="*70)
print("数式サイズ バランス調整テスト")
print("="*70)

print(f"\n設定:")
print(f"  本文フォントサイズ: {STYLE_CONFIG['body_size']}pt")
print(f"  数式フォントサイズ: {STYLE_CONFIG['math_font_size']}pt")
print(f"  インライン数式の高さ: {STYLE_CONFIG['inline_math_height']}pt")

# 初期化
parser = HTMLParser()
math_converter = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, math_converter)

# テストファイル
test_file = 'data/input/test_size_adjust.html'
output_file = 'data/output/test_balanced.docx'

print(f"\n変換: {test_file} → {output_file}")

# HTMLを読み込み
with open(test_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 解析・変換
problems = parser.parse(html_content)
doc = generator.create_document(problems)
doc.save(output_file)

print(f"✓ 完了: {output_file}")
print("="*70)

print("\n確認してください:")
print(f"  open {output_file}")

print("\nサイズ調整のガイドライン:")
print("  - 現在: 本文11pt、数式11pt、高さ12pt")
print("  - より小さく: inline_math_height を 11 に")
print("  - より大きく: inline_math_height を 13 に")
print("  - 設定ファイル: src/core/style_config.py")
TEST_BALANCED_EOF

echo "✓ テストスクリプトを作成しました"

echo ""
echo "============================================"
echo "バランス調整完了"
echo "============================================"
echo ""
echo "調整後の設定:"
echo "  - 本文フォントサイズ: 11pt"
echo "  - 数式フォントサイズ: 11pt（本文と同じ）"
echo "  - インライン数式の高さ: 12pt（本文より少し大きく）"
echo ""
echo "テストを実行:"
echo "  python test_balanced.py"
echo ""
echo "確認:"
echo "  open data/output/test_balanced.docx"
echo ""
echo "微調整が必要な場合:"
echo "  src/core/style_config.py を編集"
echo "  inline_math_height: 11〜13 の範囲で調整"
echo ""
