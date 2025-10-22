# MathConverter API リファレンス

## クラス概要

```python
from core.math_converter import MathConverter
MathConverter クラスは、LaTeX形式の数式を高品質なPNG画像に変換します。

クラス定義
Copyclass MathConverter:
    def __init__(self, config: dict)
    def latex_to_image(self, latex_str: str) -> BinaryIO
    def test_conversion(self, latex_str: str) -> bool
初期化
__init__(config: dict)
Copyconverter = MathConverter(config)
説明: MathConverterのインスタンスを作成します。

パラメータ:

config (dict): スタイル設定辞書
必要な設定キー:

math_dpi (int): 画像解像度（72〜600推奨）
math_font_size (int): フォントサイズ（8〜24推奨）
math_color (str): 数式の色
使用例:

Copyfrom core.style_config import STYLE_CONFIG
from core.math_converter import MathConverter

# 標準設定で初期化
converter = MathConverter(STYLE_CONFIG)

# カスタム設定で初期化
custom_config = {
    'math_dpi': 600,
    'math_font_size': 16,
    'math_color': 'blue'
}
converter = MathConverter(custom_config)
メソッド
latex_to_image(latex_str: str)
Copydef latex_to_image(self, latex_str: str) -> BinaryIO
説明: LaTeX数式をPNG画像に変換し、バイナリストリームで返します。

パラメータ:

latex_str (str): LaTeX数式文字列（$記号は不要）
戻り値: BinaryIO - PNG画像のバイナリストリーム

画像の特性:

フォーマット: PNG
背景: 透過（設定による）
解像度: 設定によるDPI
色深度: 32bit RGBA
使用例:

Copy# 基本的な使用
img_stream = converter.latex_to_image('x^2 + y^2 = r^2')

# python-docxで使用
from docx import Document
from docx.shared import Inches

doc = Document()
para = doc.add_paragraph()
run = para.add_run()
run.add_picture(img_stream, width=Inches(2.0))
doc.save('output.docx')
対応LaTeX記法:

Copy# 基本演算
converter.latex_to_image('x + y - z')
converter.latex_to_image('x \\times y \\div z')

# 上付き・下付き
converter.latex_to_image('x^2 + y^3')
converter.latex_to_image('x_i + x_{i+1}')

# 分数
converter.latex_to_image(r'\frac{a}{b}')
converter.latex_to_image(r'\frac{x^2 + 1}{x - 1}')

# 根号
converter.latex_to_image(r'\sqrt{x}')
converter.latex_to_image(r'\sqrt[3]{x}')
converter.latex_to_image(r'\sqrt{x^2 + y^2}')

# 積分
converter.latex_to_image(r'\int f(x) dx')
converter.latex_to_image(r'\int_{0}^{1} x^2 dx')
converter.latex_to_image(r'\int_{-\infty}^{\infty} e^{-x^2} dx')

# 総和
converter.latex_to_image(r'\sum_{i=1}^{n} i')
converter.latex_to_image(r'\sum_{i=1}^{\infty} \frac{1}{i^2}')

# ギリシャ文字
converter.latex_to_image(r'\alpha + \beta = \gamma')
converter.latex_to_image(r'\Delta x \cdot \Delta y')

# 行列
converter.latex_to_image(r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}')

# 複雑な数式
converter.latex_to_image(
    r'\int_{0}^{\infty} \frac{\sin x}{x} dx = \frac{\pi}{2}'
)
エラー処理:

Copytry:
    img_stream = converter.latex_to_image('x^2 + y^2')
    # 成功時の処理
except Exception as e:
    print(f"変換エラー: {e}")
    # エラー時は代替画像が返される
パフォーマンス:

簡単な数式: 約0.1〜0.3秒
複雑な数式: 約0.5〜1.0秒
行列・積分: 約1.0〜2.0秒
test_conversion(latex_str: str)
Copydef test_conversion(self, latex_str: str) -> bool
説明: 数式変換が正しく動作するかテストします。

パラメータ:

latex_str (str): テストするLaTeX文字列
戻り値: bool

True: 変換成功
False: 変換失敗
使用例:

Copy# 単一の数式をテスト
if converter.test_conversion('x^2 + y^2'):
    print("変換成功")
else:
    print("変換失敗")

# 複数の数式をテスト
test_formulas = [
    'x^2 + y^2 = r^2',
    r'\frac{a}{b}',
    r'\int_{0}^{1} x dx',
    r'\sum_{i=1}^{n} i',
]

for formula in test_formulas:
    result = converter.test_conversion(formula)
    status = "OK" if result else "NG"
    print(f"{formula}: {status}")
実践的な使用例
複数の数式を一括変換
Copyfrom core.style_config import STYLE_CONFIG
from core.math_converter import MathConverter

converter = MathConverter(STYLE_CONFIG)

equations = [
    'x^2 + y^2 = r^2',
    r'\frac{a}{b} = c',
    r'\int_{0}^{1} x dx = \frac{1}{2}',
]

images = []
for eq in equations:
    try:
        img_stream = converter.latex_to_image(eq)
        images.append(img_stream)
        print(f"変換成功: {eq}")
    except Exception as e:
        print(f"変換失敗: {eq} - {e}")

print(f"\n合計 {len(images)} 個の画像を生成しました")
異なる解像度で変換
Copy# 印刷用高解像度
print_config = STYLE_CONFIG.copy()
print_config['math_dpi'] = 600
print_converter = MathConverter(print_config)

# Web用標準解像度
web_config = STYLE_CONFIG.copy()
web_config['math_dpi'] = 150
web_converter = MathConverter(web_config)

latex = 'x^2 + y^2 = r^2'

# 用途に応じて使い分け
print_img = print_converter.latex_to_image(latex)
web_img = web_converter.latex_to_image(latex)
カスタム色で変換
Copy# 青色の数式
blue_config = STYLE_CONFIG.copy()
blue_config['math_color'] = 'blue'
blue_converter = MathConverter(blue_config)

# RGB指定
red_config = STYLE_CONFIG.copy()
red_config['math_color'] = (1.0, 0.0, 0.0)  # 赤
red_converter = MathConverter(red_config)

latex = r'\int_{0}^{1} x^2 dx'
blue_img = blue_converter.latex_to_image(latex)
red_img = red_converter.latex_to_image(latex)
エラーハンドリング付き変換
Copydef safe_convert(converter, latex_str, fallback_text="[数式エラー]"):
    """エラーハンドリング付きの安全な変換"""
    try:
        img_stream = converter.latex_to_image(latex_str)
        return img_stream, True
    except Exception as e:
        print(f"警告: 数式変換エラー - {latex_str}")
        print(f"  エラー内容: {e}")
        
        # フォールバック画像を生成
        try:
            fallback_img = converter.latex_to_image(fallback_text)
            return fallback_img, False
        except:
            return None, False

# 使用
latex = 'x^2 + y^2 = r^2'
img_stream, success = safe_convert(converter, latex)

if success:
    print("変換成功")
else:
    print("フォールバック画像を使用")
バッチ処理
Copyimport time

def batch_convert(converter, latex_list, show_progress=True):
    """複数の数式を効率的に変換"""
    results = []
    total = len(latex_list)
    
    for i, latex in enumerate(latex_list, 1):
        if show_progress:
            print(f"処理中... {i}/{total}")
        
        try:
            img_stream = converter.latex_to_image(latex)
            results.append({
                'latex': latex,
                'image': img_stream,
                'status': 'success'
            })
        except Exception as e:
            results.append({
                'latex': latex,
                'image': None,
                'status': 'error',
                'error': str(e)
            })
    
    # 統計情報
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"\n完了: {success_count}/{total} 個の数式を変換しました")
    
    return results

# 使用
equations = [
    'x^2 + y^2 = r^2',
    r'\frac{a}{b}',
    r'\int_{0}^{1} x dx',
    # ... 多数の数式
]

results = batch_convert(converter, equations)
キャッシング機能
Copyfrom functools import lru_cache
import hashlib

class CachedMathConverter(MathConverter):
    """キャッシング機能付き数式変換"""
    
    def __init__(self, config):
        super().__init__(config)
        self.cache = {}
    
    def latex_to_image(self, latex_str: str):
        # キャッシュキーを生成
        cache_key = hashlib.md5(latex_str.encode()).hexdigest()
        
        # キャッシュにあれば返す
        if cache_key in self.cache:
            print(f"キャッシュヒット: {latex_str[:30]}...")
            return self.cache[cache_key]
        
        # 変換して キャッシュに保存
        img_stream = super().latex_to_image(latex_str)
        self.cache[cache_key] = img_stream
        
        return img_stream
    
    def clear_cache(self):
        """キャッシュをクリア"""
        self.cache.clear()
        print("キャッシュをクリアしました")

# 使用
cached_converter = CachedMathConverter(STYLE_CONFIG)

# 同じ数式を複数回変換（2回目以降は高速）
latex = 'x^2 + y^2 = r^2'
img1 = cached_converter.latex_to_image(latex)  # 通常の変換
img2 = cached_converter.latex_to_image(latex)  # キャッシュから取得
トラブルシューティング
問題: 画像が粗い
原因: DPI設定が低すぎる

解決策:

Copyconfig = STYLE_CONFIG.copy()
config['math_dpi'] = 600  # 高解像度に変更
converter = MathConverter(config)
問題: 変換が遅い
原因: 複雑な数式や高DPI設定

解決策:

Copy# 解像度を下げる
config['math_dpi'] = 150

# または並列処理を使用
from concurrent.futures import ThreadPoolExecutor

def convert_parallel(latex_list):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(converter.latex_to_image, latex_list))
    return results
問題: LaTeX構文エラー
原因: 不正なLaTeX記法

解決策:

Copy# バックスラッシュを正しくエスケープ
converter.latex_to_image(r'\frac{a}{b}')  # OK
# converter.latex_to_image('\frac{a}{b}')  # NG

# raw文字列を使用
latex = r'\int_{0}^{1} x dx'
converter.latex_to_image(latex)
問題: メモリ使用量が多い
原因: 大量の画像を同時に保持

解決策:

Copy# 画像を生成したらすぐに使用し、参照を削除
for latex in latex_list:
    img_stream = converter.latex_to_image(latex)
    # すぐに使用
    run.add_picture(img_stream, width=Inches(2.0))
    # 参照を削除（自動的にガベージコレクション）
    del img_stream
