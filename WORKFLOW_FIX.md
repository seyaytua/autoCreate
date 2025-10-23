# GitHub Actionsワークフロー修正手順

## 問題
GitHub Appの権限制限により、`.github/workflows/build-release.yml`の変更を自動的にプッシュできません。

## 手動で適用する変更

`.github/workflows/build-release.yml`の以下の箇所に`--collect-all`フラグを追加してください：

### Mac版ビルド（26行目付近）
```yaml
--collect-all=pyperclip \
--collect-all=matplotlib \
--collect-all=PySide6 \
--collect-all=PIL \          # ← 追加
--collect-all=docx \         # ← 追加
--collect-all=bs4 \          # ← 追加
--collect-all=lxml \         # ← 追加
src/unified_gui.py
```

### Windows版ビルド（98行目付近）
```yaml
--collect-all=pyperclip `
--collect-all=matplotlib `
--collect-all=PySide6 `
--collect-all=PIL `          # ← 追加
--collect-all=docx `         # ← 追加
--collect-all=bs4 `          # ← 追加
--collect-all=lxml `         # ← 追加
src/unified_gui.py
```

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
