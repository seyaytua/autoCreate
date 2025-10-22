#!/bin/bash

echo "Phase 2のセットアップを開始します..."

# ディレクトリ作成
mkdir -p src/prompts
mkdir -p src/validators
mkdir -p src/batch

echo "✓ ディレクトリを作成しました"

# プロンプトテンプレートファイルを作成
cat > src/prompts/problem_templates.py << 'TEMPLATE_EOF'
"""問題生成用プロンプトテンプレート"""

# 基本的なプロンプトテンプレート
BASE_PROMPT = """
あなたは数学問題作成AIです。
以下の厳密なフォーマットで問題を生成してください。

【HTML構造の規則】
必ず以下の構造を守ってください：

<div class="problem">
  <h2 class="problem-title">大問{number}</h2>
  <p class="problem-text">問題文をここに記述</p>
  <div class="math">$$LaTeX数式$$</div>
  <ol class="choices">
    <li>選択肢1</li>
    <li>選択肢2</li>
    <li>選択肢3</li>
    <li>選択肢4</li>
  </ol>
</div>

【数式記法の規則】
- インライン数式: \\(x^2\\)
- 独立数式: $$\\frac{{a}}{{b}}$$
- 必ずLaTeX記法を使用
- バックスラッシュは二重にエスケープ

【クラス名の規則】
- 問題ブロック: class="problem"
- タイトル: class="problem-title"
- 問題文: class="problem-text"
- 数式ブロック: class="math"
- 選択肢: class="choices"

【禁止事項】
- HTMLタグはdiv, p, h2, ol, liのみ使用
- style属性の使用禁止
- 数式以外のフォーマット指定禁止
"""

# 難易度別テンプレート
DIFFICULTY_TEMPLATES = {
    'easy': {
        'name': '初級',
        'description': '基本的な計算問題',
        'prompt_addition': """
【初級問題の特徴】
- 四則演算中心
- 1次方程式レベル
- 計算ステップは2〜3段階
- 選択肢は明確に区別可能
"""
    },
    'medium': {
        'name': '中級',
        'description': '標準的な応用問題',
        'prompt_addition': """
【中級問題の特徴】
- 2次方程式、関数
- 計算ステップは3〜5段階
- 概念理解が必要
- 選択肢に類似した値を含む
"""
    },
    'hard': {
        'name': '上級',
        'description': '発展的な問題',
        'prompt_addition': """
【上級問題の特徴】
- 積分、微分、複素数
- 複数の概念を組み合わせ
- 計算ステップは5段階以上
- 論理的思考が必要
"""
    }
}

# 分野別テンプレート
CATEGORY_TEMPLATES = {
    'algebra': {
        'name': '代数',
        'topics': ['方程式', '不等式', '因数分解', '式の計算'],
        'prompt_addition': """
【代数分野の要件】
- 文字式の操作が中心
- 等式・不等式の性質を活用
- 解の検証を含める
"""
    },
    'geometry': {
        'name': '幾何',
        'topics': ['図形の性質', '面積', '体積', '三角比'],
        'prompt_addition': """
【幾何分野の要件】
- 図形の性質を活用
- 定理の適用を明示
- 単位に注意
"""
    },
    'calculus': {
        'name': '微積分',
        'topics': ['微分', '積分', '極限', '関数'],
        'prompt_addition': """
【微積分分野の要件】
- 微分・積分の計算
- 関数の性質を考察
- グラフとの関連を意識
"""
    },
    'statistics': {
        'name': '統計',
        'topics': ['確率', '統計', 'データ分析'],
        'prompt_addition': """
【統計分野の要件】
- データの解釈
- 確率の計算
- 統計量の理解
"""
    }
}

def generate_prompt(difficulty='medium', category='algebra', count=1, **kwargs):
    """
    問題生成用のプロンプトを生成
    
    Parameters:
        difficulty (str): 難易度 ('easy', 'medium', 'hard')
        category (str): 分野 ('algebra', 'geometry', 'calculus', 'statistics')
        count (int): 生成する問題数
        **kwargs: その他のカスタムパラメータ
    
    Returns:
        str: 生成されたプロンプト
    """
    prompt_parts = [BASE_PROMPT]
    
    # 難易度の追加
    if difficulty in DIFFICULTY_TEMPLATES:
        template = DIFFICULTY_TEMPLATES[difficulty]
        prompt_parts.append(f"\n【難易度】: {template['name']}")
        prompt_parts.append(template['prompt_addition'])
    
    # 分野の追加
    if category in CATEGORY_TEMPLATES:
        template = CATEGORY_TEMPLATES[category]
        prompt_parts.append(f"\n【分野】: {template['name']}")
        prompt_parts.append(f"【トピック】: {', '.join(template['topics'])}")
        prompt_parts.append(template['prompt_addition'])
    
    # 問題数の指定
    prompt_parts.append(f"\n【生成する問題数】: {count}問")
    
    # カスタムパラメータの追加
    if kwargs:
        prompt_parts.append("\n【追加要件】:")
        for key, value in kwargs.items():
            prompt_parts.append(f"- {key}: {value}")
    
    # 最終的な指示
    prompt_parts.append("""
\n【出力形式】
上記のHTML構造に厳密に従って、問題を生成してください。
各問題は必ず<div class="problem">で囲んでください。
複数問題を生成する場合は、連続して出力してください。
""")
    
    return '\n'.join(prompt_parts)

def get_example_html():
    """正しいHTMLの例を返す"""
    return """
<div class="problem">
  <h2 class="problem-title">大問1</h2>
  <p class="problem-text">次の方程式を解きなさい。</p>
  <div class="math">$$x^2 + 5x + 6 = 0$$</div>
  <ol class="choices">
    <li>x = -2, -3</li>
    <li>x = 2, 3</li>
    <li>x = -1, -6</li>
    <li>x = 1, 6</li>
  </ol>
</div>
"""

# 使用例を追加
if __name__ == '__main__':
    # 基本的な使用
    prompt = generate_prompt(
        difficulty='medium',
        category='algebra',
        count=2
    )
    print(prompt)
    
    print("\n" + "="*50)
    print("正しいHTMLの例:")
    print("="*50)
    print(get_example_html())
TEMPLATE_EOF

echo "✓ プロンプトテンプレートを作成しました"

# HTMLバリデーターを作成
cat > src/validators/html_validator.py << 'VALIDATOR_EOF'
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
VALIDATOR_EOF

echo "✓ HTMLバリデーターを作成しました"

# バッチ変換モジュールを作成
cat > src/batch/batch_converter.py << 'BATCH_EOF'
"""バッチ変換モジュール"""
import os
from pathlib import Path
from typing import List, Optional
import logging
from datetime import datetime

# 親ディレクトリのモジュールをインポート
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

class BatchConverter:
    """複数のHTMLファイルを一括変換するクラス"""
    
    def __init__(self, style_config=None):
        """
        初期化
        
        Args:
            style_config (dict, optional): スタイル設定
        """
        self.config = style_config or STYLE_CONFIG
        self.parser = HTMLParser()
        self.math_converter = MathConverter(self.config)
        self.generator = WordGenerator(self.config, self.math_converter)
        
        # ログ設定
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """ロガーを設定"""
        logger = logging.getLogger('BatchConverter')
        logger.setLevel(logging.INFO)
        
        # ファイルハンドラ
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        fh = logging.FileHandler(log_dir / f'batch_{timestamp}.log')
        fh.setLevel(logging.DEBUG)
        
        # コンソールハンドラ
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def convert_folder(self, input_folder: str, output_folder: str, 
                      pattern: str = '*.html') -> dict:
        """
        フォルダ内のHTMLファイルを一括変換
        
        Args:
            input_folder (str): 入力フォルダ
            output_folder (str): 出力フォルダ
            pattern (str): ファイルパターン
        
        Returns:
            dict: 変換結果の統計情報
        """
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        
        # 出力フォルダを作成
        output_path.mkdir(parents=True, exist_ok=True)
        
        # HTMLファイルを取得
        html_files = list(input_path.glob(pattern))
        total = len(html_files)
        
        if total == 0:
            self.logger.warning(f"HTMLファイルが見つかりません: {input_folder}")
            return {'total': 0, 'success': 0, 'failed': 0}
        
        self.logger.info(f"変換開始: {total}個のファイル")
        
        # 統計情報
        stats = {
            'total': total,
            'success': 0,
            'failed': 0,
            'files': []
        }
        
        # 各ファイルを変換
        for i, html_file in enumerate(html_files, 1):
            self.logger.info(f"[{i}/{total}] 処理中: {html_file.name}")
            
            try:
                # 変換実行
                output_file = output_path / f"{html_file.stem}.docx"
                success = self._convert_single_file(html_file, output_file)
                
                if success:
                    stats['success'] += 1
                    stats['files'].append({
                        'input': str(html_file),
                        'output': str(output_file),
                        'status': 'success'
                    })
                    self.logger.info(f"  ✓ 完了: {output_file.name}")
                else:
                    stats['failed'] += 1
                    stats['files'].append({
                        'input': str(html_file),
                        'output': None,
                        'status': 'failed'
                    })
                    self.logger.error(f"  ✗ 失敗: {html_file.name}")
                
            except Exception as e:
                stats['failed'] += 1
                self.logger.error(f"  ✗ エラー: {str(e)}")
        
        # 結果サマリー
        self.logger.info(f"\n変換完了: 成功 {stats['success']}/{total}, 失敗 {stats['failed']}/{total}")
        
        return stats
    
    def _convert_single_file(self, input_file: Path, output_file: Path) -> bool:
        """
        単一ファイルを変換
        
        Args:
            input_file (Path): 入力ファイル
            output_file (Path): 出力ファイル
        
        Returns:
            bool: 成功時True
        """
        try:
            # HTMLを読み込み
            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 解析
            problems = self.parser.parse(html_content)
            
            if not problems:
                self.logger.warning(f"  問題が検出されませんでした: {input_file.name}")
                return False
            
            self.logger.debug(f"  {len(problems)}個の問題を検出")
            
            # Word文書生成
            doc = self.generator.create_document(problems)
            
            # 保存
            doc.save(str(output_file))
            
            return True
            
        except Exception as e:
            self.logger.error(f"  変換エラー: {str(e)}")
            return False
    
    def convert_multiple_files(self, input_files: List[str], 
                              output_folder: str) -> dict:
        """
        指定されたファイルリストを変換
        
        Args:
            input_files (List[str]): 入力ファイルのリスト
            output_folder (str): 出力フォルダ
        
        Returns:
            dict: 変換結果の統計情報
        """
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        total = len(input_files)
        self.logger.info(f"変換開始: {total}個のファイル")
        
        stats = {
            'total': total,
            'success': 0,
            'failed': 0,
            'files': []
        }
        
        for i, input_file in enumerate(input_files, 1):
            input_path = Path(input_file)
            self.logger.info(f"[{i}/{total}] 処理中: {input_path.name}")
            
            try:
                output_file = output_path / f"{input_path.stem}.docx"
                success = self._convert_single_file(input_path, output_file)
                
                if success:
                    stats['success'] += 1
                    stats['files'].append({
                        'input': str(input_path),
                        'output': str(output_file),
                        'status': 'success'
                    })
                else:
                    stats['failed'] += 1
                    stats['files'].append({
                        'input': str(input_path),
                        'output': None,
                        'status': 'failed'
                    })
            
            except Exception as e:
                stats['failed'] += 1
                self.logger.error(f"  ✗ エラー: {str(e)}")
        
        self.logger.info(f"\n変換完了: 成功 {stats['success']}/{total}, 失敗 {stats['failed']}/{total}")
        
        return stats

def main():
    """コマンドライン実行"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HTMLファイルをバッチ変換')
    parser.add_argument('input', help='入力フォルダまたはファイル')
    parser.add_argument('output', help='出力フォルダ')
    parser.add_argument('--pattern', default='*.html', help='ファイルパターン')
    
    args = parser.parse_args()
    
    converter = BatchConverter()
    
    input_path = Path(args.input)
    if input_path.is_dir():
        stats = converter.convert_folder(args.input, args.output, args.pattern)
    elif input_path.is_file():
        stats = converter.convert_multiple_files([args.input], args.output)
    else:
        print(f"エラー: {args.input} が見つかりません")
        return 1
    
    return 0 if stats['failed'] == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
BATCH_EOF

echo "✓ バッチ変換モジュールを作成しました"

# 統合変換スクリプトを作成
cat > src/batch/unified_converter.py << 'UNIFIED_EOF'
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
UNIFIED_EOF

echo "✓ 統合変換スクリプトを作成しました"

# テスト用のHTMLファイルを作成
cat > data/input/test_problem1.html << 'TEST1_EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>テスト問題1</title>
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">大問1</h2>
        <p class="problem-text">次の方程式を解きなさい。</p>
        <div class="math">$$2x + 5 = 13$$</div>
        <ol class="choices">
            <li>x = 3</li>
            <li>x = 4</li>
            <li>x = 5</li>
            <li>x = 6</li>
        </ol>
    </div>
</body>
</html>
TEST1_EOF

cat > data/input/test_problem2.html << 'TEST2_EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>テスト問題2</title>
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">大問2</h2>
        <p class="problem-text">次の不等式を解きなさい。</p>
        <div class="math">$$3x - 7 < 11$$</div>
        <ol class="choices">
            <li>\(x < 6\)</li>
            <li>\(x < 7\)</li>
            <li>\(x > 6\)</li>
            <li>\(x > 7\)</li>
        </ol>
    </div>
</body>
</html>
TEST2_EOF

echo "✓ テスト用HTMLファイルを作成しました"

# READMEを作成
cat > docs/phase2_README.md << 'README_EOF'
# Phase 2: 統一感強化とプロンプトテンプレート

## 新機能

### 1. プロンプトテンプレート (`src/prompts/problem_templates.py`)

AI問題生成用の構造化プロンプトテンプレート：

```python
from prompts.problem_templates import generate_prompt

# 基本的な使用
prompt = generate_prompt(
    difficulty='medium',
    category='algebra',
    count=2
)
print(prompt)
難易度: easy, medium, hard
分野: algebra, geometry, calculus, statistics
2. HTMLバリデーター (src/validators/html_validator.py)
生成されたHTMLの構造を検証：

Copypython src/validators/html_validator.py data/input/sample_problem.html
検証内容:

必須要素の存在確認
クラス名の検証
数式記法の確認
構造の整合性チェック
3. バッチ変換 (src/batch/batch_converter.py)
複数ファイルの一括変換：

Copy# フォルダ内のすべてのHTMLを変換
python src/batch/batch_converter.py data/input data/output

# 特定のファイルを変換
python src/batch/batch_converter.py data/input/problem1.html data/output
4. 統合変換 (src/batch/unified_converter.py)
複数のHTMLを1つの文書に統合：

Copy# フォルダ内のすべてを統合
python src/batch/unified_converter.py data/input -o data/output/unified.docx

# 複数ファイルを指定して統合
python src/batch/unified_converter.py \
    data/input/problem1.html \
    data/input/problem2.html \
    -o data/output/combined.docx
使用例
例1: プロンプト生成
Copyfrom prompts.problem_templates import generate_prompt

# 中級の代数問題を2問生成
prompt = generate_prompt(
    difficulty='medium',
    category='algebra',
    count=2,
    topic='2次方程式',
    include_graph=False
)

# このプロンプトをAIに送信
例2: HTML検証
Copy# コマンドラインから
python src/validators/html_validator.py data/input/problem.html

# Pythonコードから
from validators.html_validator import HTMLValidator

validator = HTMLValidator()
is_valid, errors, warnings = validator.validate(html_content)

if not is_valid:
    print("エラー:", errors)
else:
    print("検証OK")
例3: バッチ変換
Copy# すべてのHTMLファイルを変換
python src/batch/batch_converter.py data/input data/output

# ログファイルが logs/ に生成される
例4: 統合変換
Copy# 複数の大問を1つの文書に
python src/batch/unified_converter.py \
    data/input/test_problem1.html \
    data/input/test_problem2.html \
    -o data/output/test_combined.docx
ディレクトリ構造
App_autoCreate/
├── src/
│   ├── prompts/              # 新規: プロンプトテンプレート
│   │   └── problem_templates.py
│   ├── validators/           # 新規: 検証モジュール
│   │   └── html_validator.py
│   ├── batch/                # 新規: バッチ処理
│   │   ├── batch_converter.py
│   │   └── unified_converter.py
│   └── core/                 # 既存: コアモジュール
│       ├── __init__.py
│       ├── style_config.py
│       ├── html_parser.py
│       ├── math_converter.py
│       └── word_generator.py
├── logs/                     # 新規: ログファイル
└── docs/
    └── phase2_README.md
次のステップ
Phase 3: GUI実装
Phase 4: フォルダ監視と自動化
Phase 5: AI統合
README_EOF

echo "✓ Phase 2 READMEを作成しました"

echo ""
echo "============================================"
echo "Phase 2のセットアップが完了しました！"
echo "============================================"
echo ""
echo "作成されたファイル:"
echo "  - src/prompts/problem_templates.py"
echo "  - src/validators/html_validator.py"
echo "  - src/batch/batch_converter.py"
echo "  - src/batch/unified_converter.py"
echo "  - data/input/test_problem1.html"
echo "  - data/input/test_problem2.html"
echo "  - docs/phase2_README.md"
echo ""
echo "動作確認:"
echo "  1. HTMLバリデーション:"
echo "     python src/validators/html_validator.py data/input/test_problem1.html"
echo ""
echo "  2. バッチ変換:"
echo "     python src/batch/batch_converter.py data/input data/output"
echo ""
echo "  3. 統合変換:"
echo "     python src/batch/unified_converter.py data/input -o data/output/unified.docx"
echo ""
