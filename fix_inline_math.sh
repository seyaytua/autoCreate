#!/bin/bash

echo "インライン数式の完全修正を開始します..."

# word_generator.pyを修正（インライン数式の処理を改善）
cat > src/core/word_generator.py << 'WORD_GEN_FIX_EOF'
"""Word文書生成モジュール（完全修正版）"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from typing import List, Dict, Any
import re

class WordGenerator:
    def __init__(self, style_config: dict, math_converter):
        self.config = style_config
        self.math_converter = math_converter
        self.problem_counter = 0
    
    def create_document(self, problems: List[Dict[str, Any]]) -> Document:
        """複数の問題からWord文書を生成"""
        doc = Document()
        self._apply_global_style(doc)
        
        for i, problem in enumerate(problems):
            self.problem_counter = i + 1
            self._add_problem(doc, problem)
            
            # 大問間の間隔（最後の問題以外）
            if i < len(problems) - 1:
                doc.add_paragraph()
        
        return doc
    
    def _apply_global_style(self, doc: Document):
        """文書全体のスタイル設定"""
        sections = doc.sections
        for section in sections:
            # 余白設定
            margin = Cm(self.config['page_margin'])
            section.top_margin = margin
            section.bottom_margin = margin
            section.left_margin = margin
            section.right_margin = margin
        
        # スタイル定義
        styles = doc.styles
        
        # 見出しスタイル
        if 'Heading 1' in styles:
            style = styles['Heading 1']
            style.font.name = self.config['title_font']
            style.font.size = Pt(self.config['title_size'])
            style.font.bold = self.config['title_bold']
    
    def _add_problem(self, doc: Document, problem: Dict[str, Any]):
        """問題を文書に追加"""
        # タイトル
        if problem['title']:
            title = doc.add_heading(problem['title'], level=1)
            self._apply_title_style(title)
        else:
            title = doc.add_heading(f'大問{self.problem_counter}', level=1)
            self._apply_title_style(title)
        
        # 問題文（テキストと数式が混在）
        current_para = None
        
        for element in problem['text']:
            if element['type'] == 'text':
                # テキスト要素
                if current_para is None:
                    current_para = doc.add_paragraph()
                    self._apply_body_style(current_para)
                
                # テキストを追加
                run = current_para.add_run(element['content'])
                
            elif element['type'] == 'math':
                # インライン数式
                if current_para is None:
                    current_para = doc.add_paragraph()
                    self._apply_body_style(current_para)
                
                # 数式画像を追加
                try:
                    img_stream = self.math_converter.latex_to_image(element['content'])
                    run = current_para.add_run()
                    # インライン数式は小さめに
                    run.add_picture(img_stream, height=Pt(self.config['body_size'] + 2))
                except Exception as e:
                    # エラー時はテキストで表示
                    run = current_para.add_run(f"[{element['content']}]")
                    run.font.color.rgb = RGBColor(255, 0, 0)
        
        # 段落が作成されていれば、終了
        if current_para is not None:
            current_para = None
        
        # 独立した数式
        for equation in problem['equations']:
            self._add_display_math(doc, equation)
        
        # 選択肢
        if problem['choices']:
            self._add_choices(doc, problem['choices'])
    
    def _apply_title_style(self, paragraph):
        """タイトルスタイルを適用"""
        for run in paragraph.runs:
            run.font.name = self.config['title_font']
            run._element.rPr.rFonts.set(qn('w:eastAsia'), self.config['title_font'])
            run.font.size = Pt(self.config['title_size'])
            run.font.bold = self.config['title_bold']
    
    def _apply_body_style(self, paragraph):
        """本文スタイルを適用"""
        paragraph.paragraph_format.line_spacing = self.config['paragraph_spacing']
        
        for run in paragraph.runs:
            run.font.name = self.config['body_font']
            run._element.rPr.rFonts.set(qn('w:eastAsia'), self.config['body_font'])
            run.font.size = Pt(self.config['body_size'])
    
    def _add_display_math(self, doc: Document, latex_str: str):
        """独立した数式を追加（中央揃え）"""
        para = doc.add_paragraph()
        para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        run = para.add_run()
        
        try:
            # 数式を画像化
            img_stream = self.math_converter.latex_to_image(latex_str)
            run.add_picture(img_stream, width=Inches(2.5))
        except Exception as e:
            # エラー時
            run.text = f"[数式エラー: {latex_str[:30]}...]"
            run.font.color.rgb = RGBColor(255, 0, 0)
        
        para.paragraph_format.space_after = Pt(12)
    
    def _add_choices(self, doc: Document, choices: List[str]):
        """選択肢を追加"""
        for i, choice in enumerate(choices, 1):
            # 選択肢にもインライン数式が含まれる可能性がある
            para = doc.add_paragraph()
            para.paragraph_format.left_indent = Cm(self.config['choice_indent'])
            
            # 番号を追加
            run = para.add_run(f'{i}. ')
            run.font.name = self.config['choice_font']
            run._element.rPr.rFonts.set(qn('w:eastAsia'), self.config['choice_font'])
            run.font.size = Pt(self.config['choice_size'])
            
            # 選択肢テキストを解析してインライン数式を処理
            self._add_text_with_inline_math(para, choice)
    
    def _add_text_with_inline_math(self, paragraph, text: str):
        """テキスト内のインライン数式を処理して段落に追加"""
        # インライン数式パターン: \(...\) または $...$
        pattern = r'\\\((.+?)\\\)|\$([^$]+)\$'
        
        last_end = 0
        for match in re.finditer(pattern, text):
            # 数式の前のテキスト
            if match.start() > last_end:
                plain_text = text[last_end:match.start()]
                run = paragraph.add_run(plain_text)
                run.font.name = self.config['choice_font']
                run._element.rPr.rFonts.set(qn('w:eastAsia'), self.config['choice_font'])
                run.font.size = Pt(self.config['choice_size'])
            
            # 数式部分
            latex_str = match.group(1) or match.group(2)
            if latex_str:
                try:
                    img_stream = self.math_converter.latex_to_image(latex_str.strip())
                    run = paragraph.add_run()
                    run.add_picture(img_stream, height=Pt(self.config['choice_size'] + 2))
                except Exception as e:
                    # エラー時はテキストで表示
                    run = paragraph.add_run(f"[{latex_str}]")
                    run.font.color.rgb = RGBColor(255, 0, 0)
            
            last_end = match.end()
        
        # 残りのテキスト
        if last_end < len(text):
            plain_text = text[last_end:]
            run = paragraph.add_run(plain_text)
            run.font.name = self.config['choice_font']
            run._element.rPr.rFonts.set(qn('w:eastAsia'), self.config['choice_font'])
            run.font.size = Pt(self.config['choice_size'])
WORD_GEN_FIX_EOF

echo "✓ word_generator.pyを修正しました"

# 新しいテストHTMLを作成
cat > data/input/test_inline_math.html << 'INLINE_TEST_EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>インライン数式テスト</title>
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">[1] 数と式・集合と命題</h2>
        <p class="problem-text">
            1. \(x + y = 4\) （(1)より）
        </p>
        <p class="problem-text">
            2. \(x^2 + y^2 = 10\) （問題文より）
        </p>
        <p class="problem-text">
            3. \(xy = 3\) （問題文より）
        </p>
        <div class="math">$$(x + y)^2 = x^2 + 2xy + y^2$$</div>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">[2] 図形と計量</h2>
        <p class="problem-text">
            1. 俯角の定義を正確に理解する
        </p>
        <p class="problem-text">
            2. 高さの差を正しく表現する
        </p>
        <p class="problem-text">
            3. \(\tan\) の値から辺の比を求める
        </p>
        <p class="problem-text">
            4. 図を描いて直角三角形を見つける
        </p>
        <div class="math">$$\tan \theta = \frac{h}{d}$$</div>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">[3] 2次関数</h2>
        <p class="problem-text">
            1. \(a < 0\)：上に凸 → 最大値 \(q\)
        </p>
        <p class="problem-text">
            2. \(a > 0\)：下に凸 → 最小値 \(q\)
        </p>
        <div class="math">$$f(x) = ax^2 + bx + c$$</div>
        <p class="problem-text">
            頂点の座標は \(\left(-\frac{b}{2a}, q\right)\) である。
        </p>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">[4] 選択肢に数式を含む問題</h2>
        <p class="problem-text">
            次の方程式を解きなさい。
        </p>
        <div class="math">$$x^2 - 5x + 6 = 0$$</div>
        <ol class="choices">
            <li>\(x = 2, 3\)</li>
            <li>\(x = -2, -3\)</li>
            <li>\(x = 1, 6\)</li>
            <li>\(x = -1, -6\)</li>
        </ol>
    </div>
</body>
</html>
INLINE_TEST_EOF

echo "✓ テスト用HTMLファイルを作成しました"

# 包括的なテストスクリプト
cat > test_inline_complete.py << 'TEST_INLINE_EOF'
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
TEST_INLINE_EOF

echo "✓ テストスクリプトを作成しました"

echo ""
echo "============================================"
echo "インライン数式の完全修正が完了しました！"
echo "============================================"
echo ""
echo "テストを実行:"
echo "  python test_inline_complete.py"
echo ""
echo "結果を確認:"
echo "  open data/output/test_inline_math.docx"
echo ""
echo "GUIで確認:"
echo "  python run_gui.py"
echo "  → test_inline_math.html を選択して変換"
echo ""
