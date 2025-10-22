"""HTML構造の検証モジュール"""
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import re

class HTMLValidator:
    """HTML構造を検証するクラス"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.latex_pattern = re.compile(r'\$\$(.*?)\$\$|\\\((.*?)\\\)')
    
    def validate(self, html_content: str) -> Tuple[bool, List[str], List[str]]:
        """
        HTMLを検証
        
        Returns:
            Tuple[bool, List[str], List[str]]: (検証結果, エラーリスト, 警告リスト)
        """
        self.errors = []
        self.warnings = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            self.errors.append(f"HTML解析エラー: {str(e)}")
            return False, self.errors, self.warnings
        
        # 問題ブロックの存在チェック
        problems = soup.find_all('div', class_='problem')
        if not problems:
            self.warnings.append("class='problem'のdivが見つかりません")
            # h2タグで分割可能かチェック
            h2_tags = soup.find_all('h2')
            if h2_tags:
                self.warnings.append(f"h2タグで{len(h2_tags)}個の問題に分割されます")
            else:
                self.errors.append("問題を識別できる構造がありません")
                return False, self.errors, self.warnings
        
        # 各問題の構造チェック
        for i, problem in enumerate(problems, 1):
            self._validate_problem_structure(problem, i)
        
        # 数式記法のチェック
        self._validate_math_notation(html_content)
        
        # 結果の判定
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_problem_structure(self, problem_div, problem_num: int):
        """個別の問題構造を検証"""
        
        # タイトルチェック
        title = problem_div.find(['h1', 'h2', 'h3'])
        if not title:
            self.errors.append(f"問題{problem_num}: タイトル(h1/h2/h3)が見つかりません")
        elif not title.get('class'):
            self.warnings.append(f"問題{problem_num}: タイトルにclass属性がありません")
        
        # 問題文チェック
        text_paras = problem_div.find_all('p')
        if not text_paras:
            self.warnings.append(f"問題{problem_num}: 問題文(p)が見つかりません")
        
        # 数式ブロックチェック
        math_divs = problem_div.find_all('div', class_='math')
        if not math_divs:
            self.warnings.append(f"問題{problem_num}: 数式ブロックが見つかりません")
        
        # 選択肢チェック
        choices = problem_div.find(['ol', 'ul'])
        if choices:
            if not choices.get('class'):
                self.warnings.append(f"問題{problem_num}: 選択肢にclass属性がありません")
            
            li_items = choices.find_all('li')
            if len(li_items) < 2:
                self.warnings.append(f"問題{problem_num}: 選択肢が2個未満です")
        else:
            self.warnings.append(f"問題{problem_num}: 選択肢が見つかりません（記述式の場合は問題ありません）")
    
    def _validate_math_notation(self, html_content: str):
        """数式記法を検証"""
        
        # $$...$$のチェック
        display_math = re.findall(r'\$\$(.*?)\$\$', html_content, re.DOTALL)
        for i, math in enumerate(display_math, 1):
            if not math.strip():
                self.errors.append(f"ディスプレイ数式{i}: 内容が空です")
            
            # 基本的なLaTeX構文チェック
            if '\\' not in math and not math.replace(' ', '').replace('+', '').replace('-', '').replace('=', '').replace('x', '').replace('y', '').isdigit():
                self.warnings.append(f"ディスプレイ数式{i}: LaTeX記法が使われていない可能性があります")
        
        # \(...\)のチェック
        inline_math = re.findall(r'\\\((.*?)\\\)', html_content)
        for i, math in enumerate(inline_math, 1):
            if not math.strip():
                self.errors.append(f"インライン数式{i}: 内容が空です")
    
    def get_validation_report(self) -> str:
        """検証レポートを生成"""
        report = []
        report.append("="*50)
        report.append("HTML検証レポート")
        report.append("="*50)
        
        if self.errors:
            report.append("\n【エラー】")
            for error in self.errors:
                report.append(f"  ✗ {error}")
        
        if self.warnings:
            report.append("\n【警告】")
            for warning in self.warnings:
                report.append(f"  ⚠ {warning}")
        
        if not self.errors and not self.warnings:
            report.append("\n✓ 問題は検出されませんでした")
        
        report.append("="*50)
        return '\n'.join(report)

def validate_html_file(file_path: str) -> bool:
    """
    HTMLファイルを検証
    
    Args:
        file_path (str): HTMLファイルのパス
    
    Returns:
        bool: 検証結果
    """
    validator = HTMLValidator()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return False
    
    is_valid, errors, warnings = validator.validate(html_content)
    
    print(validator.get_validation_report())
    
    return is_valid

# 使用例
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python html_validator.py <HTMLファイル>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    is_valid = validate_html_file(file_path)
    
    sys.exit(0 if is_valid else 1)
