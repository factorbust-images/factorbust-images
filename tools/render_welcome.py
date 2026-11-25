import asyncio, sys
sys.path.insert(0, '/home/claude/factorbust-images/tools')
from playwright.async_api import async_playwright
import importlib.util
spec = importlib.util.spec_from_file_location("r", "/home/claude/factorbust-images/tools/render.py")
src = open("/home/claude/factorbust-images/tools/render.py").read()
CSS = src.split('CSS = """')[1].split('"""')[0]
CSS += """
.steps{margin-top:auto;display:flex;flex-direction:column;gap:46px}
.step{display:flex;gap:36px;align-items:flex-start;font-size:46px;line-height:1.3;font-weight:500}
.n{font-family:'Anton';font-size:84px;line-height:.9;color:#e63b2e;min-width:62px}
.step:nth-child(2) .n{color:#1e9e57}.step:nth-child(3) .n{color:#e0a526}
.step b{font-weight:800;color:#fff}
.h{font-family:'Anton';font-size:120px;line-height:1;text-transform:uppercase;margin-top:70px}
.drop{margin-top:auto;font-family:'Anton';font-size:58px;text-transform:uppercase;color:#f3ead7}
.drop em{font-style:normal;color:#1e9e57}
"""
S1 = """<div class=rings></div><div class=wrap>
<div class=top><span><b>Fact or Bust?</b></span><span>#000</span></div>
<div class=claim style="font-size:168px;line-height:.98">Welcome<br>to the<br><em>oche.</em><div style="font-family:Inter;text-transform:none;font-size:46px;line-height:1.35;color:#bfb59f;font-weight:500;margin-top:44px">One darts claim. Every day.<br>You make the call.</div></div>
<div class=q><span class="pill f">FACT</span><span class=or>or</span><span class="pill b">BUST</span></div>
<div class=foot><span>@factorbust.darts</span><span>Swipe for the rules →</span></div></div>"""
S2 = """<div class=rings></div><div class=wrap>
<div class=top><span><b>How it works</b></span><span>#000</span></div>
<div class=h>3 darts.<br>That's all.</div>
<div class=steps>
<div class=step><span class=n>1</span><span>We throw a <b>darts claim</b> at you. Records, myths and legends.</span></div>
<div class=step><span class=n>2</span><span>You call it in the comments: <b>Fact</b> or <b>Bust</b>?</span></div>
<div class=step><span class=n>3</span><span>Swipe for the answer. <b>Every one fact-checked</b>, sources included.</span></div>
</div>
<div class=drop style="margin-top:70px">First claim: <em>tomorrow, 6:30 pm UK</em> 🎯</div>
<div class=foot><span>@factorbust.darts</span><span>Follow so you don't miss it</span></div></div>"""
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        p=await b.new_page(viewport={'width':1080,'height':1350})
        for i,h in enumerate((S1,S2),1):
            await p.set_content(f"<html><head><style>{CSS}</style></head><body>{h}</body></html>")
            await p.evaluate("document.fonts.ready")
            await p.screenshot(path=f"fob-000-{i}.png")
        await b.close()
asyncio.run(main())
