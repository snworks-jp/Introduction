# Bing Webmaster Tools にサイトを登録する

- 対象: Introductionサイト（検索エンジン対策）
- 優先度: 中
- 作成日: 2026-10-12

## 提案内容
Googleに加えて、Bing（Microsoftの検索。Edgeの標準検索）にもサイトを登録する。

1. Bing Webmaster Tools（無料）に、サイト `https://snworks-jp.github.io/Introduction/` を追加する。
2. 所有確認は、Search Console からのインポートを優先する（ファイルやタグの追加が不要なため）。
   インポートできない場合は、確認用ファイルをリポジトリに置く方法をとる（管理者がファイルを用意、運営者がアップロード）。
3. サイトマップ `https://snworks-jp.github.io/Introduction/sitemap.xml` を送信する。
4. 登録後、数日〜数週間後に、インデックスされたページ数を確認する。

## 手順の分担
- ログイン、許可（OAuthの同意）、アップロードは運営者が行う（認証情報はエージェントに扱わせない）。
- 手順の案内と、ファイルが必要な場合の準備は管理者が行う。

## 理由・根拠
- ScoreMateはWindows向けアプリで、Windowsの標準ブラウザはEdge（検索はBing）。Windowsユーザーに見つけてもらうには、Bingへの登録に意味がある。
- Yahoo! JAPANはGoogleの検索技術を使っているとされ、Google側の対応でカバーできる見込み。Bingは別なので、個別の登録が必要。
- 一度登録すれば、サイトマップは公開のたびに自動更新されるため、運用の手間は増えない。
- 注意: Search Console 側も、現在は「データを処理中」で反映待ち（2026-10-12時点）。

---

## 対応結果（管理者、2026-10-12）
運営者（二階堂さん）がBingのブラウザ画面で以下を実施し、完了しました。

1. Bing Webmaster Tools にMicrosoftアカウントでサインイン。
2. 「Import your sites from GSC」で、Google Search Console から `https://snworks-jp.github.io/Introduction/` をインポート
   （インポート直後に画面が一時的に白くなる不具合があったが、再読み込みで登録済みと確認できた。
   「Your data and reports are being processed and it may take upto 48 hours to reflect.」と表示）。
3. Sitemaps画面から `https://snworks-jp.github.io/Introduction/sitemap.xml` を送信。Known sitemaps が 1 になり、
   ステータスは処理中（Processing）。

認証情報の入力・ログイン・アップロードはすべて運営者が行い、管理者（このセッション）は画面遷移の案内のみ行った。

アカウントは依頼書に書かれていた判断基準（Partner Centerと揃えるか、個人アカウントのままでよいか）を
運営者に説明したうえで、運営者の判断で進めてもらった。

インデックス状況の確認（手順4）は数日〜数週間後になるため未実施。目安として2026年11月頭を目安に
Bing Webmaster Tools の URL Inspection / インデックス状況を確認する。
