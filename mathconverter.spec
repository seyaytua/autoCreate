# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# データファイルのリスト
datas = [
    ('src/core', 'src/core'),
    ('src/batch', 'src/batch'),
    ('src/validators', 'src/validators'),
    ('src/prompts', 'src/prompts'),
]

a = Analysis(
    ['src/unified_gui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'pyperclip',
        'matplotlib.backends.backend_agg',
        'PIL._imaging',
        'docx',
        'bs4',
        'lxml.etree',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MathConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS用アプリバンドル
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='MathConverter.app',
        icon=None,
        bundle_identifier='com.seyaytua.mathconverter',
        info_plist={
            'CFBundleName': 'MathConverter',
            'CFBundleDisplayName': '数学問題変換システム',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
        },
    )
