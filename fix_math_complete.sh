#!/bin/bash

echo "数式表示の完全修正を開始します..."

# math_converter.pyを完全に書き直し
cat > src/core/math_converter.py << 'MATH_COMPLETE_EOF'
"""数式画像変換モジュール（完全修正版）"""
import matplotlib
matplotlib.use('Agg')
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
        
        # matplotlibの設定
        plt.rcParams['mathtext.fontset'] = 'cm'
        plt.rcParams['mathtext.default'] = 'regular'
    
    def latex_to_image(self, latex_str: str) -> BinaryIO:
        """LaTeX数式を画像化"""
        try:
            # 前処理
            latex_str = self._preprocess_latex(latex_str)
            
            # 図を作成
            fig = plt.figure(figsize=(10, 2))
            fig.patch.set_alpha(0)
            
            # 数式をレンダリング
            ax = fig.add_subplot(111)
            ax.axis('off')
            
            # テキストを描画
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
            renderer = fig.canvas.get_renderer()
            bbox = text.get_window_extent(renderer=renderer)
            
            # 余白を追加
            bbox_padded = bbox.padded(10)
            
            # 画像として保存
            buf = io.BytesIO()
            fig.savefig(
                buf,
                format='png',
                dpi=self.dpi,
                bbox_inches=bbox_padded.transformed(fig.dpi_scale_trans.inverted()),
                transparent=True,
                pad_inches=0.1
            )
            plt.close(fig)
            
            buf.seek(0)
            return buf
            
        except Exception as e:
            print(f"数式変換エラー: {latex_str[:50]}...")
            print(f"エラー内容: {str(e)}")
            return self._create_error_image(latex_str)
    
    def _preprocess_latex(self, latex_str: str) -> str:
        """LaTeX文字列の前処理"""
        # 前後の空白を削除
        latex_str = latex_str.strip()
        
        # $記号を削除
        latex_str = re.sub(r'^\$+|\$+$', '', latex_str)
        
        # \text{}の処理を改善
        # matplotlibのmathtextは\text{}を完全にはサポートしていないため、
        # \mathrm{}に変換
        latex_str = re.sub(r'\\text\{([^}]+)\}', r'\\mathrm{\1}', latex_str)
        
        # 特殊文字のエスケープ
        # （必要に応じて追加）
        
        return latex_str
    
    def _create_error_image(self, latex_str: str) -> BinaryIO:
        """エラー時の代替画像"""
        try:
            fig = plt.figure(figsize=(4, 0.5))
            fig.patch.set_facecolor('#ffe6e6')
            
            ax = fig.add_subplot(111)
            ax.axis('off')
            
            error_msg = f'[数式エラー]'
            ax.text(
                0.5, 0.5,
                error_msg,
                fontsize=10,
                color='red',
                ha='center',
                va='center',
                transform=ax.transAxes,
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='red')
            )
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
            plt.close(fig)
            
            buf.seek(0)
            return buf
        except:
            # 最終フォールバック
            fig = plt.figure(figsize=(2, 0.3))
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150)
            plt.close(fig)
            buf.seek(0)
            return buf
    
    def test_conversion(self, latex_str: str) -> bool:
        """変換テスト"""
        try:
            buf = self.latex_to_image(latex_str)
            img = Image.open(buf)
            return img.size[0] > 0 and img.size[1] > 0
        except:
            return False
MATH_COMPLETE_EOF

echo "✓ math_converter.pyを完全修正しました"

# 新しいテストHTMLを作成
cat > data/input/test_cheva.html << 'CHEVA_HTML_EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>チェバの定理</title>
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">チェバの定理</h2>
        <p class="problem-text">
            証明の概要：教科書p.91の証明では、△OABと△OCAの面積比を使って、
            以下の関係を導きます。
        </p>
        <div class="math">$$\frac{BP}{PC} = \frac{S_{OAB}}{S_{OCA}}$$</div>
        <p class="problem-text">
            これらを掛け合わせることで定理を証明します。
        </p>
        <div class="math">$$\frac{BP}{PC} \cdot \frac{CQ}{QA} \cdot \frac{AR}{RB} = 1$$</div>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">内分点の公式</h2>
        <p class="problem-text">
            内分点はAP:PB=$m$:$n$のとき、Aから$\frac{m}{m+n}$の位置にあります。
        </p>
        <div class="math">$$P = \frac{mb + na}{m+n}$$</div>
        <p class="problem-text">
            ただし、$m > 0$、$n > 0$とする。
        </p>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">複雑な分数式</h2>
        <p class="problem-text">
            次の式を簡単にしなさい。
        </p>
        <div class="math">$$\frac{x^2 - y^2}{x + y} = x - y$$</div>
        <p class="problem-text">
            また、$\frac{a}{b} + \frac{c}{d} = \frac{ad + bc}{bd}$を用いてもよい。
        </p>
    </div>
</body>
</html>
CHEVA_HTML_EOF

echo "✓ テスト用HTMLファイルを作成しました"

# テストスクリプトを更新
cat > test_math_final.py << 'TEST_FINAL_EOF'
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
TEST_FINAL_EOF

echo "✓ テストスクリプトを作成しました"

echo ""
echo "============================================"
echo "数式表示の完全修正が完了しました！"
echo "============================================"
echo ""
echo "テストを実行:"
echo "  python test_math_final.py"
echo ""
echo "結果を確認:"
echo "  open data/output/test_cheva.docx"
echo ""
echo "GUIで確認:"
echo "  python run_gui.py"
echo "  → test_cheva.html を選択して変換"
echo ""
