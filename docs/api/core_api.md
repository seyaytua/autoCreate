# コアAPI リファレンス

## モジュールインポート

```python
from core import STYLE_CONFIG, TEMPLATES
from core import HTMLParser, MathConverter, WordGenerator
基本的な使用フロー
Copy# 1. 設定とコンバーターの初期化
from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

parser = HTMLParser()
math_converter = MathConverter(STYLE_CONFIG)
word_generator = WordGenerator(STYLE_CONFIG, math_converter)

# 2. HTMLの読み込みと解析
with open('problem.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

problems = parser.parse(html_content)

# 3. Word文書の生成
doc = word_generator.create_document(problems)

# 4. 保存
doc.save('output.docx')
クラスとメソッドの詳細
STYLE_CONFIG
型: Dict[str, Union[int, float, str, bool]]

説明: システム全体のスタイル設定を格納する辞書

キー一覧:

キー	型	デフォルト値	説明
math_dpi	int	300	数式画像の解像度
math_font_size	int	14	数式のフォントサイズ
math_color	str	'black'	数式の色
math_background	str	'transparent'	数式の背景色
title_font	str	'MS Gothic'	タイトルフォント
title_size	int	16	タイトルサイズ（pt）
title_bold	bool	True	タイトル太字
body_font	str	'MS Mincho'	本文フォント
body_size	int	11	本文サイズ（pt）
problem_spacing	float	1.5	問題間の行間
paragraph_spacing	float	1.15	段落の行間
page_margin	float	2.54	ページ余白（cm）
choice_font	str	'MS Mincho'	選択肢フォント
choice_size	int	11	選択肢サイズ（pt）
choice_indent	float	1.0	選択肢インデント（cm）
使用例:

Copy# 設定の取得
dpi = STYLE_CONFIG['math_dpi']

# 設定の変更
STYLE_CONFIG['math_dpi'] = 600

# カスタム設定の作成
custom_config = STYLE_CONFIG.copy()
custom_config['title_size'] = 18
custom_config['body_size'] = 12
TEMPLATES
型: Dict[str, Dict[str, Any]]

説明: 文書テンプレートの定義

テンプレート一覧:

standard: 標準問題集
exam: 定期試験
homework: 宿題プリント
テンプレート構造:

Copy{
    'name': str,              # テンプレート名
    'header': Optional[str],  # ヘッダーテキスト
    'footer': Optional[str],  # フッターテキスト
    'title_style': str,       # タイトルスタイル
    'numbering': bool,        # ページ番号表示
    # その他のカスタム設定
}
使用例:

Copy# テンプレートの取得
exam_template = TEMPLATES['exam']

# テンプレート名の一覧
template_names = list(TEMPLATES.keys())

# 新しいテンプレートの追加
TEMPLATES['custom'] = {
    'name': 'カスタム',
    'header': 'カスタムヘッダー',
    'footer': 'ページ {page}',
    'title_style': '見出し 1',
    'numbering': True,
}
エラーハンドリング
例外の種類
FileNotFoundError

発生条件: 指定されたファイルが存在しない
対処方法: ファイルパスを確認
ValueError

発生条件: 不正な設定値
対処方法: 設定値の型と範囲を確認
RuntimeError

発生条件: 数式変換エラー
対処方法: LaTeX構文を確認
エラーハンドリングの例
Copytry:
    # HTMLファイルを読み込み
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析と変換
    problems = parser.parse(html_content)
    doc = word_generator.create_document(problems)
    doc.save(output_file)
    
except FileNotFoundError as e:
    print(f"ファイルが見つかりません: {e}")
    
except ValueError as e:
    print(f"設定エラー: {e}")
    
except RuntimeError as e:
    print(f"変換エラー: {e}")
    
except Exception as e:
    print(f"予期しないエラー: {e}")
    import traceback
    traceback.print_exc()
パフォーマンス最適化
メモリ管理
Copy# 大量の問題を処理する場合は、バッチ処理を使用
def process_large_html(html_file, batch_size=10):
    parser = HTMLParser()
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    problems = parser.parse(html_content)
    
    # バッチごとに処理
    for i in range(0, len(problems), batch_size):
        batch = problems[i:i+batch_size]
        
        math_converter = MathConverter(STYLE_CONFIG)
        word_generator = WordGenerator(STYLE_CONFIG, math_converter)
        
        doc = word_generator.create_document(batch)
        doc.save(f'output_batch_{i//batch_size + 1}.docx')
        
        # メモリ解放
        del math_converter
        del word_generator
並列処理
Copyfrom concurrent.futures import ThreadPoolExecutor

def convert_single_file(html_file):
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    word_generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    problems = parser.parse(html_content)
    doc = word_generator.create_document(problems)
    
    output_file = html_file.replace('.html', '.docx')
    doc.save(output_file)
    
    return output_file

# 複数ファイルを並列処理
html_files = ['file1.html', 'file2.html', 'file3.html']

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(convert_single_file, html_files)
    
for result in results:
    print(f"完了: {result}")
デバッグとロギング
ロギングの設定
Copyimport logging

# ロガーの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('converter.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 使用例
logger.info("変換開始")
logger.debug(f"問題数: {len(problems)}")
logger.warning("数式変換に失敗しました")
logger.error("ファイルの保存に失敗しました")
デバッグ情報の出力
Copydef debug_problem_data(problems):
    """問題データの内容を詳細に出力"""
    for i, problem in enumerate(problems, 1):
        print(f"\n=== 問題 {i} ===")
        print(f"タイトル: {problem['title']}")
        print(f"テキスト要素数: {len(problem['text'])}")
        print(f"数式数: {len(problem['equations'])}")
        print(f"選択肢数: {len(problem['choices'])}")
        
        print("\nテキスト詳細:")
        for j, element in enumerate(problem['text']):
            print(f"  [{j}] {element['type']}: {element['content'][:50]}...")
        
        print("\n数式:")
        for j, eq in enumerate(problem['equations']):
            print(f"  [{j}] {eq}")
        
        print("\n選択肢:")
        for j, choice in enumerate(problem['choices']):
            print(f"  [{j+1}] {choice}")

# 使用
problems = parser.parse(html_content)
debug_problem_data(problems)
テストとバリデーション
設定のバリデーション
Copydef validate_config(config):
    """設定値の妥当性をチェック"""
    errors = []
    
    # DPIチェック
    if not isinstance(config['math_dpi'], int) or config['math_dpi'] < 72:
        errors.append("math_dpiは72以上の整数である必要があります")
    
    # フォントサイズチェック
    if not isinstance(config['math_font_size'], int) or config['math_font_size'] < 8:
        errors.append("math_font_sizeは8以上の整数である必要があります")
    
    # 余白チェック
    if not isinstance(config['page_margin'], (int, float)) or config['page_margin'] < 0:
        errors.append("page_marginは0以上の数値である必要があります")
    
    if errors:
        raise ValueError("\n".join(errors))
    
    return True

# 使用
try:
    validate_config(STYLE_CONFIG)
    print("設定は正常です")
except ValueError as e:
    print(f"設定エラー:\n{e}")
HTMLのバリデーション
Copydef validate_html_structure(html_content):
    """HTMLの構造をチェック"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    warnings = []
    
    # 問題ブロックの存在チェック
    problems = soup.find_all('div', class_='problem')
    if not problems:
        warnings.append("警告: class='problem'のdivが見つかりません")
    
    # 各問題の構造チェック
    for i, problem in enumerate(problems, 1):
        # タイトルチェック
        if not problem.find(['h1', 'h2', 'h3']):
            warnings.append(f"問題{i}: タイトルが見つかりません")
        
        # 問題文チェック
        if not problem.find('p'):
            warnings.append(f"問題{i}: 問題文が見つかりません")
    
    return warnings

# 使用
warnings = validate_html_structure(html_content)
for warning in warnings:
    print(warning)
数式のテスト
Copydef test_latex_conversion(latex_strings):
    """複数のLaTeX数式の変換をテスト"""
    from core import STYLE_CONFIG, MathConverter
    
    converter = MathConverter(STYLE_CONFIG)
    results = {}
    
    for latex in latex_strings:
        try:
            success = converter.test_conversion(latex)
            results[latex] = 'OK' if success else 'FAIL'
        except Exception as e:
            results[latex] = f'ERROR: {str(e)}'
    
    return results

# 使用
test_formulas = [
    'x^2 + y^2 = r^2',
    r'\frac{a}{b}',
    r'\int_{0}^{\infty} e^{-x} dx',
    r'\sum_{i=1}^{n} i = \frac{n(n+1)}{2}',
]

results = test_latex_conversion(test_formulas)
for formula, result in results.items():
    print(f"{formula}: {result}")
