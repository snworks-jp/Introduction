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
        posts.append(dict(file=p.name, title=title.strip(), summary=summary.strip(), date=date))
    posts.sort(key=lambda x: (x["date"], x["file"]), reverse=True)
    return posts

def card(p, i, prefix):
    cls = "r1" if i % 2 == 0 else "r2"
    return (f'      <li>\n        <a class="note {cls}" href="{prefix}{p["file"]}">\n'
            f'          <strong>{html.escape(p["title"])}</strong>\n'
            + (f'          <span class="d">{html.escape(p["summary"])}</span>\n' if p["summary"] else "")
            + '        </a>\n      </li>')

INDEX_TMPL = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BLOG｜SN Works</title>
<meta name="description" content="SN WorksのBLOG。金管楽器の上達に役立つコラムや、演奏の記録の残し方などを載せています。">
<link rel="canonical" href="__BASE__blog/">
<style>
  :root { --bg:#eef1ff; --ink:#1a1a3c; --muted:#4f5078; --yellow:#ffd23f; --blue:#3d5afe; --mint:#2fd39a;
    --round:"Hiragino Maru Gothic ProN","Yu Gothic","Meiryo",system-ui,sans-serif; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font-family:var(--round); line-height:1.8; overflow-x:clip; }
  a { color:inherit; } a:focus-visible { outline:3px solid var(--blue); outline-offset:4px; }
  .wrap { max-width:1040px; margin:0 auto; padding:0 20px; }
  .bar { position:sticky; top:0; z-index:10; background:var(--ink); border-bottom:4px solid var(--yellow); }
  .bar .wrap { display:flex; align-items:center; min-height:52px; }
  .brand { color:#fff; text-decoration:none; font-size:20px; font-weight:800; }
  h1 { margin:40px 0 6px; font-size:clamp(32px,8vw,52px); font-weight:800; line-height:1.1; }
  .lede { margin:0 0 32px; color:var(--muted); }
  .notes { display:grid; gap:22px; list-style:none; margin:0; padding:0 0 8px; }
  @media (min-width:720px) { .notes { grid-template-columns:1fr 1fr; } }
  .note { display:block; position:relative; text-decoration:none; padding:30px 24px 24px; border-radius:6px 6px 18px 6px; background:#fff;
    box-shadow:0 10px 0 -6px rgba(26,26,60,.12), 0 16px 26px -14px rgba(26,26,60,.35); transform:rotate(var(--tilt,0deg));
    transition:transform .28s cubic-bezier(.3,1.5,.5,1), box-shadow .28s; }
  .note::before { content:""; position:absolute; top:-12px; left:50%; width:84px; height:24px; margin-left:-42px; background:rgba(255,255,255,.65); border:1px solid rgba(26,26,60,.08); transform:rotate(-2deg); }
  .note:hover { transform:rotate(0) translateY(-6px) scale(1.015); }
  .note strong { display:block; font-size:18px; line-height:1.5; font-weight:800; }
  .note .d { display:block; margin-top:8px; font-size:14.5px; color:var(--muted); }
  .r1 { --tilt:1deg; border-top:8px solid var(--blue); } .r2 { --tilt:-1deg; border-top:8px solid var(--mint); }
  footer { padding:48px 0; color:var(--muted); font-size:13px; text-align:center; }
  @media (prefers-reduced-motion:reduce) { .note { transition:none; } }
</style>
</head>
<body>
<div class="bar"><div class="wrap"><a class="brand" href="../">SN Works</a></div></div>
<main class="wrap">
  <h1>BLOG</h1>
  <p class="lede">金管楽器の上達に役立つコラムなどを、載せています。</p>
  <ul class="notes">
__CARDS__
  </ul>
</main>
<footer><div class="wrap"><a href="../">SN Works トップへ</a><br>© 2026 SN Works</div></footer>
</body>
</html>
"""

def build_blog_index(posts):
    cards = "\n".join(card(p, i, "") for i, p in enumerate(posts))
    out = INDEX_TMPL.replace("__BASE__", BASE).replace("__CARDS__", cards)
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
    for rel in ["pages/ScoreMate_Introduction.html", "pages/concert-calendar.html"]:
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
