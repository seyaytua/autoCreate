#!/bin/bash

echo "GitHubへのプッシュを開始します..."

# .gitignoreを作成
cat > .gitignore << 'GITIGNORE_EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 仮想環境
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# ログファイル
logs/
*.log

# 出力ファイル
data/output/*.docx
data/output/*.pdf

# 一時ファイル
*.tmp
*.bak
GITIGNORE_EOF

echo "✓ .gitignoreを作成しました"

# READMEを作成
cat > README.md << 'README_EOF'
# 数学問題作成システム

HTML形式の数学問題をWord文書に変換するシステムです。

## 特徴

- **HTML → Word変換**: HTML形式の数学問題を美しいWord文書に変換
- **LaTeX数式対応**: LaTeX記法の数式を高品質な画像として埋め込み
- **統一されたスタイル**: 複数の問題でも一貫したフォーマット
- **バッチ処理**: 複数ファイルの一括変換
- **GUI対応**: 使いやすいグラフィカルインターフェース

## システム要件

- Python 3.8以上
- macOS / Windows / Linux

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/seyaytua/autoCreate.git
cd autoCreate

# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate  # Mac/Linux
# または
venv\Scripts\activate  # Windows

# 依存パッケージをインストール
pip install --upgrade pip
pip install PySide6 python-docx beautifulsoup4 lxml matplotlib pillow
クイックスタート
1. コマンドラインから変換
Copy# 単一ファイルを変換
python src/main_converter.py data/input/sample_problem.html data/output/result.docx

# フォルダ内のすべてのファイルを変換
python src/batch/batch_converter.py data/input data/output

# 複数ファイルを1つの文書に統合
python src/batch/unified_converter.py data/input -o data/output/unified.docx
2. GUIから変換
Copypython run_gui.py
使用例
HTML形式の入力
Copy<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">次の方程式を解きなさい。</p>
    <div class="math">$$x^2 + 5x + 6 = 0$$</div>
    <ol class="choices">
        <li>x = -2, -3</li>
        <li>x = 2, 3</li>
    </ol>
</div>
数式記法
インライン数式: \(x^2 + y^2\) または $x^2 + y^2$
ディスプレイ数式: $$\frac{a}{b}$$
プロジェクト構成
App_autoCreate/
├── src/
│   ├── core/              # コアモジュール
│   │   ├── style_config.py    # スタイル設定
│   │   ├── html_parser.py     # HTML解析
│   │   ├── math_converter.py  # 数式変換
│   │   └── word_generator.py  # Word生成
│   ├── prompts/           # AIプロンプトテンプレート
│   ├── validators/        # HTML検証
│   ├── batch/             # バッチ処理
│   └── gui/               # GUIアプリケーション
├── data/
│   ├── input/             # 入力HTMLファイル
│   └── output/            # 出力Wordファイル
├── docs/                  # ドキュメント
├── logs/                  # ログファイル
└── run_gui.py            # GUIランチャー
機能
Phase 1: 基本変換システム
HTML解析
LaTeX数式の画像化
Word文書生成
統一スタイル適用
Phase 2: 統一感強化
プロンプトテンプレート
HTML検証機能
バッチ変換
複数問題の統合変換
Phase 3: GUI実装
ファイル選択
変換モード切替
リアルタイム検証
進捗表示
スタイルのカスタマイズ
src/core/style_config.pyを編集してスタイルをカスタマイズできます：

CopySTYLE_CONFIG = {
    'math_font_size': 11,        # 数式のフォントサイズ
    'inline_math_height': 12,    # インライン数式の高さ
    'title_size': 16,            # タイトルサイズ
    'body_size': 11,             # 本文サイズ
    # ...
}
トラブルシューティング
数式が表示されない
LaTeX構文を確認してください
バックスラッシュを正しくエスケープしてください
フォントが表示されない
システムにフォントがインストールされているか確認
style_config.pyでフォント名を変更
変換が遅い
DPI設定を下げる: math_dpi = 150
バッチ処理を使用
詳細はドキュメントを参照してください。

ライセンス
MIT License

作者
seyaytua

貢献
Issue、Pull Requestを歓迎します！ README_EOF

echo "✓ README.mdを作成しました"

Gitの初期化
echo "" echo "Gitを初期化中..." git init

echo "✓ Git初期化完了"

ファイルを追加
echo "" echo "ファイルを追加中..." git add .

echo "✓ ファイル追加完了"

最初のコミット
echo "" echo "コミット中..." git commit -m "Initial commit: 数学問題作成システム Phase 1-3

Phase 1: 基本変換システム（HTML→Word、数式画像化）
Phase 2: バッチ処理、HTML検証、統合変換
Phase 3: PySide6 GUI実装
インライン数式とディスプレイ数式のサポート
統一されたスタイル設定
詳細なドキュメント"
echo "✓ コミット完了"

リモートリポジトリを追加
echo "" echo "リモートリポジトリを追加中..." git remote add origin https://github.com/seyaytua/autoCreate.git

echo "✓ リモートリポジトリ追加完了"

ブランチ名をmainに変更
echo "" echo "ブランチ名をmainに変更中..." git branch -M main

echo "✓ ブランチ名変更完了"

GitHubにプッシュ
echo "" echo "GitHubにプッシュ中..." echo "注意: GitHubの認証が必要です" echo ""

git push -u origin main

if [ $? -eq 0 ]; then echo "" echo "" echo "✓ GitHubへのプッシュが完了しました！" echo "" echo "" echo "リポジトリURL:" echo " https://github.com/seyaytua/autoCreate" echo "" echo "次のステップ:" echo " 1. ブラウザでリポジトリを確認" echo " 2. README.mdを確認" echo " 3. 必要に応じてリポジトリの説明を追加" echo "" else echo "" echo "" echo "エラー: プッシュに失敗しました" echo "" echo "" echo "考えられる原因:" echo " 1. GitHubの認証が必要" echo " 2. リポジトリが存在しない" echo " 3. 権限がない" echo "" echo "解決方法:" echo " 1. GitHubで個人アクセストークンを作成" echo " 2. 以下のコマンドを実行:" echo " git push -u origin main" echo " 3. ユーザー名とトークンを入力" echo "" fi

