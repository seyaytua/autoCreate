"""クリップボードからHTML→Word変換"""
import sys
from pathlib import Path
import pyperclip
from datetime import datetime
from core import STYLE_CONFIG, TEMPLATES, HTMLParser, MathConverter, WordGenerator, TemplateManager

def convert_from_clipboard(output_file: str = None, template_name: str = 'standard', **kwargs):
    """クリップボードのHTMLをWord文書に変換"""
    
    print("="*60)
    print("クリップボードから変換")
    print("="*60)
    
    try:
        # クリップボードからHTML取得
        print("\nクリップボードからHTMLを読み込み中...")
        html_content = pyperclip.paste()
        
        if not html_content.strip():
            print("✗ エラー: クリップボードが空です")
            return False
        
        print(f"✓ {len(html_content)}文字のHTMLを取得")
        
        # 出力ファイル名の自動生成
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'data/output/clipboard_{timestamp}.docx'
        
        # 初期化
        parser = HTMLParser()
        math_converter = MathConverter(STYLE_CONFIG)
        word_generator = WordGenerator(STYLE_CONFIG, math_converter)
        template_manager = TemplateManager(TEMPLATES)
        
        # HTMLを解析
        print("\nHTMLを解析中...")
        problems = parser.parse(html_content)
        
        if not problems:
            print("✗ エラー: 問題が検出されませんでした")
            print("\nHTMLの先頭100文字:")
            print(html_content[:100])
            return False
        
        print(f"✓ {len(problems)}個の問題を検出")
        
        # Word文書を生成
        print("\nWord文書を生成中...")
        doc = word_generator.create_document(problems)
        
        # テンプレートを適用
        if template_name != 'none':
            print(f"テンプレート '{template_name}' を適用中...")
            template_manager.apply_template(doc, template_name, **kwargs)
        
        # 保存
        doc.save(output_file)
        
        print(f"\n✓ 完了: {output_file}")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    output_file = sys.argv[1] if len(sys.argv) > 1 else None
    template_name = sys.argv[2] if len(sys.argv) > 2 else 'standard'
    
    # テンプレートに応じた追加パラメータ
    kwargs = {}
    if template_name == 'exam':
        kwargs['school_name'] = '○○高等学校'
    elif template_name == 'homework':
        kwargs['date'] = datetime.now().strftime('%Y年%m月%d日')
    
    success = convert_from_clipboard(output_file, template_name, **kwargs)
    sys.exit(0 if success else 1)
