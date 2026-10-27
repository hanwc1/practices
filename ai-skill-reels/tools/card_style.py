# @aimateur.lab 카드 스타일: 손글씨 태그, 고양이 스티커, 말풍선, 하단 헤드라인 패널 (다크 네이비 + 주황/노랑)
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from common import (S, W, MONO_PATH, BG, CARD, LINE, WHITE, GREY, ACC, GREEN, BLUE, YEL, RED, F, layer, paste, text_el, rich_el,
                    card_el, tw, clamp, ease, fade, check)

HAND = f"{S}/fonts/Gaegu-Bold.ttf"
def HF(s): return ImageFont.truetype(HAND, s)
INK = (20, 20, 24); PANEL = (24, 29, 37); HANDLE = "@aimateur.lab"
CAT_PATH = os.path.join(os.path.dirname(S), "assets", "cat.webp")

def background(w, h):
    bg = Image.new("RGBA", (w, h), BG + (255,)); d = ImageDraw.Draw(bg)
    for x in range(0, w, 60): d.line([(x, 0), (x, h)], fill=(19, 24, 31))
    for y in range(0, h, 60): d.line([(0, y), (w, y)], fill=(19, 24, 31))
    g = layer(w, h); ImageDraw.Draw(g).ellipse((-300, -700, w + 300, 700), fill=ACC + (40,)); bg.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    return bg

def pill(text, size=44):
    f = HF(size); w = tw(text, f) + 64; h = int(size * 1.45)
    im = card_el(w, h, fill=ACC, outline=ACC, r=h // 2); ImageDraw.Draw(im).text((32, size * 0.14), text, font=f, fill=INK); return im

def sticker(img, outline=14, shadow=True):
    a = img.getchannel("A").point(lambda v: 255 if v > 40 else 0)
    big = Image.new("L", (img.width + outline * 4, img.height + outline * 4), 0); big.paste(a, (outline * 2, outline * 2))
    ring = big.filter(ImageFilter.MaxFilter(outline * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
    out = layer(big.width, big.height)
    if shadow:
        sh = layer(big.width, big.height); sh.paste((0, 0, 0, 150), (0, 0), ring); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (0, 0))
        out = out.transform(out.size, Image.AFFINE, (1, 0, -6, 0, 1, -12))  # 그림자 살짝 아래로
    wl = layer(big.width, big.height); wl.paste((255, 255, 255, 255), (0, 0), ring); out.alpha_composite(wl)
    out.alpha_composite(img, (outline * 2, outline * 2)); return out

_cat_cache = {}
COSTUME = None  # 편마다 설정: hero, caveman, artist, detective, dev (costumes.py)
def cat(height, flip=False, costume=None):
    """height = 후추 사진 높이. 코스튬의 모자 등이 위로 튀어나온 만큼 이미지가 더 커짐"""
    costume = costume or COSTUME; k = (height, flip, costume)
    if k not in _cat_cache:
        im = Image.open(CAT_PATH).convert("RGBA"); h = height
        if costume:
            from costumes import dress, PAD
            im = dress(im, costume, MONO_PATH); h = int(height * im.height / (im.height - PAD))
        im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        _cat_cache[k] = sticker(im)
    return _cat_cache[k]

def bubble(lines, size=58, w=None, angle=-3):
    f = HF(size); lw = max(tw(s, f) for s in lines); w = w or int(lw + 110); h = int(70 + size * 1.25 * len(lines))
    im = card_el(w, h, fill=(255, 255, 255), outline=INK, r=40, width=6); d = ImageDraw.Draw(im)
    for i, s in enumerate(lines): d.text((55, 30 + i * size * 1.25), s, font=f, fill=INK)
    return im.rotate(angle, expand=True, resample=Image.BICUBIC)

def headline(lines, size=84, hl_p=1.0):
    """lines: [[(text, highlight?), ...], ...] → 형광펜 강조가 들어간 헤드라인 이미지"""
    f = F("Black", size); lh = int(size * 1.25); wmax = max(sum(tw(s, f) for s, _ in ln) for ln in lines)
    im = layer(wmax + 20, lh * len(lines) + 10); d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = 0; y = i * lh
        for s, hl in ln:
            sw = tw(s, f)
            if hl and hl_p > 0: d.rectangle((x - 6, y + size * 0.62, x - 6 + (sw + 12) * hl_p, y + size * 1.12), fill=ACC + (235,))
            x += sw
        x = 0
        for s, hl in ln: d.text((x, y), s, font=f, fill=WHITE); x += tw(s, f)
    return im

def panel(fr, split_y, h):
    d = ImageDraw.Draw(fr); d.rectangle((0, split_y, W, h), fill=PANEL); d.rectangle((0, split_y - 3, W, split_y + 3), fill=ACC)

def footer(fr, y, left):
    d = ImageDraw.Draw(fr); f = F("Bold", 36)
    d.text((80, y), left, font=f, fill=GREY); d.text((W - 80 - tw(HANDLE, f), y), HANDLE, font=f, fill=GREY)

def star_sticker(n_text, angle=4):
    c = card_el(480, 150, fill=CARD, outline=(70, 78, 88), r=26, width=3); d = ImageDraw.Draw(c)
    from ep_utils import star
    star(d, 70, 74, 40, YEL); d.text((125, 28), n_text, font=F("Black", 70), fill=WHITE)
    return c.rotate(angle, expand=True, resample=Image.BICUBIC)
