
使用例集
目次
基本的な使用例
数式の使用例
複数問題の処理
カスタマイズ例
自動化の例
実践的なワークフロー
基本的な使用例
例1: シンプルな方程式問題
HTML (problem1.html):

Copy<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">大問1</h2>
        <p class="problem-text">次の方程式を解きなさい。</p>
        <div class="math">$$2x + 5 = 13$$</div>
        <ol class="choices">
            <li>x = 4</li>
            <li>x = 5</li>
            <li>x = 6</li>
            <li>x = 9</li>
        </ol>
    </div>
</body>
</html>
変換コマンド:

Copypython src/main_converter.py data/input/problem1.html data/output/problem1.docx
例2: 複数の段落を含む問題
HTML (problem2.html):

Copy<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">
        次の条件を満たす関数を求めなさい。
    </p>
    <p class="problem-text">
        条件1: \(f(0) = 1\)
    </p>
    <p class="problem-text">
        条件2: \(f'(x) = 2x\)
    </p>
    <div class="math">$$f(x) = ?$$</div>
    <ol class="choices">
        <li>\(f(x) = x^2 + 1\)</li>
        <li>\(f(x) = x^2 - 1\)</li>
        <li>\(f(x) = 2x + 1\)</li>
        <li>\(f(x) = x^2\)</li>
    </ol>
</div>
例3: 記述式問題（選択肢なし）
HTML (problem3.html):

Copy<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">
        次の定積分を計算しなさい。
    </p>
    <div class="math">$$\int_{0}^{2} (3x^2 + 2x + 1) dx$$</div>
</div>
数式の使用例
例4: 分数を含む問題
HTML:

Copy<div class="problem">
    <h2>大問1</h2>
    <p>次の式を簡単にしなさい。</p>
    <div class="math">

    $$\frac{x^2 - 4}{x - 2}$$
    </div>
    <ol>
        <li>\(x + 2\)</li>
        <li>\(x - 2\)</li>
        <li>\(x^2 + 2\)</li>
        <li>簡単にできない</li>
    </ol>
</div>
例5: 根号を含む問題
HTML:

Copy<div class="problem">
    <h2>大問1</h2>
    <p>次の式の値を求めなさい。</p>
    <div class="math">

    $$\sqrt{16} + \sqrt{25}$$
    </div>
    <ol>
        <li>7</li>
        <li>9</li>
        <li>11</li>
        <li>13</li>
    </ol>
</div>
例6: 積分を含む問題
HTML:

Copy<div class="problem">
    <h2>大問1</h2>
    <p>次の不定積分を求めなさい。</p>
    <div class="math">

    $$\int (3x^2 + 2x + 1) dx$$
    </div>
    <ol>
        <li>\(x^3 + x^2 + x + C\)</li>
        <li>\(3x^3 + 2x^2 + x + C\)</li>
        <li>\(x^3 + x^2 + C\)</li>
        <li>\(3x^2 + 2x + C\)</li>
    </ol>
</div>
例7: 総和記号を含む問題
HTML:

Copy<div class="problem">
    <h2>大問1</h2>
    <p>次の和を求めなさい。</p>
    <div class="math">

    $$\sum_{k=1}^{10} k$$
    </div>
    <ol>
        <li>45</li>
        <li>50</li>
        <li>55</li>
        <li>60</li>
    </ol>
</div>
例8: 行列を含む問題
HTML:

Copy<div class="problem">
    <h2>大問1</h2>
    <p>次の行列の行列式を求めなさい。</p>
    <div class="math">

    $$\begin{vmatrix}
    1 & 2 \\
    3 & 4
    \end{vmatrix}$$
    </div>
    <ol>
        <li>-2</li>
        <li>-1</li>
        <li>1</li>
        <li>2</li>
    </ol>
</div>
例9: 場合分けを含む問題
HTML:

Copy<div class="problem">
    <h2>大問1</h2>
    <p>次の関数の値を求めなさい。</p>
    <div class="math">

    $$f(x) = \begin{cases}
    x^2 & (x \geq 0) \\
    -x^2 & (x < 0)
    \end{cases}$$
    </div>
    <p>このとき、\(f(-2)\) の値は？</p>
    <ol>
        <li>-4</li>
        <li>-2</li>
        <li>2</li>
        <li>4</li>
    </ol>
</div>
複数問題の処理
例10: 複数の大問を1つのファイルに
HTML (exam.html):

Copy<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>数学テスト</title>
</head>
<body>
    <div class="problem">
        <h2 class="problem-title">大問1</h2>
        <p class="problem-text">次の方程式を解きなさい。</p>
        <div class="math">$$x^2 - 5x + 6 = 0$$</div>
        <ol class="choices">
            <li>x = 2, 3</li>
            <li>x = -2, -3</li>
            <li>x = 1, 6</li>
            <li>x = -1, -6</li>
        </ol>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">大問2</h2>
        <p class="problem-text">次の不等式を解きなさい。</p>
        <div class="math">$$2x + 3 < 11$$</div>
        <ol class="choices">
            <li>\(x < 4\)</li>
            <li>\(x < 5\)</li>
            <li>\(x > 4\)</li>
            <li>\(x > 5\)</li>
        </ol>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">大問3</h2>
        <p class="problem-text">次の関数の最大値を求めなさい。</p>
        <div class="math">$$f(x) = -x^2 + 4x + 1$$</div>
        <p class="problem-text">ただし、\(0 \leq x \leq 5\) とする。</p>
        <ol class="choices">
            <li>最大値 5 (x = 2 のとき)</li>
            <li>最大値 6 (x = 3 のとき)</li>
            <li>最大値 1 (x = 0 のとき)</li>
            <li>最大値 -4 (x = 5 のとき)</li>
        </ol>
    </div>
</body>
</html>
変換:

Copypython src/main_converter.py data/input/exam.html data/output/exam.docx
例11: 複数ファイルの一括変換
シェルスクリプト (convert_all.sh):

Copy#!/bin/bash

# 入力ディレクトリ
INPUT_DIR="data/input"
OUTPUT_DIR="data/output"

# 出力ディレクトリを作成
mkdir -p "$OUTPUT_DIR"

# すべてのHTMLファイルを変換
for html_file in "$INPUT_DIR"/*.html; do
    # ファイル名を取得（拡張子なし）
    filename=$(basename "$html_file" .html)
    
    # 変換実行
    echo "変換中: $filename"
    python src/main_converter.py "$html_file" "$OUTPUT_DIR/${filename}.docx"
    
    if [ $? -eq 0 ]; then
        echo "✓ 完了: ${filename}.docx"
    else
        echo "✗ エラー: $filename"
    fi
    echo ""
done

echo "すべての変換が完了しました"
実行:

Copychmod +x convert_all.sh
./convert_all.sh
例12: Pythonスクリプトでバッチ処理
batch_convert.py:

Copyimport os
from pathlib import Path
from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

def convert_all_files(input_dir, output_dir):
    """指定ディレクトリ内のすべてのHTMLファイルを変換"""
    
    # 初期化
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    # 出力ディレクトリを作成
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # HTMLファイルを取得
    html_files = list(Path(input_dir).glob('*.html'))
    total = len(html_files)
    
    print(f"変換開始: {total}個のファイル\n")
    
    success_count = 0
    for i, html_file in enumerate(html_files, 1):
        try:
            print(f"[{i}/{total}] 処理中: {html_file.name}")
            
            # HTMLを読み込み
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 変換
            problems = parser.parse(html_content)
            doc = generator.create_document(problems)
            
            # 保存
            output_file = Path(output_dir) / f"{html_file.stem}.docx"
            doc.save(str(output_file))
            
            print(f"  ✓ 完了: {output_file.name}\n")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ エラー: {str(e)}\n")
    
    print(f"完了: {success_count}/{total}個のファイルを変換しました")

if __name__ == '__main__':
    convert_all_files('data/input', 'data/output')
実行:

Copypython batch_convert.py
カスタマイズ例
例13: 印刷用高品質設定
custom_convert.py:

Copyfrom core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

# 印刷用設定
print_config = STYLE_CONFIG.copy()
print_config['math_dpi'] = 600          # 高解像度
print_config['math_font_size'] = 16     # 大きめのフォント
print_config['title_size'] = 18
print_config['body_size'] = 12
print_config['page_margin'] = 3.0       # 広めの余白

# 初期化
parser = HTMLParser()
math_converter = MathConverter(print_config)
generator = WordGenerator(print_config, math_converter)

# 変換
with open('data/input/problem.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

problems = parser.parse(html_content)
doc = generator.create_document(problems)
doc.save('data/output/print_quality.docx')

print("印刷用高品質文書を生成しました")
例14: Web表示用軽量設定
web_convert.py:

Copyfrom core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

# Web用設定
web_config = STYLE_CONFIG.copy()
web_config['math_dpi'] = 150            # 標準解像度
web_config['math_font_size'] = 14
web_config['page_margin'] = 2.0         # 標準余白

# 初期化と変換
parser = HTMLParser()
math_converter = MathConverter(web_config)
generator = WordGenerator(web_config, math_converter)

with open('data/input/problem.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

problems = parser.parse(html_content)
doc = generator.create_document(problems)
doc.save('data/output/web_version.docx')

print("Web用軽量文書を生成しました")
例15: カラー数式
color_convert.py:

Copyfrom core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

# 青色の数式
blue_config = STYLE_CONFIG.copy()
blue_config['math_color'] = 'blue'

parser = HTMLParser()
math_converter = MathConverter(blue_config)
generator = WordGenerator(blue_config, math_converter)

with open('data/input/problem.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

problems = parser.parse(html_content)
doc = generator.create_document(problems)
doc.save('data/output/blue_math.docx')

print("青色の数式で文書を生成しました")
自動化の例
例16: フォルダ監視による自動変換
watch_folder.py:

Copyimport time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

class HTMLFileHandler(FileSystemEventHandler):
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.parser = HTMLParser()
        self.math_converter = MathConverter(STYLE_CONFIG)
        self.generator = WordGenerator(STYLE_CONFIG, self.math_converter)
    
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.html'):
            return
        
        print(f"\n新しいファイル検出: {event.src_path}")
        time.sleep(0.5)  # ファイルの書き込み完了を待つ
        
        try:
            # 変換処理
            with open(event.src_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            problems = self.parser.parse(html_content)
            doc = self.generator.create_document(problems)
            
            # 出力ファイル名を生成
            input_file = Path(event.src_path)
            output_file = Path(self.output_dir) / f"{input_file.stem}.docx"
            
            doc.save(str(output_file))
            print(f"✓ 変換完了: {output_file}")
            
        except Exception as e:
            print(f"✗ エラー: {str(e)}")

def start_watching(input_dir, output_dir):
    """フォルダ監視を開始"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    event_handler = HTMLFileHandler(output_dir)
    observer = Observer()
    observer.schedule(event_handler, input_dir, recursive=False)
    observer.start()
    
    print(f"監視開始: {input_dir}")
    print("HTMLファイルを配置すると自動的に変換されます")
    print("終了するには Ctrl+C を押してください\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n監視を終了しました")
    
    observer.join()

if __name__ == '__main__':
    start_watching('data/input', 'data/output')
実行:

Copy# watchdogをインストール
pip install watchdog

# 監視開始
python watch_folder.py
例17: 定期実行（cron）
crontabに登録:

Copy# crontabを編集
crontab -e

# 毎日午前9時に変換を実行
0 9 * * * cd ~/App_autoCreate && source venv/bin/activate && python batch_convert.py

# 1時間ごとに変換を実行
0 * * * * cd ~/App_autoCreate && source venv/bin/activate && python batch_convert.py
実践的なワークフロー
例18: 週次テスト作成ワークフロー
workflow.sh:

Copy#!/bin/bash

# 設定
WEEK=$(date +%U)
DATE=$(date +%Y%m%d)
INPUT_DIR="data/input/week_${WEEK}"
OUTPUT_DIR="data/output/week_${WEEK}"

# ディレクトリを作成
mkdir -p "$INPUT_DIR"
mkdir -p "$OUTPUT_DIR"

echo "==================================="
echo "週次テスト作成 - 第${WEEK}週"
echo "==================================="
echo ""

# HTMLファイルを変換
python src/main_converter.py "${INPUT_DIR}/test.html" "${OUTPUT_DIR}/test_${DATE}.docx"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ テストを作成しました: test_${DATE}.docx"
    
    # ファイルを開く
    open "${OUTPUT_DIR}/test_${DATE}.docx"
else
    echo ""
    echo "✗ エラーが発生しました"
fi
例19: 難易度別問題集作成
create_problem_set.py:

Copyimport os
from pathlib import Path
from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

def create_problem_set_by_difficulty():
    """難易度別に問題集を作成"""
    
    difficulties = ['easy', 'medium', 'hard']
    
    for difficulty in difficulties:
        print(f"\n{'='*50}")
        print(f"{difficulty.upper()} レベルの問題集を作成中...")
        print(f"{'='*50}")
        
        # 入力ディレクトリ
        input_dir = Path(f'data/input/{difficulty}')
        if not input_dir.exists():
            print(f"警告: {input_dir} が存在しません")
            continue
        
        # 初期化
        parser = HTMLParser()
        math_converter = MathConverter(STYLE_CONFIG)
        generator = WordGenerator(STYLE_CONFIG, math_converter)
        
        # すべての問題を収集
        all_problems = []
        html_files = sorted(input_dir.glob('*.html'))
        
        for html_file in html_files:
            print(f"  読み込み: {html_file.name}")
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            problems = parser.parse(html_content)
            all_problems.extend(problems)
        
        if all_problems:
            # 文書生成
            doc = generator.create_document(all_problems)
            
            # 保存
            output_file = f'data/output/problem_set_{difficulty}.docx'
            doc.save(output_file)
            
            print(f"  ✓ 完了: {len(all_problems)}問を含む問題集を作成")
            print(f"  ファイル: {output_file}")
        else:
            print(f"  警告: 問題が見つかりませんでした")

if __name__ == '__main__':
    create_problem_set_by_difficulty()
ディレクトリ構造:

data/input/
├── easy/
│   ├── problem1.html
│   ├── problem2.html
│   └── problem3.html
├── medium/
│   ├── problem1.html
│   └── problem2.html
└── hard/
    └── problem1.html
実行:

Copypython create_problem_set.py
例20: レポート生成付き変換
convert_with_report.py:

Copyimport json
from datetime import datetime
from pathlib import Path
from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

def convert_with_report(input_file, output_file):
    """変換とレポート生成"""
    
    start_time = datetime.now()
    
    # 初期化
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    # HTMLを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析
    problems = parser.parse(html_content)
    
    # 統計情報を収集
    stats = {
        'input_file': str(input_file),
        'output_file': str(output_file),
        'timestamp': start_time.isoformat(),
        'problem_count': len(problems),
        'total_equations': sum(len(p['equations']) for p in problems),
        'total_choices': sum(len(p['choices']) for p in problems),
        'problems': []
    }
    
    for i, problem in enumerate(problems, 1):
        stats['problems'].append({
            'number': i,
            'title': problem['title'],
            'text_elements': len(problem['text']),
            'equations': len(problem['equations']),
            'choices': len(problem['choices'])
        })
    
    # 変換
    doc = generator.create_document(problems)
    doc.save(output_file)
    
    # 処理時間
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    stats['duration_seconds'] = duration
    
    # レポートを保存
    report_file = Path(output_file).with_suffix('.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    # コンソールに表示
    print(f"\n{'='*50}")
    print("変換レポート")
    print(f"{'='*50}")
    print(f"入力ファイル: {input_file}")
    print(f"出力ファイル: {output_file}")
    print(f"問題数: {stats['problem_count']}")
    print(f"総数式数: {stats['total_equations']}")
    print(f"総選択肢数: {stats['total_choices']}")
    print(f"処理時間: {duration:.2f}秒")
    print(f"レポート: {report_file}")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    convert_with_report(
        'data/input/sample_problem.html',
        'data/output/result.docx'
    )
これらの例を参考に、あなたのワークフローに合わせてカスタマイズしてください。

次のステップ
トラブルシューティング - 問題解決
APIリファレンス - より高度な使い方
スタイルガイド - カスタマイズ方法 
EO
