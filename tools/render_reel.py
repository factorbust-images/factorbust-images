"""Render a 9:16 Reel (MP4) per post from a week JSON file.

Usage: python3 tools/render_reel.py data/week-YYYY-WW.json posts [no ...]
Output: <outdir>/fob-NNN-reel.mp4 (+ fob-NNN-reel-cover.png)

Timeline: claim 3.5 s -> countdown 3-2-1 (0.7 s each) -> reveal (9 s). H.264/AAC (silent track), 30 fps.
Layout keeps text inside Instagram's Reel safe zone (top 250 px, bottom 440 px, right 170 px).
"""
import sys, json, os, asyncio, subprocess, tempfile, shutil
from playwright.async_api import async_playwright

W, H, FPS = 1080, 1920, 30
T_CLAIM, T_COUNT, T_ANSWER, T_FADE = 3.5, 0.7, 9.0, 0.3

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;background:#0d0e0b;font-family:'Inter',sans-serif;color:#f3ead7;position:relative}
.rings{position:absolute;right:-520px;top:50%;transform:translateY(-50%);width:1300px;height:1300px;border-radius:50%;
 background:repeating-radial-gradient(circle,#15170f 0 44px,#0d0e0b 44px 88px)}
.rings:after{content:'';position:absolute;inset:0;border-radius:50%;
 background:repeating-conic-gradient(from 9deg,rgba(230,59,46,.10) 0 18deg,rgba(30,158,87,.10) 18deg 36deg)}
.wrap{position:absolute;left:90px;right:170px;top:250px;bottom:440px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;font-weight:700;letter-spacing:.18em;font-size:30px;text-transform:uppercase;color:#bfb59f}
.top b{color:#f3ead7}
.claim{font-family:'Anton';font-size:100px;line-height:1.04;text-transform:uppercase;margin:auto 0}
.claim em{font-style:normal;color:#e63b2e}
.q{font-family:'Anton';font-size:64px;display:flex;gap:26px;align-items:center}
.pill{padding:12px 38px;border-radius:999px;border:5px solid}
.f{border-color:#1e9e57;color:#1e9e57}.b{border-color:#e63b2e;color:#e63b2e}
.or{font-size:40px;color:#bfb59f}
.hint{margin-top:34px;font-size:34px;font-weight:600;color:#bfb59f}
.dim .claim,.dim .q,.dim .hint{opacity:.22}
.count{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:'Anton';font-size:620px;color:#f3ead7;line-height:1}
.stamp{font-family:'Anton';font-size:220px;line-height:1;transform:rotate(-6deg);display:inline-block;padding:6px 44px;border:12px solid;border-radius:28px;margin-top:60px;align-self:flex-start}
.stamp.fact{color:#1e9e57;border-color:#1e9e57}.stamp.bust{color:#e63b2e;border-color:#e63b2e}.stamp.legend{color:#e0a526;border-color:#e0a526;font-size:160px}
.body{font-size:46px;line-height:1.38;margin-top:auto;font-weight:500}
.body strong{color:#fff;font-weight:800}
.src{margin-top:34px;font-size:26px;color:#8f877a;line-height:1.4}
.handle{margin-top:30px;font-size:30px;font-weight:600;color:#bfb59f}
"""

def claim_html(p, dim=False, n=None):
    c = f"<div class=count>{n}</div>" if n else ""
    return f"""<div class=rings></div><div class="wrap {'dim' if dim else ''}">
<div class=top><span><b>Fact or Bust?</b></span><span>#{p['no']:03d}</span></div>
<div class=claim>{p['claim']}</div>
<div class=q><span class="pill f">FACT</span><span class=or>or</span><span class="pill b">BUST</span></div>
<div class=hint>Comment your guess before the reveal 👇</div></div>{c}"""

def answer_html(p):
    return f"""<div class=rings></div><div class=wrap>
<div class=top><span><b>The answer</b></span><span>#{p['no']:03d}</span></div>
<div class="stamp {p['verdict'].lower()}">{p['verdict'].upper()}</div>
<div class=body>{p['answer']}</div>
<div class=src>Sources: {p['sources']}</div>
<div class=handle>@factorbust.darts · follow for daily darts facts</div></div>"""

async def frames(posts, tmp):
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width': W, 'height': H})
        for p in posts:
            parts = [('q', claim_html(p)), ('c3', claim_html(p, True, 3)), ('c2', claim_html(p, True, 2)),
                     ('c1', claim_html(p, True, 1)), ('a', answer_html(p))]
            for name, html in parts:
                await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{html}</body></html>")
                await pg.evaluate("document.fonts.ready")
                await pg.screenshot(path=os.path.join(tmp, f"{p['no']:03d}-{name}.png"))
        await b.close()

def encode(no, tmp, out):
    f = lambda n: os.path.join(tmp, f"{no:03d}-{n}.png")
    durs = [T_CLAIM, T_COUNT, T_COUNT, T_COUNT, T_ANSWER]
    names = ['q', 'c3', 'c2', 'c1', 'a']
    args = ['ffmpeg', '-y', '-loglevel', 'error']
    for n, d in zip(names, durs):
        args += ['-loop', '1', '-t', str(d), '-framerate', str(FPS), '-i', f(n)]
    total = sum(durs) - T_FADE
    args += ['-f', 'lavfi', '-t', str(total), '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100']
    # hard cuts for claim -> countdown, short fade into the reveal
    fc = ("[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0,fps=30,format=yuv420p[pre];"
          f"[4:v]fps=30,format=yuv420p[ans];"
          f"[pre][ans]xfade=transition=fade:duration={T_FADE}:offset={T_CLAIM + 3*T_COUNT - T_FADE}[v]")
    out_mp4 = os.path.join(out, f"fob-{no:03d}-reel.mp4")
    args += ['-filter_complex', fc, '-map', '[v]', '-map', '5:a', '-c:v', 'libx264', '-preset', 'veryfast',
             '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '128k',
             '-shortest', '-movflags', '+faststart', out_mp4]
    subprocess.run(args, check=True)
    shutil.copy(f('q'), os.path.join(out, f"fob-{no:03d}-reel-cover.png"))
    return out_mp4

def main():
    spec, out = sys.argv[1], sys.argv[2]
    only = {int(x) for x in sys.argv[3:]}
    posts = [p for p in json.load(open(spec)) if not only or p['no'] in only]
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    asyncio.run(frames(posts, tmp))
    for p in posts:
        print(encode(p['no'], tmp, out))

if __name__ == '__main__':
    main()
