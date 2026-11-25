import sys, json, asyncio, os
OUT = sys.argv[2] if len(sys.argv) > 2 else "posts"
os.makedirs(OUT, exist_ok=True)
from playwright.async_api import async_playwright

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;background:#0d0e0b;font-family:'Inter',sans-serif;color:#f3ead7;position:relative}
.rings{position:absolute;right:-420px;top:50%;transform:translateY(-50%);width:1100px;height:1100px;border-radius:50%;
 background:repeating-radial-gradient(circle,#15170f 0 38px,#0d0e0b 38px 76px);opacity:.9}
.rings:after{content:'';position:absolute;inset:0;border-radius:50%;
 background:repeating-conic-gradient(from 9deg,rgba(230,59,46,.10) 0 18deg,rgba(30,158,87,.10) 18deg 36deg)}
.wrap{position:absolute;inset:0;padding:96px 88px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;font-weight:700;letter-spacing:.18em;font-size:26px;text-transform:uppercase;color:#bfb59f}
.top b{color:#f3ead7}
.claim{font-family:'Anton';font-size:104px;line-height:1.02;text-transform:uppercase;margin-top:auto;margin-bottom:auto}
.claim em{font-style:normal;color:#e63b2e}
.q{font-family:'Anton';font-size:64px;display:flex;gap:28px;align-items:center}
.pill{padding:14px 40px;border-radius:999px;border:5px solid}
.f{border-color:#1e9e57;color:#1e9e57}.b{border-color:#e63b2e;color:#e63b2e}
.or{font-size:40px;color:#bfb59f}
.foot{margin-top:56px;display:flex;justify-content:space-between;font-size:28px;color:#bfb59f;font-weight:600}
.stamp{font-family:'Anton';font-size:230px;line-height:1;transform:rotate(-6deg);display:inline-block;padding:6px 44px;border:12px solid;border-radius:28px;margin-top:40px;align-self:flex-start}
.stamp.fact{color:#1e9e57;border-color:#1e9e57}.stamp.bust{color:#e63b2e;border-color:#e63b2e}.stamp.legend{color:#e0a526;border-color:#e0a526;font-size:170px}
.body{font-size:44px;line-height:1.38;margin-top:auto;font-weight:500}
.body strong{color:#fff;font-weight:800}
.src{margin-top:40px;font-size:24px;color:#8f877a;line-height:1.4}
"""

def slide_q(p):
    return f"""<div class=rings></div><div class=wrap>
<div class=top><span><b>Fact or Bust?</b></span><span>#{p['no']:03d}</span></div>
<div class=claim>{p['claim']}</div>
<div class=q><span class="pill f">FACT</span><span class=or>or</span><span class="pill b">BUST</span></div>
<div class=foot><span>@factorbust.darts</span><span>Swipe for the answer →</span></div></div>"""

def slide_a(p):
    return f"""<div class=rings></div><div class=wrap>
<div class=top><span><b>The answer</b></span><span>#{p['no']:03d}</span></div>
<div class="stamp {p['verdict'].lower()}">{p['verdict'].upper()}</div>
<div class=body>{p['answer']}</div>
<div class=src>Sources: {p['sources']}</div>
<div class=foot><span>@factorbust.darts</span><span>Did you get it? 👇</span></div></div>"""

async def main(spec):
    posts = json.load(open(spec))
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width':1080,'height':1350})
        for p in posts:
            for i,fn in enumerate((slide_q, slide_a),1):
                await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{fn(p)}</body></html>")
                await pg.evaluate("document.fonts.ready")
                out=f"{OUT}/fob-{p['no']:03d}-{i}.png"
                await pg.screenshot(path=out)
                print(out)
        await b.close()
asyncio.run(main(sys.argv[1]))
