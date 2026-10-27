# 카드 스타일 에피소드 엔진: 장면 팩토리 + 렌더러 + 썸네일/커버. EP.02부터 사용
import math, os, subprocess
from PIL import Image, ImageDraw, ImageFont
from common import MONO_PATH, FPS, H
from card_style import *
from ep_utils import star

SPLIT = 1180; HEAD_Y = 1250; SUB_Y = 1490
MONO44 = ImageFont.truetype(MONO_PATH, 44); MONO30 = ImageFont.truetype(MONO_PATH, 30); MONO34 = ImageFont.truetype(MONO_PATH, 34)
PURPLE = (210, 120, 255)

def cx(el): return (W - el.width) / 2

def pop(fr, el, x, y, t, at, s0=0.8):
    p = clamp((t - at) / .35)
    if p <= 0: return
    sc = s0 + (1 - s0) * ease(p) + 0.06 * math.sin(p * math.pi)
    im = el if abs(sc - 1) < .01 else el.resize((max(1, int(el.width * sc)), max(1, int(el.height * sc))), Image.BILINEAR)
    paste(fr, im, x + (el.width - im.width) / 2, y + (el.height - im.height) / 2, min(1, p * 2))

def rise(fr, el, x, y, t, at): p = fade(t, at); paste(fr, el, x, y + 36 * (1 - p), p)

def head(fr, t, lines, sub=None):
    hd = headline(lines, 86, hl_p=ease((t - .55) / .4)); rise(fr, hd, 80, HEAD_Y, t, .1)
    if sub: rise(fr, text_el(sub, F("Bold", 42), GREY), 80, SUB_Y, t, .4)

def fit_font(s, weight, size, maxw):
    while size > 30 and tw(s, F(weight, size)) > maxw: size -= 4
    return F(weight, size)

def chat(lines, me, w=None):
    f = F("SemiBold", 42); w = w or int(max(tw(s, f) for s in lines) + 80); h = 50 + 62 * len(lines)
    c = card_el(w, h, fill=(31, 111, 235) if me else (36, 42, 52), outline=(31, 111, 235) if me else (70, 78, 88), r=34); d = ImageDraw.Draw(c)
    for i, s in enumerate(lines): d.text((36, 26 + i * 62), s, font=f, fill=WHITE)
    return c

def star_count(n):
    s = f"{n:,}"; f = F("Black", 70); c = card_el(int(tw(s, f) + 170), 150, fill=CARD, outline=(70, 78, 88), r=26, width=3); d = ImageDraw.Draw(c)
    star(d, 70, 74, 40, YEL); d.text((125, 28), s, font=f, fill=WHITE)
    return c.rotate(5, expand=True, resample=Image.BICUBIC)

def numbered(n, h, sub, col, w, hgt, active):
    c = card_el(w, hgt, outline=col if active else LINE, width=4); d = ImageDraw.Draw(c); m = (hgt - 90) // 2
    d.ellipse((30, m, 120, m + 90), fill=col); nf = F("Black", 54 if len(n) < 2 else 40)
    d.text((75 - tw(n, nf) / 2, m + 6 + (0 if len(n) < 2 else 10)), n, font=nf, fill=INK)
    hangul = any("\uac00" <= ch <= "\ud7a3" for ch in h)  # 코드 폰트엔 한글이 없음
    hf = MONO44 if h.startswith("/") and not hangul else fit_font(h, "ExtraBold", 50, w - 190)
    sc = YEL if col == ACC else GREY
    if hgt < 130:  # 낮은 행: 제목 옆에 설명
        d.text((150, m + 14), h, font=hf, fill=WHITE); x = 150 + tw(h, hf) + 30
        d.text((x, m + 22), sub, font=fit_font(sub, "SemiBold", 36, w - x - 30), fill=sc)
    else:
        d.text((150, m - 12), h, font=hf, fill=WHITE); d.text((150, m + 58), sub, font=fit_font(sub, "SemiBold", 36, w - 190), fill=sc)
    return c

def tiles(items, top=340, cols=2, tw_=440, th=230, gap=40, step=.45, first=.4):
    """items: [(큰 숫자, 설명, 색)] 숫자 타일 격자"""
    els = []
    for big, label, col in items:
        c = card_el(tw_, th, outline=col, width=4); d = ImageDraw.Draw(c)
        d.text((36, 24), big, font=F("Black", 96), fill=col); d.text((36, 150), label, font=fit_font(label, "Bold", 42, tw_ - 60), fill=WHITE); els.append(c)
    def f(fr, t):
        for i, c in enumerate(els):
            pop(fr, c, 70 + (i % cols) * (tw_ + gap) + (940 - cols * tw_ - (cols - 1) * gap) / 2, top + (i // cols) * (th + gap), t, first + i * step)
    return f

def chip(s, col=WHITE, outline=LINE, mono=False):
    f = MONO44 if mono else F("ExtraBold", 46); el = card_el(tw(s, f) + 60, 84, fill=CARD, outline=outline, r=42, width=3)
    ImageDraw.Draw(el).text((30, 14 if not mono else 16), s, font=f, fill=col); return el

# ---------- 장면 팩토리 (각각 (함수, 길이) 반환) ----------
def hook(bubble_lines, stars, head_lines, sub, dur=4.5):
    def f(fr, t):
        c = cat(800); pop(fr, c, W - c.width + 70, SPLIT - c.height + 40, t, 0, .9)
        pop(fr, bubble(bubble_lines, 60), 50, 440, t, .6)
        if t > .9: paste(fr, star_count(int(stars * ease((t - .9) / 1.8))), 40, 800, fade(t, .9))
        head(fr, t, head_lines, sub)
    return f, dur

def intro(owner, name, desc, rows, head_lines, sub, bubble_lines, dur=5.5):
    c = card_el(900, 470, outline=(70, 78, 88)); d = ImageDraw.Draw(c)
    d.text((50, 45), owner + " /", font=F("SemiBold", 50), fill=BLUE); d.text((50, 108), name, font=fit_font(name, "Black", 100, 800), fill=BLUE)
    d.text((50, 255), desc, font=fit_font(desc, "Bold", 40, 800), fill=WHITE)
    for i, (k, v) in enumerate(rows):
        d.text((50, 335 + i * 58), k, font=F("Bold", 36), fill=GREY); d.text((230, 335 + i * 58), v, font=fit_font(v, "SemiBold", 36, 620), fill=WHITE)
    card = c.rotate(-2, expand=True, resample=Image.BICUBIC); bub = bubble(bubble_lines, 54, angle=4)
    def f(fr, t):
        pop(fr, card, 80, 470, t, .2); pop(fr, bub, W - 60 - bub.width, 300, t, 1.2); head(fr, t, head_lines, sub)
    return f, dur

def rows(items, head_lines, sub, dur, top=330, row_h=140, gap=20, step=1.9, first=.5):
    """items: [(번호, 제목, 설명, 색)] 차례로 등장하는 번호 카드 목록"""
    def f(fr, t):
        for i, (n, h, s, col) in enumerate(items):
            at = first + i * step
            if t < at: continue
            p = fade(t, at, .45); c = numbered(n, h, s, col, 940, row_h, t < at + step or i == len(items) - 1)
            paste(fr, c, 70 - 100 * (1 - p), top + i * (row_h + gap), p)
        head(fr, t, head_lines, sub)
    return f, dur

def chat_demo(msgs, head_lines, sub, dur, result=None, example=True):
    """msgs: [(줄들, 내가 보냄?, 등장시각)], result: (제목, 경로/코드, 설명, 등장시각)"""
    def f(fr, t):
        if example:
            tag = text_el("예시 화면", F("Bold", 32), GREY); paste(fr, tag, W - 70 - tag.width, 215, fade(t, 0))
        y = 330
        for lines, me, at in msgs:
            b = chat(lines, me, None); rise(fr, b, (W - 70 - b.width) if me else 70, y, t, at); y += b.height + 40
        if result:
            title, mono, note, at = result
            ch = card_el(940, 210, fill=(18, 40, 28), outline=GREEN, r=30, width=4); d = ImageDraw.Draw(ch)
            d.text((40, 30), title, font=F("ExtraBold", 48), fill=WHITE); d.text((40, 100), mono, font=MONO30, fill=GREEN)
            d.text((40, 148), note, font=F("SemiBold", 34), fill=GREY); rise(fr, ch, 70, max(y, 880), t, at)
        head(fr, t, head_lines, sub)
    return f, dur

def install(lines, head_lines, sub, bubble_lines, title="claude", dur=6.5):
    """lines: 터미널에 타이핑될 줄. '>' 또는 '$'로 시작하면 명령 줄(초록)"""
    hgt = 160 + 66 * len(lines) + 80
    term = card_el(960, hgt, fill=(10, 12, 16), outline=(70, 78, 88)); td = ImageDraw.Draw(term)
    td.rectangle((3, 3, 956, 70), fill=(30, 36, 44)); [td.ellipse((28 + i * 40, 24, 50 + i * 40, 46), fill=c) for i, c in enumerate([RED, YEL, GREEN])]
    td.text((170, 18), title, font=MONO34, fill=GREY)
    bub = bubble(bubble_lines, 54, angle=-4); total = sum(map(len, lines))
    def f(fr, t):
        rise(fr, term, 60, 400, t, .2)
        if t > .7:
            d = ImageDraw.Draw(fr); k = int(total * clamp((t - .9) / 2.6)); y = 520
            for ln in lines:
                part = ln[:max(0, k)]; k -= len(ln)
                d.text((110, y), part, font=MONO44, fill=GREEN if ln[:1] in ">$" else WHITE); y += 66
            if t > 3.7: d.text((110, y + 10), "✓ installed", font=MONO44, fill=GREEN)
        pop(fr, bub, W - 60 - bub.width, min(400 + hgt + 30, SPLIT - bub.height - 20), t, 4.0)
        head(fr, t, head_lines, sub)
    return f, dur

def tips(items, head_lines, sub, dur=9.0):
    return rows([(str(i + 1), h, ex, ACC) for i, (h, ex) in enumerate(items)], head_lines, sub, dur, top=340, row_h=220, gap=40, step=2.6)

def review(pros, cons, dur=6.5):
    g = card_el(940, 300, outline=GREEN, width=4); gd = ImageDraw.Draw(g); gd.text((40, 34), "이런 분께 강추", font=F("Black", 52), fill=GREEN)
    for i, s in enumerate(pros):
        check(gd, 46, 135 + i * 85, 40, GREEN, 8); gd.text((110, 127 + i * 85), s, font=fit_font(s, "Bold", 42, 790), fill=WHITE)
    r = card_el(940, 270, outline=ACC, width=4); rd = ImageDraw.Draw(r); rd.text((40, 34), "아쉬운 점", font=F("Black", 52), fill=ACC)
    for i, s in enumerate(cons): rd.text((40, 125 + i * 60), s, font=fit_font(s, "Bold", 42, 860), fill=WHITE)
    def f(fr, t):
        rise(fr, g, 70, 360, t, .3); rise(fr, r, 70, 720, t, 2.0)
        head(fr, t, [[("솔직 평가", False)], [("강추", True), (" vs 아쉬운 점", False)]])
    return f, dur

def outro(bubble_lines, next_tag, next_title, next_sub, head_lines, sub, dur=5.0):
    n = card_el(470, 250, outline=BLUE, width=4); d = ImageDraw.Draw(n)
    d.text((36, 28), next_tag, font=F("Black", 38), fill=BLUE); d.text((36, 82), next_title, font=fit_font(next_title, "Black", 66, 400), fill=WHITE)
    d.text((36, 172), next_sub, font=fit_font(next_sub, "SemiBold", 36, 400), fill=GREY); n = n.rotate(-3, expand=True, resample=Image.BICUBIC)
    bub = bubble(bubble_lines, 58)
    def f(fr, t):
        c = cat(760); pop(fr, c, W - c.width + 70, SPLIT - c.height + 40, t, 0, .9)
        pop(fr, bub, 50, 380, t, .5); pop(fr, n, 40, 760, t, 1.1); head(fr, t, head_lines, sub)
    return f, dur

def custom(fn, head_lines, sub, dur):
    def f(fr, t): fn(fr, t); head(fr, t, head_lines, sub)
    return f, dur

# ---------- 렌더 ----------
def render(scenes, out_file, tag, footer_left, snap_prefix=None):
    base = background(W, H); paste(base, pill(tag), 70, 200); panel(base, SPLIT, H); footer(base, 1580, footer_left)
    total = sum(d for _, d in scenes)
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                             "-c:a", "aac", "-b:a", "128k", "-t", f"{total:.2f}", "-movflags", "+faststart", out_file], stdin=subprocess.PIPE)
    start = 0.0; si = 0
    for i in range(int(total * FPS)):
        gt = i / FPS
        while gt >= start + scenes[si][1]: start += scenes[si][1]; si += 1
        fn, dur = scenes[si]; lt = gt - start
        lay = layer(W, H); fn(lay, lt)
        fr = base.copy(); paste(fr, lay, 0, 0, clamp((dur - lt) / .25))
        ImageDraw.Draw(fr).rectangle((0, 0, int(W * gt / total), 8), fill=ACC)
        if snap_prefix and abs(lt - (dur - 0.6)) < 0.5 / FPS: fr.convert("RGB").resize((360, 640)).save(f"{snap_prefix}_{si:02}.png")
        proc.stdin.write(fr.tobytes())
    proc.stdin.close(); proc.wait()
    return total

def thumbnails(out_dir, tag, bubble_lines, stars_text, head_lines, footer_left):
    """4:5 썸네일 + 9:16 커버 (커버 가운데 4:5 = 썸네일과 동일)"""
    def design(h, oy):
        im = background(W, h); split = oy + 930
        paste(im, pill(tag), 70, oy + 60)
        c = cat(820); paste(im, c, W - c.width + 70, split - c.height + 40)
        panel(im, split, h)
        paste(im, bubble(bubble_lines, 60), 50, oy + 250)
        st =card_el(int(tw(stars_text, F("Black", 70)) + 170), 150, fill=CARD, outline=(70, 78, 88), r=26, width=3); d = ImageDraw.Draw(st)
        star(d, 70, 74, 40, YEL); d.text((125, 28), stars_text, font=F("Black", 70), fill=WHITE)
        paste(im, st.rotate(5, expand=True, resample=Image.BICUBIC), 40, oy + 600)
        paste(im, headline(head_lines, 86), 80, split + 70)
        footer(im, oy + 1270, footer_left)
        return im.convert("RGB")
    design(1350, 0).save(f"{out_dir}/thumbnail_4x5.png"); design(1920, 285).save(f"{out_dir}/cover_9x16.png")

def stamp_card(title, lines, stamp_text, tag=None, line_font=None, at_stamp=3.0):
    """제목 + 줄 목록 카드가 차례로 보이고, 끝에 빨간 도장이 쾅"""
    lf = line_font or F("Bold", 44); h = 150 + 78 * len(lines)
    c = card_el(900, h, fill=(24, 29, 37), outline=(70, 78, 88), r=28); d = ImageDraw.Draw(c)
    d.text((40, 34), title, font=F("Black", 50), fill=GREY)
    st = card_el(int(tw(stamp_text, F("Black", 60)) + 80), 140, fill=(40, 12, 12, 240), outline=RED, r=20, width=10)
    ImageDraw.Draw(st).text((40, 30), stamp_text, font=F("Black", 60), fill=RED); st = st.rotate(-5, expand=True, resample=Image.BICUBIC)
    def f(fr, t):
        if tag:
            el = text_el(tag, F("Bold", 32), GREY); paste(fr, el, W - 70 - el.width, 215, fade(t, 0))
        cc = c.copy(); dd = ImageDraw.Draw(cc)
        for i, s in enumerate(lines):
            if t > .6 + i * .45:
                y = 125 + i * 78; x = 40
                if s[:2] in ("☐ ", "✔ "):  # 체크박스는 직접 그림 (폰트에 기호가 없을 수 있어서)
                    dd.rounded_rectangle((40, y + 8, 84, y + 52), 8, outline=GREY if s[0] == "☐" else GREEN, width=5)
                    if s[0] == "✔": check(dd, 46, y + 12, 32, GREEN, 6)
                    s = s[2:]; x = 104
                dd.text((x, y), s, font=lf, fill=WHITE if x == 40 or "☐" in lines[i][:1] else GREY)
        rise(fr, cc, 90, 360, t, .2); pop(fr, st, (W - st.width) / 2, 360 + h - 60, t, at_stamp, 1.5)
    return f

def info_card(title, items, icon_text=None, top=360):
    """제목 + 체크 항목 카드 (설명용)"""
    h = 190 + 110 * len(items)
    c = card_el(940, h, fill=(45, 30, 18), outline=ACC, width=5); d = ImageDraw.Draw(c)
    x0 = 50
    if icon_text:
        d.rounded_rectangle((50, 46, 150, 146), 22, fill=ACC); d.text((100 - tw(icon_text, F("Black", 40)) / 2, 72), icon_text, font=F("Black", 40), fill=INK); x0 = 180
    d.text((x0, 62), title, font=fit_font(title, "Black", 56, 940 - x0 - 40), fill=WHITE)
    def f(fr, t):
        cc = c.copy(); dd = ImageDraw.Draw(cc)
        for i, (head_, sub_) in enumerate(items):
            if t > .8 + i * .7:
                y = 190 + i * 110; check(dd, 56, y + 6, 44, GREEN, 9)
                dd.text((130, y - 4), head_, font=fit_font(head_, "Bold", 44, 770), fill=WHITE)
                if sub_: dd.text((130, y + 52), sub_, font=fit_font(sub_, "SemiBold", 32, 770), fill=GREY)
        pop(fr, cc, 70, top, t, .2)
    return f
