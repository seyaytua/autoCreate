"""数式変換のテスト"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

def test_conversion():
    """変換テスト"""
    print("="*50)
    print("数式変換テスト")
    print("="*50)
    
    # 初期化
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    # テストHTMLを読み込み
    test_file = 'data/input/test_math_display.html'
    
    print(f"\n入力ファイル: {test_file}")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析
    print("\nHTMLを解析中...")
    problems = parser.parse(html_content)
    print(f"  {len(problems)}個の問題を検出")
    
    # 各問題の詳細を表示
    for i, problem in enumerate(problems, 1):
        print(f"\n--- 問題 {i} ---")
        print(f"タイトル: {problem['title']}")
        print(f"テキスト要素数: {len(problem['text'])}")
        
        print("\nテキスト詳細:")
        for j, element in enumerate(problem['text']):
            if element['type'] == 'text':
                print(f"  [{j}] テキスト: {element['content'][:50]}...")
            else:
                print(f"  [{j}] 数式: {element['content']}")
        
        print(f"\nディスプレイ数式: {len(problem['equations'])}個")
        for eq in problem['equations']:
            print(f"  - {eq}")
        
        print(f"\n選択肢: {len(problem['choices'])}個")
        for choice in problem['choices']:
            print(f"  - {choice}")
    
    # Word文書を生成
    print("\n" + "="*50)
    print("Word文書を生成中...")
    
    output_file = 'data/output/test_math_display.docx'
    doc = generator.create_document(problems)
    doc.save(output_file)
    
    print(f"✓ 完了: {output_file}")
    print("="*50)
    
    return True

if __name__ == '__main__':
    try:
        success = test_conversion()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nエラー: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
