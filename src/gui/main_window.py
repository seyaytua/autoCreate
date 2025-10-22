"""メインGUIウィンドウ"""
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFileDialog, QComboBox,
    QGroupBox, QMessageBox, QProgressBar, QListWidget, QSplitter
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QTextCursor

# 親ディレクトリのモジュールをインポート
sys.path.append(str(Path(__file__).parent.parent))

from core import STYLE_CONFIG, HTMLParser, MathConverter, WordGenerator
from validators.html_validator import HTMLValidator
from batch.unified_converter import UnifiedMathConverter

class ConversionThread(QThread):
    """変換処理を別スレッドで実行"""
    progress = Signal(int, str)
    finished = Signal(bool, str)
    
    def __init__(self, input_files, output_file, mode='single'):
        super().__init__()
        self.input_files = input_files
        self.output_file = output_file
        self.mode = mode
    
    def run(self):
        try:
            if self.mode == 'unified':
                # 統合変換
                converter = UnifiedMathConverter()
                
                all_problems = []
                for i, html_file in enumerate(self.input_files, 1):
                    self.progress.emit(
                        int(i / len(self.input_files) * 50),
                        f"読み込み中: {Path(html_file).name}"
                    )
                    
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    problems = converter.parser.parse(html_content)
                    all_problems.extend(problems)
                
                self.progress.emit(75, "Word文書を生成中...")
                
                # 問題番号を振り直す
                for i, problem in enumerate(all_problems, 1):
                    if not problem['title'] or problem['title'].startswith('大問'):
                        problem['title'] = f'大問{i}'
                
                doc = converter.generator.create_document(all_problems)
                doc.save(self.output_file)
                
                self.progress.emit(100, "完了")
                self.finished.emit(True, f"✓ 変換完了\n{len(all_problems)}問を統合しました")
            
            else:
                # 単一ファイル変換
                parser = HTMLParser()
                math_converter = MathConverter(STYLE_CONFIG)
                generator = WordGenerator(STYLE_CONFIG, math_converter)
                
                self.progress.emit(25, "HTMLを解析中...")
                
                with open(self.input_files[0], 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                problems = parser.parse(html_content)
                
                self.progress.emit(50, "Word文書を生成中...")
                
                doc = generator.create_document(problems)
                doc.save(self.output_file)
                
                self.progress.emit(100, "完了")
                self.finished.emit(True, f"✓ 変換完了\n{len(problems)}問を変換しました")
        
        except Exception as e:
            self.finished.emit(False, f"✗ エラー: {str(e)}")

class MainWindow(QMainWindow):
    """メインウィンドウ"""
    
    def __init__(self):
        super().__init__()
        self.input_files = []
        self.output_file = ""
        
        self.init_ui()
    
    def init_ui(self):
        """UIを初期化"""
        self.setWindowTitle("数学問題変換システム - Phase 3")
        self.setGeometry(100, 100, 1000, 700)
        
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QVBoxLayout(central_widget)
        
        # タイトル
        title_label = QLabel("数学問題変換システム")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # スプリッター（左右分割）
        splitter = QSplitter(Qt.Horizontal)
        
        # 左側：ファイル選択エリア
        left_widget = self._create_file_selection_area()
        splitter.addWidget(left_widget)
        
        # 右側：プレビュー・ログエリア
        right_widget = self._create_preview_area()
        splitter.addWidget(right_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        # 下部：変換ボタンとプログレスバー
        bottom_layout = self._create_bottom_area()
        main_layout.addLayout(bottom_layout)
    
    def _create_file_selection_area(self):
        """ファイル選択エリアを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 入力ファイル選択
        input_group = QGroupBox("入力ファイル")
        input_layout = QVBoxLayout(input_group)
        
        # ボタン
        btn_layout = QHBoxLayout()
        
        self.btn_select_file = QPushButton("ファイルを選択")
        self.btn_select_file.clicked.connect(self.select_input_files)
        btn_layout.addWidget(self.btn_select_file)
        
        self.btn_select_folder = QPushButton("フォルダを選択")
        self.btn_select_folder.clicked.connect(self.select_input_folder)
        btn_layout.addWidget(self.btn_select_folder)
        
        input_layout.addLayout(btn_layout)
        
        # ファイルリスト
        self.file_list = QListWidget()
        input_layout.addWidget(self.file_list)
        
        # クリアボタン
        self.btn_clear = QPushButton("クリア")
        self.btn_clear.clicked.connect(self.clear_file_list)
        input_layout.addWidget(self.btn_clear)
        
        layout.addWidget(input_group)
        
        # 出力設定
        output_group = QGroupBox("出力設定")
        output_layout = QVBoxLayout(output_group)
        
        # 変換モード
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("変換モード:"))
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("単一ファイル変換", "single")
        self.mode_combo.addItem("統合変換（1つの文書に）", "unified")
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        
        output_layout.addLayout(mode_layout)
        
        # 出力ファイル
        output_file_layout = QHBoxLayout()
        self.output_label = QLabel("出力先: 未設定")
        output_file_layout.addWidget(self.output_label)
        
        self.btn_select_output = QPushButton("選択")
        self.btn_select_output.clicked.connect(self.select_output_file)
        output_file_layout.addWidget(self.btn_select_output)
        
        output_layout.addLayout(output_file_layout)
        
        layout.addWidget(output_group)
        
        # 検証ボタン
        self.btn_validate = QPushButton("HTMLを検証")
        self.btn_validate.clicked.connect(self.validate_html)
        layout.addWidget(self.btn_validate)
        
        return widget
    
    def _create_preview_area(self):
        """プレビュー・ログエリアを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # ログ表示
        log_group = QGroupBox("ログ")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier", 10))
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        return widget
    
    def _create_bottom_area(self):
        """下部エリアを作成"""
        layout = QVBoxLayout()
        
        # プログレスバー
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # ステータスラベル
        self.status_label = QLabel("準備完了")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 変換ボタン
        button_layout = QHBoxLayout()
        
        self.btn_convert = QPushButton("変換開始")
        self.btn_convert.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.btn_convert.clicked.connect(self.start_conversion)
        button_layout.addWidget(self.btn_convert)
        
        layout.addLayout(button_layout)
        
        return layout
    
    def select_input_files(self):
        """入力ファイルを選択"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "HTMLファイルを選択",
            str(Path.home()),
            "HTML Files (*.html *.htm)"
        )
        
        if files:
            self.input_files.extend(files)
            self._update_file_list()
            self.log(f"✓ {len(files)}個のファイルを追加しました")
    
    def select_input_folder(self):
        """入力フォルダを選択"""
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
                self.log(f"✓ {len(html_files)}個のファイルを追加しました")
            else:
                self.log("⚠ HTMLファイルが見つかりませんでした")
    
    def clear_file_list(self):
        """ファイルリストをクリア"""
        self.input_files = []
        self._update_file_list()
        self.log("✓ ファイルリストをクリアしました")
    
    def _update_file_list(self):
        """ファイルリストを更新"""
        self.file_list.clear()
        for file_path in self.input_files:
            self.file_list.addItem(Path(file_path).name)
    
    def select_output_file(self):
        """出力ファイルを選択"""
        file, _ = QFileDialog.getSaveFileName(
            self,
            "出力ファイルを指定",
            str(Path.home() / "output.docx"),
            "Word Files (*.docx)"
        )
        
        if file:
            self.output_file = file
            self.output_label.setText(f"出力先: {Path(file).name}")
            self.log(f"✓ 出力先を設定: {file}")
    
    def on_mode_changed(self):
        """変換モードが変更された"""
        mode = self.mode_combo.currentData()
        if mode == 'unified':
            self.log("📝 統合モード: 複数ファイルを1つの文書に統合します")
        else:
            self.log("📝 単一ファイルモード: 1つのファイルを変換します")
    
    def validate_html(self):
        """HTMLを検証"""
        if not self.input_files:
            QMessageBox.warning(self, "警告", "入力ファイルを選択してください")
            return
        
        self.log("\n=== HTML検証開始 ===")
        
        validator = HTMLValidator()
        
        for file_path in self.input_files:
            self.log(f"\n検証中: {Path(file_path).name}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                is_valid, errors, warnings = validator.validate(html_content)
                
                if is_valid:
                    self.log("  ✓ 検証OK")
                else:
                    self.log("  ✗ エラーあり")
                    for error in errors:
                        self.log(f"    - {error}")
                
                if warnings:
                    self.log("  ⚠ 警告:")
                    for warning in warnings:
                        self.log(f"    - {warning}")
            
            except Exception as e:
                self.log(f"  ✗ エラー: {str(e)}")
        
        self.log("\n=== 検証完了 ===\n")
    
    def start_conversion(self):
        """変換を開始"""
        # 入力チェック
        if not self.input_files:
            QMessageBox.warning(self, "警告", "入力ファイルを選択してください")
            return
        
        if not self.output_file:
            QMessageBox.warning(self, "警告", "出力ファイルを指定してください")
            return
        
        # モード取得
        mode = self.mode_combo.currentData()
        
        if mode == 'single' and len(self.input_files) > 1:
            reply = QMessageBox.question(
                self,
                "確認",
                f"{len(self.input_files)}個のファイルが選択されていますが、\n"
                "単一ファイルモードでは最初のファイルのみが変換されます。\n"
                "続行しますか？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        # UIを無効化
        self.btn_convert.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.log("\n=== 変換開始 ===")
        
        # 変換スレッドを開始
        self.conversion_thread = ConversionThread(
            self.input_files,
            self.output_file,
            mode
        )
        self.conversion_thread.progress.connect(self.on_progress)
        self.conversion_thread.finished.connect(self.on_finished)
        self.conversion_thread.start()
    
    def on_progress(self, value, message):
        """進捗更新"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        self.log(message)
    
    def on_finished(self, success, message):
        """変換完了"""
        self.log(message)
        self.log("\n=== 変換完了 ===\n")
        
        # UIを有効化
        self.btn_convert.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("準備完了")
        
        if success:
            reply = QMessageBox.information(
                self,
                "完了",
                f"{message}\n\n出力ファイルを開きますか？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.open_output_file()
        else:
            QMessageBox.critical(self, "エラー", message)
    
    def open_output_file(self):
        """出力ファイルを開く"""
        import subprocess
        import platform
        
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', self.output_file])
            elif platform.system() == 'Windows':
                subprocess.call(['start', self.output_file], shell=True)
            else:  # Linux
                subprocess.call(['xdg-open', self.output_file])
        except Exception as e:
            self.log(f"ファイルを開けませんでした: {str(e)}")
    
    def log(self, message):
        """ログを追加"""
        self.log_text.append(message)
        # 自動スクロール
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)

def main():
    app = QApplication(sys.argv)
    
    # スタイルシート
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
