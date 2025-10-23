"""テンプレート機能のテスト"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import STYLE_CONFIG, TEMPLATES, HTMLParser, MathConverter, WordGenerator, TemplateManager

def test_all_templates():
    """すべてのテンプレートをテスト"""
    
    # 初期化
    parser = HTMLParser()
    math_converter = MathConverter(STYLE_CONFIG)
    word_generator = WordGenerator(STYLE_CONFIG, math_converter)
    template_manager = TemplateManager(TEMPLATES)
    
    # サンプルHTMLを読み込み
    test_file = 'data/input/sample_problem.html'
    
    print("="*60)
    print("テンプレート機能テスト")
    print("="*60)
    
    with open(test_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    problems = parser.parse(html_content)
    print(f"\n✓ {len(problems)}個の問題を検出")
    
    # 各テンプレートでテスト
    for template_name, template_info in TEMPLATES.items():
        print(f"\n{'─'*60}")
        print(f"テンプレート: {template_name} ({template_info['name']})")
        print(f"{'─'*60}")
        
        try:
            # Word文書生成
            doc = word_generator.create_document(problems)
            
            # テンプレート適用
            kwargs = {}
            if template_name == 'exam':
                kwargs['school_name'] = '○○高等学校'
            elif template_name == 'homework':
                from datetime import datetime
                kwargs['date'] = datetime.now().strftime('%Y年%m月%d日')
            
            template_manager.apply_template(doc, template_name, **kwargs)
            
            # 保存
            output_file = f'data/output/test_{template_name}.docx'
            doc.save(output_file)
            
            print(f"✓ 生成成功: {output_file}")
            
            # テンプレート情報を表示
            if template_info.get('header'):
                print(f"  ヘッダー: {template_info['header']}")
            if template_info.get('footer'):
                print(f"  フッター: {template_info['footer']}")
            
        except Exception as e:
            print(f"✗ エラー: {str(e)}")
    
    print(f"\n{'='*60}")
    print("テスト完了")
    print(f"{'='*60}")
    print("\n生成されたファイル:")
    for template_name in TEMPLATES.keys():
        print(f"  - data/output/test_{template_name}.docx")

if __name__ == '__main__':
    test_all_templates()
