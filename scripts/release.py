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
        posts.append(dict(file=p.name, title=title.strip(), summary=summary.strip(), date=date, category=category))
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
<title>BLOG｜SN Works</title>
<link rel="icon" href="/Introduction/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/Introduction/favicon-32.png">
<link rel="apple-touch-icon" href="/Introduction/apple-touch-icon.png">
<meta name="description" content="SN WorksのBLOG。金管楽器の上達に役立つコラムや、演奏の記録の残し方などを載せています。">
<link rel="canonical" href="__BASE__blog/">
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
  .lede { margin:0 0 48px; color:var(--desc); font-size:15px; }
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
<div class="bar"><div class="wrap"><a class="brand" href="../">SN WORKS</a></div></div>
<main class="wrap">
  <h1>BLOG</h1>
  <p class="lede">金管楽器の上達に役立つコラムなどを、載せています。</p>
__SECTIONS__
</main>
<footer><div class="wrap"><span>SN WORKS</span><a href="../pages/privacy.html">プライバシーポリシー</a><span>© 2026 SN Works</span></div></footer>
</body>
</html>
"""

SECTION_TITLES = {"column": "コラム", "announcement": "お知らせ"}
SECTION_LABELS = {"column": "COLUMN", "announcement": "NEWS"}

def build_blog_index(posts):
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
    out = INDEX_TMPL.replace("__BASE__", BASE).replace("__SECTIONS__", "\n".join(sections))
    (ROOT / "blog" / "index.html").write_text(out, encoding="utf-8")

def build_top(posts):
    f = ROOT / "index.html"
    t = f.read_text(encoding="utf-8")
    if MARK_START not in t or MARK_END not in t:
        raise SystemExit("index.html に BLOG の目印コメントがありません")
    cards = "\n".join(card(p, i, "blog/") for i, p in enumerate(posts[:TOP_COUNT]))
    new = f"{MARK_START}\n{cards}\n      {MARK_END}"
    t = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), lambda _: new, t, flags=re.S)
    f.write_text(t, encoding="utf-8")

def build_sitemap(posts):
    urls = [(BASE, today().isoformat()), (BASE + "blog/", posts[0]["date"] if posts else today().isoformat())]
    for rel in ["pages/ScoreMate_Introduction.html", "pages/concert-calendar.html", "pages/privacy.html"]:
        if (ROOT / rel).exists():
            urls.append((BASE + rel, today().isoformat()))
    urls += [(BASE + "blog/" + p["file"], p["date"]) for p in posts]
    body = "\n".join(f"  <url><loc>{html.escape(u)}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n",
        encoding="utf-8")

def main():
    if "--no-release" not in sys.argv:
        release_one()
    posts = read_posts()
    build_blog_index(posts)
    build_top(posts)
    build_sitemap(posts)
    print(f"記事 {len(posts)} 本 / 予約残り {len(list((ROOT/'_queue').glob('*.html')))} 本")

if __name__ == "__main__":
    main()
