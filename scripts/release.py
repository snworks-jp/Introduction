#!/usr/bin/env python3
"""毎日1本、_queue/ の先頭の記事を blog/ に公開し、一覧・トップ・サイトマップを作り直す。

使い方:
  python3 scripts/release.py              # 1本公開して、一覧などを更新
  python3 scripts/release.py --no-release # 公開はせず、一覧などだけ更新
  python3 scripts/release.py --date 2026-10-19  # 公開日を指定（省略時は今日・日本時間）

_queue/NNN-スラッグ.html（NNN は並び順の番号）に、確認済みの記事を置いておく。
記事の中の __SLUG__ / __DATE__（2026-10-13）/ __DATE_JA__（2026年10月13日）は公開時に置き換わる。
"""
import html, json, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://snworks-jp.github.io/Introduction/"
JST = timezone(timedelta(hours=9))
TOP_COUNT = 4          # トップページに出す最新記事の数
MARK_START, MARK_END = "<!-- BLOG:START -->", "<!-- BLOG:END -->"
REL_START, REL_END = "<!-- RELATED:START -->", "<!-- RELATED:END -->"

# topic: スラッグ -> (表示名, まとめページ用の短い説明1〜2文)
TOPIC_TITLES = {
    "long-tone": ("ロングトーン", "ロングトーンの目的ややり方についての記事です。"),
    "lip-slur": ("リップスラー", "リップスラーの練習の目的やコツについての記事です。"),
    "high-notes": ("高い音", "高い音を力まずに出すための考え方についての記事です。"),
    "tonguing": ("タンギング", "タンギングの練習方法についての記事です。"),
    "practice-menu": ("練習メニュー", "短時間でのウォームアップや基礎練習の組み立て方についての記事です。"),
    "lip-fatigue": ("唇のバテ", "唇のバテや疲労との付き合い方についての記事です。"),
    "breath": ("ブレス", "息の吸い方・流し方・タイミングについての記事です。"),
    "records": ("記録・整理", "演奏会や練習の記録の残し方についての記事です。"),
    "other": ("その他", "金管楽器の上達に役立つ、その他のテーマの記事です。"),
}
# instrument: スラッグ -> 表示名
INSTRUMENT_TITLES = {
    "trumpet": "トランペット",
    "trombone": "トロンボーン",
    "horn": "ホルン",
    "euphonium": "ユーフォニアム",
    "tuba": "チューバ",
    "brass-band": "ブラスバンド",
    "all": "すべての楽器",
}

def today():
    if "--date" in sys.argv:
        return datetime.strptime(sys.argv[sys.argv.index("--date") + 1], "%Y-%m-%d").date()
    return datetime.now(JST).date()

def release_one():
    q = sorted(p for p in (ROOT / "_queue").glob("*.html"))
    if not q:
        print("予約の置き場（_queue）が空です。記事の補充が必要です。")
        return None
    src = q[0]
    slug = re.sub(r"^\d+[-_]?", "", src.stem)
    dst = ROOT / "blog" / f"{slug}.html"
    if dst.exists():
        raise SystemExit(f"すでに存在します: {dst.name}（スラッグが重複しています）")
    d = today()
    text = src.read_text(encoding="utf-8")
    # 同じ紹介記事（外部リンク）だけで構成された記事は公開しない。一部の重複は許可。
    ext = lambda t: set(re.findall(r'class="src" href="([^"]+)"', t))
    used = set().union(*[ext(p.read_text(encoding="utf-8")) for p in (ROOT / "blog").glob("*.html")])
    new = ext(text)
    if new and new <= used:
        raise SystemExit(f"中止: {src.name} の紹介記事はすべて公開済みの記事と重複しています。作り直してください。")
    text = (text.replace("__SLUG__", slug)
                .replace("__DATE_JA__", f"{d.year}年{d.month}月{d.day}日")
                .replace("__DATE__", d.isoformat()))
    dst.write_text(text, encoding="utf-8")
    src.unlink()
    print(f"公開: {dst.relative_to(ROOT)}")
    return dst

def meta(text, name):
    m = re.search(rf'<meta name="{name}" content="([^"]*)"', text)
    return html.unescape(m.group(1)) if m else ""

def fmt_date_ja(date):
    y, m, d = date.split("-")
    return f"{int(y)}年{int(m)}月{int(d)}日"

def fmt_date_dot(date):
    y, m, d = date.split("-")
    return f"{int(y)}.{int(m):02d}.{int(d):02d}"

def read_posts():
    posts = []
    for p in (ROOT / "blog").glob("*.html"):
        if p.name == "index.html":
            continue
        t = p.read_text(encoding="utf-8")
        title_full = html.unescape(re.search(r"<title>(.*?)</title>", t, re.S).group(1)).strip()
        m = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', t)
        date = m.group(1) if m else "1970-01-01"
        if "｜" in title_full:
            title, summary = title_full.split("｜", 1)
        else:
            title, summary = title_full, ""
        summary = meta(t, "card-summary") or summary or meta(t, "description")[:44]
        # category: "announcement"（お知らせ）以外はすべて「コラム」として扱う
        category = meta(t, "category") or "column"
        # topic / instrument: 未指定・未知の値はエラーにせず other / all として扱う
        topic = meta(t, "topic") or "other"
        if topic not in TOPIC_TITLES:
            topic = "other"
        instrument = meta(t, "instrument") or "all"
        if instrument not in INSTRUMENT_TITLES:
            instrument = "all"
        posts.append(dict(file=p.name, title=title.strip(), summary=summary.strip(), date=date,
                           category=category, topic=topic, instrument=instrument))
    posts.sort(key=lambda x: (x["date"], x["file"]), reverse=True)
    return posts

def card(p, i, prefix, date_fmt="ja"):
    cls = "r1" if i % 2 == 0 else "r2"
    date_str = fmt_date_dot(p["date"]) if date_fmt == "dot" else fmt_date_ja(p["date"])
    return (f'      <li>\n        <a class="note {cls}" href="{prefix}{p["file"]}">\n'
            f'          <strong>{html.escape(p["title"])}</strong>\n'
            + (f'          <span class="d">{html.escape(p["summary"])}</span>\n' if p["summary"] else "")
            + f'          <span class="date">{date_str}</span>\n'
            + '        </a>\n      </li>')

def related_posts(p, posts):
    """同じtopic優先 → 同じinstrument（all以外）→ 新しい順、で最大3本（自分は除く）。"""
    others = [q for q in posts if q["file"] != p["file"]]
    picked, seen = [], {p["file"]}
    def add(lst):
        for q in lst:
            if len(picked) >= 3:
                return
            if q["file"] not in seen:
                picked.append(q)
                seen.add(q["file"])
    add([q for q in others if q["topic"] == p["topic"]])
    if p["instrument"] != "all":
        add([q for q in others if q["instrument"] == p["instrument"]])
    add(others)
    return picked[:3]

def build_related(posts):
    for p in posts:
        f = ROOT / "blog" / p["file"]
        t = f.read_text(encoding="utf-8")
        if REL_START not in t or REL_END not in t:
            continue  # 目印コメントがない古い記事はスキップ（エラーにしない）
        rel = related_posts(p, posts)
        if rel:
            cards = "\n".join(card(r, i, "", date_fmt="dot") for i, r in enumerate(rel))
            block = (f'{REL_START}\n  <div class="related">\n    <h2>関連する記事</h2>\n'
                     f'    <ul class="blog-list">\n{cards}\n    </ul>\n  </div>\n  {REL_END}')
        else:
            block = f'{REL_START}\n  {REL_END}'
        new_t = re.sub(re.escape(REL_START) + r".*?" + re.escape(REL_END), lambda _: block, t, flags=re.S)
        if new_t != t:
            f.write_text(new_t, encoding="utf-8")

INDEX_TMPL = """<!doctype html>
<html lang="ja">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BRLV8TND0G"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-BRLV8TND0G');
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="icon" href="/Introduction/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/Introduction/favicon-32.png">
<link rel="apple-touch-icon" href="/Introduction/apple-touch-icon.png">
<meta name="description" content="__DESC__">
<link rel="canonical" href="__CANONICAL__">
<style>
  :root { --bg:#141311; --ink:#ece6da; --muted:#a39b8c; --desc:#cfc7b8; --line:#2c2a25; --gold:#c9a96a; --gold-hover:#d8bd83;
    --serif:"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho",serif;
    --sans:"Noto Sans JP","Hiragino Sans","Yu Gothic",sans-serif;
    --eng:"Cormorant Garamond","Times New Roman",serif; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font-family:var(--sans); font-weight:300; line-height:1.9; overflow-x:clip; }
  a { color:inherit; text-decoration:none; } a:focus-visible { outline:2px solid var(--gold); outline-offset:3px; }
  .wrap { max-width:1040px; margin:0 auto; padding:0 24px; }
  .bar { border-bottom:1px solid var(--line); }
  .bar .wrap { display:flex; align-items:center; min-height:64px; }
  .brand { font-family:var(--eng); font-size:18px; letter-spacing:.3em; color:var(--ink); }
  h1 { font-family:var(--serif); font-weight:500; font-size:clamp(32px,6vw,52px); line-height:1.2; margin:56px 0 10px; color:var(--ink); }
  .lede { margin:0 0 20px; color:var(--desc); font-size:15px; }
  .filters { margin:0 0 48px; font-size:13.5px; color:var(--muted); line-height:2.1; }
  .filters .flabel { color:var(--gold); font-weight:600; margin-right:4px; }
  .filters a { color:var(--ink); text-decoration:none; border-bottom:1px solid var(--line); }
  .filters a:hover { color:var(--gold); border-color:var(--gold); }
  .sec-block { padding:48px 0; border-top:1px solid var(--line); }
  .sec-block:first-of-type { border-top:none; padding-top:0; }
  .num { font-family:var(--eng); font-size:12px; letter-spacing:.3em; color:var(--gold); margin:0 0 16px; }
  h2.sec { font-family:var(--serif); font-weight:500; font-size:20px; margin:0 0 24px; color:var(--ink); }
  .blog-list { list-style:none; margin:0; padding:0; border-top:1px solid var(--line); }
  .blog-list li { border-bottom:1px solid var(--line); }
  .blog-list .note { display:flex; align-items:baseline; flex-wrap:wrap; gap:20px; padding:20px 2px; }
  .blog-list .date { order:-2; flex:0 0 96px; font-family:var(--eng); font-size:13px; letter-spacing:.04em; color:var(--muted); }
  .blog-list strong { order:-1; flex:0 0 auto; font-family:var(--serif); font-weight:500; font-size:16px; color:var(--ink); transition:color .2s; }
  .blog-list .d { order:0; flex:1 1 220px; font-size:13.5px; color:var(--desc); }
  .blog-list .note::after { content:"→"; order:1; margin-left:auto; color:var(--gold); transition:color .2s; }
  .blog-list .note:hover strong { color:var(--gold); }
  .blog-list .note:hover::after { color:var(--gold-hover); }
  @media (max-width:640px) {
    .blog-list .note { flex-direction:column; align-items:flex-start; gap:6px; }
    .blog-list .date, .blog-list .d { flex:0 1 auto; }
    .blog-list .note::after { display:none; }
  }
  footer { border-top:1px solid var(--line); padding:40px 0; margin-top:16px; }
  footer .wrap { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; font-size:12px; color:var(--muted); }
  footer a { color:var(--muted); } footer a:hover { color:var(--gold); }
  @media (prefers-reduced-motion:reduce) { .blog-list .note, .blog-list strong, .blog-list .note::after { transition:none; } }
</style>
</head>
<body>
<div class="bar"><div class="wrap"><a class="brand" href="__HOME__">SN WORKS</a></div></div>
<main class="wrap">
  <h1>__H1__</h1>
  <p class="lede">__LEDE__</p>
__FILTERS__
__SECTIONS__
</main>
<footer><div class="wrap"><span>SN WORKS</span><a href="__PRIVACY__">プライバシーポリシー</a><span>© 2026 SN Works</span></div></footer>
</body>
</html>
"""

SECTION_TITLES = {"column": "コラム", "announcement": "お知らせ"}
SECTION_LABELS = {"column": "COLUMN", "announcement": "NEWS"}

def render_list_page(path, title, desc, canonical, h1, lede, sections_html, filters="", home="../", privacy="../pages/privacy.html"):
    out = (INDEX_TMPL
           .replace("__TITLE__", title)
           .replace("__DESC__", desc)
           .replace("__CANONICAL__", canonical)
           .replace("__HOME__", home)
           .replace("__H1__", h1)
           .replace("__LEDE__", lede)
           .replace("__FILTERS__", filters)
           .replace("__SECTIONS__", sections_html)
           .replace("__PRIVACY__", privacy))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out, encoding="utf-8")

def build_filters_html(topic_pages, instrument_pages):
    if not topic_pages and not instrument_pages:
        return ""
    lines = ['  <p class="filters">']
    if topic_pages:
        order = [k for k in TOPIC_TITLES if k in topic_pages]
        links = " / ".join(f'<a href="topic/{k}.html">{TOPIC_TITLES[k][0]}</a>' for k in order)
        lines.append(f'    <span class="flabel">悩み別：</span>{links}<br>')
    if instrument_pages:
        order = [k for k in INSTRUMENT_TITLES if k in instrument_pages]
        links = " / ".join(f'<a href="instrument/{k}.html">{INSTRUMENT_TITLES[k]}</a>' for k in order)
        lines.append(f'    <span class="flabel">楽器別：</span>{links}')
    lines.append('  </p>')
    return "\n".join(lines)

def build_blog_index(posts, topic_pages, instrument_pages):
    sections = []
    groups = [key for key in ("column", "announcement") if any(p["category"] == key for p in posts)]
    for idx, key in enumerate(groups, start=1):
        group = [p for p in posts if p["category"] == key]
        cards = "\n".join(card(p, i, "", date_fmt="dot") for i, p in enumerate(group))
        sections.append(f'  <div class="sec-block">\n'
                         f'    <p class="num">{idx:02d} — {SECTION_LABELS[key]}</p>\n'
                         f'    <h2 class="sec">{SECTION_TITLES[key]}</h2>\n'
                         f'    <ul class="blog-list">\n{cards}\n    </ul>\n'
                         f'  </div>')
    render_list_page(
        ROOT / "blog" / "index.html",
        title="BLOG｜SN Works",
        desc="SN WorksのBLOG。金管楽器の上達に役立つコラムや、演奏の記録の残し方などを載せています。",
        canonical=BASE + "blog/",
        h1="BLOG",
        lede="金管楽器の上達に役立つコラムなどを、載せています。",
        sections_html="\n".join(sections),
        filters=build_filters_html(topic_pages, instrument_pages),
        home="../", privacy="../pages/privacy.html",
    )

def build_topic_instrument_pages(posts):
    by_topic, by_instrument = {}, {}
    for p in posts:
        by_topic.setdefault(p["topic"], []).append(p)
        by_instrument.setdefault(p["instrument"], []).append(p)

    # テーマ別まとめページ: 記事が2本以上あるテーマだけ作る
    topic_pages = {t: plist for t, plist in by_topic.items() if len(plist) >= 2 and t in TOPIC_TITLES}
    # 楽器別まとめページ: all 以外で、該当記事があるものを作る
    instrument_pages = {i: plist for i, plist in by_instrument.items() if i != "all" and i in INSTRUMENT_TITLES}

    for topic, plist in topic_pages.items():
        name, desc = TOPIC_TITLES[topic]
        cards = "\n".join(card(p, i, "../", date_fmt="dot") for i, p in enumerate(plist))
        sections_html = (f'  <div class="sec-block">\n    <h2 class="sec">{name}の記事</h2>\n'
                          f'    <ul class="blog-list">\n{cards}\n    </ul>\n  </div>')
        render_list_page(
            ROOT / "blog" / "topic" / f"{topic}.html",
            title=f"{name}｜SN Works BLOG",
            desc=desc,
            canonical=BASE + f"blog/topic/{topic}.html",
            h1=name,
            lede=desc,
            sections_html=sections_html,
            home="../../", privacy="../../pages/privacy.html",
        )

    for inst, plist in instrument_pages.items():
        name = INSTRUMENT_TITLES[inst]
        plist_sorted = sorted(plist, key=lambda x: (x["date"], x["file"]), reverse=True)
        cards = "\n".join(card(p, i, "../", date_fmt="dot") for i, p in enumerate(plist_sorted))
        lede = f"{name}に関する記事をまとめています。"
        sections_html = (f'  <div class="sec-block">\n    <h2 class="sec">{name}の記事</h2>\n'
                          f'    <ul class="blog-list">\n{cards}\n    </ul>\n  </div>')
        render_list_page(
            ROOT / "blog" / "instrument" / f"{inst}.html",
            title=f"{name}の記事｜SN Works BLOG",
            desc=lede,
            canonical=BASE + f"blog/instrument/{inst}.html",
            h1=f"{name}の記事",
            lede=lede,
            sections_html=sections_html,
            home="../../", privacy="../../pages/privacy.html",
        )

    return topic_pages, instrument_pages

def build_top(posts):
    f = ROOT / "index.html"
    t = f.read_text(encoding="utf-8")
    if MARK_START not in t or MARK_END not in t:
        raise SystemExit("index.html に BLOG の目印コメントがありません")
    cards = "\n".join(card(p, i, "blog/") for i, p in enumerate(posts[:TOP_COUNT]))
    new = f"{MARK_START}\n{cards}\n      {MARK_END}"
    t = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), lambda _: new, t, flags=re.S)
    f.write_text(t, encoding="utf-8")

def build_sitemap(posts, topic_pages, instrument_pages):
    urls = [(BASE, today().isoformat()), (BASE + "blog/", posts[0]["date"] if posts else today().isoformat())]
    for rel in ["pages/ScoreMate_Introduction.html", "pages/concert-calendar.html", "pages/privacy.html"]:
        if (ROOT / rel).exists():
            urls.append((BASE + rel, today().isoformat()))
    for topic, plist in sorted(topic_pages.items()):
        urls.append((BASE + f"blog/topic/{topic}.html", max(p["date"] for p in plist)))
    for inst, plist in sorted(instrument_pages.items()):
        urls.append((BASE + f"blog/instrument/{inst}.html", max(p["date"] for p in plist)))
    urls += [(BASE + "blog/" + p["file"], p["date"]) for p in posts]
    body = "\n".join(f"  <url><loc>{html.escape(u)}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n",
        encoding="utf-8")

def main():
    if "--no-release" not in sys.argv:
        release_one()
    posts = read_posts()
    topic_pages, instrument_pages = build_topic_instrument_pages(posts)
    build_blog_index(posts, topic_pages, instrument_pages)
    build_related(posts)
    build_top(posts)
    build_sitemap(posts, topic_pages, instrument_pages)
    print(f"記事 {len(posts)} 本 / 予約残り {len(list((ROOT/'_queue').glob('*.html')))} 本")

if __name__ == "__main__":
    main()
