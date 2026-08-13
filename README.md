# lai-ig-poster

**@lai_japanese**（実写ライ・ペルソナ）の Instagram 自動投稿。
@laifu_japanese 用 `laifu-ig-poster` の姉妹リポで、**中身は同じ骨組み・デザインだけ別**
（Didot＋明朝＋金稲妻のエレガント版。Impact/コーラルは混ぜない）。

毎日 21:00 JST に GitHub Actions が `drafts/YYYY-MM-queue.csv` の最上段（未投稿・承認済み）を
FIFO で1本 Instagram Graph API に公開する。

## しくみ

- `scripts/post_to_instagram.py` … カルーセル/リールを1本 publish。画像は公開HTTPS URLが必須なので、
  この repo を **public** にして `raw.githubusercontent.com/<owner>/<repo>/main/...` で配信する。
- `.github/workflows/post-scheduled.yml` … 毎日 21:00 JST の cron ＋ 手動 `Run workflow`（dry_run対応）。
- `.github/workflows/refresh-token.yml` … 60日トークンの月次延長（恒久Pageトークンなら無効化可）。
- `drafts/*.csv` … 投稿キュー。`status` 空欄＝承認、`draft/hold/skip` はスキップ。
- `posts/<slug>/1..N.jpg` … スライド画像（＋任意 `caption.md`）。

## 投稿を出す

1. `posts/<slug>/` に画像（と caption.md）を置く
2. `drafts/YYYY-MM-queue.csv` に行を足し、`status` を空欄に
3. push。あとは cron が拾う。急ぎは Actions → Run workflow（dry_run=0）

デザイン生成は `../lai-ig-persona/lai_carousel_builder.py`。セットアップ手順は `SETUP.md`。
