# 数学問題作成システム

HTML形式の数学問題をWord文書に変換するシステムです。

## 特徴

- HTML → Word変換
- LaTeX数式対応
- 統一されたスタイル
- バッチ処理
- GUI対応

## インストール

```bash
git clone https://github.com/seyaytua/autoCreate.git
cd autoCreate
python3 -m venv venv
source venv/bin/activate
pip install PySide6 python-docx beautifulsoup4 lxml matplotlib pillow
使い方
Copy# GUIを起動
python run_gui.py

# コマンドラインから変換
python src/main_converter.py input.html output.docx
ライセンス
MIT License 
