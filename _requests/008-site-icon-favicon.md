# 008 サイトのアイコン（ファビコン）を設定する

- 対象: Introductionサイト（全ページの `<head>` とルート直下の画像ファイル）
- 優先度: 中
- 作成日: 2026-10-31
- ユーザー承認: 二階堂さん作成・承認済み（Canvaで制作したPNGから変換）

## 提案内容

ブラウザのタブ、ブックマーク、スマホのホーム画面に表示されるアイコンを設定したい。
デザインは「黒背景に金の八分音符、右下に白い SN」。サイトの配色（黒＋金）に合わせている。

### 1. 配置するファイル
二階堂さんが `icon/` フォルダ（`Documents/GitHub/Introduction/icon/`）に保存したPNGから作った下記の画像を、
サイトのルート直下（`index.html` と同じ階層）に置く。

| ファイル名 | サイズ | 用途 |
|---|---|---|
| `favicon.ico` | 16・32・48px（1ファイルに格納） | ブラウザのタブ・古いブラウザ |
| `favicon-32.png` | 32×32 | 一般ブラウザ（`<link rel="icon">`） |
| `apple-touch-icon.png` | 180×180 | iPhone/iPadのホーム画面 |
| `icon-192.png` | 192×192 | Androidのホーム画面 |
| `icon-512.png` | 512×512 | Android・検索結果などで使用 |

※ 画像は、二階堂さんから受け取ったファイルをそのまま配置してください（私の側では、リポジトリに置いていません）。

### 2. 各ページの `<head>` に追加するタグ
`index.html`、`pages/*.html`、`blog/*.html`、`blog/index.html` と、
**自動生成される側のテンプレート**（`scripts/release.py` が出力する `blog/index.html`、
`scripts/template-curation.html`）にも同じタグを入れる。
そうしないと、次回の記事公開で `blog/index.html` からアイコンのタグが消える。

```html
<link rel="icon" href="/Introduction/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/Introduction/favicon-32.png">
<link rel="apple-touch-icon" href="/Introduction/apple-touch-icon.png">
```

- GitHub Pagesのプロジェクトサイト（`/Introduction/` 配下）なので、パスは `/Introduction/...` から始める。
  相対パスにする場合は、階層ごと（`pages/` や `blog/` は `../`）に変える。
- 192px・512pxの画像は、将来 `manifest.json`（ホーム画面追加用）を作るときに使う。
  今回は画像を置いておくだけでよい。

### 3. 確認方法
- ブラウザのタブに、金の音符のアイコンが出る（ハードリロード、またはタブを開き直す。キャッシュで古いまま見える場合あり）
- `https://snworks-jp.github.io/Introduction/favicon.ico` を直接開くと画像が出る
- 検索結果に反映されるまでは、数日〜数週間かかることがある（こちらは待つだけでよい）

### 4. 注意
- 既存の `googleb39988c901ff592a.html`（Search Console確認用）は変更・削除しない。
- GA4タグ（`G-BRLV8TND0G`）など、既存の `<head>` の内容は変えない。
- 依頼書007（トップページのデザイン変更）と同時に作業してもよい。007の `<head>` 変更と衝突しないように、
  タグは `<title>` の近くにまとめて入れる。

## 理由・根拠
- いま、ブラウザのタブにはアイコンがなく、サイトの印象が弱く、ブックマークや複数タブの中で見分けにくい。
- 16pxで見ても、金の音符の形は読める。「SN」の文字は小さくて読みにくいが、音符の形で十分に識別できる。
  ブランド名（SN Works）は、32px以上（ホーム画面・ブックマークなど）で読める。
