"""サイズ調整のテスト"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

def main():
    print("="*70)
    print("数式サイズ調整テスト")
    print("="*70)
    
    # 設定を表示
    print("\n現在の設定:")
    print(f"  数式フォントサイズ: {STYLE_CONFIG['math_font_size']}pt")
    print(f"  インライン数式の高さ: {STYLE_CONFIG['inline_math_height']}pt")
    print(f"  本文フォントサイズ: {STYLE_CONFIG['body_size']}pt")
    print(f"  ディスプレイ数式の幅: {STYLE_CONFIG['display_math_width']}インチ")
    
    # 初期化
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    # テストファイル
    test_file = 'data/input/test_size_adjust.html'
    output_file = 'data/output/test_size_adjust.docx'
    
    print(f"\n入力: {test_file}")
    print(f"出力: {output_file}")
    
    # HTMLを読み込み
    with open(test_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析
    print("\nHTMLを解析中...")
    problems = parser.parse(html_content)
    print(f"✓ {len(problems)}個の問題を検出")
    
    # Word文書を生成
    print("\nWord文書を生成中...")
    doc = generator.create_document(problems)
    doc.save(output_file)
    
    print(f"✓ 完了: {output_file}")
    print("="*70)
    
    print("\n生成されたファイルを確認してください:")
    print(f"  open {output_file}")
    print("\nサイズが適切でない場合は、src/core/style_config.py で以下を調整:")
    print("  - inline_math_height: インライン数式の高さ（現在: 14pt）")
    print("  - math_font_size: 数式のフォントサイズ（現在: 12pt）")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
