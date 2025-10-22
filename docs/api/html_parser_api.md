
HTMLParser API リファレンス
クラス概要
Copyfrom core.html_parser import HTMLParser
HTMLParser クラスは、HTML形式の数学問題を解析し、構造化されたデータに変換します。

クラス定義
Copyclass HTMLParser:
    def __init__(self)
    def parse(self, html_content: str) -> List[Dict[str, Any]]
    def _split_by_headers(self, soup) -> List
    def _extract_title(self, problem_div) -> str
    def _extract_text(self, problem_div) -> List[Dict[str, Any]]
    def _split_text_and_math(self, text: str) -> List[Dict[str, Any]]
    def _extract_equations(self, problem_div) -> List[str]
    def _extract_choices(self, problem_div) -> List[str]
初期化
__init__()
Copyparser = HTMLParser()
説明: HTMLParserのインスタンスを作成します。

パラメータ: なし

戻り値: HTMLParserインスタンス

初期化される属性:

latex_pattern: LaTeX数式を検出する正規表現パターン
$$...$$ 形式
\(...\) 形式
使用例:

Copyparser = HTMLParser()
print(parser.latex_pattern.pattern)
# 出力: r'\$\$(.*?)\$\$|\\\((.*?)\\\)'
パブリックメソッド
parse(html_content: str)
Copydef parse(self, html_content: str) -> List[Dict[str, Any]]
説明: HTML文字列を解析し、問題データのリストを返します。

パラメータ:

html_content (str): 解析するHTML文字列
戻り値: List[Dict[str, Any]] - 問題データのリスト

戻り値の構造:

Copy[
    {
        'title': str,                    # 問題タイトル（例: "大問1"）
        'text': List[Dict[str, Any]],    # 問題文の要素リスト
        'equations': List[str],          # 独立した数式のリスト
        'choices': List[str],            # 選択肢のリスト
        'raw_html': str                  # 元のHTML文字列
    },
    # ... 他の問題
]
text要素の構造:

Copy[
    {'type': 'text', 'content': '問題文のテキスト'},
    {'type': 'math', 'content': 'x^2 + y^2'},
    # ...
]
使用例:

Copyhtml = '''
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

parser = HTMLParser()
problems = parser.parse(html)

# 結果の確認
print(f"問題数: {len(problems)}")
print(f"タイトル: {problems[0]['title']}")
print(f"数式: {problems[0]['equations']}")
print(f"選択肢数: {len(problems[0]['choices'])}")
出力例:

問題数: 1
タイトル: 大問1
数式: ['x^2 + 5x + 6 = 0']
選択肢数: 2
エラー処理:

不正なHTMLの場合: 空のリストを返す
class="problem" がない場合: _split_by_headers() で自動分割
プライベートメソッド
_split_by_headers(soup)
Copydef _split_by_headers(self, soup) -> List
説明: class="problem" がない場合、h2タグで問題を分割します。

パラメータ:

soup: BeautifulSoupオブジェクト
戻り値: List - 問題要素のリスト

使用例:

Copyhtml = '''
<h2>大問1</h2>
<p>問題文</p>
<h2>大問2</h2>
<p>問題文</p>
'''

soup = BeautifulSoup(html, 'html.parser')
parser = HTMLParser()
problems = parser._split_by_headers(soup)
print(f"分割された問題数: {len(problems)}")
_extract_title(problem_div)
Copydef _extract_title(self, problem_div) -> str
説明: 問題のタイトルを抽出します。

パラメータ:

problem_div: BeautifulSoupの要素オブジェクト
戻り値: str - タイトル文字列（見つからない場合は空文字列）

検索順序:

<h1|h2|h3 class="problem-title">
<h1|h2|h3>
見つからない場合: ""
使用例:

Copyhtml = '<div><h2 class="problem-title">大問1</h2></div>'
soup = BeautifulSoup(html, 'html.parser')
div = soup.find('div')

parser = HTMLParser()
title = parser._extract_title(div)
print(title)  # "大問1"
_extract_text(problem_div)
Copydef _extract_text(self, problem_div) -> List[Dict[str, Any]]
説明: 問題文を抽出し、テキストと数式に分離します。

パラメータ:

problem_div: BeautifulSoupの要素オブジェクト
戻り値: List[Dict[str, Any]] - テキスト要素のリスト

戻り値の構造:

Copy[
    {'type': 'text', 'content': '次の方程式を解きなさい。'},
    {'type': 'math', 'content': 'x^2 + 5x + 6 = 0'},
]
使用例:

Copyhtml = '''
<div>
    <p class="problem-text">次の方程式を解きなさい。</p>
    <p class="problem-text">ただし、\(x \neq 0\) とする。</p>
</div>
'''

soup = BeautifulSoup(html, 'html.parser')
div = soup.find('div')

parser = HTMLParser()
text_elements = parser._extract_text(div)

for element in text_elements:
    print(f"{element['type']}: {element['content']}")
_split_text_and_math(text: str)
Copydef _split_text_and_math(self, text: str) -> List[Dict[str, Any]]
説明: テキスト内の数式を検出し、テキストと数式に分離します。

パラメータ:

text (str): 分離するテキスト
戻り値: List[Dict[str, Any]] - 分離された要素のリスト

対応する数式パターン:

$$...$$: ディスプレイ数式
\(...\): インライン数式
使用例:

Copytext = "ただし、\(x \neq 0\) とする。また、$$y = x^2$$ である。"

parser = HTMLParser()
parts = parser._split_text_and_math(text)

for part in parts:
    print(f"{part['type']}: {part['content']}")
出力:

text: ただし、
math: x \neq 0
text: とする。また、
math: y = x^2
text: である。
_extract_equations(problem_div)
Copydef _extract_equations(self, problem_div) -> List[str]
説明: 独立した数式ブロック（<div class="math">）を抽出します。

パラメータ:

problem_div: BeautifulSoupの要素オブジェクト
戻り値: List[str] - LaTeX数式のリスト

処理内容:

$$...$$ を自動的に除去
前後の空白をトリミング
使用例:

Copyhtml = '''
<div>
    <div class="math">$$x^2 + y^2 = r^2$$</div>
    <div class="math">$$\frac{a}{b} = c$$</div>
</div>
'''

soup = BeautifulSoup(html, 'html.parser')
div = soup.find('div')

parser = HTMLParser()
equations = parser._extract_equations(div)

for eq in equations:
    print(eq)
出力:

x^2 + y^2 = r^2
\frac{a}{b} = c
_extract_choices(problem_div)
Copydef _extract_choices(self, problem_div) -> List[str]
説明: 選択肢を抽出します。

パラメータ:

problem_div: BeautifulSoupの要素オブジェクト
戻り値: List[str] - 選択肢のリスト

対応タグ:

<ol class="choices">
<ul class="choices">
class属性なしの <ol>, <ul>
使用例:

Copyhtml = '''
<div>
    <ol class="choices">
        <li>選択肢1</li>
        <li>選択肢2</li>
        <li>選択肢3</li>
    </ol>
</div>
'''

soup = BeautifulSoup(html, 'html.parser')
div = soup.find('div')

parser = HTMLParser()
choices = parser._extract_choices(div)

for i, choice in enumerate(choices, 1):
    print(f"{i}. {choice}")
出力:

1. 選択肢1
2. 選択肢2
3. 選択肢3
対応HTML構造
標準形式（推奨）
Copy<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">問題文</p>
    <div class="math">$$数式$$</div>
    <ol class="choices">
        <li>選択肢1</li>
        <li>選択肢2</li>
    </ol>
</div>
簡易形式
Copy<h2>大問1</h2>
<p>問題文</p>
<div>$$数式$$</div>
<ol>
    <li>選択肢1</li>
    <li>選択肢2</li>
</ol>
複雑な構造
Copy<div class="problem">
    <h2 class="problem-title">大問1</h2>
    <p class="problem-text">次の方程式を解きなさい。</p>
    <div class="math">$$x^2 + 5x + 6 = 0$$</div>
    <p class="problem-text">ただし、\(x \neq 0\) とする。</p>
    <p class="problem-text">また、次の条件を満たす。</p>
    <div class="math">$$y = 2x + 1$$</div>
    <ol class="choices">
        <li>x = -2, -3</li>
        <li>x = 2, 3</li>
        <li>x = -1, -6</li>
        <li>x = 1, 6</li>
    </ol>
</div>
実践的な使用例
複数の問題を含むHTMLの解析
Copyhtml = '''
<!DOCTYPE html>
<html>
<body>
    <div class="problem">
        <h2 class="problem-title">大問1</h2>
        <p class="problem-text">次の方程式を解きなさい。</p>
        <div class="math">$$x^2 + 5x + 6 = 0$$</div>
        <ol class="choices">
            <li>x = -2, -3</li>
            <li>x = 2, 3</li>
        </ol>
    </div>
    
    <div class="problem">
        <h2 class="problem-title">大問2</h2>
        <p class="problem-text">次の関数の最大値を求めなさい。</p>
        <div class="math">$$f(x) = -x^2 + 4x + 1$$</div>
        <p class="problem-text">ただし、\(0 \leq x \leq 5\) とする。</p>
        <ol class="choices">
            <li>最大値 5</li>
            <li>最大値 6</li>
        </ol>
    </div>
</body>
</html>
'''

parser = HTMLParser()
problems = parser.parse(html)

# 各問題の情報を表示
for i, problem in enumerate(problems, 1):
    print(f"\n{'='*50}")
    print(f"問題 {i}")
    print(f"{'='*50}")
    print(f"タイトル: {problem['title']}")
    print(f"\nテキスト要素:")
    for element in problem['text']:
        print(f"  - {element['type']}: {element['content'][:50]}")
    print(f"\n数式:")
    for eq in problem['equations']:
        print(f"  - {eq}")
    print(f"\n選択肢:")
    for j, choice in enumerate(problem['choices'], 1):
        print(f"  {j}. {choice}")
エラーハンドリング
Copydef safe_parse(html_content):
    """エラーハンドリング付きの安全な解析"""
    parser = HTMLParser()
    
    try:
        problems = parser.parse(html_content)
        
        if not problems:
            print("警告: 問題が見つかりませんでした")
            return []
        
        # 各問題の妥当性チェック
        for i, problem in enumerate(problems, 1):
            if not problem['title']:
                print(f"警告: 問題{i}にタイトルがありません")
            
            if not problem['text'] and not problem['equations']:
                print(f"警告: 問題{i}に内容がありません")
        
        return problems
        
    except Exception as e:
        print(f"エラー: HTMLの解析に失敗しました - {e}")
        import traceback
        traceback.print_exc()
        return []

# 使用
problems = safe_parse(html_content)
カスタム解析ルール
Copyclass CustomHTMLParser(HTMLParser):
    """カスタマイズされたHTMLパーサー"""
    
    def parse(self, html_content: str) -> List[Dict[str, Any]]:
        """カスタム解析ロジック"""
        problems = super().parse(html_content)
        
        # 追加の処理
        for problem in problems:
            # タイトルが空の場合、自動生成
            if not problem['title']:
                problem['title'] = f"問題{problems.index(problem) + 1}"
            
            # 選択肢がない場合、記述式として扱う
            if not problem['choices']:
                problem['type'] = 'descriptive'
            else:
                problem['type'] = 'multiple_choice'
        
        return problems

# 使用
custom_parser = CustomHTMLParser()
problems = custom_parser.parse(html_content)
