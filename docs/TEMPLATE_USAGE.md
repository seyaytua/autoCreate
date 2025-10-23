# テンプレート機能の使い方

## 概要

テンプレート機能を使用すると、用途に応じたヘッダー・フッターを自動で挿入できます。

## 利用可能なテンプレート

### 1. standard（標準問題集）
- **用途**: 一般的な問題集
- **ヘッダー**: なし
- **フッター**: ページ番号

```bash
python src/template_converter.py input.html output.docx standard
2. exam（定期試験）
用途: 学校の試験
ヘッダー: 学校名 + テスト名
フッター: 氏名・得点欄
Copypython src/template_converter.py input.html output.docx exam
3. homework（宿題プリント）
用途: 宿題
ヘッダー: 提出日
フッター: クラス・番号・氏名欄
Copypython src/template_converter.py input.html output.docx homework
基本的な使い方
コマンドライン
Copy# 標準テンプレート
python src/template_converter.py data/input/problem.html data/output/result.docx

# 試験用テンプレート
python src/template_converter.py data/input/problem.html data/output/exam.docx exam

# 宿題用テンプレート
python src/template_converter.py data/input/problem.html data/output/homework.docx homework
Pythonコード
Copyfrom core import STYLE_CONFIG, TEMPLATES, HTMLParser, MathConverter, WordGenerator, TemplateManager

# 初期化
parser = HTMLParser()
math_converter = MathConverter(STYLE_CONFIG)
generator = WordGenerator(STYLE_CONFIG, math_converter)
template_manager = TemplateManager(TEMPLATES)

# HTMLを解析
with open('input.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

problems = parser.parse(html_content)

# Word文書生成
doc = generator.create_document(problems)

# テンプレート適用
template_manager.apply_template(
    doc, 
    'exam',
    school_name='○○高等学校'
)

doc.save('output.docx')
カスタムテンプレートの追加
src/core/style_config.py の TEMPLATES に追加します：

CopyTEMPLATES = {
    # 既存のテンプレート...
    
    'custom': {
        'name': 'カスタムテンプレート',
        'header': 'カスタムヘッダー: {title}',
        'footer': 'カスタムフッター',
        'title_style': '見出し 1',
    }
}
テスト
すべてのテンプレートをテスト：

Copypython test_templates.py
生成されるファイル：

data/output/test_standard.docx
data/output/test_exam.docx
data/output/test_homework.docx
