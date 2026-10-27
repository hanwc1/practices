# EP.01 obra/superpowers 릴스 (카드 스타일 v2): 위쪽 비주얼 + 아래쪽 헤드라인 패널, 고양이 말풍선, 무음
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
from common import MONO_PATH, FPS, H
from card_style import *
import card_style; card_style.COSTUME = "hero"
from ep_utils import star

OUT = sys.argv[1]
os.makedirs(f"{S}/build", exist_ok=True)
STARS = 306000  # 2026-10-26 GitHub 저장소 페이지 기준
SPLIT = 1180; HEAD_Y = 1250; SUB_Y = 1490
MONO44 = ImageFont.truetype(MONO_PATH, 44); MONO30 = ImageFont.truetype(MONO_PATH, 30)

BASE = background(W, H); paste(BASE, pill("GitHub 인기 스킬 #1"), 70, 200)
panel(BASE, SPLIT, H); footer(BASE, 1580, "EP.01 · obra/superpowers")

def cx(el): return (W - el.width) / 2

def pop(fr, el, x, y, t, at, s0=0.8):  # 통통 튀며 등장
    p = clamp((t - at) / .35)
    if p <= 0: return
    sc = s0 + (1 - s0) * ease(p) + 0.06 * math.sin(p * math.pi)
    im = el if abs(sc - 1) < .01 else el.resize((max(1, int(el.width * sc)), max(1, int(el.height * sc))), Image.BILINEAR)
    paste(fr, im, x + (el.width - im.width) / 2, y + (el.height - im.height) / 2, min(1, p * 2))

def rise(fr, el, x, y, t, at): p = fade(t, at); paste(fr, el, x, y + 36 * (1 - p), p)

def head(fr, t, lines, sub=None):
    hd = headline(lines, 86, hl_p=ease((t - .55) / .4)); rise(fr, hd, 80, HEAD_Y, t, .1)
    if sub: rise(fr, text_el(sub, F("Bold", 42), GREY), 80, SUB_Y, t, .4)

def chat(lines, me, w):
    f = F("SemiBold", 42); h = 50 + 62 * len(lines)
    c = card_el(w, h, fill=(31, 111, 235) if me else (36, 42, 52), outline=(31, 111, 235) if me else (70, 78, 88), r=34); d = ImageDraw.Draw(c)
    for i, s in enumerate(lines): d.text((36, 26 + i * 62), s, font=f, fill=WHITE)
    return c

def star_count(n):
    c = card_el(480, 150, fill=CARD, outline=(70, 78, 88), r=26, width=3); d = ImageDraw.Draw(c)
    star(d, 70, 74, 40, YEL); d.text((125, 28), f"{n:,}", font=F("Black", 70), fill=WHITE)
    return c.rotate(5, expand=True, resample=Image.BICUBIC)

def numbered(n, h, sub, col, w, hgt, active):
    c = card_el(w, hgt, outline=col if active else LINE, width=4); d = ImageDraw.Draw(c); m = (hgt - 90) // 2
    d.ellipse((30, m, 120, m + 90), fill=col); d.text((75 - tw(n, F("Black", 54)) / 2, m + 6), n, font=F("Black", 54), fill=INK)
    d.text((150, m - 12), h, font=F("ExtraBold", 50), fill=WHITE); d.text((150, m + 58), sub, font=F("SemiBold", 36), fill=GREY if col != ACC else YEL)
    return c

# ---------- 장면 ----------
def s_hook(fr, t):
    c = cat(800); pop(fr, c, W - c.width + 70, SPLIT - c.height + 40, t, 0, .9)
    pop(fr, bubble(["별이 30만 개", "실화냥?"], 60), 50, 440, t, .6)
    if t > .9: paste(fr, star_count(int(STARS * ease((t - .9) / 1.8))), 40, 800, fade(t, .9))
    head(fr, t, [[("GitHub 별 30만 개,", False)], [("이 스킬 ", False), ("뭐길래?", True)]], "개발자들이 열광하는 그 스킬")

def s_intro(fr, t):
    c = card_el(900, 470, outline=(70, 78, 88)); d = ImageDraw.Draw(c)
    d.text((50, 45), "obra /", font=F("SemiBold", 50), fill=BLUE); d.text((50, 108), "superpowers", font=F("Black", 100), fill=BLUE)
    d.text((50, 255), "AI 코딩 에이전트용 스킬 + 개발 방법론", font=F("Bold", 40), fill=WHITE)
    for i, (k, v) in enumerate([("라이선스", "MIT · 무료"), ("지원", "Claude Code · Codex · Cursor 등")]):
        d.text((50, 335 + i * 58), k, font=F("Bold", 36), fill=GREY); d.text((230, 335 + i * 58), v, font=F("SemiBold", 36), fill=WHITE)
    pop(fr, c.rotate(-2, expand=True, resample=Image.BICUBIC), 80, 470, t, .2)
    pop(fr, bubble(["이름부터", "세다냥"], 54, angle=4), 640, 320, t, 1.2)
    head(fr, t, [[("오늘의 스킬은", False)], [("superpowers", True)]], "개인 개발자가 만든 커뮤니티 스킬")

def s_problem(fr, t):
    u = chat(["할 일 관리 앱 만들어줘"], True, 620); rise(fr, u, W - 70 - u.width, 340, t, .3)
    if t > 1.0:
        p = clamp((t - 1.0) / 1.8); box = card_el(900, 540, fill=(10, 12, 16), outline=(70, 78, 88), r=28); bd = ImageDraw.Draw(box)
        cols = [BLUE, WHITE, GREEN, GREY, YEL, WHITE, BLUE, GREY, GREEN, WHITE]
        for i in range(min(10, int(10 * p) + 1)):
            ind = [0, 1, 2, 2, 1, 2, 3, 3, 2, 0][i] * 40
            bd.rounded_rectangle((40 + ind, 40 + i * 48, 40 + ind + [520, 420, 600, 380, 500, 640, 300, 450, 560, 200][i], 62 + i * 48), 11, fill=cols[i])
        paste(fr, box, 90, 520, fade(t, 1.0, .3))
    if t > 3.0:
        st = card_el(640, 140, fill=(40, 12, 12, 240), outline=RED, r=20, width=10); sd = ImageDraw.Draw(st)
        s = "내가 원한 거 아닌데…"; sd.text(((640 - tw(s, F("Black", 64))) / 2, 28), s, font=F("Black", 64), fill=RED)
        pop(fr, st.rotate(-6, expand=True, resample=Image.BICUBIC), 210, 700, t, 3.0, 1.5)
    head(fr, t, [[("AI 코딩,", False)], [("이런 적 있죠?", True)]], "묻지도 않고 코드부터 300줄…")

def s_solution(fr, t):
    c = cat(760, flip=True); pop(fr, c, -70, SPLIT - c.height + 40, t, 0, .9)
    pop(fr, bubble(["순서만 바꾸면", "된다냥!"], 60, angle=3), 520, 400, t, .6)
    chips = ["묻고", "설계하고", "테스트하고", "만든다"]
    for i, s in enumerate(chips):
        el = card_el(tw(s, F("ExtraBold", 46)) + 60, 84, fill=CARD, outline=ACC if i == 3 else LINE, r=42, width=3)
        ImageDraw.Draw(el).text((30, 14), s, font=F("ExtraBold", 46), fill=YEL if i == 3 else WHITE)
        rise(fr, el, 620, 700 + i * 105, t, 1.2 + i * .35)
    head(fr, t, [[("AI가 일하는", False)], [("순서", True), ("가 바뀌어요", False)]], "superpowers를 깔면 생기는 변화")

FLOW = [("브레인스토밍", "질문부터, 한 번에 하나씩", BLUE), ("설계 문서", "승인 전엔 코드 0줄", (210, 120, 255)),
        ("작업 계획", "작은 단위로 쪼개기", YEL), ("테스트 먼저 (TDD)", "실패하는 테스트 → 코드", GREEN), ("코드 리뷰", "계획대로 됐는지 검사", ACC)]
def s_flow(fr, t):
    for i, (h, sub, col) in enumerate(FLOW):
        at = .5 + i * 1.9
        if t < at: continue
        p = fade(t, at, .45); c = numbered(str(i + 1), h, sub, col, 940, 140, t < at + 1.9 or i == 4)
        paste(fr, c, 70 - 100 * (1 - p), 330 + i * 160, p)
    head(fr, t, [[("자동으로 돌아가는", False)], [("5단계", True)]], "스킬이 알아서 순서대로 켜져요")

def s_demo(fr, t):
    tag = text_el("예시 화면", F("Bold", 32), GREY); paste(fr, tag, W - 70 - tag.width, 215, fade(t, 0))
    u = chat(["할 일 관리 앱 만들어줘"], True, 620); rise(fr, u, W - 70 - u.width, 330, t, .3)
    a = chat(["만들기 전에 하나만 여쭤볼게요.", "혼자 쓰시나요, 팀이 같이 쓰나요?"], False, 880); rise(fr, a, 70, 480, t, 1.4)
    u2 = chat(["팀 3명이 같이 써요"], True, 560); rise(fr, u2, W - 70 - u2.width, 710, t, 3.2)
    ch = card_el(900, 210, fill=(18, 40, 28), outline=GREEN, r=30, width=4); d = ImageDraw.Draw(ch)
    d.text((40, 30), "설계 문서 작성 완료", font=F("ExtraBold", 48), fill=WHITE)
    d.text((40, 100), "docs/superpowers/specs/…-design.md", font=MONO30, fill=GREEN)
    d.text((40, 148), "승인하시면 계획 → 테스트 → 구현 시작", font=F("SemiBold", 34), fill=GREY)
    rise(fr, ch, 70, 880, t, 4.6)
    head(fr, t, [[("깔고 나면", False)], [("이렇게 달라져요", True)]], "승인 전엔 코드 한 줄도 안 써요")

def s_install(fr, t):
    term = card_el(960, 470, fill=(10, 12, 16), outline=(70, 78, 88)); td = ImageDraw.Draw(term)
    td.rectangle((3, 3, 956, 70), fill=(30, 36, 44)); [td.ellipse((28 + i * 40, 24, 50 + i * 40, 46), fill=c) for i, c in enumerate([RED, YEL, GREEN])]
    td.text((170, 18), "claude", font=ImageFont.truetype(MONO_PATH, 34), fill=GREY)
    rise(fr, term, 60, 420, t, .2)
    if t > .7:
        d = ImageDraw.Draw(fr); lines = ["> /plugin install", "  superpowers", "  @claude-plugins-official"]
        k = int(sum(map(len, lines)) * clamp((t - .9) / 2.4)); y = 540
        for ln in lines:
            part = ln[:max(0, k)]; k -= len(ln); d.text((110, y), part, font=MONO44, fill=GREEN if ln.startswith(">") else WHITE); y += 66
        if t > 3.5: d.text((110, y + 10), "✓ installed", font=MONO44, fill=GREEN)
    pop(fr, bubble(["복붙하면", "끝이다냥"], 54, angle=-4), 580, 930, t, 3.8)
    head(fr, t, [[("설치는", False)], [("딱 한 줄", True)]], "Claude Code 기준 · 다른 도구는 README 참고")

TIPS = [("명령어 필요 없음", "평소처럼 \"~ 만들자\"라고 말하기"), ("질문엔 꼼꼼히 답하기", "구체적일수록 결과가 좋아져요"), ("설계 문서는 꼭 읽기", "여기서 방향 잡아야 안 꼬여요")]
def s_tips(fr, t):
    for i, (h, ex) in enumerate(TIPS):
        at = .5 + i * 2.6
        if t < at: continue
        p = fade(t, at, .45); c = numbered(str(i + 1), h, ex, ACC, 940, 220, t < at + 2.6 or i == 2)
        paste(fr, c, 70 - 100 * (1 - p), 340 + i * 260, p)
    head(fr, t, [[("사용법", False)], [("꿀팁 3", True)]], "명령어 없이 평소처럼 말하면 돼요")

def s_review(fr, t):
    g = card_el(940, 300, outline=GREEN, width=4); gd = ImageDraw.Draw(g); gd.text((40, 34), "이런 분께 강추", font=F("Black", 52), fill=GREEN)
    for i, s in enumerate(["바이브코딩하다 코드가 자꾸 엉키는 분", "AI가 만든 코드를 믿기 어려운 분"]):
        check(gd, 46, 135 + i * 85, 40, GREEN, 8); gd.text((110, 127 + i * 85), s, font=F("Bold", 42), fill=WHITE)
    rise(fr, g, 70, 360, t, .3)
    r = card_el(940, 270, outline=ACC, width=4); rd = ImageDraw.Draw(r); rd.text((40, 34), "아쉬운 점", font=F("Black", 52), fill=ACC)
    rd.text((40, 125), "질문·설계 단계가 있어서", font=F("Bold", 42), fill=WHITE); rd.text((40, 185), "1줄짜리 빠른 수정엔 과할 수 있어요", font=F("Bold", 42), fill=WHITE)
    rise(fr, r, 70, 720, t, 2.0)
    head(fr, t, [[("솔직 평가", False)], [("강추", True), (" vs 아쉬운 점", False)]])

def s_outro(fr, t):
    c = cat(760); pop(fr, c, W - c.width + 70, SPLIT - c.height + 40, t, 0, .9)
    pop(fr, bubble(["저장 안 하면", "까먹는다냥"], 58), 50, 380, t, .5)
    n = card_el(470, 250, outline=BLUE, width=4); d = ImageDraw.Draw(n)
    d.text((36, 28), "NEXT EP.02", font=F("Black", 38), fill=BLUE); d.text((36, 82), "caveman", font=F("Black", 66), fill=WHITE)
    d.text((36, 172), "원시인 말투 스킬?", font=F("SemiBold", 36), fill=GREY)
    pop(fr, n.rotate(-3, expand=True, resample=Image.BICUBIC), 40, 760, t, 1.1)
    head(fr, t, [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 편: caveman · 원시인 말투로 토큰 절약?")

SCENES = [(s_hook, 4.5), (s_intro, 5.5), (s_problem, 5.5), (s_solution, 5.0), (s_flow, 11.0), (s_demo, 8.5), (s_install, 6.5), (s_tips, 9.0), (s_review, 6.0), (s_outro, 5.0)]
TOTAL = sum(d for _, d in SCENES)
proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                         "-c:a", "aac", "-b:a", "128k", "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", f"{OUT}/EP01_superpowers.mp4"], stdin=subprocess.PIPE)
start = 0.0; si = 0
for i in range(int(TOTAL * FPS)):
    gt = i / FPS
    while gt >= start + SCENES[si][1]: start += SCENES[si][1]; si += 1
    fn, dur = SCENES[si]; lt = gt - start
    lay = layer(W, H); fn(lay, lt)
    fr = BASE.copy(); paste(fr, lay, 0, 0, clamp((dur - lt) / .25))  # 장면 끝에서 내용만 페이드아웃, 틀은 유지
    ImageDraw.Draw(fr).rectangle((0, 0, int(W * gt / TOTAL), 8), fill=ACC)
    if abs(lt - (dur - 0.6)) < 0.5 / FPS: fr.convert("RGB").resize((360, 640)).save(f"{S}/build/v2_{si:02}.png")
    proc.stdin.write(fr.tobytes())
proc.stdin.close(); proc.wait()
print("done", TOTAL)
