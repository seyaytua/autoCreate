#!/bin/bash

echo "ローカルビルドを開始します..."
echo ""

# 仮想環境を有効化
if [ ! -d "venv" ]; then
    echo "仮想環境を作成中..."
    python3 -m venv venv
fi

source venv/bin/activate

# 依存関係をインストール
echo "依存関係をインストール中..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# ビルド実行
echo ""
echo "PyInstallerでビルド中..."
pyinstaller mathconverter.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "✓ ビルド完了"
    echo "============================================"
    echo ""
    
    if [ "$(uname)" == "Darwin" ]; then
        echo "Mac用アプリ:"
        echo "  dist/MathConverter.app"
        echo ""
        echo "起動:"
        echo "  open dist/MathConverter.app"
    else
        echo "実行ファイル:"
        echo "  dist/MathConverter"
        echo ""
        echo "起動:"
        echo "  ./dist/MathConverter"
    fi
else
    echo ""
    echo "✗ ビルドに失敗しました"
fi
