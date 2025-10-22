"""GUIアプリケーションのランチャー"""
import sys
from pathlib import Path

# srcディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from gui.main_window import main

if __name__ == '__main__':
    main()
