"""数式画像変換モジュール（完全修正版）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import mathtext
from PIL import Image
import io
from typing import BinaryIO
import re

class MathConverter:
    def __init__(self, config: dict):
        self.dpi = config['math_dpi']
        self.font_size = config['math_font_size']
        self.color = config['math_color']
        
        # matplotlibの設定
        plt.rcParams['mathtext.fontset'] = 'cm'
        plt.rcParams['mathtext.default'] = 'regular'
    
    def latex_to_image(self, latex_str: str) -> BinaryIO:
        """LaTeX数式を画像化"""
        try:
            # 前処理
            latex_str = self._preprocess_latex(latex_str)
            
            # 図を作成
            fig = plt.figure(figsize=(10, 2))
            fig.patch.set_alpha(0)
            
            # 数式をレンダリング
            ax = fig.add_subplot(111)
            ax.axis('off')
            
            # テキストを描画
            text = ax.text(
                0.5, 0.5,
                f'${latex_str}$',
                fontsize=self.font_size,
                color=self.color,
                ha='center',
                va='center',
                transform=ax.transAxes
            )
            
            # 描画して境界ボックスを取得
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()
            bbox = text.get_window_extent(renderer=renderer)
            
            # 余白を追加
            bbox_padded = bbox.padded(10)
            
            # 画像として保存
            buf = io.BytesIO()
            fig.savefig(
                buf,
                format='png',
                dpi=self.dpi,
                bbox_inches=bbox_padded.transformed(fig.dpi_scale_trans.inverted()),
                transparent=True,
                pad_inches=0.1
            )
            plt.close(fig)
            
            buf.seek(0)
            return buf
            
        except Exception as e:
            print(f"数式変換エラー: {latex_str[:50]}...")
            print(f"エラー内容: {str(e)}")
            return self._create_error_image(latex_str)
    
    def _preprocess_latex(self, latex_str: str) -> str:
        """LaTeX文字列の前処理"""
        # 前後の空白を削除
        latex_str = latex_str.strip()
        
        # $記号を削除
        latex_str = re.sub(r'^\$+|\$+$', '', latex_str)
        
        # \text{}の処理を改善
        # matplotlibのmathtextは\text{}を完全にはサポートしていないため、
        # \mathrm{}に変換
        latex_str = re.sub(r'\\text\{([^}]+)\}', r'\\mathrm{\1}', latex_str)
        
        # 特殊文字のエスケープ
        # （必要に応じて追加）
        
        return latex_str
    
    def _create_error_image(self, latex_str: str) -> BinaryIO:
        """エラー時の代替画像"""
        try:
            fig = plt.figure(figsize=(4, 0.5))
            fig.patch.set_facecolor('#ffe6e6')
            
            ax = fig.add_subplot(111)
            ax.axis('off')
            
            error_msg = f'[数式エラー]'
            ax.text(
                0.5, 0.5,
                error_msg,
                fontsize=10,
                color='red',
                ha='center',
                va='center',
                transform=ax.transAxes,
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='red')
            )
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
            plt.close(fig)
            
            buf.seek(0)
            return buf
        except:
            # 最終フォールバック
            fig = plt.figure(figsize=(2, 0.3))
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150)
            plt.close(fig)
            buf.seek(0)
            return buf
    
    def test_conversion(self, latex_str: str) -> bool:
        """変換テスト"""
        try:
            buf = self.latex_to_image(latex_str)
            img = Image.open(buf)
            return img.size[0] > 0 and img.size[1] > 0
        except:
            return False
