# サイト用のプライバシーポリシーページを新設し、各ページから案内する

- 対象: Introductionサイト（新規ページ pages/privacy.html、全ページのフッター、scripts/template-curation.html、scripts/release.py が生成する blog/index.html、index.html）
- 優先度: 高
- 作成日: 2026-10-12

## 提案内容
ScoreMateアプリ用のポリシー（https://scoremate-app.netlify.app/privacy.html）とは別に、サイト用のプライバシーポリシーページを作る。運営者の了承済み事項: 連絡先は、アプリ用ポリシーに公開済みの scoremate.feedback@gmail.com と同じものを使う。

### 1. 新規ページ pages/privacy.html（文面案）
タイトル: プライバシーポリシー（SN Works サイト）
最終更新日: （作成日を入れる）

**運営者**
SN Works（個人が運営）。

**1. 演奏会カレンダーで受け付ける情報**
演奏会カレンダーの投稿フォームでお送りいただいた情報（日付、開演時刻、団体名・演奏会名、都道府県、会場、ジャンル、入場料、関連URL）は、掲載の可否を確認するために保存し、承認したものをカレンダーに掲載します。保存には Google のサービス（Google スプレッドシート）を使っています。
個人の氏名や連絡先など、個人を特定できる情報は入力しないでください。掲載内容の取り下げを希望する場合は、下記の連絡先までご連絡ください。

**2. 外部の情報の掲載**
演奏会カレンダーには、コンサートスクウェアが公開している演奏会情報（RSS）から取得した内容を、出典を明記して掲載している場合があります。

**3. アクセス解析** ※依頼書005で解析ツールを導入した時点で有効にする（導入前は「現在は行っていません」と書く）
当サイトでは、利用状況を把握するために Google アナリティクス（GA4）を利用します。閲覧したページ、流入元、端末の種類などの情報が、Cookie等を通じて Google に送信されます。個人を特定する情報は取得しません。Googleでの取り扱いは、Google のプライバシーポリシーをご覧ください。ブラウザの設定や、Googleが提供するオプトアウト用の機能で、収集を無効にできます。

**4. 広告・アフィリエイト** ※導入時に更新する（現在は広告・アフィリエイトを行っていない旨を書く）

**5. ScoreMateアプリについて**
アプリでの個人情報の取り扱いは、アプリ用のプライバシーポリシー（https://scoremate-app.netlify.app/privacy.html）をご覧ください。

**6. お問い合わせ**
scoremate.feedback@gmail.com

**7. 改定について**
内容は、予告なく改定する場合があります。改定後は、このページに掲載します。

### 2. 各ページのフッターにリンクを追加
トップ、アプリ紹介、演奏会カレンダー、BLOG一覧、各記事（雛形含む）のフッターに「プライバシーポリシー」へのリンクを追加する。
- pages/ と blog/ からは、相対パス `privacy.html` / `../pages/privacy.html`。
- release.py の blog/index.html 生成部分と、scripts/template-curation.html にも反映する（今後の記事にも入るように）。

### 3. 方針の変更点（運営者了承済み）
これまで「連絡先・ポリシーは載せない」としていたが、広告・アフィリエイトを見据えて、公開する方針に変更する。連絡先は上記1つのみとする。

## 理由・根拠
- 演奏会カレンダーは、すでに投稿フォームで情報を受け付けているが、扱いの説明がない。計測や広告の有無に関係なく、先に必要。
- アクセス解析（依頼書005）や、アフィリエイト・広告の審査では、プライバシーポリシーの掲載が求められることが多い。
- アプリ用ポリシーは「広告・解析は行わない」と書かれているため、サイトのポリシーは別にして、役割を分けておく必要がある。
- 外部送信（Cookieなど）に関する通知の要否は、導入前に最新の情報で確認すること。

---

## 対応結果（管理者、2026-10-12）
運営者に方針変更と文面案の事実関係を確認したうえで実施しました。

- `pages/privacy.html` を新設。文面案どおり、演奏会カレンダーの投稿情報の扱い（Googleスプレッドシート保存）、外部情報（コンサートスクウェアのRSS、出典明記）、アクセス解析・広告の現状（「現在は行っていません」）、ScoreMateアプリ用ポリシーへの案内、連絡先（scoremate.feedback@gmail.com）、改定についての7項目構成。
- フッターへのリンク追加: `index.html`、`pages/ScoreMate_Introduction.html`、`pages/concert-calendar.html`、BLOG記事5本（`long-tone.html` `lip-slur.html` `high-notes.html` `youtube-performance-record.html` `concert-record.html`）、`scripts/template-curation.html`（今後の記事用）、`scripts/release.py` の `INDEX_TMPL`（`blog/index.html` 生成部分）。
- `scripts/release.py` の `build_sitemap()` にも `pages/privacy.html` を追加し、`python3 scripts/release.py --no-release` を実行して `blog/index.html` と `sitemap.xml` を再生成（`index.html` のBLOGカード部分は対象外のため変化なし、フッターは直接編集）。
- 合計13ファイルをリポジトリに反映済み。

「3. アクセス解析」の節は、依頼書005でGA4を導入した時点で有効な文面に差し替える。
