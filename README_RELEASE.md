# リリース手順

## 1. ローカルでテスト

```bash
# ローカルビルド
./build_local.sh

# 動作確認
open dist/MathConverter.app  # Mac
# または
dist/MathConverter.exe  # Windows
2. バージョンタグを作成
Copy# タグを作成
git tag v1.0.0

# タグをプッシュ
git push origin v1.0.0
3. GitHub Actionsが自動実行
Mac用 .dmg ファイルをビルド
Windows用 .zip ファイルをビルド
GitHubのReleasesページに公開
4. リリースページで確認
https://github.com/seyaytua/autoCreate/releases

バージョン番号の付け方
メジャーバージョン: v1.0.0 → v2.0.0 (大きな変更)
マイナーバージョン: v1.0.0 → v1.1.0 (機能追加)
パッチバージョン: v1.0.0 → v1.0.1 (バグ修正)
手動でワークフローを実行
GitHubのリポジトリページ:

"Actions" タブをクリック
"Build and Release" を選択
"Run workflow" をクリック
