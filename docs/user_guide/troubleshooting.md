# トラブルシューティングガイド

## 目次

1. [インストール関連](#インストール関連)
2. [変換エラー](#変換エラー)
3. [数式関連](#数式関連)
4. [フォント・スタイル関連](#フォントスタイル関連)
5. [パフォーマンス関連](#パフォーマンス関連)
6. [FAQ](#faq)

## インストール関連

### 問題: `python3: command not found`

**症状**:
```bash
zsh: command not found: python3
原因: Pythonがインストールされていない

解決策:

Mac:

Copy# Homebrewをインストール（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Pythonをインストール
brew install python3

# 確認
python3 --version
Ubuntu/Debian:

Copysudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# 確認
python3 --version
Windows:

Python公式サイトからインストーラーをダウンロード
インストーラーを実行
"Add Python to PATH"にチェックを入れる
"Install Now"をクリック
問題: pip install が失敗する
症状:

ERROR: Could not install packages due to an OSError
原因1: 権限不足

解決策:

Copy# --userオプションを使用
pip install --user PySide6 python-docx beautifulsoup4 lxml matplotlib pillow
原因2: pipが古い

解決策:

Copy# pipをアップグレード
pip install --upgrade pip

# 再度インストール
pip install PySide6 python-docx beautifulsoup4 lxml matplotlib pillow
原因3: ネットワークエラー

解決策:

Copy# タイムアウトを延長
pip install --timeout=120 PySide6 python-docx beautifulsoup4 lxml matplotlib pillow

# または、ミラーサイトを使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PySide6
問題: 仮想環境が作成できない
症状:

Error: Command '['/path/to/venv/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1
解決策:

Copy# venvモジュールをインストール（Ubuntu/Debian）
sudo apt-get install python3-venv

# 仮想環境を再作成
rm -rf venv
python3 -m venv venv
問題: matplotlibのインストールが失敗する
症状:

ERROR: Failed building wheel for matplotlib
解決策 (Mac):

Copy# Xcode Command Line Toolsをインストール
xcode-select --install

# 必要なライブラリをインストール
brew install freetype pkg-config

# 再度インストール
pip install matplotlib
解決策 (Ubuntu/Debian):

Copy# 開発ツールをインストール
sudo apt-get install python3-dev build-essential libfreetype6-dev

# 再度インストール
pip install matplotlib
変換エラー
問題: FileNotFoundError
症状:

FileNotFoundError: [Errno 2] No such file or directory: 'problem.html'
原因: ファイルパスが間違っている

解決策:

Copy# ファイルの存在を確認
ls data/input/problem.html

# 絶対パスを使用
python src/main_converter.py /Users/syuta/App_autoCreate/data/input/problem.html

# カレントディレクトリを確認
pwd

# 正しいディレクトリに移動
cd ~/App_autoCreate
問題: UnicodeDecodeError
症状:

UnicodeDecodeError: 'utf-8' codec can't decode byte...
原因: ファイルのエンコーディングがUTF-8ではない

解決策:

Copy# ファイルのエンコーディングを確認
file -I data/input/problem.html

# UTF-8に変換（Mac/Linux）
iconv -f SHIFT-JIS -t UTF-8 problem.html > problem_utf8.html

# または、エディタで開いて「UTF-8で保存」
問題: HTMLの解析に失敗
症状:

HTMLを解析中...
  0個の問題を検出
原因: HTML構造が不正または認識されない

解決策:

1. HTML構造を確認:

Copy<!-- 正しい構造 -->
<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">問題文</p>
</div>

<!-- または簡易構造 -->
<h2>大問1</h2>
<p>問題文</p>
2. デバッグ出力を追加:

Copyfrom core.html_parser import HTMLParser
from bs4 import BeautifulSoup

with open('data/input/problem.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
print("問題ブロック:", soup.find_all('div', class_='problem'))
print("h2タグ:", soup.find_all('h2'))
print("pタグ:", soup.find_all('p'))
問題: Word文書の保存に失敗
症状:

PermissionError: [Errno 13] Permission denied: 'output.docx'
原因1: ファイルが開かれている

解決策: Wordファイルを閉じてから再実行

原因2: 書き込み権限がない

解決策:

Copy# ディレクトリの権限を確認
ls -la data/output/

# 権限を変更
chmod 755 data/output/

# または、別のディレクトリに保存
python src/main_converter.py input.html ~/Desktop/output.docx
数式関連
問題: 数式が画像として表示されない
症状: 数式の部分が空白または [数式エラー] と表示される

原因1: LaTeX構文エラー

解決策:

Copy<!-- 間違い -->
<div class="math">$$frac{a}{b}$$</div>

<!-- 正しい -->
<div class="math">$$\frac{a}{b}$$</div>
バックスラッシュのエスケープに注意:

Copy<!-- HTMLファイル内では -->

$$\frac{a}{b}$$

<!-- Pythonコード内では -->
latex = r'\frac{a}{b}'  # raw文字列を使用
原因2: 数式が複雑すぎる

解決策:

Copy# タイムアウトを確認
import matplotlib
matplotlib.rcParams['text.usetex'] = False  # LaTeXエンジンを使用しない
問題: 数式の画像が粗い
症状: 数式がぼやけて見える

原因: DPI設定が低い

解決策:

Copy# src/core/style_config.py を編集
STYLE_CONFIG['math_dpi'] = 600  # デフォルト: 300

# または、カスタム設定を作成
from core import STYLE_CONFIG
custom_config = STYLE_CONFIG.copy()
custom_config['math_dpi'] = 600
問題: 特定の数式記号が表示されない
症状: ギリシャ文字や特殊記号が表示されない

原因: フォントの問題

解決策:

Copy# matplotlibのフォント設定を確認
import matplotlib.pyplot as plt
print(plt.rcParams['font.family'])

# Computer Modernフォントを使用
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
問題: 行列が正しく表示されない
症状: 行列の要素が崩れる

原因: 構文エラー

解決策:

Copy<!-- 正しい行列の書き方 -->
<div class="math">

$$\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}$$
</div>

<!-- 行列式 -->
<div class="math">

$$\begin{vmatrix}
a & b \\
c & d
\end{vmatrix}$$
</div>
フォント・スタイル関連
問題: 日本語フォントが表示されない
症状: 日本語が□や?で表示される

原因: 指定したフォントがシステムにない

解決策:

Mac:

Copy# src/core/style_config.py
STYLE_CONFIG['title_font'] = 'Hiragino Sans'
STYLE_CONFIG['body_font'] = 'Hiragino Mincho ProN'
Windows:

CopySTYLE_CONFIG['title_font'] = 'MS Gothic'
STYLE_CONFIG['body_font'] = 'MS Mincho'
Linux:

Copy# IPAフォントをインストール
sudo apt-get install fonts-ipafont fonts-ipaexfont

# Notoフォントをインストール
sudo apt-get install fonts-noto-cjk
CopySTYLE_CONFIG['title_font'] = 'IPAGothic'
STYLE_CONFIG['body_font'] = 'IPAMincho'
問題: フォントサイズが反映されない
症状: 設定を変更してもフォントサイズが変わらない

原因: python-docxのバグまたは設定の適用タイミング

解決策:

Copy# 設定を変更後、Pythonを再起動
# または、明示的にスタイルを適用

from docx.shared import Pt

# 段落のスタイルを直接設定
for para in doc.paragraphs:
    for run in para.runs:
        run.font.size = Pt(12)
問題: レイアウトが崩れる
症状: 余白や行間が意図した通りにならない

原因: 設定値が不適切

解決策:

Copy# 設定を確認
print(STYLE_CONFIG['page_margin'])  # cm単位
print(STYLE_CONFIG['paragraph_spacing'])  # 倍率

# 適切な値に調整
STYLE_CONFIG['page_margin'] = 2.5  # 2.5cm
STYLE_CONFIG['paragraph_spacing'] = 1.15  # 1.15倍
パフォーマンス関連
問題: 変換が遅い
症状: 1つの問題の変換に数十秒かかる

原因1: 数式が多いまたは複雑

解決策:

Copy# 並列処理を使用
from concurrent.futures import ThreadPoolExecutor

def convert_problem(problem):
    # 変換処理
    pass

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(convert_problem, problems)
原因2: DPI設定が高すぎる

解決策:

Copy# DPIを下げる
STYLE_CONFIG['math_dpi'] = 150  # デフォルト: 300
問題: メモリ不足
症状:

MemoryError: Unable to allocate...
原因: 大量の問題を一度に処理

解決策:

Copy# バッチ処理を使用
def process_in_batches(problems, batch_size=10):
    for i in range(0, len(problems), batch_size):
        batch = problems[i:i+batch_size]
        
        # バッチごとに処理
        doc = generator.create_document(batch)
        doc.save(f'output_batch_{i//batch_size + 1}.docx')
        
        # メモリ解放
        del doc
問題: ファイルサイズが大きすぎる
症状: 生成されたdocxファイルが数十MBになる

原因: 高解像度の画像

解決策:

Copy# DPIを下げる
STYLE_CONFIG['math_dpi'] = 150

# または、画像を圧縮
from PIL import Image

def compress_image(img_stream):
    img = Image.open(img_stream)
    # 圧縮処理
    return compressed_stream
FAQ
Q1: 複数の問題を1つのファイルにまとめるには？
A: HTMLファイル内に複数の <div class="problem"> を記述してください：

Copy<div class="problem">
    <h2>大問1</h2>
    <!-- 問題1 -->
</div>

<div class="problem">
    <h2>大問2</h2>
    <!-- 問題2 -->
</div>
Q2: 問題ごとに改ページするには？
A: カスタムジェネレーターを作成：

Copyclass PageBreakGenerator(WordGenerator):
    def create_document(self, problems):
        doc = Document()
        self._apply_global_style(doc)
        
        for i, problem in enumerate(problems):
            self.problem_counter = i + 1
            self._add_problem(doc, problem)
            
            if i < len(problems) - 1:
                doc.add_page_break()  # 改ページ
        
        return doc
Q3: ヘッダーやフッターを追加するには？
A: 文書生成後に追加：

Copyfrom docx.shared import Pt

doc = generator.create_document(problems)

# ヘッダー
section = doc.sections[0]
header = section.header
header_para = header.paragraphs[0]
header_para.text = "数学テスト"
header_para.style.font.size = Pt(10)

# フッター
footer = section.footer
footer_para = footer.paragraphs[0]
footer_para.text = "ページ"
footer_para.style.font.size = Pt(10)

doc.save('output.docx')
Q4: 選択肢の番号形式を変更するには？
A: _add_choices メソッドをオーバーライド：

Copyclass CustomGenerator(WordGenerator):
    def _add_choices(self, doc, choices):
        for i, choice in enumerate(choices):
            # (A), (B), (C)形式
            label = chr(65 + i)  # A, B, C...
            para = doc.add_paragraph(f'({label}) {choice}')
            # スタイル適用
            self._apply_body_style(para)
Q5: LaTeX以外の数式記法に対応できますか？
A: 現在はLaTeXのみ対応しています。他の記法を使用する場合は、LaTeXに変換する必要があります：

Copydef mathml_to_latex(mathml_str):
    # MathMLからLaTeXへの変換
    # 外部ライブラリ（例: latexml）を使用
    pass
Q6: 画像形式をPNG以外にできますか？
A: math_converter.py を修正：

Copy# SVGで保存
buf = io.BytesIO()
plt.savefig(buf, format='svg', ...)

# JPEGで保存（非推奨：背景透過不可）
buf = io.BytesIO()
plt.savefig(buf, format='jpeg', ...)
Q7: テンプレートを切り替えるには？
A: 現在Phase 1では基本機能のみ実装されています。Phase 3でテンプレート機能が追加される予定です。

Q8: エラーログを出力するには？
A: loggingモジュールを使用：

Copyimport logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('converter.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("変換開始")
logger.error("エラー発生")
Q9: 変換の進捗を表示するには？
A: tqdmライブラリを使用：

Copypip install tqdm
Copyfrom tqdm import tqdm

for problem in tqdm(problems, desc="変換中"):
    # 処理
    pass
Q10: コマンドラインオプションを追加するには？
A: argparseを使用：

Copyimport argparse

parser = argparse.ArgumentParser(description='HTML to Word converter')
parser.add_argument('input', help='入力HTMLファイル')
parser.add_argument('output', help='出力Wordファイル')
parser.add_argument('--dpi', type=int, default=300, help='画像解像度')
parser.add_argument('--verbose', action='store_true', help='詳細表示')

args = parser.parse_args()

if args.verbose:
    print(f"DPI: {args.dpi}")
サポート
ドキュメント
インストールガイド
クイックスタート
使用例集
APIリファレンス
コミュニティ
GitHub Issues: [リポジトリURL/issues]
ディスカッション: [リポジトリURL/discussions]
バグ報告
バグを発見した場合は、以下の情報を含めて報告してください：

エラーメッセージ（全文）
使用したHTMLファイル（サンプル）
実行したコマンド
環境情報（OS、Pythonバージョン）
Copy# 環境情報の取得
python --version
pip list
uname -a  # Mac/Linux
systeminfo  # Windows
