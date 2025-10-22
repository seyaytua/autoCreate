#!/bin/bash

echo "数式表示の修正を開始します..."

# math_converter.pyを修正
cat > src/core/math_converter.py << 'MATH_FIX_EOF'
"""数式画像変換モジュール（修正版）"""
import matplotlib
matplotlib.use('Agg')  # GUIバックエンドを使用しない
import matplotlib.pyplot as plt
from matplotlib import mathtext
from PIL import Image
import io
from typing import BinaryIO
import re

class MathConverter:
    def __init__(self, config: dict):
        self.dpi = config['math_dpi']
        self.font_size = config['math_font_size']
        self.color = config['math_color']
        
        # mathtextの設定
        plt.rcParams['mathtext.fontset'] = 'cm'
        plt.rcParams['mathtext.default'] = 'regular'
        plt.rcParams['font.size'] = self.font_size
    
    def latex_to_image(self, latex_str: str) -> BinaryIO:
        """
        LaTeX数式を画像化してバイナリストリームで返す
        
        Args:
            latex_str (str): LaTeX数式文字列（$記号は不要）
        
        Returns:
            BinaryIO: PNG画像のバイナリストリーム
        """
        try:
            # $記号を削除（念のため）
            latex_str = latex_str.strip()
            latex_str = re.sub(r'^\$+|\$+$', '', latex_str)
            
            # 図を作成（サイズを動的に調整）
            fig, ax = plt.subplots(figsize=(0.1, 0.1))
            fig.patch.set_alpha(0)  # 透過背景
            ax.axis('off')
            
            # 数式をレンダリング
            text = ax.text(
                0.5, 0.5,
                f'${latex_str}$',
                fontsize=self.font_size,
                color=self.color,
                ha='center',
                va='center',
                transform=ax.transAxes
            )
            
            # 描画して境界ボックスを取得
            fig.canvas.draw()
            bbox = text.get_window_extent(fig.canvas.get_renderer())
            
            # 図のサイズを調整
            width = bbox.width / fig.dpi + 0.2
            height = bbox.height / fig.dpi + 0.2
            fig.set_size_inches(width, height)
            
            # 画像として保存
            buf = io.BytesIO()
            plt.savefig(
                buf,
                format='png',
                dpi=self.dpi,
                bbox_inches='tight',
                transparent=True,
                pad_inches=0.05
            )
            plt.close(fig)
            
            buf.seek(0)
            return buf
            
        except Exception as e:
            print(f"数式変換エラー: {latex_str}")
            print(f"エラー内容: {str(e)}")
            
            # エラー時は代替画像を生成
            return self._create_error_image(latex_str)
    
    def _create_error_image(self, latex_str: str) -> BinaryIO:
        """エラー時の代替画像を生成"""
        try:
            fig, ax = plt.subplots(figsize=(3, 0.5))
            fig.patch.set_facecolor('white')
            ax.axis('off')
            
            # エラーメッセージを表示
            error_text = f'[数式エラー: {latex_str[:30]}...]'
            ax.text(
                0.5, 0.5,
                error_text,
                fontsize=10,
                color='red',
                ha='center',
                va='center',
                transform=ax.transAxes
            )
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
            plt.close(fig)
            
            buf.seek(0)
            return buf
        except:
            # 最終的なフォールバック
            fig = plt.figure(figsize=(2, 0.3))
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=self.dpi)
            plt.close(fig)
            buf.seek(0)
            return buf
    
    def test_conversion(self, latex_str: str) -> bool:
        """数式変換が正しく動作するかテスト"""
        try:
            buf = self.latex_to_image(latex_str)
            img = Image.open(buf)
            return img.size[0] > 0 and img.size[1] > 0
        except:
            return False
MATH_FIX_EOF

echo "✓ math_converter.pyを修正しました"

# html_parser.pyも修正（$記号の処理を改善）
cat > src/core/html_parser.py << 'PARSER_FIX_EOF'
"""HTML解析モジュール（修正版）"""
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any

class HTMLParser:
    def __init__(self):
        # LaTeX数式パターン
        # $$...$$（ディスプレイ数式）
        self.display_math_pattern = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)
        # $...$ または \(...\)（インライン数式）
        self.inline_math_pattern = re.compile(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)|\\\((.+?)\\\)', re.DOTALL)
    
    def parse(self, html_content: str) -> List[Dict[str, Any]]:
        """HTMLを解析して問題データを抽出"""
        soup = BeautifulSoup(html_content, 'html.parser')
        problems = []
        
        # 問題ブロックを探す
        problem_divs = soup.find_all('div', class_='problem')
        
        if not problem_divs:
            # class指定がない場合、h2タグで区切る
            problem_divs = self._split_by_headers(soup)
        
        for problem_div in problem_divs:
            problem_data = {
                'title': self._extract_title(problem_div),
                'text': self._extract_text(problem_div),
                'equations': self._extract_equations(problem_div),
                'choices': self._extract_choices(problem_div),
                'raw_html': str(problem_div)
            }
            problems.append(problem_data)
        
        return problems
    
    def _split_by_headers(self, soup):
        """h2タグで問題を分割"""
        problems = []
        current_problem = None
        
        for element in soup.find_all(['h2', 'p', 'div', 'ol', 'ul']):
            if element.name == 'h2':
                if current_problem:
                    problems.append(current_problem)
                current_problem = BeautifulSoup('<div class="problem"></div>', 'html.parser').div
                current_problem.append(element)
            elif current_problem is not None:
                current_problem.append(element)
        
        if current_problem:
            problems.append(current_problem)
        
        return problems
    
    def _extract_title(self, problem_div) -> str:
        """タイトルを抽出"""
        title_elem = problem_div.find(['h1', 'h2', 'h3'], class_='problem-title')
        if not title_elem:
            title_elem = problem_div.find(['h1', 'h2', 'h3'])
        
        return title_elem.get_text(strip=True) if title_elem else ""
    
    def _extract_text(self, problem_div) -> List[Dict[str, Any]]:
        """問題文を抽出（テキストと数式を分離）"""
        text_elements = []
        
        # 問題文パラグラフを探す
        text_paras = problem_div.find_all('p', class_='problem-text')
        if not text_paras:
            text_paras = problem_div.find_all('p')
        
        for para in text_paras:
            # パラグラフ内のテキストと数式を分離
            content = para.get_text()
            parts = self._split_text_and_math(content)
            
            for part in parts:
                text_elements.append(part)
        
        return text_elements
    
    def _split_text_and_math(self, text: str) -> List[Dict[str, Any]]:
        """テキスト内の数式を分離"""
        parts = []
        last_end = 0
        
        # まずディスプレイ数式を処理（$$...$$）
        display_matches = list(self.display_math_pattern.finditer(text))
        
        # 次にインライン数式を処理（$...$ または \(...\)）
        inline_matches = list(self.inline_math_pattern.finditer(text))
        
        # すべてのマッチを位置順にソート
        all_matches = sorted(
            display_matches + inline_matches,
            key=lambda m: m.start()
        )
        
        for match in all_matches:
            # 数式の前のテキスト
            if match.start() > last_end:
                plain_text = text[last_end:match.start()].strip()
                if plain_text:
                    parts.append({'type': 'text', 'content': plain_text})
            
            # 数式部分
            # ディスプレイ数式の場合
            if match in display_matches:
                latex_str = match.group(1).strip()
            # インライン数式の場合
            else:
                latex_str = (match.group(1) or match.group(2)).strip()
            
            if latex_str:
                parts.append({'type': 'math', 'content': latex_str})
            
            last_end = match.end()
        
        # 残りのテキスト
        if last_end < len(text):
            plain_text = text[last_end:].strip()
            if plain_text:
                parts.append({'type': 'text', 'content': plain_text})
        
        # 数式が見つからなかった場合は全体をテキストとして返す
        if not parts and text.strip():
            parts.append({'type': 'text', 'content': text.strip()})
        
        return parts
    
    def _extract_equations(self, problem_div) -> List[str]:
        """独立した数式ブロックを抽出"""
        equations = []
        
        # mathクラスのdivを探す
        math_divs = problem_div.find_all('div', class_='math')
        
        for math_div in math_divs:
            content = math_div.get_text(strip=True)
            # $$...$$を除去
            content = re.sub(r'^\$\$|\$\$$', '', content).strip()
            if content:
                equations.append(content)
        
        return equations
    
    def _extract_choices(self, problem_div) -> List[str]:
        """選択肢を抽出"""
        choices = []
        
        # olまたはulタグを探す
        choice_list = problem_div.find(['ol', 'ul'], class_='choices')
        if not choice_list:
            choice_list = problem_div.find(['ol', 'ul'])
        
        if choice_list:
            for li in choice_list.find_all('li'):
                choice_text = li.get_text(strip=True)
                choices.append(choice_text)
        
        return choices
PARSER_FIX_EOF

echo "✓ html_parser.pyを修正しました"

# テスト用HTMLファイルを作成
cat > data/input/test_math_display.html << 'TEST_HTML_EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>数式表示テスト</title>
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">大問1：内分点の問題</h2>
        <p class="problem-text">
            実際に数直線や図を描かせることで、内分点はAP:PB=$m$:$n$のとき、
            Aから$\frac{m}{m+n}$の位置にあることを発見させます。
        </p>
        <div class="math">$$\text{内分点の座標} = \frac{mb + na}{m+n}$$</div>
        <p class="problem-text">
            ただし、$m > 0$、$n > 0$とする。
        </p>
        <ol class="choices">
            <li>$\frac{1}{2}$の位置</li>
            <li>$\frac{m}{m+n}$の位置</li>
            <li>$\frac{n}{m+n}$の位置</li>
            <li>$\frac{m+n}{2}$の位置</li>
        </ol>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">大問2：複雑な数式</h2>
        <p class="problem-text">
            次の積分を計算しなさい。ただし、$x > 0$とする。
        </p>
        <div class="math">$$\int_{0}^{1} \frac{x^2 + 1}{x^2 - 1} dx$$</div>
        <p class="problem-text">
            また、$\lim_{x \to 0} \frac{\sin x}{x} = 1$を用いてもよい。
        </p>
        <ol class="choices">
            <li>$\frac{\pi}{4}$</li>
            <li>$\frac{\pi}{2}$</li>
            <li>$\pi$</li>
            <li>発散する</li>
        </ol>
    </div>
</body>
</html>
TEST_HTML_EOF

echo "✓ テスト用HTMLファイルを作成しました"

# 変換テストスクリプトを作成
cat > test_math_conversion.py << 'TEST_SCRIPT_EOF'
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
TEST_SCRIPT_EOF

echo "✓ テストスクリプトを作成しました"

echo ""
echo "============================================"
echo "数式表示の修正が完了しました！"
echo "============================================"
echo ""
echo "テストを実行:"
echo "  python test_math_conversion.py"
echo ""
echo "生成されたWordファイルを確認:"
echo "  open data/output/test_math_display.docx"
echo ""
