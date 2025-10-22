
WordGenerator API リファレンス
クラス概要
Copyfrom core.word_generator import WordGenerator
WordGenerator クラスは、構造化された問題データからWord文書を生成します。

クラス定義
Copyclass WordGenerator:
    def __init__(self, style_config: dict, math_converter: MathConverter)
    def create_document(self, problems: List[Dict[str, Any]]) -> Document
    def _apply_global_style(self, doc: Document) -> None
    def _add_problem(self, doc: Document, problem: Dict[str, Any]) -> None
    def _apply_title_style(self, paragraph) -> None
    def _apply_body_style(self, paragraph) -> None
    def _add_inline_math(self, doc: Document, latex_str: str) -> None
    def _add_display_math(self, doc: Document, latex_str: str) -> None
    def _add_choices(self, doc: Document, choices: List[str]) -> None
初期化
__init__(style_config: dict, math_converter: MathConverter)
Copygenerator = WordGenerator(style_config, math_converter)
説明: WordGeneratorのインスタンスを作成します。

パラメータ:

style_config (dict): スタイル設定辞書
math_converter (MathConverter): 数式変換オブジェクト
使用例:

Copyfrom core.style_config import STYLE_CONFIG
from core.math_converter import MathConverter
from core.word_generator import WordGenerator

# 初期化
math_converter = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, math_converter)
パブリックメソッド
create_document(problems: List[Dict[str, Any]])
Copydef create_document(self, problems: List[Dict[str, Any]]) -> Document
説明: 問題データのリストからWord文書を生成します。

パラメータ:

problems (List[Dict]): HTMLParserから取得した問題データのリスト
戻り値: Document - python-docxのDocumentオブジェクト

使用例:

Copyfrom core.html_parser import HTMLParser

# HTMLを解析
parser = HTMLParser()
problems = parser.parse(html_content)

# Word文書を生成
doc = generator.create_document(problems)

# 保存
doc.save('output.docx')
完全な例:

Copyfrom core.style_config import STYLE_CONFIG
from core.html_parser import HTMLParser
from core.math_converter import MathConverter
from core.word_generator import WordGenerator

# 初期化
parser = HTMLParser()
math_converter = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, math_converter)

# HTMLを読み込み
with open('problem.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 解析
problems = parser.parse(html_content)

# Word文書生成
doc = generator.create_document(problems)

# 保存
doc.save('output.docx')
print("Word文書を生成しました")
プライベートメソッド
_apply_global_style(doc: Document)
Copydef _apply_global_style(self, doc: Document) -> None
説明: 文書全体のスタイルを設定します。

設定内容:

ページ余白（上下左右）
デフォルトフォント
見出しスタイル
適用されるスタイル:

Copy# 余白設定
margin = Cm(style_config['page_margin'])
section.top_margin = margin
section.bottom_margin = margin
section.left_margin = margin
section.right_margin = margin

# 見出しスタイル
style.font.name = style_config['title_font']
style.font.size = Pt(style_config['title_size'])
style.font.bold = style_config['title_bold']
_add_problem(doc: Document, problem: Dict[str, Any])
Copydef _add_problem(self, doc: Document, problem: Dict[str, Any]) -> None
説明: 1つの問題を文書に追加します。

処理順序:

タイトル追加（見出し1）
問題文追加（テキストと数式を分離）
独立数式追加（中央揃え）
選択肢追加（番号付きリスト）
使用される問題データ:

Copyproblem = {
    'title': '大問1',
    'text': [
        {'type': 'text', 'content': '問題文'},
        {'type': 'math', 'content': 'x^2'},
    ],
    'equations': ['x^2 + y^2 = r^2'],
    'choices': ['選択肢1', '選択肢2'],
}
_apply_title_style(paragraph)
Copydef _apply_title_style(self, paragraph) -> None
説明: タイトル段落にスタイルを適用します。

適用されるスタイル:

フォント: title_font
サイズ: title_size
太字: title_bold
東アジア言語フォント設定
_apply_body_style(paragraph)
Copydef _apply_body_style(self, paragraph) -> None
説明: 本文段落にスタイルを適用します。

適用されるスタイル:

フォント: body_font
サイズ: body_size
行間: paragraph_spacing
東アジア言語フォント設定
_add_inline_math(doc: Document, latex_str: str)
Copydef _add_inline_math(self, doc: Document, latex_str: str) -> None
説明: インライン数式を追加します。

画像設定:

幅: 1.5インチ（自動調整）
配置: 左揃え
行間: paragraph_spacing
使用例:

Copy# 文中に数式を挿入
generator._add_inline_math(doc, 'x^2 + y^2')
_add_display_math(doc: Document, latex_str: str)
Copydef _add_display_math(self, doc: Document, latex_str: str) -> None
説明: 独立した数式を中央揃えで追加します。

画像設定:

幅: 2.0インチ（自動調整）
配置: 中央揃え
下部余白: 12pt
使用例:

Copy# 独立した数式を挿入
generator._add_display_math(doc, r'\int_{0}^{1} x^2 dx = \frac{1}{3}')
_add_choices(doc: Document, choices: List[str])
Copydef _add_choices(self, doc: Document, choices: List[str]) -> None
説明: 選択肢を番号付きリストで追加します。

書式:

番号形式: 1. 2. 3. ...
インデント: choice_indent
フォント: choice_font
サイズ: choice_size
使用例:

Copychoices = [
    'x = -2, -3',
    'x = 2, 3',
    'x = -1, -6',
]
generator._add_choices(doc, choices)
実践的な使用例
基本的な文書生成
Copyfrom core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

# 初期化
parser = HTMLParser()
math_converter = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, math_converter)

# HTML解析
html = '''
<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">次の方程式を解きなさい。</p>
    <div class="math">$$x^2 + 5x + 6 = 0$$</div>
    <ol class="choices">
        <li>x = -2, -3</li>
        <li>x = 2, 3</li>
    </ol>
</div>
'''

problems = parser.parse(html)

# Word文書生成
doc = generator.create_document(problems)
doc.save('output.docx')
カスタムスタイルで生成
Copy# カスタム設定を作成
custom_config = STYLE_CONFIG.copy()
custom_config['title_size'] = 18
custom_config['body_size'] = 12
custom_config['math_dpi'] = 600

# カスタム設定で初期化
math_converter = MathConverter(custom_config)
generator = WordGenerator(custom_config, math_converter)

# 文書生成
doc = generator.create_document(problems)
doc.save('custom_output.docx')
複数の文書を生成
Copydef generate_multiple_documents(html_files, output_dir):
    """複数のHTMLファイルから文書を生成"""
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    for html_file in html_files:
        # HTMLを読み込み
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 解析と生成
        problems = parser.parse(html_content)
        doc = generator.create_document(problems)
        
        # 保存
        output_file = os.path.join(
            output_dir,
            os.path.basename(html_file).replace('.html', '.docx')
        )
        doc.save(output_file)
        print(f"生成完了: {output_file}")

# 使用
html_files = ['problem1.html', 'problem2.html', 'problem3.html']
generate_multiple_documents(html_files, 'output/')
ヘッダー・フッターの追加
Copyfrom docx.shared import Pt

def add_header_footer(doc, header_text, footer_text):
    """ヘッダーとフッターを追加"""
    section = doc.sections[0]
    
    # ヘッダー
    header = section.header
    header_para = header.paragraphs[0]
    header_para.text = header_text
    header_para.style.font.size = Pt(10)
    
    # フッター
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.text = footer_text
    footer_para.style.font.size = Pt(10)

# 使用
doc = generator.create_document(problems)
add_header_footer(doc, '数学テスト', 'ページ')
doc.save('output.docx')
問題ごとに改ページ
Copyclass PageBreakGenerator(WordGenerator):
    """問題ごとに改ページするジェネレーター"""
    
    def create_document(self, problems):
        doc = Document()
        self._apply_global_style(doc)
        
        for i, problem in enumerate(problems):
            self.problem_counter = i + 1
            self._add_problem(doc, problem)
            
            # 最後の問題以外は改ページ
            if i < len(problems) - 1:
                doc.add_page_break()
        
        return doc

# 使用
page_break_generator = PageBreakGenerator(STYLE_CONFIG, math_converter)
doc = page_break_generator.create_document(problems)
doc.save('output_with_breaks.docx')
エラーハンドリング
Copydef safe_generate_document(problems, output_file):
    """エラーハンドリング付きの安全な文書生成"""
    try:
        math_converter = MathConverter(STYLE_CONFIG)
        generator = WordGenerator(STYLE_CONFIG, math_converter)
        
        # 問題データの検証
        if not problems:
            raise ValueError("問題データが空です")
        
        for i, problem in enumerate(problems, 1):
            if not problem.get('title') and not problem.get('text'):
                print(f"警告: 問題{i}に内容がありません")
        
        # 文書生成
        doc = generator.create_document(problems)
        doc.save(output_file)
        
        print(f"成功: {output_file} を生成しました")
        return True
        
    except ValueError as e:
        print(f"データエラー: {e}")
        return False
        
    except Exception as e:
        print(f"生成エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

# 使用
success = safe_generate_document(problems, 'output.docx')
進捗表示付き生成
Copydef generate_with_progress(problems, output_file):
    """進捗表示付きで文書を生成"""
    from tqdm import tqdm
    
    math_converter = MathConverter(STYLE_CONFIG)
    generator = WordGenerator(STYLE_CONFIG, math_converter)
    
    # 進捗バーを作成
    with tqdm(total=len(problems), desc="文書生成中") as pbar:
        doc = Document()
        generator._apply_global_style(doc)
        
        for i, problem in enumerate(problems):
            generator.problem_counter = i + 1
            generator._add_problem(doc, problem)
            
            if i < len(problems) - 1:
                doc.add_paragraph()
            
            pbar.update(1)
    
    doc.save(output_file)
    print(f"\n完了: {output_file}")

# 使用（tqdmのインストールが必要: pip install tqdm）
generate_with_progress(problems, 'output.docx')
トラブルシューティング
問題: フォントが適用されない
原因: 指定したフォントがシステムにない

解決策:

Copyimport platform

# OSに応じてフォントを切り替え
if platform.system() == 'Darwin':  # Mac
    STYLE_CONFIG['title_font'] = 'Hiragino Sans'
    STYLE_CONFIG['body_font'] = 'Hiragino Mincho ProN'
elif platform.system() == 'Windows':
    STYLE_CONFIG['title_font'] = 'MS Gothic'
    STYLE_CONFIG['body_font'] = 'MS Mincho'
問題: 画像のサイズが不適切
原因: 画像の幅設定が固定されている

解決策:

Copy# _add_inline_math や _add_display_math をオーバーライド
class CustomGenerator(WordGenerator):
    def _add_display_math(self, doc, latex_str):
        para = doc.add_paragraph()
        para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        run = para.add_run()
        
        img_stream = self.math_converter.latex_to_image(latex_str)
        run.add_picture(img_stream, width=Inches(3.0))  # 幅を変更
        
        para.paragraph_format.space_after = Pt(12)
問題: メモリ不足
原因: 大量の問題を一度に処理

解決策:

Copy# バッチ処理を使用
def generate_in_batches(all_problems, batch_size=10):
    for i in range(0, len(all_problems), batch_size):
        batch = all_problems[i:i+batch_size]
        
        math_converter = MathConverter(STYLE_CONFIG)
        generator = WordGenerator(STYLE_CONFIG, math_converter)
        
        doc = generator.create_document(batch)
        doc.save(f'output_batch_{i//batch_size + 1}.docx')
        
        # メモリ解放
        del math_converter
        del generator
