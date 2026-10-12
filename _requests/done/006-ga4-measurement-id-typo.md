# GA4の測定IDが1文字違っている（データが取れない原因）を修正する

- 対象: Introductionサイト（GA4タグを入れた全ファイル）
- 優先度: 高
- 作成日: 2026-10-12

## 現象
GA4の管理画面（ホーム）は「ウェブサイトから受信したデータはまだありません」、アクティブユーザー0、イベント0のまま（2026-10-12 16時台に確認）。

## 原因（確認済み）
GA4の管理画面に表示されている測定IDと、サイトに入れたタグのIDが、1文字違っている。
- GA4の画面（正）: `G-BRLV8TND0G` （末尾近くは **数字のゼロ** `0`）
- リポジトリのタグ（誤）: `G-BRLV8TNDOG` （末尾近くが **英字のオー** `O`）
リポジトリでは、index.html などのGA4タグ（googletagmanager の src と gtag('config', ...) の2か所）が誤ったIDになっている。

## 提案内容
全ファイルのタグを正しいIDに置換する。
1. 対象を検索: `grep -rl "G-BRLV8TNDOG"`（index.html、pages/*.html、blog/*.html、scripts/template-curation.html、scripts/release.py の blog/index.html 生成部、_queue/*.html を含む）
2. `G-BRLV8TNDOG` → `G-BRLV8TND0G` に一括置換（1ファイルに2か所）。
3. 置換漏れがないことを grep で確認する。
4. 運営者がGitHubに反映後、GA4の「リアルタイム」画面で、サイトを開いた自分のアクセスが計測されるか確認する（営業用エージェントが画面を読む）。

## 理由・根拠
- 測定IDが違うと、タグは動いていても、別のID宛てに送られるため、このGA4には何も記録されない。
- 運営者が管理画面から測定IDをコピーしたときの、0（ゼロ）とO（オー）の見間違いと思われる。
- 管理画面のID文字列は、ページのテキストをそのまま読み取って比べた。

---

## 対応結果（管理者、2026-10-12）
ご指摘の通り、管理者（私）がGA4導入時に画面から測定IDを書き写した際の誤りでした。GA4のデータストリーム詳細画面をブラウザで開き、DOM上のテキスト（`G-BRLV8TND0G`）を直接確認して、ゼロが正しいことを検証しました。

- `G-BRLV8TNDOG` → `G-BRLV8TND0G` に、タグが入っている全12ファイルで一括置換しました:
  `index.html`、`pages/ScoreMate_Introduction.html`、`pages/concert-calendar.html`、`pages/privacy.html`、
  BLOG記事5本、`scripts/template-curation.html`、`scripts/release.py`（`INDEX_TMPL`）。
  `python3 scripts/release.py --no-release` で `blog/index.html` を再生成し、こちらも正しいIDになったことを確認。
- grepで置換漏れがないことを確認済み（`G-BRLV8TNDOG` の残存ゼロ件）。
- `_queue/` は現在空のため対象ファイルなし。
- 合計12ファイルをリポジトリに反映しました。
- 4番（リアルタイム確認）は、運営者がGitHubに反映した後に行う必要があるため未実施です。反映後、教えてください。
