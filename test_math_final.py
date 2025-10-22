"""数式変換の最終テスト"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

def test_individual_formulas():
    """個別の数式をテスト"""
    print("="*60)
    print("個別数式のテスト")
    print("="*60)
    
    converter = MathConverter(STYLE_CONFIG)
    
    test_cases = [
        # 基本的な数式
        ('x^2 + y^2 = r^2', '基本的な2次式'),
        
        # 分数
        (r'\frac{a}{b}', '単純な分数'),
        (r'\frac{x^2 + 1}{x - 1}', '複雑な分数'),
        
        # テキストを含む分数
        (r'\frac{BP}{PC}', '文字の分数'),
        (r'\frac{S_{OAB}}{S_{OCA}}', '添字付き分数'),
        
        # 複雑な式
        (r'\frac{BP}{PC} \cdot \frac{CQ}{QA} \cdot \frac{AR}{RB} = 1', 'チェバの定理'),
        (r'\frac{m}{m+n}', '内分点の公式'),
        (r'\frac{mb + na}{m+n}', '座標の内分点'),
    ]
    
    print("\n各数式の変換テスト:")
    for latex, description in test_cases:
        print(f"\n  テスト: {description}")
        print(f"  LaTeX: {latex}")
        
        try:
            result = converter.test_conversion(latex)
            status = "✓ OK" if result else "✗ NG"
            print(f"  結果: {status}")
        except Exception as e:
            print(f"  結果: ✗ エラー - {str(e)}")
    
    print("\n" + "="*60)

def test_full_conversion():
    """完全な変換テスト"""
    print("\n" + "="*60)
    print("完全変換テスト")
    print("="*60)
    
    # 初期化
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    # テストファイル
    test_file = 'data/input/test_cheva.html'
    output_file = 'data/output/test_cheva.docx'
    
    print(f"\n入力: {test_file}")
    print(f"出力: {output_file}")
    
    # HTMLを読み込み
    with open(test_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析
    print("\nHTMLを解析中...")
    problems = parser.parse(html_content)
    print(f"  {len(problems)}個の問題を検出")
    
    # 詳細表示
    for i, problem in enumerate(problems, 1):
        print(f"\n--- 問題 {i}: {problem['title']} ---")
        
        print("テキスト要素:")
        for j, element in enumerate(problem['text']):
            if element['type'] == 'text':
                text_preview = element['content'][:40]
                print(f"  [{j}] テキスト: {text_preview}...")
            else:
                print(f"  [{j}] 数式: {element['content']}")
        
        if problem['equations']:
            print("ディスプレイ数式:")
            for eq in problem['equations']:
                print(f"  - {eq}")
    
    # Word文書を生成
    print("\n" + "-"*60)
    print("Word文書を生成中...")
    
    doc = generator.create_document(problems)
    doc.save(output_file)
    
    print(f"✓ 完了: {output_file}")
    print("="*60)
    
    return True

def main():
    """メイン実行"""
    try:
        # 個別テスト
        test_individual_formulas()
        
        # 完全変換テスト
        test_full_conversion()
        
        print("\n" + "="*60)
        print("すべてのテストが完了しました")
        print("生成されたファイルを確認してください:")
        print("  open data/output/test_cheva.docx")
        print("="*60)
        
        return 0
    except Exception as e:
        print(f"\nエラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
