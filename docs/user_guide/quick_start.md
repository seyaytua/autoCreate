
クイックスタートガイド
概要
このガイドでは、数学問題作成システムの基本的な使い方を5分で学べます。

前提条件
システムが正しくインストールされている
仮想環境が有効化されている
インストールがまだの場合は、インストールガイドを参照してください。

基本的な使い方
ステップ1: 仮想環境の有効化
Copycd ~/App_autoCreate
source venv/bin/activate  # Mac/Linux
# または
venv\Scripts\activate  # Windows
プロンプトに (venv) が表示されればOKです。

ステップ2: HTMLファイルの準備
方法1: サンプルファイルを使用

既にサンプルファイルが用意されています：

Copyls data/input/sample_problem.html
方法2: 自分でHTMLファイルを作成

data/input/my_problem.html を作成：

Copy<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>数学問題</title>
</head>
<body>
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
</body>
</html>
ステップ3: 変換の実行
基本的なコマンド:

Copypython src/main_converter.py data/input/sample_problem.html data/output/result.docx
出力例:

変換開始: data/input/sample_problem.html
HTMLを解析中...
  2個の問題を検出
Word文書を生成中...
完了: data/output/result.docx
ステップ4: 結果の確認
生成されたWord文書を開きます：

Copy# Mac
open data/output/result.docx

# Windows
start data/output/result.docx

# Linux
xdg-open data/output/result.docx
よく使うコマンド
出力ファイル名を省略
出力ファイル名を指定しない場合、入力ファイル名から自動生成されます：

Copypython src/main_converter.py data/input/sample_problem.html
# → data/input/sample_problem.docx が生成される
複数のファイルを変換
Copy# ループで複数ファイルを変換
for file in data/input/*.html; do
    python src/main_converter.py "$file"
done
相対パスで実行
Copy# srcディレクトリから実行
cd src
python main_converter.py ../data/input/sample_problem.html ../data/output/result.docx
HTMLの書き方の基本
最小限のHTML
Copy<div class="problem">
    <h2>大問1</h2>
    <p>問題文</p>
    <div>$$数式$$</div>
    <ol>
        <li>選択肢1</li>
        <li>選択肢2</li>
    </ol>
</div>
推奨されるHTML（class属性付き）
Copy<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">問題文</p>
    <div class="math">$$数式$$</div>
    <ol class="choices">
        <li>選択肢1</li>
        <li>選択肢2</li>
    </ol>
</div>
数式の書き方
インライン数式（文中）:

Copy<p>ただし、\(x \neq 0\) とする。</p>
ディスプレイ数式（独立）:

Copy<div class="math">$$x^2 + y^2 = r^2$$</div>
よく使う数式の例:

Copy<!-- 分数 -->
<div class="math">$$\frac{a}{b}$$</div>

<!-- 根号 -->
<div class="math">$$\sqrt{x^2 + y^2}$$</div>

<!-- 積分 -->
<div class="math">$$\int_{0}^{1} x^2 dx$$</div>

<!-- 総和 -->
<div class="math">$$\sum_{i=1}^{n} i$$</div>

<!-- 行列 -->
<div class="math">

$$\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}$$
</div>
スタイルのカスタマイズ
基本設定の変更
設定ファイルを開きます：

Copyopen src/core/style_config.py  # Mac
# または
vim src/core/style_config.py   # エディタで編集
よく変更する設定
数式の解像度を上げる（印刷用）:

CopySTYLE_CONFIG['math_dpi'] = 600  # デフォルト: 300
フォントサイズを変更:

CopySTYLE_CONFIG['title_size'] = 18  # デフォルト: 16
STYLE_CONFIG['body_size'] = 12   # デフォルト: 11
余白を調整:

CopySTYLE_CONFIG['page_margin'] = 3.0  # デフォルト: 2.54 (cm)
設定を変更したら、再度変換を実行してください。

Pythonスクリプトで使用
コマンドラインではなく、Pythonスクリプトから使用することもできます：

convert.py を作成:

Copyfrom core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

# 初期化
parser = HTMLParser()
math_converter = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, math_converter)

# HTMLを読み込み
with open('data/input/sample_problem.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 変換
problems = parser.parse(html_content)
doc = generator.create_document(problems)
doc.save('data/output/result.docx')

print("変換完了！")
実行:

Copypython convert.py
よくある質問
Q1: 数式が画像として表示されない
A: LaTeX構文を確認してください。特にバックスラッシュのエスケープに注意：

Copy<!-- 正しい -->
<div class="math">$$\frac{a}{b}$$</div>

<!-- 間違い -->
<div class="math">$$frac{a}{b}$$</div>
Q2: 日本語フォントが表示されない
A: src/core/style_config.py でフォント名を確認してください：

Copy# Mac
STYLE_CONFIG['title_font'] = 'Hiragino Sans'
STYLE_CONFIG['body_font'] = 'Hiragino Mincho ProN'

# Windows
STYLE_CONFIG['title_font'] = 'MS Gothic'
STYLE_CONFIG['body_font'] = 'MS Mincho'
Q3: 複数の大問を1つのファイルにまとめたい
A: HTMLファイル内に複数の <div class="problem"> を記述してください：

Copy<div class="problem">
    <h2>大問1</h2>
    <!-- 問題1の内容 -->
</div>

<div class="problem">
    <h2>大問2</h2>
    <!-- 問題2の内容 -->
</div>
Q4: 変換が遅い
A: 数式の数や複雑さによって時間がかかります。以下で改善できます：

DPI設定を下げる: STYLE_CONFIG['math_dpi'] = 150
不要な数式を削除する
バッチ処理を使用する（詳細は使用例参照）
Q5: エラーメッセージが表示される
A: エラーメッセージの内容を確認してください：

FileNotFoundError: ファイルパスを確認
数式変換エラー: LaTeX構文を確認
HTMLの解析に失敗: HTML構造を確認
詳細はトラブルシューティングを参照してください。

次のステップ
基本的な使い方を理解したら、以下のドキュメントを参照してください：

より詳しい使用例

使用例集
実践的なテクニック
カスタマイズ方法

スタイル設定ガイド
テンプレートの作成
API リファレンス

コアAPI
プログラムからの使用方法
トラブルシューティング

問題解決ガイド
FAQ
ヘルプ
問題が発生した場合：

トラブルシューティングを確認
エラーメッセージをコピーして検索
GitHub Issuesで質問
それでは、数学問題の作成を楽しんでください！
