"""統一スタイル設定（バランス調整版）"""

STYLE_CONFIG = {
    # 数式画像設定
    'math_dpi': 300,
    'math_font_size': 250,  # 少し大きく（11pt）
    'math_color': 'black',
    'math_background': 'transparent',
    
    # インライン数式の高さ設定（ポイント単位）
    'inline_math_height': 8,  # 本文より少し大きく（12pt）
    'display_math_width': 2.5,  # インチ単位
    
    # テキストスタイル
    'title_font': 'MS Gothic',
    'title_size': 16,
    'title_bold': True,
    'body_font': 'MS Mincho',
    'body_size': 11,
    
    # レイアウト
    'problem_spacing': 1.5,
    'paragraph_spacing': 1.15,
    'page_margin': 2.54,  # cm
    
    # 選択肢スタイル
    'choice_font': 'MS Mincho',
    'choice_size': 11,
    'choice_indent': 1.0,  # cm
}

# テンプレート定義
TEMPLATES = {
    'standard': {
        'name': '標準問題集',
        'header': None,
        'footer': 'ページ {page}',
        'title_style': '見出し 1',
        'numbering': True,
    },
    'exam': {
        'name': '定期試験',
        'header': '{school_name} 数学テスト',
        'footer': '氏名:__________ 得点:____/100',
        'title_style': '見出し 2',
        'time_limit': True,
    },
    'homework': {
        'name': '宿題プリント',
        'header': '提出日: {date}',
        'footer': 'クラス:____ 番号:____ 氏名:__________',
        'answer_space': True,
    }
}
