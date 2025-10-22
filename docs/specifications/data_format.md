
データフォーマット仕様書
1. HTML入力フォーマット
1.1 標準構造
完全な例:

Copy<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>数学問題</title>
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">大問1</h2>
        <p class="problem-text">次の方程式を解きなさい。</p>
        <div class="math">$$x^2 + 5x + 6 = 0$$</div>
        <p class="problem-text">ただし、\(x \neq 0\) とする。</p>
        <ol class="choices">
            <li>x = -2, -3</li>
            <li>x = 2, 3</li>
            <li>x = -1, -6</li>
            <li>x = 1, 6</li>
        </ol>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">大問2</h2>
        <!-- 次の問題 -->
    </div>
</body>
</html>
1.2 必須要素
問題ブロック:

Copy<div class="problem">
    <!-- 問題の内容 -->
</div>
タイトル:

Copy<h2 class="problem-title">大問1</h2>
<h1>, <h2>, <h3> のいずれか
class="problem-title" 推奨（なくても可）
問題文:

Copy<p class="problem-text">問題文をここに記述</p>
複数の <p> タグを使用可能
インライン数式を含めることが可能
独立数式:

Copy<div class="math">$$LaTeX数式$$</div>
$$...$$ で囲む
1行に1つの数式を推奨
選択肢:

Copy<ol class="choices">
    <li>選択肢1</li>
    <li>選択肢2</li>
    <li>選択肢3</li>
    <li>選択肢4</li>
</ol>
<ol> または <ul> を使用
class="choices" 推奨
1.3 数式記法
ディスプレイ数式（独立した数式）:

Copy<div class="math">$$x^2 + y^2 = r^2$$</div>
インライン数式（文中の数式）:

Copy<p>ただし、\(x \neq 0\) とする。</p>
複数行数式:

Copy<div class="math">

$$
\begin{align}
x + y &= 5 \\
2x - y &= 1
\end{align}

$$
</div>
1.4 簡易フォーマット
class属性を省略した簡易形式も対応しています：

Copy<h2>大問1</h2>
<p>次の方程式を解きなさい。</p>
<div>$$x^2 + 5x + 6 = 0$$</div>
<ol>
    <li>x = -2, -3</li>
    <li>x = 2, 3</li>
</ol>
2. 内部データ構造
2.1 問題データ構造
型定義:

CopyProblemData = {
    'title': str,                    # 問題タイトル
    'text': List[TextElement],       # 問題文
    'equations': List[str],          # 独立数式
    'choices': List[str],            # 選択肢
    'raw_html': str                  # 元のHTML
}

TextElement = {
    'type': Literal['text', 'math'], # 要素タイプ
    'content': str                   # 内容
}
具体例:

Copy{
    'title': '大問1',
    'text': [
        {
            'type': 'text',
            'content': '次の方程式を解きなさい。'
        },
        {
            'type': 'text',
            'content': 'ただし、'
        },
        {
            'type': 'math',
            'content': 'x \\neq 0'
        },
        {
            'type': 'text',
            'content': 'とする。'
        }
    ],
    'equations': [
        'x^2 + 5x + 6 = 0'
    ],
    'choices': [
        'x = -2, -3',
        'x = 2, 3',
        'x = -1, -6',
        'x = 1, 6'
    ],
    'raw_html': '<div class="problem">...</div>'
}
2.2 スタイル設定構造
型定義:

CopyStyleConfig = {
    # 数式画像設定
    'math_dpi': int,
    'math_font_size': int,
    'math_color': str,
    'math_background': str,
    
    # テキストスタイル
    'title_font': str,
    'title_size': int,
    'title_bold': bool,
    'body_font': str,
    'body_size': int,
    
    # レイアウト
    'problem_spacing': float,
    'paragraph_spacing': float,
    'page_margin': float,
    
    # 選択肢スタイル
    'choice_font': str,
    'choice_size': int,
    'choice_indent': float,
}
2.3 テンプレート構造
型定義:

CopyTemplate = {
    'name': str,                      # テンプレート名
    'header': Optional[str],          # ヘッダーテキスト
    'footer': Optional[str],          # フッターテキスト
    'title_style': str,               # タイトルスタイル
    'numbering': bool,                # ページ番号
    # その他のカスタム設定
}
3. Word出力フォーマット
3.1 文書構造
Word文書 (.docx)
├── セクション1
│   ├── ヘッダー（テンプレートによる）
│   ├── 本文
│   │   ├── 大問1
│   │   │   ├── 見出し（レベル1）
│   │   │   ├── 段落（問題文）
│   │   │   ├── 画像（数式）
│   │   │   └── 番号付きリスト（選択肢）
│   │   ├── 大問2
│   │   │   └── ...
│   │   └── 大問N
│   └── フッター（テンプレートによる）
3.2 スタイル設定
見出し1（大問タイトル）:

フォント: MS Gothic（設定による）
サイズ: 16pt（設定による）
太字: あり
配置: 左揃え
本文（問題文）:

フォント: MS Mincho（設定による）
サイズ: 11pt（設定による）
行間: 1.15（設定による）
配置: 両端揃え
数式画像:

配置: 中央揃え
幅: 2.0インチ（自動調整）
解像度: 300 DPI（設定による）
背景: 透過
選択肢:

フォント: MS Mincho（設定による）
サイズ: 11pt（設定による）
インデント: 1.0cm（設定による）
番号形式: 1. 2. 3. ...
3.3 ページ設定
余白:

上下左右: 2.54cm（設定による）
用紙サイズ:

A4（210mm × 297mm）
向き:

縦
4. LaTeX数式フォーマット
4.1 基本記法
上付き・下付き:

Copyx^2          # x²
x_i          # xᵢ
x^{2n}       # x²ⁿ
x_{i+1}      # xᵢ₊₁
分数:

Copy\frac{a}{b}                    # a/b
\frac{x^2 + 1}{x - 1}          # (x² + 1)/(x - 1)
根号:

Copy\sqrt{x}                       # √x
\sqrt[3]{x}                    # ³√x
\sqrt{x^2 + y^2}               # √(x² + y²)
括弧:

Copy(x + y)                        # 通常の括弧
\left( \frac{a}{b} \right)     # 自動サイズ調整
\{ x \in \mathbb{R} \}         # 波括弧
4.2 演算子
基本演算:

Copyx + y        # 加算
x - y        # 減算
x \times y   # 乗算（×）
x \cdot y    # 乗算（・）
x \div y     # 除算（÷）
比較演算:

Copyx = y        # 等号
x \neq y     # 不等号
x < y        # 小なり
x > y        # 大なり
x \leq y     # 以下
x \geq y     # 以上
4.3 関数
三角関数:

Copy\sin x
\cos x
\tan x
\sin^2 x     # sin²x
対数・指数:

Copy\log x
\ln x
e^x
\log_2 x     # log₂x
4.4 総和・積分
総和:

Copy\sum_{i=1}^{n} x_i
\sum_{i=1}^{\infty} \frac{1}{i^2}
積分:

Copy\int f(x) dx
\int_{0}^{1} x^2 dx
\int_{0}^{\infty} e^{-x} dx
二重積分:

Copy\iint f(x,y) dxdy
4.5 ギリシャ文字
小文字:

Copy\alpha \beta \gamma \delta \epsilon
\theta \lambda \mu \pi \sigma
大文字:

Copy\Gamma \Delta \Theta \Lambda \Pi \Sigma
4.6 行列
基本行列:

Copy\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
行列式:

Copy\begin{vmatrix}
a & b \\
c & d
\end{vmatrix}
4.7 複数行数式
連立方程式:

Copy\begin{align}
x + y &= 5 \\
2x - y &= 1
\end{align}
場合分け:

Copyf(x) = \begin{cases}
x^2 & (x \geq 0) \\
-x^2 & (x < 0)
\end{cases}
5. エラーフォーマット
5.1 ログフォーマット
標準出力:

変換開始: problem.html
HTMLを解析中...
  2個の問題を検出
Word文書を生成中...
完了: problem.docx
エラー出力:

エラー: HTMLの解析に失敗しました
Traceback (most recent call last):
  File "main_converter.py", line 25, in convert_html_to_word
    problems = parser.parse(html_content)
  ...
5.2 警告メッセージ
数式変換警告:

数式変換エラー: x^2 + y^2
エラー内容: Invalid LaTeX syntax
代替画像を使用します
HTML構造警告:

警告: class="problem" が見つかりません
h2タグで自動分割します
