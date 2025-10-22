"""問題生成用プロンプトテンプレート"""

# 基本的なプロンプトテンプレート
BASE_PROMPT = """
あなたは数学問題作成AIです。
以下の厳密なフォーマットで問題を生成してください。

【HTML構造の規則】
必ず以下の構造を守ってください：

<div class="problem">
  <h2 class="problem-title">大問{number}</h2>
  <p class="problem-text">問題文をここに記述</p>
  <div class="math">$$LaTeX数式$$</div>
  <ol class="choices">
    <li>選択肢1</li>
    <li>選択肢2</li>
    <li>選択肢3</li>
    <li>選択肢4</li>
  </ol>
</div>

【数式記法の規則】
- インライン数式: \\(x^2\\)
- 独立数式: $$\\frac{{a}}{{b}}$$
- 必ずLaTeX記法を使用
- バックスラッシュは二重にエスケープ

【クラス名の規則】
- 問題ブロック: class="problem"
- タイトル: class="problem-title"
- 問題文: class="problem-text"
- 数式ブロック: class="math"
- 選択肢: class="choices"

【禁止事項】
- HTMLタグはdiv, p, h2, ol, liのみ使用
- style属性の使用禁止
- 数式以外のフォーマット指定禁止
"""

# 難易度別テンプレート
DIFFICULTY_TEMPLATES = {
    'easy': {
        'name': '初級',
        'description': '基本的な計算問題',
        'prompt_addition': """
【初級問題の特徴】
- 四則演算中心
- 1次方程式レベル
- 計算ステップは2〜3段階
- 選択肢は明確に区別可能
"""
    },
    'medium': {
        'name': '中級',
        'description': '標準的な応用問題',
        'prompt_addition': """
【中級問題の特徴】
- 2次方程式、関数
- 計算ステップは3〜5段階
- 概念理解が必要
- 選択肢に類似した値を含む
"""
    },
    'hard': {
        'name': '上級',
        'description': '発展的な問題',
        'prompt_addition': """
【上級問題の特徴】
- 積分、微分、複素数
- 複数の概念を組み合わせ
- 計算ステップは5段階以上
- 論理的思考が必要
"""
    }
}

# 分野別テンプレート
CATEGORY_TEMPLATES = {
    'algebra': {
        'name': '代数',
        'topics': ['方程式', '不等式', '因数分解', '式の計算'],
        'prompt_addition': """
【代数分野の要件】
- 文字式の操作が中心
- 等式・不等式の性質を活用
- 解の検証を含める
"""
    },
    'geometry': {
        'name': '幾何',
        'topics': ['図形の性質', '面積', '体積', '三角比'],
        'prompt_addition': """
【幾何分野の要件】
- 図形の性質を活用
- 定理の適用を明示
- 単位に注意
"""
    },
    'calculus': {
        'name': '微積分',
        'topics': ['微分', '積分', '極限', '関数'],
        'prompt_addition': """
【微積分分野の要件】
- 微分・積分の計算
- 関数の性質を考察
- グラフとの関連を意識
"""
    },
    'statistics': {
        'name': '統計',
        'topics': ['確率', '統計', 'データ分析'],
        'prompt_addition': """
【統計分野の要件】
- データの解釈
- 確率の計算
- 統計量の理解
"""
    }
}

def generate_prompt(difficulty='medium', category='algebra', count=1, **kwargs):
    """
    問題生成用のプロンプトを生成
    
    Parameters:
        difficulty (str): 難易度 ('easy', 'medium', 'hard')
        category (str): 分野 ('algebra', 'geometry', 'calculus', 'statistics')
        count (int): 生成する問題数
        **kwargs: その他のカスタムパラメータ
    
    Returns:
        str: 生成されたプロンプト
    """
    prompt_parts = [BASE_PROMPT]
    
    # 難易度の追加
    if difficulty in DIFFICULTY_TEMPLATES:
        template = DIFFICULTY_TEMPLATES[difficulty]
        prompt_parts.append(f"\n【難易度】: {template['name']}")
        prompt_parts.append(template['prompt_addition'])
    
    # 分野の追加
    if category in CATEGORY_TEMPLATES:
        template = CATEGORY_TEMPLATES[category]
        prompt_parts.append(f"\n【分野】: {template['name']}")
        prompt_parts.append(f"【トピック】: {', '.join(template['topics'])}")
        prompt_parts.append(template['prompt_addition'])
    
    # 問題数の指定
    prompt_parts.append(f"\n【生成する問題数】: {count}問")
    
    # カスタムパラメータの追加
    if kwargs:
        prompt_parts.append("\n【追加要件】:")
        for key, value in kwargs.items():
            prompt_parts.append(f"- {key}: {value}")
    
    # 最終的な指示
    prompt_parts.append("""
\n【出力形式】
上記のHTML構造に厳密に従って、問題を生成してください。
各問題は必ず<div class="problem">で囲んでください。
複数問題を生成する場合は、連続して出力してください。
""")
    
    return '\n'.join(prompt_parts)

def get_example_html():
    """正しいHTMLの例を返す"""
    return """
<div class="problem">
  <h2 class="problem-title">大問1</h2>
  <p class="problem-text">次の方程式を解きなさい。</p>
  <div class="math">$$x^2 + 5x + 6 = 0$$</div>
  <ol class="choices">
    <li>x = -2, -3</li>
    <li>x = 2, 3</li>
    <li>x = -1, -6</li>
    <li>x = 1, 6</li>
  </ol>
</div>
"""

# 使用例を追加
if __name__ == '__main__':
    # 基本的な使用
    prompt = generate_prompt(
        difficulty='medium',
        category='algebra',
        count=2
    )
    print(prompt)
    
    print("\n" + "="*50)
    print("正しいHTMLの例:")
    print("="*50)
    print(get_example_html())
