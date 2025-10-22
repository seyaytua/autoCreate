# モジュール詳細仕様書

## 1. style_config.py

### 1.1 概要
システム全体で使用するスタイル設定を一元管理するモジュールです。

### 1.2 定数定義

#### STYLE_CONFIG
**型**: `Dict[str, Any]`

**説明**: 文書のスタイル設定を定義する辞書

**構造**:
```python
{
    # 数式画像設定
    'math_dpi': int,              # 画像解像度（推奨: 300）
    'math_font_size': int,        # 数式フォントサイズ（推奨: 14）
    'math_color': str,            # 数式の色（'black', 'blue'など）
    'math_background': str,       # 背景色（'transparent'推奨）
    
    # テキストスタイル
    'title_font': str,            # タイトルフォント
    'title_size': int,            # タイトルサイズ（pt）
    'title_bold': bool,           # タイトル太字
    'body_font': str,             # 本文フォント
    'body_size': int,             # 本文サイズ（pt）
    
    # レイアウト
    'problem_spacing': float,     # 問題間の行間
    'paragraph_spacing': float,   # 段落の行間
    'page_margin': float,         # ページ余白（cm）
    
    # 選択肢スタイル
    'choice_font': str,           # 選択肢フォント
    'choice_size': int,           # 選択肢サイズ（pt）
    'choice_indent': float,       # 選択肢インデント（cm）
}
使用例:

Copyfrom core.style_config import STYLE_CONFIG

# 数式のDPI設定を取得
dpi = STYLE_CONFIG['math_dpi']

# カスタム設定を作成
custom_config = STYLE_CONFIG.copy()
custom_config['math_dpi'] = 600  # 高解像度に変更
TEMPLATES
型: Dict[str, Dict[str, Any]]

説明: 文書テンプレートの定義

テンプレート種類:

standard: 標準問題集
exam: 定期試験
homework: 宿題プリント
構造:

Copy{
    'template_name': {
        'name': str,              # テンプレート表示名
        'header': Optional[str],  # ヘッダーテキスト
        'footer': Optional[str],  # フッターテキスト
        'title_style': str,       # タイトルスタイル
        'numbering': bool,        # ページ番号表示
        # その他のテンプレート固有設定
    }
}
1.3 カスタマイズ方法
フォント変更:

Copy# Macの場合
STYLE_CONFIG['title_font'] = 'Hiragino Sans'
STYLE_CONFIG['body_font'] = 'Hiragino Mincho ProN'

# Windowsの場合
STYLE_CONFIG['title_font'] = 'MS Gothic'
STYLE_CONFIG['body_font'] = 'MS Mincho'
解像度調整:

Copy# 印刷用高解像度
STYLE_CONFIG['math_dpi'] = 600

# Web用標準解像度
STYLE_CONFIG['math_dpi'] = 150
2. html_parser.py
2.1 概要
HTML形式の数学問題を解析し、構造化されたデータに変換するモジュールです。

2.2 クラス: HTMLParser
2.2.1 初期化
Copyparser = HTMLParser()
パラメータ: なし

初期化される属性:

latex_pattern: LaTeX数式を検出する正規表現パターン
2.2.2 メソッド: parse()
シグネチャ:

Copydef parse(self, html_content: str) -> List[Dict[str, Any]]
説明: HTML文字列を解析し、問題データのリストを返します。

パラメータ:

html_content (str): 解析するHTML文字列
戻り値: List[Dict[str, Any]]

Copy[
    {
        'title': str,                    # 問題タイトル
        'text': List[Dict[str, Any]],    # 問題文（テキストと数式）
        'equations': List[str],          # 独立した数式
        'choices': List[str],            # 選択肢
        'raw_html': str                  # 元のHTML
    },
    ...
]
使用例:

Copyparser = HTMLParser()

html = '''
<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">次の方程式を解きなさい。</p>
    <div class="math">$$x^2 + 5x + 6 = 0$$</div>
</div>
'''

problems = parser.parse(html)
print(problems[0]['title'])  # "大問1"
print(problems[0]['equations'])  # ['x^2 + 5x + 6 = 0']
エラー処理:

不正なHTMLの場合: 空のリストを返す
class属性がない場合: h2タグで自動分割
2.2.3 メソッド: _extract_title()
シグネチャ:

Copydef _extract_title(self, problem_div) -> str
説明: 問題のタイトルを抽出します。

検索順序:

<h2 class="problem-title"> を検索
見つからない場合、<h2> タグを検索
どちらもない場合、空文字列を返す
2.2.4 メソッド: _extract_text()
シグネチャ:

Copydef _extract_text(self, problem_div) -> List[Dict[str, Any]]
説明: 問題文を抽出し、テキストと数式に分離します。

戻り値の構造:

Copy[
    {'type': 'text', 'content': '次の方程式を解きなさい。'},
    {'type': 'math', 'content': 'x^2 + 5x + 6 = 0'},
    {'type': 'text', 'content': 'ただし、'},
    {'type': 'math', 'content': 'x \\neq 0'},
]
2.2.5 メソッド: _extract_equations()
シグネチャ:

Copydef _extract_equations(self, problem_div) -> List[str]
説明: 独立した数式ブロック（<div class="math">）を抽出します。

処理:

$$...$$ を自動的に除去
空白をトリミング
2.2.6 メソッド: _extract_choices()
シグネチャ:

Copydef _extract_choices(self, problem_div) -> List[str]
説明: 選択肢を抽出します。

対応タグ:

<ol class="choices">
<ul class="choices">
class属性なしの <ol>, <ul>
2.3 対応HTML構造
標準形式:

Copy<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">問題文</p>
    <div class="math">$$数式$$</div>
    <ol class="choices">
        <li>選択肢1</li>
        <li>選択肢2</li>
    </ol>
</div>
簡易形式（class属性なし）:

Copy<h2>大問1</h2>
<p>問題文</p>
<div>$$数式$$</div>
<ol>
    <li>選択肢1</li>
    <li>選択肢2</li>
</ol>
2.4 LaTeX数式の対応形式
ディスプレイ数式:


$$x^2 + y^2 = r^2$$
インライン数式:

\(x^2 + y^2 = r^2\)
3. math_converter.py
3.1 概要
LaTeX形式の数式を高品質なPNG画像に変換するモジュールです。

3.2 クラス: MathConverter
3.2.1 初期化
Copyconverter = MathConverter(config: dict)
パラメータ:

config (dict): スタイル設定辞書（STYLE_CONFIGを使用）
必要な設定キー:

math_dpi: 画像解像度
math_font_size: フォントサイズ
math_color: 数式の色
使用例:

Copyfrom core.style_config import STYLE_CONFIG
from core.math_converter import MathConverter

converter = MathConverter(STYLE_CONFIG)
3.2.2 メソッド: latex_to_image()
シグネチャ:

Copydef latex_to_image(self, latex_str: str) -> BinaryIO
説明: LaTeX文字列をPNG画像に変換し、バイナリストリームで返します。

パラメータ:

latex_str (str): LaTeX数式文字列（$記号なし）
戻り値: BinaryIO - PNG画像のバイナリストリーム

使用例:

Copy# 簡単な数式
img_stream = converter.latex_to_image('x^2 + y^2 = r^2')

# 分数
img_stream = converter.latex_to_image(r'\frac{a}{b}')

# 複雑な数式
img_stream = converter.latex_to_image(
    r'\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}'
)

# python-docxで使用
from docx import Document
doc = Document()
para = doc.add_paragraph()
run = para.add_run()
run.add_picture(img_stream, width=Inches(2.0))
エラー処理:

LaTeX構文エラーの場合: [数式エラー] テキストの画像を返す
レンダリング失敗の場合: 例外をキャッチして代替画像を生成
対応LaTeX記法:

基本演算: +, -, \times, \div
上付き・下付き: x^2, x_i
分数: \frac{a}{b}
根号: \sqrt{x}, \sqrt[n]{x}
積分: \int, \iint, \oint
総和: \sum, \prod
ギリシャ文字: \alpha, \beta, \gammaなど
括弧: \left(, \right), \{, \}
行列: \begin{pmatrix}...\end{pmatrix}
3.2.3 メソッド: test_conversion()
シグネチャ:

Copydef test_conversion(self, latex_str: str) -> bool
説明: 数式変換が正しく動作するかテストします。

パラメータ:

latex_str (str): テストするLaTeX文字列
戻り値: bool - 変換成功時True、失敗時False

使用例:

Copy# 変換テスト
if converter.test_conversion('x^2 + y^2'):
    print("変換成功")
else:
    print("変換失敗")
3.3 画像品質設定
解像度の推奨値:

印刷用: 300〜600 DPI
画面表示用: 150〜200 DPI
Web用: 96〜150 DPI
フォントサイズの推奨値:

標準: 14pt
大きめ: 16〜18pt
小さめ: 10〜12pt
色の指定:

Copy# 基本色
'black', 'white', 'red', 'blue', 'green'

# RGB指定
(0.0, 0.0, 0.0)  # 黒
(1.0, 0.0, 0.0)  # 赤
3.4 パフォーマンス
処理時間:

簡単な数式: 約0.1〜0.3秒
複雑な数式: 約0.5〜1.0秒
行列・積分: 約1.0〜2.0秒
メモリ使用量:

1つの数式: 約1〜5MB（一時的）
画像サイズ: 約10〜100KB
4. word_generator.py
4.1 概要
構造化された問題データからWord文書を生成するモジュールです。

4.2 クラス: WordGenerator
4.2.1 初期化
Copygenerator = WordGenerator(style_config: dict, math_converter: MathConverter)
パラメータ:

style_config (dict): スタイル設定辞書
math_converter (MathConverter): 数式変換オブジェクト
使用例:

Copyfrom core.style_config import STYLE_CONFIG
from core.math_converter import MathConverter
from core.word_generator import WordGenerator

math_conv = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, math_conv)
4.2.2 メソッド: create_document()
シグネチャ:

Copydef create_document(self, problems: List[Dict[str, Any]]) -> Document
説明: 問題データのリストからWord文書を生成します。

パラメータ:

problems (List[Dict]): HTMLParserから取得した問題データ
戻り値: Document - python-docxのDocumentオブジェクト

使用例:

Copy# HTMLを解析
parser = HTMLParser()
problems = parser.parse(html_content)

# Word文書を生成
doc = generator.create_document(problems)

# 保存
doc.save('output.docx')
4.2.3 メソッド: _apply_global_style()
シグネチャ:

Copydef _apply_global_style(self, doc: Document) -> None
説明: 文書全体のスタイルを設定します。

設定内容:

ページ余白
デフォルトフォント
見出しスタイル
4.2.4 メソッド: _add_problem()
シグネチャ:

Copydef _add_problem(self, doc: Document, problem: Dict[str, Any]) -> None
説明: 1つの問題を文書に追加します。

処理順序:

タイトル追加
問題文追加（テキストと数式）
独立数式追加
選択肢追加
4.2.5 メソッド: _add_inline_math()
シグネチャ:

Copydef _add_inline_math(self, doc: Document, latex_str: str) -> None
説明: インライン数式を追加します。

画像サイズ: 幅1.5インチ（自動調整）

4.2.6 メソッド: _add_display_math()
シグネチャ:

Copydef _add_display_math(self, doc: Document, latex_str: str) -> None
説明: 独立した数式を中央揃えで追加します。

画像サイズ: 幅2.0インチ（自動調整）

4.2.7 メソッド: _add_choices()
シグネチャ:

Copydef _add_choices(self, doc: Document, choices: List[str]) -> None
説明: 選択肢を番号付きリストで追加します。

書式:

インデント: 1cm
番号形式: 1. 2. 3. ...
4.3 スタイル適用
タイトルスタイル:

フォント: title_font
サイズ: title_size
太字: title_bold
本文スタイル:

フォント: body_font
サイズ: body_size
行間: paragraph_spacing
選択肢スタイル:

フォント: choice_font
サイズ: choice_size
インデント: choice_indent
4.4 文書構造
文書
├── 大問1
│   ├── タイトル（見出し1）
│   ├── 問題文（本文）
│   ├── 数式（中央揃え画像）
│   └── 選択肢（番号付きリスト）
├── 大問2
│   └── ...
└── 大問N
5. main_converter.py
5.1 概要
すべてのモジュールを統合し、HTMLファイルをWord文書に変換するメインスクリプトです。

5.2 関数: convert_html_to_word()
シグネチャ:

Copydef convert_html_to_word(html_file: str, output_file: str = None) -> bool
説明: HTMLファイルをWord文書に変換します。

パラメータ:

html_file (str): 入力HTMLファイルのパス
output_file (str, optional): 出力Wordファイルのパス（省略時は自動生成）
戻り値: bool - 成功時True、失敗時False

使用例:

Copy# 基本的な使用
success = convert_html_to_word('problem.html')

# 出力ファイル名を指定
success = convert_html_to_word('problem.html', 'output.docx')

# エラーチェック
if success:
    print("変換成功")
else:
    print("変換失敗")
5.3 コマンドライン使用
基本形式:

Copypython src/main_converter.py <HTMLファイル> [出力ファイル]
例:

Copy# 自動的に output.docx を生成
python src/main_converter.py input.html

# 出力ファイル名を指定
python src/main_converter.py input.html result.docx

# 相対パス
python src/main_converter.py data/input/problem.html data/output/result.docx

# 絶対パス
python src/main_converter.py /Users/syuta/problem.html /Users/syuta/result.docx
5.4 エラーメッセージ
ファイルが見つからない:

FileNotFoundError: [Errno 2] No such file or directory: 'problem.html'
HTML解析エラー:

エラー: HTMLの解析に失敗しました
数式変換エラー:

数式変換エラー: x^2 + y^2
エラー内容: Invalid LaTeX syntax
Word保存エラー:

エラー: Word文書の保存に失敗しました
