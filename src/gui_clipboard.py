"""クリップボード変換GUI（改善版）"""
import sys
from pathlib import Path
from datetime import datetime
import pyperclip
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QComboBox, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

sys.path.append(str(Path(__file__).parent))

from core import STYLE_CONFIG, TEMPLATES, HTMLParser, MathConverter, WordGenerator, TemplateManager

class ClipboardConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.html_content = ""
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("クリップボード変換")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        title = QLabel("クリップボードからWord変換")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel("HTMLをコピーしてから「クリップボードから読み込み」をクリック")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        btn_load = QPushButton("📋 クリップボードから読み込み")
        btn_load.clicked.connect(self.load_from_clipboard)
        layout.addWidget(btn_load)
        
        preview_label = QLabel("プレビュー:")
        layout.addWidget(preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.preview_text)
        
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("テンプレート:"))
        
        self.template_combo = QComboBox()
        self.template_combo.addItem("標準問題集", "standard")
        self.template_combo.addItem("定期試験", "exam")
        self.template_combo.addItem("宿題プリント", "homework")
        self.template_combo.addItem("なし", "none")
        template_layout.addWidget(self.template_combo)
        
        layout.addLayout(template_layout)
        
        btn_convert = QPushButton("📄 Word文書に変換")
        btn_convert.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_convert.clicked.connect(self.convert_to_word)
        layout.addWidget(btn_convert)
    
    def load_from_clipboard(self):
        try:
            self.html_content = pyperclip.paste()
            
            if not self.html_content.strip():
                QMessageBox.warning(self, "警告", "クリップボードが空です")
                return
            
            preview = self.html_content[:1000]
            if len(self.html_content) > 1000:
                preview += "\n\n... (続きがあります)"
            
            self.preview_text.setPlainText(preview)
            
            parser = HTMLParser()
            try:
                problems = parser.parse(self.html_content)
                if problems:
                    QMessageBox.information(
                        self, 
                        "成功", 
                        f"✓ {len(self.html_content)}文字のHTMLを読み込みました\n\n{len(problems)}個の問題を検出"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "警告",
                        "HTMLは読み込みましたが、問題が検出されませんでした"
                    )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "警告",
                    f"HTMLは読み込みましたが、解析時に警告があります:\n\n{str(e)}"
                )
            
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"読み込みエラー:\n{str(e)}")
    
    def convert_to_word(self):
        try:
            if not self.html_content.strip():
                QMessageBox.warning(
                    self, 
                    "警告", 
                    "HTMLが読み込まれていません\n\n先に「クリップボードから読み込み」をクリックしてください"
                )
                return
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_name = f"clipboard_{timestamp}.docx"
            
            output_file, _ = QFileDialog.getSaveFileName(
                self,
                "保存先を選択",
                str(Path.home() / default_name),
                "Word Files (*.docx)"
            )
            
            if not output_file:
                return
            
            parser = HTMLParser()
            math_converter = MathConverter(STYLE_CONFIG)
            word_generator = WordGenerator(STYLE_CONFIG, math_converter)
            template_manager = TemplateManager(TEMPLATES)
            
            problems = parser.parse(self.html_content)
            
            if not problems:
                QMessageBox.warning(
                    self, 
                    "警告", 
                    "問題が検出されませんでした"
                )
                return
            
            doc = word_generator.create_document(problems)
            
            template_name = self.template_combo.currentData()
            if template_name != 'none':
                kwargs = {}
                if template_name == 'exam':
                    kwargs['school_name'] = '○○高等学校'
                elif template_name == 'homework':
                    kwargs['date'] = datetime.now().strftime('%Y年%m月%d日')
                
                template_manager.apply_template(doc, template_name, **kwargs)
            
            doc.save(output_file)
            
            reply = QMessageBox.information(
                self,
                "完了",
                f"✓ 変換完了\n\n{len(problems)}問を変換しました\n\nファイルを開きますか？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                import subprocess
                import platform
                
                if platform.system() == 'Darwin':
                    subprocess.call(['open', output_file])
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            QMessageBox.critical(
                self, 
                "エラー", 
                f"変換エラー:\n\n{str(e)}"
            )

def main():
    app = QApplication(sys.argv)
    window = ClipboardConverterGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
