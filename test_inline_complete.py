"""インライン数式の完全テスト"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

def main():
    print("="*70)
    print("インライン数式の完全テスト")
    print("="*70)
    
    # 初期化
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    # テストファイル
    test_file = 'data/input/test_inline_math.html'
    output_file = 'data/output/test_inline_math.docx'
    
    print(f"\n入力: {test_file}")
    print(f"出力: {output_file}")
    
    # HTMLを読み込み
    print("\nHTMLを読み込み中...")
    with open(test_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析
    print("HTMLを解析中...")
    problems = parser.parse(html_content)
    print(f"✓ {len(problems)}個の問題を検出")
    
    # 各問題の詳細を表示
    for i, problem in enumerate(problems, 1):
        print(f"\n{'─'*70}")
        print(f"問題 {i}: {problem['title']}")
        print(f"{'─'*70}")
        
        print("\nテキスト要素:")
        for j, element in enumerate(problem['text']):
            if element['type'] == 'text':
                print(f"  [{j}] テキスト: {element['content'][:50]}...")
            else:
                print(f"  [{j}] インライン数式: {element['content']}")
        
        if problem['equations']:
            print("\nディスプレイ数式:")
            for eq in problem['equations']:
                print(f"  - {eq}")
        
        if problem['choices']:
            print("\n選択肢:")
            for k, choice in enumerate(problem['choices'], 1):
                print(f"  {k}. {choice}")
    
    # Word文書を生成
    print(f"\n{'='*70}")
    print("Word文書を生成中...")
    
    try:
        doc = generator.create_document(problems)
        doc.save(output_file)
        
        print(f"✓ 完了: {output_file}")
        print(f"{'='*70}")
        
        print("\n生成されたファイルを確認してください:")
        print(f"  open {output_file}")
        
        return 0
    
    except Exception as e:
        print(f"\n✗ エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
