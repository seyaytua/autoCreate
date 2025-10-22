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
