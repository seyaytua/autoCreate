# GitHub Actionsワークフロー修正手順

## 問題
1. GitHub Appの権限制限により、`.github/workflows/build-release.yml`の変更を自動的にプッシュできません
2. PowerShellの行継続文字（バッククォート `）が欠落していたため、Windows版ビルドが失敗していました

## 🔴 緊急修正が必要

### GitHubのWeb UIで直接編集してください：

1. https://github.com/seyaytua/autoCreate/blob/main/.github/workflows/build-release.yml にアクセス
2. 右上の鉛筆アイコン（Edit this file）をクリック
3. 以下の変更を適用

## 手動で適用する変更

### Mac版ビルド（43-49行目）

**変更前：**
```yaml
--collect-all=pyperclip \
--collect-all=matplotlib \
--collect-all=PySide6 \
--collect-all=PIL
--collect-all=docx
--collect-all=bs4
--collect-all=lxml
src/unified_gui.py
```

**変更後：**
```yaml
--collect-all=pyperclip \
--collect-all=matplotlib \
--collect-all=PySide6 \
--collect-all=PIL \
--collect-all=docx \
--collect-all=bs4 \
--collect-all=lxml \
src/unified_gui.py
```

### Windows版ビルド（102-109行目）

**変更前：**
```yaml
--collect-all=pyperclip \
--collect-all=matplotlib \
--collect-all=PySide6 \
--collect-all=PIL
--collect-all=docx
--collect-all=bs4
--collect-all=lxml
src/unified_gui.py
```

**変更後：**
```yaml
--collect-all=pyperclip `
--collect-all=matplotlib `
--collect-all=PySide6 `
--collect-all=PIL `
--collect-all=docx `
--collect-all=bs4 `
--collect-all=lxml `
src/unified_gui.py
```

**⚠️ 重要：** Windows版は行継続にバッククォート（`）を使用します！

## 差分の全体

```diff
diff --git a/.github/workflows/build-release.yml b/.github/workflows/build-release.yml
index 20a66f9..23f1cec 100644
--- a/.github/workflows/build-release.yml
+++ b/.github/workflows/build-release.yml
@@ -43,6 +43,10 @@ jobs:
             --collect-all=pyperclip \
             --collect-all=matplotlib \
             --collect-all=PySide6 \
+            --collect-all=PIL \
+            --collect-all=docx \
+            --collect-all=bs4 \
+            --collect-all=lxml \
             src/unified_gui.py
       
       - name: Create DMG
@@ -98,6 +102,10 @@ jobs:
             --collect-all=pyperclip `
             --collect-all=matplotlib `
             --collect-all=PySide6 `
+            --collect-all=PIL `
+            --collect-all=docx `
+            --collect-all=bs4 `
+            --collect-all=lxml `
             src/unified_gui.py
       
       - name: Create ZIP
```

## 適用後の確認

変更を適用後、新しいタグをプッシュしてビルドをテストしてください：

```bash
git tag v1.0.1
git push origin v1.0.1
```

ビルドされた実行ファイルをダウンロードして、pyperclipエラーが解消されていることを確認してください。
