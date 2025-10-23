#!/bin/bash

echo "ローカルビルドを開始します..."

# PyInstallerをインストール
pip install pyinstaller

# ビルド実行
pyinstaller build.spec

echo ""
echo "ビルド完了"
echo ""
echo "Mac: dist/MathConverter.app"
echo "Windows: dist/MathConverter.exe"
