#!/bin/bash

echo "数式サイズの調整を開始します..."

# style_config.pyを修正（数式サイズの設定を追加）
cat > src/core/style_config.py << 'STYLE_FIX_EOF'
"""統一スタイル設定（サイズ調整版）"""

STYLE_CONFIG = {
    # 数式画像設定
    'math_dpi': 300,
    'math_font_size': 12,  # 数式のフォントサイズを小さく
    'math_color': 'black',
    'math_background': 'transparent',
    
    # インライン数式の高さ設定（ポイント単位）
    'inline_math_height': 14,  # 本文とほぼ同じ高さ
    'display_math_width': 2.5,  # インチ単位
    
    # テキストスタイル
    'title_font': 'MS Gothic',
    'title_size': 16,
    'title_bold': True,
    'body_font': 'MS Mincho',
    'body_size': 11,
    
    # レイアウト
    'problem_spacing': 1.5,
    'paragraph_spacing': 1.15,
    'page_margin': 2.54,  # cm
    
    # 選択肢スタイル
    'choice_font': 'MS Mincho',
    'choice_size': 11,
    'choice_indent': 1.0,  # cm
}

# テンプレート定義
TEMPLATES = {
    'standard': {
        'name': '標準問題集',
        'header': None,
        'footer': 'ページ {page}',
        'title_style': '見出し 1',
        'numbering': True,
    },
    'exam': {
        'name': '定期試験',
        'header': '{school_name} 数学テスト',
        'footer': '氏名:__________ 得点:____/100',
        'title_style': '見出し 2',
        'time_limit': True,
    },
    'homework': {
        'name': '宿題プリント',
        'header': '提出日: {date}',
        'footer': 'クラス:____ 番号:____ 氏名:__________',
        'answer_space': True,
    }
}
STYLE_FIX_EOF

echo "✓ style_config.pyを修正しました"

# word_generator.pyを修正（サイズ設定を使用）
cat > src/core/word_generator.py << 'WORD_SIZE_FIX_EOF'
"""Word文書生成モジュール（サイズ調整版）"""
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
                
                # 数式画像を追加（小さめに）
                try:
                    img_stream = self.math_converter.latex_to_image(element['content'])
                    run = current_para.add_run()
                    # インライン数式の高さを設定から取得
                    inline_height = self.config.get('inline_math_height', 14)
                    run.add_picture(img_stream, height=Pt(inline_height))
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
            # ディスプレイ数式の幅を設定から取得
            display_width = self.config.get('display_math_width', 2.5)
            run.add_picture(img_stream, width=Inches(display_width))
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
                    # 選択肢内のインライン数式も小さめに
                    inline_height = self.config.get('inline_math_height', 14)
                    run.add_picture(img_stream, height=Pt(inline_height))
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
WORD_SIZE_FIX_EOF

echo "✓ word_generator.pyを修正しました"

# テスト用HTMLを作成
cat > data/input/test_size_adjust.html << 'SIZE_TEST_EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>サイズ調整テスト</title>
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">各大問の重要ポイント</h2>
        <p class="problem-text">
            1. 対称式：\((x + y)^2 = x^2 + 2xy + y^2\) の変形を使いこなす
        </p>
        <p class="problem-text">
            2. 3乗の和：\(x^3 + y^3 = (x + y)(x^2 - xy + y^2)\) を覚える
        </p>
        <p class="problem-text">
            3. 必要十分条件：具体例と反例で判定
        </p>
        <p class="problem-text">
            4. 俯角の問題：高さの差を正確に表現し、\(\tan\) を使う
        </p>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">2次関数の性質</h2>
        <p class="problem-text">
            1. \(a < 0\)：上に凸 → 最大値 \(q\)
        </p>
        <p class="problem-text">
            2. \(a > 0\)：下に凸 → 最小値 \(q\)
        </p>
        <div class="math">$$f(x) = a(x - p)^2 + q$$</div>
        <p class="problem-text">
            頂点の座標は \((p, q)\) である。
        </p>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">選択肢のサイズテスト</h2>
        <p class="problem-text">次の方程式を解きなさい。</p>
        <div class="math">$$x^2 - 5x + 6 = 0$$</div>
        <ol class="choices">
            <li>\(x = 2, 3\)</li>
            <li>\(x = -2, -3\)</li>
            <li>\(x = \frac{5 \pm \sqrt{1}}{2}\)</li>
            <li>解なし</li>
        </ol>
    </div>
</body>
</html>
SIZE_TEST_EOF

echo "✓ テスト用HTMLファイルを作成しました"

# テストスクリプト
cat > test_size_adjust.py << 'TEST_SIZE_EOF'
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
TEST_SIZE_EOF

echo "✓ テストスクリプトを作成しました"

echo ""
echo "============================================"
echo "数式サイズの調整が完了しました！"
echo "============================================"
echo ""
echo "設定:"
echo "  - インライン数式の高さ: 14pt（本文11ptに対して少し大きめ）"
echo "  - 数式フォントサイズ: 12pt"
echo ""
echo "テストを実行:"
echo "  python test_size_adjust.py"
echo ""
echo "結果を確認:"
echo "  open data/output/test_size_adjust.docx"
echo ""
echo "サイズを調整する場合:"
echo "  src/core/style_config.py を編集"
echo "  - inline_math_height: 12〜16 の範囲で調整"
echo "  - math_font_size: 10〜14 の範囲で調整"
echo ""
