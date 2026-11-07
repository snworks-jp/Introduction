# 014 独自ドメイン（snworks.jp）への移行：サイト側の作業

- 対象: Introductionサイト全体（リポジトリの `CNAME`、全ページの `<head>`、`sitemap.xml`、`scripts/release.py`、`scripts/template-curation.html`、`blog/*.html`、Search Console、GA4、Bing、Microsoft Storeの掲載情報）
- 優先度: 高（広告・アフィリエイトの準備、検索評価の引き継ぎのため、早いほうがよい）
- 作成日: 2026-11-07（同日、状況を反映して作り直した版。管理者への提出は、この版が最初）
- 関連: 013（アフィリエイト）、011（ページ類のデザイン）。パスを直す作業（手順B）は、他の依頼の実装と同じファイルを触るので、順番を調整する。

## これまでに二階堂さんが済ませたこと（2026-11-07）
1. ドメイン **snworks.jp** を、XServerドメインで取得した（2026-11-07登録、有効期限 2027-11-30）。
2. XServerドメインで、ネームサーバーを `ns1〜3.xdomain.ne.jp`（XServer Domain）に設定し、反映を確認した。
   （最初は、他の設定のままで、DNSの問い合わせが拒否されていた。これを直した。）
3. DNSレコードを追加した（XServerドメインのDNS設定）:
   - TXT: `_github-pages-challenge-snworks-jp` → `10eb235a25c0869165e28e8e7ddef5`（GitHubのドメイン確認用）
   - A（ドメイン直下）: `185.199.108.153`、`185.199.109.153`、`185.199.110.153`、`185.199.111.153`
   - AAAA（ドメイン直下）: `2606:50c0:8000::153`、`8001::153`、`8002::153`、`8003::153`
   - CNAME: `www` → `snworks-jp.github.io`
   外からの問い合わせで、上記がすべて見えることを確認済み。CAAレコードはなし。
4. Introductionリポジトリの Settings → Pages → Custom domain に `snworks.jp` を登録した。DNS checkは通った。
   現在は「TLS certificate is being provisioned（証明書の準備中）」の段階。進まなければ、二階堂さんが、ドメインを一度外して、再登録する。
5. アカウントのPages設定で、`snworks.jp` のドメイン確認（Verify）を試行中。TXTレコードは入っており、GitHub側が認識するのを待っている。
6. Microsoft Storeの販売は、二階堂さんが停止した。

## この依頼の範囲（管理者の作業）

### A. リポジトリの状態を取り込む（最初に必ず）
- GitHubのPages設定で、独自ドメインを登録・削除・再登録すると、リポジトリのルートの `CNAME` ファイル（内容は `snworks.jp` のみ）が、
  自動でコミットされる。ローカルで `git pull` して取り込んでから作業する。
  取り込まないまま push すると、`CNAME` が消えて、独自ドメインの設定が外れる。
- 以降の作業で、`CNAME` ファイルは、削除・変更しない。
- 事前確認: `snworks-jp.github.io` という名前の「ユーザーサイト用リポジトリ」が存在するか確認する（存在して独自ドメインが付くと、他のプロジェクトサイトに影響するため）。

### B. サイト内のURLの修正
サイトのルートが、`/Introduction/` から `/` に変わる。`/Introduction/` から始まる絶対パスは、すべて直す。`../` のような相対パスは、そのままで動く。
作業の前に、`snworks-jp.github.io`、`/Introduction/`、`Introduction/` を、リポジトリ全体で検索して、一覧にする（置換漏れの防止）。
- 全ページの `<head>`（`index.html`、`pages/*.html`、`blog/*.html`、`blog/index.html`）:
  - アイコン: `/Introduction/favicon.ico` → `/favicon.ico`、`/Introduction/favicon-32.png` → `/favicon-32.png`、`/Introduction/apple-touch-icon.png` → `/apple-touch-icon.png`
  - `<link rel="canonical">`、`og:url`、JSON-LDの `url` など: `https://snworks-jp.github.io/Introduction/...` → `https://snworks.jp/...`
  - `og:image` は、Microsoft Storeの画像のURLなので、変更しない。
- `sitemap.xml`、`robots.txt`（あれば）の `Sitemap:` 行。
- `scripts/release.py`: ベースURL、sitemap生成、一覧・トップのリンク生成、`INDEX_TMPL` の `<head>`。
- `scripts/template-curation.html`: アイコン、canonical。
- 既存の記事（`blog/*.html`）の `<head>` のみ。本文は変更しない。
- `release.py --no-release` を2回続けて実行し、冪等（2回目に差分が出ない）なことを確認する。
- `googleb39988c901ff592a.html`（Search Console確認用）は、**削除・変更しない**。

実施のタイミング: `https://snworks.jp/` がHTTPSで表示されることを確認してから（二階堂さんが連絡する）、すぐに反映する。
それまでは、アイコンの表示が一時的に壊れる可能性があるが、想定どおり。

### C. 旧URLからの転送の確認
- 独自ドメインを設定したあと、`https://snworks-jp.github.io/Introduction/` と、各記事の旧URLが、新しいURLに転送されるかを、実際に開いて確認する。
  GitHub Pagesの標準の挙動としては転送されるはずだが、公式資料では確認できていない。
- 転送されない場合は、二階堂さんに相談する。

### D. 検索・計測サービスの更新（二階堂さんと分担）
- **Search Console**: 新しいURL（`https://snworks.jp/`）をプロパティとして追加する。DNSのTXT確認が最も楽（XServerドメインで二階堂さんが追加）。
  サイトマップ（`https://snworks.jp/sitemap.xml`）を送信する。旧プロパティは、すぐには消さない。
- **GA4**: 測定ID（`G-BRLV8TND0G`）は変えない。データストリームのURLを、新しいものに直す。
- **Bing Webmaster Tools**: 新しいURLを追加し、サイトマップを送信する。
- 外部で公開済みのリンク（X、noteなど）は、旧URLからの転送で当面は動く。

### E. Microsoft Storeとアプリの案内先（二階堂さんの作業）
- Partner Centerの掲載情報に、サイトのURL（ホームページ、プライバシーポリシーのURL）があれば、新しいものに変える（現在は販売停止中なので、その期間に済ませる）。
  `_requests/current-store-listing.md` に、現在のURLが載っている。管理者は、そこに載っているURLの一覧を、二階堂さんに伝える。

## 決めたこと
- 正規のURL（canonical）は **`https://snworks.jp/`**（wwwなし）。`www.snworks.jp` は、GitHub側の自動転送でこちらに寄せる。
- ScoreMateのWebアプリ（`snworks-jp.github.io/ScoreMate/`、別リポジトリ）は、今回は変更しない。検索に出さない方針も維持。
- レンタルサーバーは契約しない（GitHub Pagesのまま）。

## 確認項目
1. `https://snworks.jp/` が開く（鍵マークあり、証明書エラーなし）。`http://` で開くと `https://` に転送される。
2. `https://www.snworks.jp/` が `https://snworks.jp/` に転送される。
3. 旧URL（`snworks-jp.github.io/Introduction/` と各記事）が、新しいURLに転送される。
4. トップ、BLOG一覧、全記事、`pages/*.html` で、タブのアイコンが表示される。
5. 全ページの canonical が `https://snworks.jp/...` になっている。
6. `sitemap.xml` のURLが新しいもの。`googleb39988c901ff592a.html` が `https://snworks.jp/googleb39988c901ff592a.html` で開く。
7. **演奏会カレンダー**: 新しいドメインで、予定の読み込みと、投稿フォームの送信が動く（Apps Script側でアクセス元を制限していないか、動作で確認する。送信は1件テストして、スプレッドシートのテスト行は後で消す）。
8. GA4のリアルタイムに、新しいドメインでの訪問が出る。
9. Search Consoleに、新しいプロパティが追加され、サイトマップが読み込まれる。
10. スマホで開いて、表示が崩れていない。
11. リポジトリのルートに `CNAME`（内容 `snworks.jp`）が残っている。

## 範囲に含めないもの
- ScoreMateのWebアプリ（別リポジトリ）の移行
- レンタルサーバーの契約、独自ドメインのメールアドレス
- 広告の掲載（013のアフィリエイトとは別。AdSenseは、記事とアクセスが増えてから検討）
- DNSの設定（二階堂さんが済ませた。管理者は触らない）

## 理由・根拠
- 独自ドメインにすると、AdSenseなどの広告サービスの審査に必要な「自分のドメイン」の条件を満たせる。
- github.ioのURLは、ブランドとして覚えにくく、将来ホスティングを変えても、URLを変えずに済む。
- 年の費用は、ドメイン代のみ（2年目以降 3,102円/年）。
- 旧URLの転送と、検索サービスの更新を、早めに済ませておくと、検索での評価の引き継ぎがうまくいく。
