# SETUP — lai-ig-poster（実写ライ @lai_japanese）

@laifu_japanese 用 `laifu-ig-poster` の姉妹。**別アカウント・別デザイン**（エレガント版）。
一度セットすれば、あとは push とキュー承認だけで毎日1本ハンズオフ投稿。

## 確定値（2026-08-13）

| キー | 値 |
|---|---|
| IG_USER_ID (@lai_japanese) | `17841438629935291` |
| Lai FB page_id | `1252151484646929` |
| Meta app = Laifu Social | `2248231139271837`（FB_APP_ID） |
| FB_APP_SECRET | Laifu Social のシークレット（`laifu-ig-poster/.env` に既存＝流用） |

> 投稿用アプリは @laifu_japanese と**同じ Laifu Social**。だから App Secret はもう手元にある。

## 1. トークンを用意（残タスク・Ryuseiのクリック1回）

投稿には `instagram_content_publish` を持つトークンが要る。**恒久Pageトークン**が理想（失効しない）。

1. **Graph API Explorer**（自動操作だと固まるのでここだけ手動）
   https://developers.facebook.com/tools/explorer/
   - App = **Laifu Social**（2248231139271837）
   - `Generate Access Token` → 7 scope を許可
     （pages_show_list / instagram_basic / instagram_content_publish /
      instagram_manage_messages / instagram_manage_comments / pages_read_engagement / business_management）
   - 出た **User Token** をコピーして Claude に渡す
2. あとは Claude が自動でやる:
   - `fb_exchange_token`（Laifu Social secret）で 60日 long-lived user token に
   - `GET /1252151484646929?fields=access_token` で **恒久 Page トークン**を取得
   - それを `IG_TOKEN` に使う

## 2. GitHub リポジトリ

```bash
cd 04-marketing-department/lai-ig-poster
git init && git add . && git commit -m "init lai ig poster"
gh repo create lai-ig-poster --private --source=. --push
```

## 3. Secrets（repo → Settings → Secrets and variables → Actions）

| 種別 | 名前 | 中身 |
|---|---|---|
| Secret | `IG_USER_ID` | `17841438629935291` |
| Secret | `IG_TOKEN` | 恒久Pageトークン（手順1） |
| Secret | `FB_APP_ID` | `2248231139271837`（延長運用する場合のみ） |
| Secret | `FB_APP_SECRET` | Laifu Social secret（同上） |
| Secret | `GH_PAT` | `secrets:write` PAT（同上・トークン自動更新用） |

> **恒久Pageトークンなら** `FB_APP_ID/SECRET/GH_PAT` と `refresh-token.yml` は不要（ワークフロー無効化でOK）。

## 4. 本番前チェック（dry run）

Actions → **Post Lai carousel → Run workflow → dry_run = 1**。
ログの `image_url` と `caption` を確認し、URL をブラウザで開いて画像が出れば準備OK。
（private repo だと raw URL が開けない → public repo か公開バケットに）

## 5. 稼働

`drafts/YYYY-MM-queue.csv` の出したい行の `status` を空欄に。
毎日 21:00 JST に FIFO で最上段から1本。急ぎは `Run workflow`（dry_run=0）で即時。

## デザインの出所

画像は `lai-ig-persona/lai_carousel_builder.py`（Didot＋明朝＋金稲妻のエレガント版）で生成し、
`posts/<slug>/1..N.jpg` に置く。@laifu_japanese の Impact/コーラル版とは**混ぜない**。

## トラブル時

- `(#10) ... permission`: `instagram_content_publish` 不足
- `media ... not ready`: コンテナ処理待ち（スクリプトが FINISHED を待つので通常自動解消）
- 画像が出ない: `PUBLIC_BASE_URL` か repo 公開設定（IG は公開URLしか取れない）
