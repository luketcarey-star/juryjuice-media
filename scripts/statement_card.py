#!/usr/bin/env python3
"""Statement/question card (Jury Juice 'stand' post): big bold white text centred on a dark gradient.
Usage: python3 scripts/statement_card.py "Text of the card" out.jpg [--logo]
1080x1350 (4:5). Text auto-sizes to fit; 4-6 lines looks best (keep to ~12 words)."""
import sys, os, re, base64, io
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
text = sys.argv[1]; out = sys.argv[2]; logo = "--logo" in sys.argv
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img = Image.new("RGB", (W, H))
px = img.load()
for x in range(W):                      # dark on the left, softly lighter on the right (diagonal tint)
    for y in range(H):
        t = min(1, max(0, (x / W) * 0.85 + (y / H) * 0.15))
        v = int(8 + 98 * (t ** 1.15))
        px[x, y] = (v, v, v + int(6 * t))
d = ImageDraw.Draw(img)
def font(sz):
    f = ImageFont.truetype(os.path.join(root, "fonts", "Montserrat.ttf"), sz)
    try: f.set_variation_by_axes([700])
    except Exception: pass
    return f
def wrap(txt, f, maxw):
    lines, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
maxw = W - 2 * 110
for sz in range(120, 50, -2):
    f = font(sz); lines = wrap(text, f, maxw)
    if len(lines) * sz * 1.22 <= H * 0.55 and len(lines) <= 6: break
lh = sz * 1.22; y0 = (H - len(lines) * lh) / 2 - 20
for i, ln in enumerate(lines):
    d.text((W / 2, y0 + i * lh), ln, font=f, fill="white", anchor="mt")
if logo:
    html = open(os.path.join(root, "renderer", "hookline.html"), encoding="utf-8").read()
    m = re.search(r'name:"Jury Juice", handle:"Juryjuice", badge:"blue", avatar:"data:image/jpeg;base64,([^"]+)"', html)
    if m:
        a = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert("RGB").resize((92, 92), Image.LANCZOS)
        mask = Image.new("L", (92, 92), 0); ImageDraw.Draw(mask).ellipse((0, 0, 91, 91), fill=255)
        img.paste(a, (W // 2 - 46, H - 190), mask)
img.save(out, quality=93)
