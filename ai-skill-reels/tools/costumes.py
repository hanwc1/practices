# 후추(assets/cat.webp) 코스튬 합성: 소품을 직접 그려 얼굴 각도에 맞춰 붙임
import math
from PIL import Image, ImageDraw, ImageFont, ImageChops

PAD = 220                     # 모자 등이 위로 튀어나올 여유
EYE_L, EYE_R = (315, 352), (440, 262)   # 원본 사진 기준 눈 중심
TILT = math.degrees(math.atan2(EYE_L[1] - EYE_R[1], EYE_R[0] - EYE_L[0]))  # ≈ 35.8° (반시계)
EYE_MID = ((EYE_L[0] + EYE_R[0]) / 2, (EYE_L[1] + EYE_R[1]) / 2)
UP = (-math.sin(math.radians(TILT)), -math.cos(math.radians(TILT)))
def head_point(dist, side=0):  # 눈 가운데에서 머리 위쪽(dist)·옆쪽(side)으로 이동한 점
    rx, ry = math.cos(math.radians(TILT)), -math.sin(math.radians(TILT))
    return (EYE_MID[0] + UP[0] * dist + rx * side, EYE_MID[1] + UP[1] * dist + ry * side)
CROWN = head_point(150)

INK = (25, 25, 30, 255); SS = 2   # 테두리 색, 슈퍼샘플링 배율
def canvas(w, h): return Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
def done(im): return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)
def s(v): return [int(x * SS) for x in v] if isinstance(v, (list, tuple)) else int(v * SS)

def put(base, prop, center, angle=TILT):
    r = prop.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(r, (int(center[0] - r.width / 2), int(center[1] + PAD - r.height / 2)))

def clip_to(layer, mask):  # 고양이 실루엣 안쪽만 남김 (옷 무늬용)
    a = ImageChops.multiply(layer.getchannel("A"), mask); layer.putalpha(a); return layer

# ---------- 소품 ----------
def eye_mask():
    w, h = 330, 130; im = canvas(w, h); d = ImageDraw.Draw(im); half = 77
    d.rounded_rectangle(s((6, 10, w - 6, h - 10)), s(56), fill=(220, 45, 55, 255), outline=INK, width=s(6))
    for sx in (-1, 1):
        cx = w / 2 + sx * half; d.ellipse(s((cx - 36, h / 2 - 34, cx + 36, h / 2 + 34)), fill=(0, 0, 0, 0), outline=INK, width=s(6))
    # 눈구멍 뚫기
    hole = Image.new("L", im.size, 0); hd = ImageDraw.Draw(hole)
    for sx in (-1, 1): cx = w / 2 + sx * half; hd.ellipse(s((cx - 31, h / 2 - 29, cx + 31, h / 2 + 29)), fill=255)
    im.putalpha(ImageChops.subtract(im.getchannel("A"), hole)); return done(im)

def cape(size):
    im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = PAD
    pts = [(250, 470 + o), (560, 440 + o), (720, 520 + o), (768, 700 + o), (768, 876 + o), (0, 876 + o), (0, 620 + o), (110, 520 + o)]
    d.polygon(pts, fill=(185, 30, 45, 255)); d.line(pts + [pts[0]], fill=INK, width=6)
    for x0, x1 in [(60, 20), (640, 740)]: d.line([(x0, 560 + o), (x1, 860 + o)], fill=(140, 20, 35, 255), width=8)
    return im

def emblem():
    w = 150; im = canvas(w, w); d = ImageDraw.Draw(im)
    d.ellipse(s((6, 6, w - 6, w - 6)), fill=(255, 205, 60, 255), outline=INK, width=s(6))
    bolt = [(82, 22), (44, 82), (72, 82), (60, 128), (106, 62), (78, 62), (92, 22)]
    d.polygon([(s(x), s(y)) for x, y in bolt], fill=(200, 35, 45, 255), outline=INK)
    return done(im)

def bone(length=260):
    h = 70; im = canvas(length, h); d = ImageDraw.Draw(im); c = (245, 236, 215, 255)
    for x in (0, length - 2 * 32):
        d.ellipse(s((x + 2, 2, x + 36, 36)), fill=c, outline=INK, width=s(5)); d.ellipse(s((x + 2, 32, x + 36, 66)), fill=c, outline=INK, width=s(5))
    d.rounded_rectangle(s((24, 20, length - 24, 50)), s(12), fill=c, outline=INK, width=s(5))
    d.rectangle(s((30, 26, length - 30, 44)), fill=c)
    return done(im)

def leopard(size, mask):
    im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = PAD
    band = [(0, 560 + o), (260, 470 + o), (768, 640 + o), (768, 876 + o), (0, 876 + o)]
    d.polygon(band, fill=(226, 168, 72, 255))
    import random; rnd = random.Random(7)
    for _ in range(70):
        x = rnd.randint(0, 768); y = rnd.randint(480, 876) + o; r = rnd.randint(14, 24)
        d.ellipse((x - r, y - r * .8, x + r, y + r * .8), outline=(70, 40, 20, 255), width=7); d.ellipse((x - r * .4, y - r * .3, x + r * .4, y + r * .3), fill=(150, 95, 40, 255))
    d.line([(0, 560 + o), (260, 470 + o), (768, 640 + o)], fill=INK, width=8)
    bm = Image.new("L", size, 0); ImageDraw.Draw(bm).polygon(band, fill=255)  # 무늬는 옷 안에만
    return clip_to(clip_to(im, bm), mask)

def club():
    w, h = 170, 430; im = canvas(w, h); d = ImageDraw.Draw(im); wood = (150, 95, 50, 255)
    d.polygon([(s(60), s(h - 10)), (s(110), s(h - 10)), (s(150), s(70)), (s(20), s(70))], fill=wood, outline=INK, width=s(6))
    d.ellipse(s((8, 8, w - 8, 190)), fill=wood, outline=INK, width=s(6))
    for x, y in [(60, 70), (110, 120), (70, 230)]: d.ellipse(s((x - 12, y - 9, x + 12, y + 9)), fill=(110, 65, 30, 255))
    return done(im)

def beret():
    w, h = 340, 170; im = canvas(w, h); d = ImageDraw.Draw(im); c = (40, 40, 52, 255)
    d.ellipse(s((10, 30, w - 10, h - 20)), fill=c, outline=INK, width=s(6))
    d.ellipse(s((w / 2 - 70, h - 60, w / 2 + 110, h - 18)), fill=(60, 60, 75, 255))
    d.rounded_rectangle(s((w / 2 - 8, 4, w / 2 + 8, 40)), s(6), fill=c, outline=INK, width=s(4))
    return done(im)

def palette():
    w, h = 330, 240; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.ellipse(s((6, 6, w - 6, h - 6)), fill=(236, 205, 150, 255), outline=INK, width=s(6))
    d.ellipse(s((210, 140, 262, 190)), fill=(0, 0, 0, 0))
    hole = Image.new("L", im.size, 0); ImageDraw.Draw(hole).ellipse(s((214, 144, 258, 186)), fill=255)
    im.putalpha(ImageChops.subtract(im.getchannel("A"), hole)); d = ImageDraw.Draw(im)
    d.ellipse(s((210, 140, 262, 190)), outline=INK, width=s(5))
    for (x, y), c in zip([(70, 70), (130, 45), (195, 55), (60, 140), (120, 175)], [(255, 140, 66), (88, 166, 255), (63, 185, 80), (255, 214, 90), (210, 120, 255)]):
        d.ellipse(s((x - 26, y - 22, x + 26, y + 22)), fill=c + (255,), outline=INK, width=s(4))
    return done(im)

def brush():
    w, h = 60, 330; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle(s((20, 90, 40, h - 6)), s(8), fill=(190, 60, 50, 255), outline=INK, width=s(4))
    d.rectangle(s((16, 70, 44, 100)), fill=(200, 200, 210, 255), outline=INK, width=s(4))
    d.polygon([(s(16), s(72)), (s(44), s(72)), (s(30), s(6))], fill=(255, 140, 66, 255), outline=INK)
    return done(im)

def fedora():
    w, h = 380, 210; im = canvas(w, h); d = ImageDraw.Draw(im); c = (92, 70, 52, 255)
    d.ellipse(s((6, h - 80, w - 6, h - 8)), fill=c, outline=INK, width=s(6))
    d.polygon([(s(85), s(h - 50)), (s(w - 85), s(h - 50)), (s(w - 110), s(20)), (s(110), s(20))], fill=c, outline=INK, width=s(6))
    d.line([(s(150), s(24)), (s(w / 2), s(52)), (s(w - 150), s(24))], fill=(70, 52, 38, 255), width=s(8))
    d.rectangle(s((92, h - 92, w - 92, h - 58)), fill=(35, 30, 30, 255))
    return done(im)

def magnifier(photo):
    r = 74; w, h = 2 * r + 40, 2 * r + 190; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); cx, cy = w // 2, r + 20
    ex, ey = EYE_R; crop = photo.crop((int(ex - r / 1.6), int(ey - r / 1.6), int(ex + r / 1.6), int(ey + r / 1.6))).resize((2 * r, 2 * r), Image.LANCZOS)
    crop = crop.rotate(-TILT, resample=Image.BICUBIC)  # 렌즈 전체가 TILT만큼 돌아가므로 미리 반대로
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    glass = Image.new("RGBA", (2 * r, 2 * r), (200, 225, 255, 255)); glass.alpha_composite(crop)
    tint = Image.new("RGBA", (2 * r, 2 * r), (180, 210, 255, 50)); glass.alpha_composite(tint); glass.putalpha(m)
    im.alpha_composite(glass, (cx - r, cy - r)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((cx - 13, cy + r + 4, cx + 13, h - 6), 10, fill=(60, 45, 35, 255), outline=INK, width=5)
    d.ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), outline=(50, 50, 58, 255), width=14)
    d.ellipse((cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), outline=INK, width=4)
    d.arc((cx - r + 18, cy - r + 18, cx + 10, cy + 10), 190, 260, fill=(255, 255, 255, 200), width=8)
    return im, (cx, cy)

def glasses():
    w, h = 330, 120; im = canvas(w, h); d = ImageDraw.Draw(im); half = 77; r = 50
    for sx in (-1, 1):
        cx = w / 2 + sx * half
        d.ellipse(s((cx - r, h / 2 - r, cx + r, h / 2 + r)), fill=(170, 210, 255, 55), outline=INK, width=s(8))
        d.arc(s((cx - r + 14, h / 2 - r + 14, cx + 6, h / 2 + 6)), 190, 250, fill=(255, 255, 255, 190), width=s(5))
    d.arc(s((w / 2 - 30, h / 2 - 26, w / 2 + 30, h / 2 + 20)), 200, 340, fill=INK, width=s(8))
    return done(im)

def laptop(mono):
    w, h = 430, 300; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle(s((10, 6, w - 10, h - 46)), s(20), fill=(205, 210, 220, 255), outline=INK, width=s(6))
    d.polygon([(s(0), s(h - 46)), (s(w), s(h - 46)), (s(w - 24), s(h - 6)), (s(24), s(h - 6))], fill=(170, 176, 188, 255), outline=INK)
    f = ImageFont.truetype(mono, s(70)); t = "</>"; tl = d.textlength(t, font=f)
    d.text(((s(w) - tl) / 2, s(80)), t, font=f, fill=(255, 140, 66, 255))
    return done(im)

def mug():
    w, h = 130, 150; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.arc(s((70, 60, 124, 116)), 270, 90, fill=INK, width=s(10))
    d.rounded_rectangle(s((10, 50, 96, h - 6)), s(14), fill=(255, 140, 66, 255), outline=INK, width=s(6))
    for x in (30, 58): d.arc(s((x - 10, 4, x + 10, 44)), 100, 260, fill=(220, 220, 230, 230), width=s(5))
    return done(im)

def mortarboard():
    w, h = 360, 230; im = canvas(w, h); d = ImageDraw.Draw(im); c = (30, 32, 40, 255)
    d.polygon([(s(110), s(120)), (s(250), s(120)), (s(240), s(200)), (s(120), s(200))], fill=c, outline=INK, width=s(5))
    d.polygon([(s(180), s(30)), (s(350), s(100)), (s(180), s(160)), (s(10), s(100))], fill=(45, 48, 58, 255), outline=INK, width=s(6))
    d.ellipse(s((170, 86, 190, 106)), fill=(255, 205, 60, 255))
    d.line([(s(180), s(96)), (s(300), s(130)), (s(305), s(200))], fill=(255, 205, 60, 255), width=s(6))
    d.rounded_rectangle(s((292, 195, 318, 228)), s(6), fill=(255, 205, 60, 255), outline=INK, width=s(3))
    return done(im)

def bowtie(col=(220, 45, 55, 255)):
    w, h = 190, 100; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.polygon([(s(95), s(50)), (s(8), s(8)), (s(8), s(92))], fill=col, outline=INK, width=s(5))
    d.polygon([(s(95), s(50)), (s(182), s(8)), (s(182), s(92))], fill=col, outline=INK, width=s(5))
    d.rounded_rectangle(s((76, 30, 114, 70)), s(10), fill=col, outline=INK, width=s(5)); return done(im)

def quill():
    w, h = 110, 340; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.polygon([(s(55), s(4)), (s(100), s(120)), (s(70), s(250)), (s(55), s(270)), (s(40), s(250)), (s(10), s(120))], fill=(250, 250, 245, 255), outline=INK, width=s(5))
    d.line([(s(55), s(20)), (s(55), s(300))], fill=(150, 150, 160, 255), width=s(4))
    for y in range(60, 240, 30): d.line([(s(55), s(y)), (s(25 if y % 60 else 85), s(y + 22))], fill=(200, 200, 210, 255), width=s(3))
    d.polygon([(s(48), s(290)), (s(62), s(290)), (s(55), s(336))], fill=(40, 40, 50, 255)); return done(im)

def manuscript(font):
    w, h = 300, 220; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle(s((6, 6, w - 6, h - 6)), s(14), fill=(255, 252, 240, 255), outline=INK, width=s(6))
    for i in range(5): d.line([(s(30), s(60 + i * 32)), (s(w - 30 - (60 if i == 4 else 0)), s(60 + i * 32))], fill=(180, 190, 210, 255), width=s(3))
    f = ImageFont.truetype(font, s(34)); d.text((s(30), s(10)), "사람 말투", font=f, fill=(220, 60, 60, 255)); return done(im)

def necktie():
    w, h = 120, 300; im = canvas(w, h); d = ImageDraw.Draw(im); c = (40, 90, 200, 255)
    d.polygon([(s(30), s(6)), (s(90), s(6)), (s(78), s(56)), (s(42), s(56))], fill=c, outline=INK, width=s(5))
    d.polygon([(s(42), s(56)), (s(78), s(56)), (s(104), s(240)), (s(60), s(294)), (s(16), s(240))], fill=c, outline=INK, width=s(5))
    for y in (100, 160, 220): d.line([(s(30), s(y + 20)), (s(90), s(y - 20))], fill=(255, 205, 60, 255), width=s(6))
    return done(im)

def badge(text, font):
    w, h = 220, 120; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle(s((6, 6, w - 6, h - 6)), s(16), fill=(255, 255, 255, 255), outline=INK, width=s(6))
    d.rectangle(s((12, 12, w - 12, 40)), fill=(255, 140, 66, 255))
    f = ImageFont.truetype(font, s(56)); tl = d.textlength(text, font=f); d.text(((s(w) - tl) / 2, s(42)), text, font=f, fill=INK); return done(im)

def megaphone():
    w, h = 300, 220; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.polygon([(s(70), s(80)), (s(270), s(10)), (s(270), s(210)), (s(70), s(140))], fill=(255, 140, 66, 255), outline=INK, width=s(6))
    d.ellipse(s((240, 10, 296, 210)), fill=(255, 190, 120, 255), outline=INK, width=s(6))
    d.rounded_rectangle(s((20, 76, 80, 144)), s(12), fill=(230, 230, 240, 255), outline=INK, width=s(6))
    d.rounded_rectangle(s((90, 140, 130, 210)), s(10), fill=(60, 60, 70, 255), outline=INK, width=s(5))
    return done(im)

def growth_chart():
    w, h = 260, 220; im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle(s((6, 6, w - 6, h - 6)), s(16), fill=(255, 255, 255, 255), outline=INK, width=s(6))
    for i, (bh, c) in enumerate([(50, (88, 166, 255)), (90, (63, 185, 80)), (140, (255, 140, 66))]):
        x = 40 + i * 65; d.rectangle(s((x, 190 - bh, x + 45, 190)), fill=c + (255,), outline=INK, width=s(4))
    d.line([(s(40), s(130)), (s(110), s(95)), (s(150), s(105)), (s(225), s(35))], fill=(220, 45, 55, 255), width=s(8))
    d.polygon([(s(232), s(26)), (s(200), s(34)), (s(222), s(58))], fill=(220, 45, 55, 255)); return done(im)

def postit(text, font, col=(255, 228, 92, 255)):
    w = 170; im = canvas(w, w); d = ImageDraw.Draw(im)
    d.rectangle(s((8, 8, w - 8, w - 8)), fill=col, outline=INK, width=s(5)); d.rectangle(s((8, 8, w - 8, 34)), fill=tuple(max(0, v - 30) for v in col[:3]) + (255,))
    size = 44
    while size > 20 and d.textlength(text, font=ImageFont.truetype(font, s(size))) > s(w - 34): size -= 2
    f = ImageFont.truetype(font, s(size)); tl = d.textlength(text, font=f); d.text(((s(w) - tl) / 2, s(66 + (44 - size) / 2)), text, font=f, fill=INK); return done(im)

# ---------- 코스튬 조합 ----------
def dress(photo, name, mono_path):
    global KFONT; KFONT = mono_path.replace("JetBrainsMono-Bold.ttf", "Pretendard-Black.otf")
    """photo: 원본 RGBA(768x876). 위쪽에 PAD만큼 여유를 둔 합성 이미지를 돌려줌"""
    W0, H0 = photo.size; size = (W0, H0 + PAD); base = Image.new("RGBA", size, (0, 0, 0, 0))
    mask = Image.new("L", size, 0); mask.paste(photo.getchannel("A"), (0, PAD))
    if name == "hero":
        base.alpha_composite(cape(size)); base.alpha_composite(photo, (0, PAD))
        put(base, eye_mask(), EYE_MID); put(base, emblem(), (430, 640), TILT * .3)
    elif name == "caveman":
        base.alpha_composite(photo, (0, PAD)); base.alpha_composite(leopard(size, mask))
        put(base, bone(), head_point(150, -10), TILT - 18); put(base, club(), (150, 700), 28)
    elif name == "artist":
        base.alpha_composite(photo, (0, PAD))
        put(base, beret(), head_point(138, -12), TILT + 8); put(base, palette(), (190, 720), 14); put(base, brush(), (590, 700), -28)
    elif name == "detective":
        base.alpha_composite(photo, (0, PAD))
        put(base, fedora(), head_point(175, -20), TILT)
        lens, (lx, ly) = magnifier(photo); r = lens.rotate(TILT, expand=True, resample=Image.BICUBIC)
        # 렌즈 중심이 오른쪽 눈 위에 오도록 회전 후 위치 보정
        ang = math.radians(TILT); dx, dy = lx - lens.width / 2, ly - lens.height / 2
        rx, ry = dx * math.cos(ang) + dy * math.sin(ang), -dx * math.sin(ang) + dy * math.cos(ang)
        base.alpha_composite(r, (int(EYE_R[0] - r.width / 2 - rx), int(EYE_R[1] + PAD - r.height / 2 - ry)))
    elif name == "dev":
        base.alpha_composite(photo, (0, PAD))
        put(base, glasses(), EYE_MID); put(base, laptop(mono_path), (420, 720), 0); put(base, mug(), (110, 770), 0)
    elif name == "professor":
        base.alpha_composite(photo, (0, PAD))
        put(base, mortarboard(), head_point(165, -10), TILT); put(base, bowtie(), (440, 478), TILT * .4)
    elif name == "writer":
        base.alpha_composite(photo, (0, PAD))
        put(base, quill(), (215, 150), TILT + 22); put(base, manuscript(KFONT), (200, 730), 10)
    elif name == "ceo":
        base.alpha_composite(photo, (0, PAD))
        put(base, necktie(), (445, 600), TILT * .25); put(base, badge("CEO", KFONT), (230, 660), 8)
    elif name == "marketer":
        base.alpha_composite(photo, (0, PAD))
        put(base, megaphone(), (170, 640), 160); put(base, growth_chart(), (610, 730), -8)
    elif name == "memory":
        base.alpha_composite(photo, (0, PAD))
        put(base, postit("기억!", KFONT), head_point(120, -70), TILT + 12)
        put(base, postit("TODO", KFONT, (150, 220, 255, 255)), head_point(105, 85), TILT - 14)
        put(base, postit("어제 한 일", KFONT, (255, 170, 200, 255)), (230, 700), -6)
    else:
        base.alpha_composite(photo, (0, PAD))
    return base
