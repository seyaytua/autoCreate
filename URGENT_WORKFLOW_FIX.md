# 🚨 緊急：ワークフローファイル修正が必要

## 問題
v1.0.5のビルドが失敗しました。原因は`.github/workflows/build-release.yml`の行継続文字の混在です。

## エラー内容
- **Mac版**: `pyinstaller: error: the following arguments are required: scriptname`
- **Windows版**: `ParserError: Missing expression after unary operator '--'`

## 修正手順

### 方法1: GitHub Web UIで直接編集（推奨）

1. GitHubでファイルを開く：
   https://github.com/seyaytua/autoCreate/edit/main/.github/workflows/build-release.yml

2. **Mac版ビルド**（26-50行目付近）を以下のように修正：
   ```yaml
   - name: Build with PyInstaller
     run: |
       pyinstaller --name="MathConverter-Mac" \
         --windowed \
         --onefile \
         --add-data "src:src" \
         --hidden-import=PySide6.QtCore \
         --hidden-import=PySide6.QtGui \
         --hidden-import=PySide6.QtWidgets \
         --hidden-import=pyperclip \
         --hidden-import=matplotlib \
         --hidden-import=matplotlib.backends.backend_agg \
         --hidden-import=PIL \
         --hidden-import=PIL._imaging \
         --hidden-import=docx \
         --hidden-import=bs4 \
         --hidden-import=lxml \
         --collect-all=pyperclip \
         --collect-all=matplotlib \
         --collect-all=PySide6 \
         --collect-all=PIL \
         --collect-all=docx \
         --collect-all=bs4 \
         --collect-all=lxml \
         src/unified_gui.py
   ```
   ⚠️ 重要：**すべての行末に `\` があることを確認**

3. **Windows版ビルド**（86-109行目付近）を以下のように修正：
   ```yaml
   - name: Build with PyInstaller
     run: |
       pyinstaller --name="MathConverter-Win" `
         --windowed `
         --onefile `
         --add-data "src;src" `
         --hidden-import=PySide6.QtCore `
         --hidden-import=PySide6.QtGui `
         --hidden-import=PySide6.QtWidgets `
         --hidden-import=pyperclip `
         --hidden-import=matplotlib `
         --hidden-import=matplotlib.backends.backend_agg `
         --hidden-import=PIL `
         --hidden-import=PIL._imaging `
         --hidden-import=docx `
         --hidden-import=bs4 `
         --hidden-import=lxml `
         --collect-all=pyperclip `
         --collect-all=matplotlib `
         --collect-all=PySide6 `
         --collect-all=PIL `
         --collect-all=docx `
         --collect-all=bs4 `
         --collect-all=lxml `
         src/unified_gui.py
   ```
   ⚠️ 重要：**すべての行末に `` ` `` （バッククォート）があることを確認**

4. コミットメッセージ：
   ```
   fix: Correct line continuation in workflow file
   ```

5. "Commit changes" をクリック

### 修正のポイント

#### ❌ 誤り（現在の状態）
```yaml
--collect-all=PIL
--collect-all=docx    # ← 行継続文字がない！
--collect-all=bs4
--collect-all=lxml
```

#### ✅ 正しい修正

**Mac版（バックスラッシュ）：**
```yaml
--collect-all=PIL \
--collect-all=docx \
--collect-all=bs4 \
--collect-all=lxml \
```

**Windows版（バッククォート）：**
```yaml
--collect-all=PIL `
--collect-all=docx `
--collect-all=bs4 `
--collect-all=lxml `
```

## 修正後の手順

1. 修正をコミットして保存
2. 新しいタグを作成：
   ```bash
   git pull origin main
   git tag -a v1.0.6 -m "Fix workflow syntax error"
   git push origin v1.0.6
   ```
3. GitHub Actionsでビルドが成功することを確認

## なぜこの修正が必要か

- **Mac/Linux**: シェルスクリプトでは行継続に `\` を使用
- **Windows PowerShell**: 行継続に `` ` `` を使用
- 行継続文字がないと、複数行のコマンドが別々のコマンドとして解釈されエラーになる

