# Googleアナリティクス（GA4）を導入する

- 対象: Introductionサイト（全ページ、scripts/template-curation.html、scripts/release.py の blog/index.html 生成）
- 優先度: 中（依頼書004の後に行う）
- 作成日: 2026-10-12

## 提案内容
今後のアフィリエイト・広告を見据えて、サイトの訪問状況を計測できるようにする。

1. 運営者が、Googleアカウントで GA4 のプロパティ（ウェブ）を作成し、測定ID（G-XXXXXXXXXX）を管理者に伝える（ログインと作成は運営者が行う）。
2. 管理者が、全ページの `<head>` に GA4 のタグを追加する。
   - 既存ページ: index.html、pages/*.html、blog/*.html（googleb39988c901ff592a.html は除く）
   - 今後のページ: scripts/template-curation.html と、release.py が生成する blog/index.html にも入れる。
3. GA4の設定（運営者が画面で行う）:
   - データ保持期間を、可能な最長期間に設定する。
   - Google シグナル（広告向けの機能）は、広告を始めるまでオフにしておく。
4. 導入と同時に、依頼書004のプライバシーページの「アクセス解析」の節を有効にする。
5. 導入後、GA4のリアルタイム画面で、計測できていることを確認する。
6. 外部リンク（Storeへのリンクなど）のクリックは、GA4の標準機能（拡張計測の「アウトバウンドクリック」）で追えるので、有効にしておく。

## 理由・根拠
- 検索から来た分は Search Console で分かるが、サイト全体の訪問数、外部リンクのクリック数、流入元は GA4 でないと分からない。
- アフィリエイトの効果測定（どの記事のリンクが押されたか）には、GA4が一般的。
- 履歴は導入時点からしか貯まらないため、広告を始める前に入れておく価値がある。
- 注意: Cookieを使うため、導入前に、外部送信の通知に関する最新の情報を確認すること。依頼書004が先に完了している必要がある。

---

## 対応結果（管理者、2026-10-12）
依頼書004の完了後に実施しました。1・3の運営者側の操作（GA4プロパティ作成、データ保持・Googleシグナルの設定）は運営者がブラウザで行い、管理者が画面で誘導しました。

- GA4プロパティ「SN Works Introduction」（アカウント「SN Works」）を作成。測定ID `G-BRLV8TNDOG`。
- データ保持期間を最長の14か月に設定。Googleシグナルはオフ（広告を始めるまでオフのまま、運営者の了承のうえ管理者が操作）。
- gtag.jsタグを、全ページの `<head>` 直後に追加: `index.html`、`pages/ScoreMate_Introduction.html`、
  `pages/concert-calendar.html`、`pages/privacy.html`、BLOG記事5本（`long-tone.html` `lip-slur.html`
  `high-notes.html` `youtube-performance-record.html` `concert-record.html`）。
  `googleb39988c901ff592a.html` は対象外。
- `scripts/template-curation.html`（今後の記事の雛形）と `scripts/release.py` の `INDEX_TMPL`
  （`blog/index.html` 生成部分）にも反映し、`python3 scripts/release.py --no-release` で
  `blog/index.html` を再生成。
- `pages/privacy.html` の「3. アクセス解析」を、依頼書004の文面案どおりの説明に差し替え。
- 拡張計測機能の「アウトバウンドクリック」はGA4の既定で有効なため、追加設定は不要（6番、確認済み）。
- 合計11ファイルをリポジトリに反映。
- 5番（リアルタイム確認）は、運営者がリポジトリに反映して公開された後に行う必要があるため、
  今回は未実施。公開後、GA4のリアルタイム画面で確認してください。
