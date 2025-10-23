"""統合GUI - シンプル洗練版"""
import sys
from pathlib import Path
from datetime import datetime
import pyperclip
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QComboBox, QFileDialog, QMessageBox,
    QRadioButton, QButtonGroup, QListWidget, QProgressBar, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QTextCursor

sys.path.append(str(Path(__file__).parent))

from core import STYLE_CONFIG, TEMPLATES, HTMLParser, MathConverter, WordGenerator, TemplateManager

class ConversionThread(QThread):
    progress = Signal(int, str)
    finished = Signal(bool, str)
    
    def __init__(self, html_content, output_file, template_name, **kwargs):
        super().__init__()
        self.html_content = html_content
        self.output_file = output_file
        self.template_name = template_name
        self.kwargs = kwargs
    
    def run(self):
        try:
            self.progress.emit(25, "HTMLを解析中...")
            
            parser = HTMLParser()
            math_converter = MathConverter(STYLE_CONFIG)
            generator = WordGenerator(STYLE_CONFIG, math_converter)
            template_manager = TemplateManager(TEMPLATES)
            
            problems = parser.parse(self.html_content)
            
            if not problems:
                self.finished.emit(False, "問題が検出されませんでした")
                return
            
            self.progress.emit(50, "Word文書を生成中...")
            doc = generator.create_document(problems)
            
            if self.template_name != 'none':
                self.progress.emit(75, "テンプレート適用中...")
                template_manager.apply_template(doc, self.template_name, **self.kwargs)
            
            self.progress.emit(90, "保存中...")
            doc.save(self.output_file)
            
            self.progress.emit(100, "完了")
            self.finished.emit(True, f"変換完了\n{len(problems)}問を変換しました")
            
        except Exception as e:
            self.finished.emit(False, f"エラー: {str(e)}")

class UnifiedConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.html_content = ""
        self.input_files = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("数学問題変換システム")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # ヘッダー
        header = self._create_header()
        main_layout.addWidget(header)
        
        # メインコンテンツ
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white;")
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(1)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 左パネル
        left_panel = self._create_left_panel()
        content_layout.addWidget(left_panel, 1)
        
        # セパレーター
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("background-color: #e0e0e0;")
        separator.setFixedWidth(1)
        content_layout.addWidget(separator)
        
        # 右パネル
        right_panel = self._create_right_panel()
        content_layout.addWidget(right_panel, 2)
        
        main_layout.addWidget(content_widget, 1)
        
        # フッター
        footer = self._create_footer()
        main_layout.addWidget(footer)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafafa;
            }
        """)
    
    def _create_header(self):
        """ヘッダー"""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                padding: 20px;
            }
        """)
        header.setFixedHeight(80)
        
        layout = QVBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)
        
        title = QLabel("数学問題変換システム")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: 600;
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("HTML → Word Document Converter")
        subtitle.setStyleSheet("""
            color: #95a5a6;
            font-size: 13px;
        """)
        layout.addWidget(subtitle)
        
        return header
    
    def _create_left_panel(self):
        """左パネル"""
        panel = QWidget()
        panel.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 入力方法
        mode_label = QLabel("入力方法")
        mode_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #2c3e50;
        """)
        layout.addWidget(mode_label)
        
        self.input_mode_group = QButtonGroup()
        
        self.radio_file = QRadioButton("ファイルから読み込み")
        self.radio_file.setChecked(True)
        self.radio_file.setStyleSheet("""
            QRadioButton {
                font-size: 13px;
                color: #34495e;
                spacing: 8px;
            }
        """)
        self.radio_file.toggled.connect(self.on_input_mode_changed)
        self.input_mode_group.addButton(self.radio_file, 0)
        layout.addWidget(self.radio_file)
        
        self.radio_clipboard = QRadioButton("クリップボードから読み込み")
        self.radio_clipboard.setStyleSheet(self.radio_file.styleSheet())
        self.radio_clipboard.toggled.connect(self.on_input_mode_changed)
        self.input_mode_group.addButton(self.radio_clipboard, 1)
        layout.addWidget(self.radio_clipboard)
        
        # 区切り線
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #ecf0f1;")
        line.setFixedHeight(1)
        layout.addWidget(line)
        
        # ファイル選択エリア
        self.file_area = QWidget()
        file_layout = QVBoxLayout(self.file_area)
        file_layout.setSpacing(10)
        
        btn_layout = QHBoxLayout()
        self.btn_select_file = QPushButton("ファイル選択")
        self.btn_select_file.setStyleSheet(self._button_style())
        self.btn_select_file.clicked.connect(self.select_files)
        btn_layout.addWidget(self.btn_select_file)
        
        self.btn_select_folder = QPushButton("フォルダ選択")
        self.btn_select_folder.setStyleSheet(self._button_style())
        self.btn_select_folder.clicked.connect(self.select_folder)
        btn_layout.addWidget(self.btn_select_folder)
        
        file_layout.addLayout(btn_layout)
        
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 8px;
                background-color: #fafafa;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 6px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        file_layout.addWidget(self.file_list)
        
        self.btn_clear = QPushButton("クリア")
        self.btn_clear.setStyleSheet(self._button_style("#95a5a6"))
        self.btn_clear.clicked.connect(self.clear_files)
        file_layout.addWidget(self.btn_clear)
        
        layout.addWidget(self.file_area)
        
        # クリップボードエリア
        self.clipboard_area = QWidget()
        clipboard_layout = QVBoxLayout(self.clipboard_area)
        clipboard_layout.setSpacing(15)
        
        self.btn_load_clipboard = QPushButton("クリップボードから読み込み")
        self.btn_load_clipboard.setStyleSheet(self._button_style("#3498db"))
        self.btn_load_clipboard.clicked.connect(self.load_from_clipboard)
        clipboard_layout.addWidget(self.btn_load_clipboard)
        
        clipboard_info = QLabel("HTMLをコピーしてから\n読み込みボタンをクリックしてください")
        clipboard_info.setStyleSheet("""
            color: #7f8c8d;
            font-size: 12px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
        """)
        clipboard_info.setAlignment(Qt.AlignCenter)
        clipboard_info.setWordWrap(True)
        clipboard_layout.addWidget(clipboard_info)
        
        clipboard_layout.addStretch()
        
        layout.addWidget(self.clipboard_area)
        self.clipboard_area.setVisible(False)
        
        layout.addStretch()
        
        return panel
    
    def _create_right_panel(self):
        """右パネル"""
        panel = QWidget()
        panel.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # プレビュー
        preview_label = QLabel("プレビュー")
        preview_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #2c3e50;
        """)
        layout.addWidget(preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 12px;
                background-color: #fafafa;
                font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
                font-size: 12px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(self.preview_text, 1)
        
        # テンプレート
        template_label = QLabel("テンプレート")
        template_label.setStyleSheet(preview_label.styleSheet())
        layout.addWidget(template_label)
        
        self.template_combo = QComboBox()
        self.template_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
                background-color: white;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dcdde1;
                selection-background-color: #3498db;
            }
        """)
        self.template_combo.addItem("標準問題集", "standard")
        self.template_combo.addItem("定期試験", "exam")
        self.template_combo.addItem("宿題プリント", "homework")
        self.template_combo.addItem("テンプレートなし", "none")
        layout.addWidget(self.template_combo)
        
        return panel
    
    def _create_footer(self):
        """フッター"""
        footer = QWidget()
        footer.setStyleSheet("background-color: white; border-top: 1px solid #e0e0e0;")
        footer.setFixedHeight(120)
        
        layout = QVBoxLayout(footer)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)
        
        # プログレスバー
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                text-align: center;
                height: 8px;
                background-color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # ステータス
        self.status_label = QLabel("準備完了")
        self.status_label.setStyleSheet("""
            color: #7f8c8d;
            font-size: 12px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 変換ボタン
        self.btn_convert = QPushButton("Word文書に変換")
        self.btn_convert.setFixedHeight(44)
        self.btn_convert.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1a252f;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.btn_convert.clicked.connect(self.start_conversion)
        layout.addWidget(self.btn_convert)
        
        return footer
    
    def _button_style(self, color="#3498db"):
        """ボタンスタイル"""
        hover_color = self._adjust_brightness(color, 0.9)
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self._adjust_brightness(color, 0.8)};
            }}
        """
    
    def _adjust_brightness(self, hex_color, factor):
        """色の明度調整"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_input_mode_changed(self):
        """入力モード切り替え"""
        if self.radio_file.isChecked():
            self.file_area.setVisible(True)
            self.clipboard_area.setVisible(False)
        else:
            self.file_area.setVisible(False)
            self.clipboard_area.setVisible(True)
    
    def select_files(self):
        """ファイル選択"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "HTMLファイルを選択",
            str(Path.home()),
            "HTML Files (*.html *.htm)"
        )
        
        if files:
            self.input_files.extend(files)
            self._update_file_list()
            self._load_file_preview()
    
    def select_folder(self):
        """フォルダ選択"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "フォルダを選択",
            str(Path.home())
        )
        
        if folder:
            html_files = list(Path(folder).glob('*.html'))
            if html_files:
                self.input_files.extend([str(f) for f in html_files])
                self._update_file_list()
                self._load_file_preview()
    
    def clear_files(self):
        """ファイルリストをクリア"""
        self.input_files = []
        self._update_file_list()
        self.preview_text.clear()
    
    def _update_file_list(self):
        """ファイルリスト更新"""
        self.file_list.clear()
        for file_path in self.input_files:
            self.file_list.addItem(Path(file_path).name)
    
    def _load_file_preview(self):
        """ファイルプレビュー"""
        if self.input_files:
            try:
                with open(self.input_files[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                preview = content[:1000]
                if len(content) > 1000:
                    preview += "\n\n..."
                self.preview_text.setPlainText(preview)
                self.html_content = content
            except Exception as e:
                self.preview_text.setPlainText(f"エラー: {str(e)}")
    
    def load_from_clipboard(self):
        """クリップボードから読み込み"""
        try:
            self.html_content = pyperclip.paste()
            
            if not self.html_content.strip():
                QMessageBox.warning(self, "警告", "クリップボードが空です")
                return
            
            preview = self.html_content[:1000]
            if len(self.html_content) > 1000:
                preview += "\n\n..."
            
            self.preview_text.setPlainText(preview)
            
            parser = HTMLParser()
            problems = parser.parse(self.html_content)
            
            if problems:
                QMessageBox.information(
                    self,
                    "成功",
                    f"{len(self.html_content)}文字のHTMLを読み込みました\n\n{len(problems)}個の問題を検出"
                )
            else:
                QMessageBox.warning(
                    self,
                    "警告",
                    "HTMLは読み込みましたが、問題が検出されませんでした"
                )
            
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"読み込みエラー:\n{str(e)}")
    
    def start_conversion(self):
        """変換開始"""
        if self.radio_file.isChecked():
            if not self.input_files:
                QMessageBox.warning(self, "警告", "ファイルを選択してください")
                return
            try:
                with open(self.input_files[0], 'r', encoding='utf-8') as f:
                    self.html_content = f.read()
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"ファイル読み込みエラー:\n{str(e)}")
                return
        else:
            if not self.html_content.strip():
                QMessageBox.warning(self, "警告", "クリップボードからHTMLを読み込んでください")
                return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_name = f"converted_{timestamp}.docx"
        
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "保存先を選択",
            str(Path.home() / default_name),
            "Word Files (*.docx)"
        )
        
        if not output_file:
            return
        
        template_name = self.template_combo.currentData()
        kwargs = {}
        if template_name == 'exam':
            kwargs['school_name'] = '○○高等学校'
        elif template_name == 'homework':
            kwargs['date'] = datetime.now().strftime('%Y年%m月%d日')
        
        self.btn_convert.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.conversion_thread = ConversionThread(
            self.html_content,
            output_file,
            template_name,
            **kwargs
        )
        self.conversion_thread.progress.connect(self.on_progress)
        self.conversion_thread.finished.connect(self.on_finished)
        self.conversion_thread.start()
    
    def on_progress(self, value, message):
        """進捗更新"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def on_finished(self, success, message):
        """変換完了"""
        self.btn_convert.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("準備完了")
        
        if success:
            reply = QMessageBox.information(
                self,
                "完了",
                f"{message}\n\nファイルを開きますか？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                import subprocess
                import platform
                
                if platform.system() == 'Darwin':
                    subprocess.call(['open', self.conversion_thread.output_file])
        else:
            QMessageBox.critical(self, "エラー", message)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = UnifiedConverterGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
