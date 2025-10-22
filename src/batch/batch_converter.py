"""バッチ変換モジュール"""
import os
from pathlib import Path
from typing import List, Optional
import logging
from datetime import datetime

# 親ディレクトリのモジュールをインポート
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator

class BatchConverter:
    """複数のHTMLファイルを一括変換するクラス"""
    
    def __init__(self, style_config=None):
        """
        初期化
        
        Args:
            style_config (dict, optional): スタイル設定
        """
        self.config = style_config or STYLE_CONFIG
        self.parser = HTMLParser()
        self.math_converter = MathConverter(self.config)
        self.generator = WordGenerator(self.config, self.math_converter)
        
        # ログ設定
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """ロガーを設定"""
        logger = logging.getLogger('BatchConverter')
        logger.setLevel(logging.INFO)
        
        # ファイルハンドラ
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        fh = logging.FileHandler(log_dir / f'batch_{timestamp}.log')
        fh.setLevel(logging.DEBUG)
        
        # コンソールハンドラ
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def convert_folder(self, input_folder: str, output_folder: str, 
                      pattern: str = '*.html') -> dict:
        """
        フォルダ内のHTMLファイルを一括変換
        
        Args:
            input_folder (str): 入力フォルダ
            output_folder (str): 出力フォルダ
            pattern (str): ファイルパターン
        
        Returns:
            dict: 変換結果の統計情報
        """
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        
        # 出力フォルダを作成
        output_path.mkdir(parents=True, exist_ok=True)
        
        # HTMLファイルを取得
        html_files = list(input_path.glob(pattern))
        total = len(html_files)
        
        if total == 0:
            self.logger.warning(f"HTMLファイルが見つかりません: {input_folder}")
            return {'total': 0, 'success': 0, 'failed': 0}
        
        self.logger.info(f"変換開始: {total}個のファイル")
        
        # 統計情報
        stats = {
            'total': total,
            'success': 0,
            'failed': 0,
            'files': []
        }
        
        # 各ファイルを変換
        for i, html_file in enumerate(html_files, 1):
            self.logger.info(f"[{i}/{total}] 処理中: {html_file.name}")
            
            try:
                # 変換実行
                output_file = output_path / f"{html_file.stem}.docx"
                success = self._convert_single_file(html_file, output_file)
                
                if success:
                    stats['success'] += 1
                    stats['files'].append({
                        'input': str(html_file),
                        'output': str(output_file),
                        'status': 'success'
                    })
                    self.logger.info(f"  ✓ 完了: {output_file.name}")
                else:
                    stats['failed'] += 1
                    stats['files'].append({
                        'input': str(html_file),
                        'output': None,
                        'status': 'failed'
                    })
                    self.logger.error(f"  ✗ 失敗: {html_file.name}")
                
            except Exception as e:
                stats['failed'] += 1
                self.logger.error(f"  ✗ エラー: {str(e)}")
        
        # 結果サマリー
        self.logger.info(f"\n変換完了: 成功 {stats['success']}/{total}, 失敗 {stats['failed']}/{total}")
        
        return stats
    
    def _convert_single_file(self, input_file: Path, output_file: Path) -> bool:
        """
        単一ファイルを変換
        
        Args:
            input_file (Path): 入力ファイル
            output_file (Path): 出力ファイル
        
        Returns:
            bool: 成功時True
        """
        try:
            # HTMLを読み込み
            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 解析
            problems = self.parser.parse(html_content)
            
            if not problems:
                self.logger.warning(f"  問題が検出されませんでした: {input_file.name}")
                return False
            
            self.logger.debug(f"  {len(problems)}個の問題を検出")
            
            # Word文書生成
            doc = self.generator.create_document(problems)
            
            # 保存
            doc.save(str(output_file))
            
            return True
            
        except Exception as e:
            self.logger.error(f"  変換エラー: {str(e)}")
            return False
    
    def convert_multiple_files(self, input_files: List[str], 
                              output_folder: str) -> dict:
        """
        指定されたファイルリストを変換
        
        Args:
            input_files (List[str]): 入力ファイルのリスト
            output_folder (str): 出力フォルダ
        
        Returns:
            dict: 変換結果の統計情報
        """
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        total = len(input_files)
        self.logger.info(f"変換開始: {total}個のファイル")
        
        stats = {
            'total': total,
            'success': 0,
            'failed': 0,
            'files': []
        }
        
        for i, input_file in enumerate(input_files, 1):
            input_path = Path(input_file)
            self.logger.info(f"[{i}/{total}] 処理中: {input_path.name}")
            
            try:
                output_file = output_path / f"{input_path.stem}.docx"
                success = self._convert_single_file(input_path, output_file)
                
                if success:
                    stats['success'] += 1
                    stats['files'].append({
                        'input': str(input_path),
                        'output': str(output_file),
                        'status': 'success'
                    })
                else:
                    stats['failed'] += 1
                    stats['files'].append({
                        'input': str(input_path),
                        'output': None,
                        'status': 'failed'
                    })
            
            except Exception as e:
                stats['failed'] += 1
                self.logger.error(f"  ✗ エラー: {str(e)}")
        
        self.logger.info(f"\n変換完了: 成功 {stats['success']}/{total}, 失敗 {stats['failed']}/{total}")
        
        return stats

def main():
    """コマンドライン実行"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HTMLファイルをバッチ変換')
    parser.add_argument('input', help='入力フォルダまたはファイル')
    parser.add_argument('output', help='出力フォルダ')
    parser.add_argument('--pattern', default='*.html', help='ファイルパターン')
    
    args = parser.parse_args()
    
    converter = BatchConverter()
    
    input_path = Path(args.input)
    if input_path.is_dir():
        stats = converter.convert_folder(args.input, args.output, args.pattern)
    elif input_path.is_file():
        stats = converter.convert_multiple_files([args.input], args.output)
    else:
        print(f"エラー: {args.input} が見つかりません")
        return 1
    
    return 0 if stats['failed'] == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
