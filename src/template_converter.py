"""テンプレート機能付き変換スクリプト"""
import sys
from pathlib import Path
from core import STYLE_CONFIG, TEMPLATES, HTMLParser, MathConverter, WordGenerator, TemplateManager

def convert_with_template(html_file: str, output_file: str, template_name: str = 'standard', **kwargs):
    """テンプレートを使用してHTMLをWord文書に変換"""
    
    print(f"変換開始: {html_file}")
    print(f"テンプレート: {template_name}")
    
    try:
        # HTMLファイルを読み込み
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 初期化
        parser = HTMLParser()
        math_converter = MathConverter(STYLE_CONFIG)
        word_generator = WordGenerator(STYLE_CONFIG, math_converter)
        template_manager = TemplateManager(TEMPLATES)
        
        # HTMLを解析
        print("HTMLを解析中...")
        problems = parser.parse(html_content)
        print(f"  {len(problems)}個の問題を検出")
        
        # Word文書を生成
        print("Word文書を生成中...")
        doc = word_generator.create_document(problems)
        
        # テンプレートを適用
        print(f"テンプレート '{template_name}' を適用中...")
        template_manager.apply_template(doc, template_name, **kwargs)
        
        # 保存
        doc.save(output_file)
        print(f"完了: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("使用方法: python template_converter.py <HTMLファイル> <出力ファイル> [テンプレート名]")
        print("\n利用可能なテンプレート:")
        tm = TemplateManager(TEMPLATES)
        for key, name in tm.list_templates().items():
            print(f"  - {key}: {name}")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = sys.argv[2]
    template_name = sys.argv[3] if len(sys.argv) > 3 else 'standard'
    
    # テンプレートに応じた追加パラメータ
    kwargs = {}
    if template_name == 'exam':
        kwargs['school_name'] = '○○高等学校'
    elif template_name == 'homework':
        from datetime import datetime
        kwargs['date'] = datetime.now().strftime('%Y年%m月%d日')
    
    success = convert_with_template(html_file, output_file, template_name, **kwargs)
    sys.exit(0 if success else 1)
