# EP.01 (튜토리얼판) 렌더러: pptx 스킬 사용법. 내레이션 없이 화면 텍스트 중심, PIL 프레임 -> ffmpeg
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FD = f"{S}/fonts"
MONO_PATH = f"{S}/fonts/JetBrainsMono-Bold.ttf"
W, H, FPS = 1080, 1920, 30

def F(w, s): return ImageFont.truetype(f"{FD}/Pretendard-{w}.otf", s)
MONO = ImageFont.truetype(MONO_PATH, 34)
BG = (13, 17, 23); CARD = (24, 29, 37); LINE = (52, 58, 66)
WHITE = (240, 246, 252); GREY = (150, 158, 168)
ACC = (255, 140, 66); GREEN = (63, 185, 80); BLUE = (88, 166, 255); YEL = (255, 214, 90); RED = (248, 81, 73)

def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def layer(w, h): return Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
_d = ImageDraw.Draw(layer(1, 1))
def tw(s, f): return _d.textlength(s, font=f)

def paste(base, el, x, y, a=1.0):
    if a <= 0: return
    if a < 1:
        el = el.copy(); el.putalpha(el.getchannel("A").point(lambda v: int(v * a)))
    base.alpha_composite(el, (int(x), int(y)))

def text_el(s, f, fill=WHITE):
    bb = _d.textbbox((0, 0), s, font=f); im = layer(bb[2] + 4, bb[3] + 10)
    ImageDraw.Draw(im).text((0, 0), s, font=f, fill=fill); return im

def rich_el(parts, f):
    w = sum(tw(s, f) for s, _ in parts); im = layer(w + 4, f.size * 1.35); d = ImageDraw.Draw(im); x = 0
    for s, c in parts: d.text((x, 0), s, font=f, fill=c); x += tw(s, f)
    return im

def card_el(w, h, fill=CARD, outline=LINE, r=28, width=3):
    im = layer(w, h); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=outline, width=width); return im

def shadowed(im, r=30, a=150):
    pad = r * 2; sh = layer(im.width + pad * 2, im.height + pad * 2)
    m = Image.new("L", im.size, a); sh.paste((0, 0, 0, 255), (pad, pad + 14), m)
    sh = sh.filter(ImageFilter.GaussianBlur(r)); sh.alpha_composite(im, (pad, pad)); return sh, pad

def check(d, x, y, s, c, w=8):
    d.line([(x, y + s * .5), (x + s * .38, y + s * .85), (x + s, y + s * .1)], fill=c, width=w, joint="curve")

def cx(el): return (W - el.width) / 2

# 공통 배경
bg = Image.new("RGBA", (W, H), BG + (255,)); d = ImageDraw.Draw(bg)
for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(19, 24, 31))
for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(19, 24, 31))
g = layer(W, H); ImageDraw.Draw(g).ellipse((-300, -700, W + 300, 700), fill=ACC + (40,)); bg.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
def make_bg(tag):
    b = bg.copy(); pill = rich_el([("GitHub 인기 AI 스킬  ", WHITE), (tag, ACC)], F("Bold", 34))
    pb = card_el(pill.width + 56, 70, fill=(30, 36, 44, 235), r=35, width=2); pb.alpha_composite(pill, (28, 13)); b.alpha_composite(pb, (int(cx(pb)), 215)); return b

TITLE = F("ExtraBold", 84); BIG = F("Black", 100); BODY = F("Bold", 48); SMALL = F("SemiBold", 38)

def toggle(d, x, y, on):  # on: 0~1 애니메이션 진행
    c = tuple(int(LINE[k] + (GREEN[k] - LINE[k]) * on) for k in range(3))
    d.rounded_rectangle((x, y, x + 130, y + 72), 36, fill=c); kx = x + 8 + 58 * on
    d.ellipse((kx, y + 8, kx + 56, y + 64), fill=WHITE)

def tap(fr, x, y, p):  # 터치 표시 동그라미
    if 0 <= p <= 1:
        r = 30 + 50 * p; a = int(200 * (1 - p)); o = layer(W, H)
        ImageDraw.Draw(o).ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, a), width=8); fr.alpha_composite(o)

def step_header(fr, n, title, t):
    e = ease(t / 0.4)
    b = card_el(190, 76, fill=ACC, outline=ACC, r=38); ImageDraw.Draw(b).text((30, 12), f"STEP {n}", font=F("Black", 44), fill=(20, 20, 20))
    paste(fr, b, cx(b), 340 - 30 * (1 - e), e)
    tt = text_el(title, TITLE); paste(fr, tt, cx(tt), 450 - 30 * (1 - ease((t - .15) / .4)), ease((t - .15) / .4))

def fade(t, a, dur=0.4): return ease((t - a) / dur)

