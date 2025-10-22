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
