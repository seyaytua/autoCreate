# Phase 2: 統一感強化とプロンプトテンプレート

## 新機能

### 1. プロンプトテンプレート (`src/prompts/problem_templates.py`)

AI問題生成用の構造化プロンプトテンプレート：

```python
from prompts.problem_templates import generate_prompt

# 基本的な使用
prompt = generate_prompt(
    difficulty='medium',
    category='algebra',
    count=2
)
print(prompt)
難易度: easy, medium, hard
分野: algebra, geometry, calculus, statistics
2. HTMLバリデーター (src/validators/html_validator.py)
生成されたHTMLの構造を検証：

Copypython src/validators/html_validator.py data/input/sample_problem.html
検証内容:

必須要素の存在確認
クラス名の検証
数式記法の確認
構造の整合性チェック
3. バッチ変換 (src/batch/batch_converter.py)
複数ファイルの一括変換：

Copy# フォルダ内のすべてのHTMLを変換
python src/batch/batch_converter.py data/input data/output

# 特定のファイルを変換
python src/batch/batch_converter.py data/input/problem1.html data/output
4. 統合変換 (src/batch/unified_converter.py)
複数のHTMLを1つの文書に統合：

Copy# フォルダ内のすべてを統合
python src/batch/unified_converter.py data/input -o data/output/unified.docx

# 複数ファイルを指定して統合
python src/batch/unified_converter.py \
    data/input/problem1.html \
    data/input/problem2.html \
    -o data/output/combined.docx
使用例
例1: プロンプト生成
Copyfrom prompts.problem_templates import generate_prompt

# 中級の代数問題を2問生成
prompt = generate_prompt(
    difficulty='medium',
    category='algebra',
    count=2,
    topic='2次方程式',
    include_graph=False
)

# このプロンプトをAIに送信
例2: HTML検証
Copy# コマンドラインから
python src/validators/html_validator.py data/input/problem.html

# Pythonコードから
from validators.html_validator import HTMLValidator

validator = HTMLValidator()
is_valid, errors, warnings = validator.validate(html_content)

if not is_valid:
    print("エラー:", errors)
else:
    print("検証OK")
例3: バッチ変換
Copy# すべてのHTMLファイルを変換
python src/batch/batch_converter.py data/input data/output

# ログファイルが logs/ に生成される
例4: 統合変換
Copy# 複数の大問を1つの文書に
python src/batch/unified_converter.py \
    data/input/test_problem1.html \
    data/input/test_problem2.html \
    -o data/output/test_combined.docx
ディレクトリ構造
App_autoCreate/
├── src/
│   ├── prompts/              # 新規: プロンプトテンプレート
│   │   └── problem_templates.py
│   ├── validators/           # 新規: 検証モジュール
│   │   └── html_validator.py
│   ├── batch/                # 新規: バッチ処理
│   │   ├── batch_converter.py
│   │   └── unified_converter.py
│   └── core/                 # 既存: コアモジュール
│       ├── __init__.py
│       ├── style_config.py
│       ├── html_parser.py
│       ├── math_converter.py
│       └── word_generator.py
├── logs/                     # 新規: ログファイル
└── docs/
    └── phase2_README.md
次のステップ
Phase 3: GUI実装
Phase 4: フォルダ監視と自動化
Phase 5: AI統合
