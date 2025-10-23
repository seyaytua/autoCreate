# 数学問題作成システム

HTML形式の数学問題をWord文書に変換するシステムです。

## ダウンロード

### 実行可能ファイル（インストール不要）

最新リリースから実行可能ファイルをダウンロードできます：

- **Mac**: [MathConverter-Mac.dmg](https://github.com/seyaytua/autoCreate/releases/latest)
- **Windows**: [MathConverter-Windows.zip](https://github.com/seyaytua/autoCreate/releases/latest)

### ソースコードから実行

```bash
git clone https://github.com/seyaytua/autoCreate.git
cd autoCreate
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/unified_gui.py
特徴
HTML → Word変換: HTML形式の数学問題を美しいWord文書に変換
LaTeX数式対応: LaTeX記法の数式を高品質な画像として埋め込み
テンプレート機能: 標準問題集、定期試験、宿題プリント
クリップボード対応: HTMLをコピーするだけで変換可能
統一されたスタイル: 複数の問題でも一貫したフォーマット
シンプルなUI: 使いやすいグラフィカルインターフェース
使い方
GUIから使用
Copypython src/unified_gui.py
入力方法を選択

ファイルから読み込み
クリップボードから読み込み
テンプレートを選択

標準問題集
定期試験
宿題プリント
Word文書に変換

コマンドラインから使用
Copy# 基本的な変換
python src/main_converter.py input.html output.docx

# テンプレート付き変換
python src/template_converter.py input.html output.docx exam

# クリップボードから変換
python src/clipboard_converter.py
HTML形式
Copy<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">次の方程式を解きなさい。</p>
    <div class="math">$$x^2 + 5x + 6 = 0$$</div>
    <ol class="choices">
        <li>x = -2, -3</li>
        <li>x = 2, 3</li>
    </ol>
</div>
開発
ローカルビルド
Copy./build_local.sh
リリース作成
Copy# タグを作成してプッシュ
git tag v1.0.0
git push origin v1.0.0
GitHub Actionsが自動的に実行可能ファイルをビルドし、リリースを作成します。

ライセンス
MIT License

作者
seyaytua
