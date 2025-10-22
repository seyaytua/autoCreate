# スタイル設定ガイド

## 1. スタイル設定の概要

スタイル設定は `src/core/style_config.py` で一元管理されています。このファイルを編集することで、生成される文書の見た目を自由にカスタマイズできます。

## 2. 基本設定

### 2.1 数式画像設定

**math_dpi**（画像解像度）
- 用途別推奨値:
  - 印刷用: 600
  - 標準: 300
  - Web用: 150
- 値が大きいほど高画質だが、ファイルサイズも増加

**math_font_size**（数式フォントサイズ）
- 推奨値: 12〜16
- 標準: 14
- 問題文のフォントサイズとバランスを取る

**math_color**（数式の色）
- 基本色: 'black', 'blue', 'red', 'green'
- RGB指定も可能: (0.0, 0.0, 0.0)

**math_background**（背景色）
- 推奨: 'transparent'（透過）
- 白背景: 'white'

### 2.2 テキストスタイル

**title_font**（タイトルフォント）
- Mac: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN'
- Windows: 'MS Gothic', 'Meiryo'
- 英語: 'Arial', 'Helvetica'

**title_size**（タイトルサイズ）
- 推奨値: 14〜18pt
- 標準: 16pt

**title_bold**（タイトル太字）
- True: 太字
- False: 標準

**body_font**（本文フォント）
- Mac: 'Hiragino Mincho ProN'
- Windows: 'MS Mincho'
- 英語: 'Times New Roman'

**body_size**（本文サイズ）
- 推奨値: 10〜12pt
- 標準: 11pt

### 2.3 レイアウト設定

**problem_spacing**（大問間の行間）
- 推奨値: 1.5〜2.0
- 標準: 1.5

**paragraph_spacing**（段落の行間）
- 推奨値: 1.0〜1.5
- 標準: 1.15

**page_margin**（ページ余白）
- 単位: cm
- 推奨値: 2.0〜3.0
- 標準: 2.54（1インチ）

### 2.4 選択肢スタイル

**choice_font**（選択肢フォント）
- 通常は本文と同じフォントを使用

**choice_size**（選択肢サイズ）
- 通常は本文と同じサイズを使用

**choice_indent**（選択肢インデント）
- 単位: cm
- 推奨値: 0.5〜1.5
- 標準: 1.0

## 3. 用途別設定例

### 3.1 印刷用高品質設定

```python
STYLE_CONFIG = {
    'math_dpi': 600,              # 高解像度
    'math_font_size': 14,
    'math_color': 'black',
    'math_background': 'transparent',
    
    'title_font': 'MS Gothic',
    'title_size': 16,
    'title_bold': True,
    'body_font': 'MS Mincho',
    'body_size': 11,
    
    'problem_spacing': 2.0,       # 広めの間隔
    'paragraph_spacing': 1.5,
    'page_margin': 2.5,           # 広めの余白
    
    'choice_font': 'MS Mincho',
    'choice_size': 11,
    'choice_indent': 1.0,
}
3.2 Web表示用設定
CopySTYLE_CONFIG = {
    'math_dpi': 150,              # 標準解像度
    'math_font_size': 14,
    'math_color': 'black',
    'math_background': 'transparent',
    
    'title_font': 'Arial',
    'title_size': 16,
    'title_bold': True,
    'body_font': 'Times New Roman',
    'body_size': 12,
    
    'problem_spacing': 1.5,
    'paragraph_spacing': 1.15,
    'page_margin': 2.0,
    
    'choice_font': 'Times New Roman',
    'choice_size': 12,
    'choice_indent': 1.0,
}
3.3 コンパクト設定
CopySTYLE_CONFIG = {
    'math_dpi': 300,
    'math_font_size': 12,         # 小さめ
    'math_color': 'black',
    'math_background': 'transparent',
    
    'title_font': 'MS Gothic',
    'title_size': 14,             # 小さめ
    'title_bold': True,
    'body_font': 'MS Mincho',
    'body_size': 10,              # 小さめ
    
    'problem_spacing': 1.0,       # 狭め
    'paragraph_spacing': 1.0,     # 狭め
    'page_margin': 1.5,           # 狭め
    
    'choice_font': 'MS Mincho',
    'choice_size': 10,            # 小さめ
    'choice_indent': 0.5,         # 狭め
}
4. フォント設定の注意点
4.1 日本語フォント
Macで利用可能な日本語フォント:

ゴシック体: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN'
明朝体: 'Hiragino Mincho ProN'
Windowsで利用可能な日本語フォント:

ゴシック体: 'MS Gothic', 'Meiryo', 'Yu Gothic'
明朝体: 'MS Mincho', 'Yu Mincho'
4.2 クロスプラットフォーム対応
環境によってフォントを切り替える例:

Copyimport platform

if platform.system() == 'Darwin':  # Mac
    STYLE_CONFIG['title_font'] = 'Hiragino Sans'
    STYLE_CONFIG['body_font'] = 'Hiragino Mincho ProN'
elif platform.system() == 'Windows':
    STYLE_CONFIG['title_font'] = 'MS Gothic'
    STYLE_CONFIG['body_font'] = 'MS Mincho'
else:  # Linux
    STYLE_CONFIG['title_font'] = 'DejaVu Sans'
    STYLE_CONFIG['body_font'] = 'DejaVu Serif'
5. テンプレート設定
5.1 標準テンプレート
Copy'standard': {
    'name': '標準問題集',
    'header': None,                    # ヘッダーなし
    'footer': 'ページ {page}',         # ページ番号のみ
    'title_style': '見出し 1',
    'numbering': True,
}
5.2 試験テンプレート
Copy'exam': {
    'name': '定期試験',
    'header': '{school_name} 数学テスト',  # 学校名を含む
    'footer': '氏名:__________ 得点:____/100',
    'title_style': '見出し 2',
    'time_limit': True,
}
5.3 宿題テンプレート
Copy'homework': {
    'name': '宿題プリント',
    'header': '提出日: {date}',
    'footer': 'クラス:____ 番号:____ 氏名:__________',
    'answer_space': True,              # 解答欄を追加
}
5.4 カスタムテンプレートの追加
新しいテンプレートを追加する例:

CopyTEMPLATES['custom'] = {
    'name': 'カスタムテンプレート',
    'header': '数学演習問題',
    'footer': '©2025 Your School',
    'title_style': '見出し 1',
    'numbering': True,
    'show_answers': False,             # 解答を表示しない
    'color_theme': 'blue',             # カラーテーマ
}
6. 色の設定
6.1 基本色
Copy# 文字列で指定
'math_color': 'black'
'math_color': 'blue'
'math_color': 'red'
6.2 RGB指定
Copy# タプルで指定（0.0〜1.0）
'math_color': (0.0, 0.0, 0.0)      # 黒
'math_color': (0.0, 0.0, 1.0)      # 青
'math_color': (1.0, 0.0, 0.0)      # 赤
'math_color': (0.5, 0.5, 0.5)      # グレー
7. 設定の適用方法
7.1 設定ファイルを直接編集
Copy# エディタで開く
open src/core/style_config.py

# または
vim src/core/style_config.py
7.2 プログラムから設定を変更
Copyfrom core.style_config import STYLE_CONFIG

# 設定を変更
STYLE_CONFIG['math_dpi'] = 600
STYLE_CONFIG['title_size'] = 18

# コンバーターを初期化
converter = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, converter)
7.3 複数の設定を使い分ける
Copy# 設定のコピーを作成
print_config = STYLE_CONFIG.copy()
print_config['math_dpi'] = 600

web_config = STYLE_CONFIG.copy()
web_config['math_dpi'] = 150

# 用途に応じて使い分ける
print_converter = MathConverter(print_config)
web_converter = MathConverter(web_config)
8. トラブルシューティング
8.1 フォントが適用されない
原因: 指定したフォントがシステムにインストールされていない

解決策:

利用可能なフォントを確認
代替フォントを指定
フォールバックフォントを設定
8.2 数式画像が粗い
原因: DPI設定が低すぎる

解決策:

CopySTYLE_CONFIG['math_dpi'] = 600  # 高解像度に変更
8.3 ファイルサイズが大きすぎる
原因: DPI設定が高すぎる

解決策:

CopySTYLE_CONFIG['math_dpi'] = 150  # 解像度を下げる
8.4 レイアウトが崩れる
原因: 余白やインデントの設定が不適切

解決策:

Copy# 余白を調整
STYLE_CONFIG['page_margin'] = 2.5

# インデントを調整
STYLE_CONFIG['choice_indent'] = 1.0
