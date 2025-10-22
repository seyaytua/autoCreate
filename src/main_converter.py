"""メイン変換スクリプト"""
import sys
from pathlib import Path
from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

def convert_html_to_word(html_file: str, output_file: str = None):
    """HTMLファイルをWord文書に変換"""
    
    # 出力ファイル名の決定
    if output_file is None:
        input_path = Path(html_file)
        output_file = input_path.with_suffix('.docx')
    
    print(f"変換開始: {html_file}")
    
    try:
        # HTMLファイルを読み込み
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # パーサーとコンバーターを初期化
        parser = HTMLParser()
        math_converter = MathConverter(STYLE_CONFIG)
        word_generator = WordGenerator(STYLE_CONFIG, math_converter)
        
        # HTMLを解析
        print("HTMLを解析中...")
        problems = parser.parse(html_content)
        print(f"  {len(problems)}個の問題を検出")
        
        # Word文書を生成
        print("Word文書を生成中...")
        doc = word_generator.create_document(problems)
        
        # 保存
        doc.save(output_file)
        print(f"完了: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python main_converter.py <HTMLファイル> [出力ファイル]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_html_to_word(html_file, output_file)
    sys.exit(0 if success else 1)
