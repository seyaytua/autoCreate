# インストールガイド

## システム要件

### 必須要件

**オペレーティングシステム**:
- macOS 10.14 以降
- Windows 10 以降
- Linux (Ubuntu 18.04 以降推奨)

**Python**:
- Python 3.8 以降
- pip (パッケージ管理ツール)

**ディスク容量**:
- 最小: 500MB
- 推奨: 1GB以上

**メモリ**:
- 最小: 4GB RAM
- 推奨: 8GB RAM以上

### 推奨環境

**フォント**:
- Mac: Hiragino Sans, Hiragino Mincho ProN
- Windows: MS Gothic, MS Mincho
- Linux: IPAフォント、Notoフォント

**その他**:
- Microsoft Word (生成されたdocxファイルを開くため)
- テキストエディタ (設定ファイル編集用)

## インストール手順

### ステップ1: リポジトリのクローン/ダウンロード

**Gitを使用する場合**:
```bash
cd ~/
git clone [リポジトリURL] App_autoCreate
cd App_autoCreate
ZIPファイルをダウンロードする場合:

ZIPファイルをダウンロード
解凍して App_autoCreate フォルダを作成
ターミナルでフォルダに移動
Copycd ~/App_autoCreate
ステップ2: 仮想環境の作成
macOS/Linux:

Copy# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate
Windows:

Copy# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
venv\Scripts\activate
仮想環境が有効化されると、プロンプトの先頭に (venv) が表示されます。

ステップ3: 依存パッケージのインストール
Copy# pipをアップグレード
pip install --upgrade pip

# 必要なパッケージをインストール
pip install PySide6 python-docx beautifulsoup4 lxml matplotlib pillow
インストールの確認:

Copypip list
以下のパッケージが表示されればOKです：

PySide6
python-docx
beautifulsoup4
lxml
matplotlib
pillow
ステップ4: ディレクトリ構造の確認
インストール後、以下のディレクトリ構造になっているか確認してください：

App_autoCreate/
├── venv/                    # 仮想環境
├── src/                     # ソースコード
│   ├── core/               # コアモジュール
│   │   ├── __init__.py
│   │   ├── style_config.py
│   │   ├── html_parser.py
│   │   ├── math_converter.py
│   │   └── word_generator.py
│   └── main_converter.py   # メインスクリプト
├── data/                    # データディレクトリ
│   ├── input/              # 入力HTMLファイル
│   └── output/             # 出力Wordファイル
├── docs/                    # ドキュメント
└── tests/                   # テストファイル
ステップ5: 動作確認
サンプルファイルで動作確認:

Copy# サンプルHTMLファイルが存在するか確認
ls data/input/sample_problem.html

# 変換を実行
python src/main_converter.py data/input/sample_problem.html data/output/test.docx

# 出力ファイルを確認
ls data/output/test.docx
正常に動作すれば、以下のようなメッセージが表示されます：

変換開始: data/input/sample_problem.html
HTMLを解析中...
  2個の問題を検出
Word文書を生成中...
完了: data/output/test.docx
トラブルシューティング
問題1: Python3が見つからない
エラーメッセージ:

zsh: command not found: python3
解決策:

Copy# Homebrewでインストール (Mac)
brew install python3

# apt-getでインストール (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3 python3-pip

# Windows: Python公式サイトからインストーラーをダウンロード
# https://www.python.org/downloads/
問題2: pipのインストールが失敗する
エラーメッセージ:

ERROR: Could not install packages due to an OSError
解決策:

Copy# 権限エラーの場合、--userオプションを使用
pip install --user PySide6 python-docx beautifulsoup4 lxml matplotlib pillow

# または、仮想環境を再作成
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install PySide6 python-docx beautifulsoup4 lxml matplotlib pillow
問題3: matplotlibのインストールが失敗する
エラーメッセージ:

ERROR: Failed building wheel for matplotlib
解決策 (Mac):

Copy# Xcode Command Line Toolsをインストール
xcode-select --install

# 再度インストール
pip install matplotlib
解決策 (Linux):

Copy# 開発ツールをインストール
sudo apt-get install python3-dev build-essential

# 再度インストール
pip install matplotlib
問題4: フォントが表示されない
症状: 生成されたWord文書でフォントが正しく表示されない

解決策:

Copy# style_config.pyを編集
open src/core/style_config.py

# または
vim src/core/style_config.py
使用可能なフォントに変更：

Copy# Mac
STYLE_CONFIG['title_font'] = 'Hiragino Sans'
STYLE_CONFIG['body_font'] = 'Hiragino Mincho ProN'

# Windows
STYLE_CONFIG['title_font'] = 'MS Gothic'
STYLE_CONFIG['body_font'] = 'MS Mincho'

# Linux
STYLE_CONFIG['title_font'] = 'Noto Sans CJK JP'
STYLE_CONFIG['body_font'] = 'Noto Serif CJK JP'
問題5: 仮想環境が有効化できない
エラーメッセージ (Mac/Linux):

-bash: venv/bin/activate: No such file or directory
解決策:

Copy# 仮想環境を再作成
python3 -m venv venv

# パスを確認
ls venv/bin/activate

# 有効化
source venv/bin/activate
エラーメッセージ (Windows):

venv\Scripts\activate : このシステムではスクリプトの実行が無効になっているため...
解決策:

Copy# PowerShellを管理者として実行
Set-ExecutionPolicy RemoteSigned

# 再度有効化を試行
venv\Scripts\activate
アンインストール
完全なアンインストール
Copy# 仮想環境を無効化
deactivate

# プロジェクトディレクトリを削除
cd ~
rm -rf App_autoCreate
仮想環境のみ削除
Copycd ~/App_autoCreate
deactivate
rm -rf venv
アップデート
パッケージのアップデート
Copy# 仮想環境を有効化
source venv/bin/activate  # Mac/Linux
# または
venv\Scripts\activate  # Windows

# すべてのパッケージをアップデート
pip install --upgrade PySide6 python-docx beautifulsoup4 lxml matplotlib pillow
プロジェクトファイルのアップデート
Gitを使用している場合:

Copycd ~/App_autoCreate
git pull origin main
手動アップデート:

新しいバージョンをダウンロード
src/ ディレクトリを上書き
設定ファイルは保持（必要に応じてマージ）
次のステップ
インストールが完了したら、以下のドキュメントを参照してください：

クイックスタート - 基本的な使い方
使用例 - 実践的な使用例
システムアーキテクチャ - システムの詳細
サポート
問題が解決しない場合：

トラブルシューティングを確認
GitHub Issuesで質問
ドキュメントのFAQを参照 
