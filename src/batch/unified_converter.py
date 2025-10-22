"""統一感を持った複数問題の変換"""
from pathlib import Path
from typing import List, Dict, Any
import sys

sys.path.append(str(Path(__file__).parent.parent))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator
from docx import Document
from docx.shared import Pt, Cm

class UnifiedMathConverter:
    """統一されたスタイルで複数問題を変換"""
    
    def __init__(self, style_config=None):
        self.config = style_config or STYLE_CONFIG
        self.parser = HTMLParser()
        self.math_converter = MathConverter(self.config)
        self.generator = WordGenerator(self.config, self.math_converter)
        self.problem_counter = 0
    
    def convert_multiple_problems(self, html_list: List[str], 
                                  output_file: str) -> bool:
        """
        複数のHTMLを統一スタイルで1つの文書に変換
        
        Args:
            html_list (List[str]): HTMLファイルパスのリスト
            output_file (str): 出力ファイルパス
        
        Returns:
            bool: 成功時True
        """
        all_problems = []
        
        # すべてのHTMLを解析
        for html_file in html_list:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                problems = self.parser.parse(html_content)
                all_problems.extend(problems)
                
                print(f"✓ 読み込み: {Path(html_file).name} ({len(problems)}問)")
                
            except Exception as e:
                print(f"✗ エラー: {Path(html_file).name} - {str(e)}")
                continue
        
        if not all_problems:
            print("エラー: 問題が見つかりませんでした")
            return False
        
        print(f"\n合計 {len(all_problems)}問を変換します...")
        
        # 問題番号を統一的に振り直す
        for i, problem in enumerate(all_problems, 1):
            if not problem['title'] or problem['title'].startswith('大問'):
                problem['title'] = f'大問{i}'
        
        # Word文書を生成
        try:
            doc = self.generator.create_document(all_problems)
            doc.save(output_file)
            print(f"\n✓ 完了: {output_file}")
            return True
            
        except Exception as e:
            print(f"\n✗ エラー: {str(e)}")
            return False
    
    def convert_folder_unified(self, input_folder: str, 
                              output_file: str) -> bool:
        """
        フォルダ内のすべてのHTMLを1つの文書に統合
        
        Args:
            input_folder (str): 入力フォルダ
            output_file (str): 出力ファイル
        
        Returns:
            bool: 成功時True
        """
        input_path = Path(input_folder)
        html_files = sorted(input_path.glob('*.html'))
        
        if not html_files:
            print(f"エラー: {input_folder} にHTMLファイルが見つかりません")
            return False
        
        print(f"{len(html_files)}個のファイルを統合します:")
        for f in html_files:
            print(f"  - {f.name}")
        print()
        
        return self.convert_multiple_problems(
            [str(f) for f in html_files],
            output_file
        )

def main():
    """コマンドライン実行"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='複数のHTMLファイルを統一されたスタイルで1つの文書に変換'
    )
    parser.add_argument('input', nargs='+', help='入力HTMLファイルまたはフォルダ')
    parser.add_argument('-o', '--output', required=True, help='出力Wordファイル')
    
    args = parser.parse_args()
    
    converter = UnifiedMathConverter()
    
    # 入力が1つでフォルダの場合
    if len(args.input) == 1 and Path(args.input[0]).is_dir():
        success = converter.convert_folder_unified(args.input[0], args.output)
    else:
        # 複数ファイルの場合
        success = converter.convert_multiple_problems(args.input, args.output)
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
