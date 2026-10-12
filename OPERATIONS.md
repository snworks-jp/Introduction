# コラム運用手順（管理者＝コード作成担当のClaudeセッション向け）

目的: SN Works の BLOG に、金管楽器の上達に役立つコラムを週1回公開する。
体制: ブログ用エージェントが記事の「準備」だけを行い、`_drafts/`に記事案を置く。
実際のファイル化・公開作業は**管理者（このセッション）が行う**（ブログ用エージェントは
`_queue/` `blog/` `index.html` `sitemap.xml` に触らず、`release.py`も実行しない）。
GitHubへの反映は運営者（二階堂）が自分で行う（管理者もpushしない）。

## 場所
- リポジトリ `snworks-jp/Introduction`（GitHub Pages: https://snworks-jp.github.io/Introduction/）
- `_drafts/` … ブログ用エージェントが置いた記事案（準備段階、まだHTML化前）。ルール書: `_drafts/README.md`
- `_requests/` … 営業用エージェントの依頼書置き場。ルール書: `_requests/README.md`
- `_requests/current-store-listing.md` … Store掲載文の現状スナップショット（管理者が更新）
- `_queue/` … 公開待ちの記事。`NNN-スラッグ.html`（NNN=公開順）。公開されない（`_`始まり）
- `_queue/themes.md` … テーマ計画（悩み別5テーマ／毎月第1週は楽器月間）
- `scripts/template-curation.html` … note紹介記事の雛形（＠＠…＠＠ を埋める）
- `scripts/release.py` … 公開処理
- `pages/privacy.html` … サイト用プライバシーポリシー（管理者が更新）

## 管理者の作業（記事案を受け取ってから）
1. `_drafts/` にある記事案を確認する。項目（テーマ名・候補タイトル・引用元3本・要点3行・
   カード用の一言・除外確認）が揃っているか、引用が適切か（有料／転載禁止／アフィリエイト色が
   強いものが混ざっていないか）をレビューする。
2. 問題なければ `scripts/template-curation.html` を複製し、記事案の内容で埋める。
   `__SLUG__` `__DATE__` `__DATE_JA__` は公開時に置換されるので雛形のまま残す。
   雛形には `<meta name="category" content="column">` が既定で入っている
   （お悩み解決シリーズ・楽器月間特集はすべて「コラム」扱いでよい）。
   雛形のフッターには「プライバシーポリシー」へのリンクが既定で入っている（下記参照）。
3. `_queue/NNN-スラッグ.html` として置く。
4. 対応済みの記事案は `_drafts/done/` に移動する。
5. 運営者から「公開して」と言われたら、公開処理を実行する。

## 公開（「公開して」と言われたとき）
```
python3 scripts/release.py              # 日本時間の今日付けで先頭の1本を公開
python3 scripts/release.py --date 2026-10-19   # 日付指定
```
実行すると、次が更新される:
- `blog/スラッグ.html`（新規） / `blog/index.html` / `index.html`（BLOGカード） / `sitemap.xml`
この4ファイルを運営者に渡す（SendUserFile）。運営者がリポジトリに上げて公開される。
上げたあと、公開URLの表示確認、Search Console で `blog/` と新記事の URL 検査→インデックス登録リクエスト（必要なら）。

## 一覧ページの見え方（2026-10-12改修）
`blog/index.html`とトップページのBLOGカードには、各記事の公開日を表示している。
また`blog/index.html`は記事の`category`メタタグで「コラム」「お知らせ」の2セクションに分けて表示する
（`announcement`のみお知らせ、それ以外はすべてコラム）。ScoreMateの機能紹介など、コラムシリーズ外の
記事を作るときは、`<meta name="category" content="announcement">` を入れること。
件数がさらに増えてきたら、ページ分割（「もっと見る」での区切り）や楽器月間特集ごとのまとめ表示を
追加で検討する。

## サイトのプライバシーポリシー（2026-10-12 追加）
`pages/privacy.html` に、サイト用（ScoreMateアプリ用とは別）のプライバシーポリシーを設置した。
演奏会カレンダーの投稿情報の扱い、外部情報（コンサートスクウェアのRSS）の掲載、アクセス解析・
広告の現状、ScoreMateアプリ用ポリシーへの案内、連絡先（scoremate.feedback@gmail.com）、改定に
ついての7項目構成。連絡先・ポリシーを公開する方針は運営者了承済み（2026-10-12）。

全ページ（トップ、アプリ紹介、演奏会カレンダー、BLOG一覧、記事ページ）のフッターに
「プライバシーポリシー」へのリンクが入っている。新しいページを作るときは、フッターに
`privacy.html`（pages/から）または `../pages/privacy.html`（blog/から）へのリンクを必ず入れること。
`scripts/template-curation.html` と `scripts/release.py`（`INDEX_TMPL` の blog/index.html 生成部分）
には既に反映済みなので、通常の記事公開フローでは追加作業不要。

「3. アクセス解析」の節は、現在「現在は行っていません」としている。GA4導入時（依頼書005）に、
計測内容を説明する文面に差し替えること。

## 営業用エージェントの依頼書を受け取ったとき
1. `_requests/` にある依頼書を確認する（対象・提案内容・理由・優先度）。
2. Store掲載文に関する依頼は、公開ページだけでなく実際にPartner Centerで現状を確認し、
   `_requests/current-store-listing.md`（スナップショット）と照らして、提案がすでに反映済みでないか
   をチェックする（依頼の前提が古い／不正確なことがあるため）。
3. 内容を評価し、必要なら運営者に実施してよいか確認してから実装する
   （Store掲載文の変更、アプリの機能追加など、影響が大きいものは特に）。
4. 実施したら `_requests/done/` に移動し、対応結果（何を反映し、何を見送ったか）を依頼書の末尾に
   追記する。Store掲載文を変更した場合は `_requests/current-store-listing.md` も更新する。

## Partner Center 操作時の注意（2026-10-12 追記）
- 公開済み（live）のSubmissionのリスティング編集画面は**読み取り専用**になっており、保存しようとすると
  コンソールに `status: 400` のエラーが出て保存できない（画面上は入力できてしまうため気づきにくい）。
- 掲載文を編集するときは、まずOverviewページで「Start update」を押して新しいドラフトSubmissionを
  作成し、そのSubmissionのリスティング編集画面（URLに新しいSubmission IDが入る）で編集・保存する。
- 編集後は「Submit for certification」を押さず、運営者の明示的な確認を都度得てから提出する。

## 注意
- `googleb39988c901ff592a.html`（Search Console 確認用）は絶対に削除しない。
- 運営者はパスワードや認証情報を扱わせない。OAuth 等は本人がクリックする。
- 外部への投稿・送信は、必ず事前に運営者の許可を取る。
- 苦情・取り下げ依頼があれば、該当記事を `blog/` から外し、`release.py --no-release` で一覧を作り直す。
- ブログ用・営業用エージェントは別のAIツール／別セッションの可能性があり、記憶を共有していない
  前提で運用する。方針変更があれば、この手順書と `_drafts/README.md` `_requests/README.md` の
  両方を更新すること。
