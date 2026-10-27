# EP.01 obra/superpowers 소개 + 사용법 릴스 (내레이션 없이 화면 텍스트 중심)
import subprocess, sys
from common import *

OUT = sys.argv[1]
os.makedirs(f"{S}/build", exist_ok=True)
BG1 = make_bg("EP.01")
STARS = 306000  # 2026-10-26 GitHub 저장소 페이지 기준

def head(fr, t, parts, y=340, f=TITLE):
    el = rich_el(parts, f) if isinstance(parts, list) else text_el(parts, f)
    paste(fr, el, cx(el), y + 30 * (1 - fade(t, 0)), fade(t, 0))

def star(d, x, y, r, fill):
    pts = [(x + (r if i % 2 == 0 else r * .45) * math.cos(-math.pi / 2 + i * math.pi / 5), y + (r if i % 2 == 0 else r * .45) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
    d.polygon(pts, fill=fill)

def bubble(text_lines, me, w=760, f=None):
    f = f or F("SemiBold", 42); h = 50 + 62 * len(text_lines)
    c = card_el(w, h, fill=(31, 111, 235) if me else (36, 42, 52), outline=(31, 111, 235) if me else (70, 78, 88), r=34)
    d = ImageDraw.Draw(c)
    for i, s in enumerate(text_lines): d.text((36, 26 + i * 62), s, font=f, fill=WHITE)
    return c

def s_hook(fr, t, D):
    a = text_el("GitHub에서", F("ExtraBold", 70), GREY); paste(fr, a, cx(a), 380, fade(t, 0))
    d = ImageDraw.Draw(fr); n = int(STARS * ease(t / 2.2)); s = f"{n:,}"; fb = F("Black", 150)
    star(d, W / 2 - tw(s, fb) / 2 - 20, 600, 70, YEL); d.text((W / 2 - tw(s, fb) / 2 + 70, 515), s, font=fb, fill=WHITE)
    b = rich_el([("별 30만 개", ACC), (" 받은 AI 스킬", WHITE)], TITLE); paste(fr, b, cx(b), 740 + 30 * (1 - fade(t, .6)), fade(t, .6))
    c = text_el("개발자들이 열광하는 이유", F("ExtraBold", 64), YEL); paste(fr, c, cx(c), 1000, fade(t, 2.3))

def s_intro(fr, t, D):
    head(fr, t, "오늘의 스킬")
    c = card_el(940, 560, outline=(70, 78, 88)); cd = ImageDraw.Draw(c)
    cd.text((50, 50), "obra /", font=F("SemiBold", 50), fill=BLUE); cd.text((50, 115), "superpowers", font=F("Black", 100), fill=BLUE)
    cd.text((50, 265), "AI 코딩 에이전트용 스킬 + 개발 방법론", font=F("Bold", 42), fill=WHITE)
    for i, (k, v) in enumerate([("만든 사람", "obra (커뮤니티 개발자)"), ("라이선스", "MIT · 무료"), ("지원", "Claude Code · Codex · Cursor 등")]):
        cd.text((50, 350 + i * 62), k, font=F("Bold", 36), fill=GREY); cd.text((250, 350 + i * 62), v, font=F("SemiBold", 36), fill=WHITE)
    p = fade(t, .3); sc = .88 + .12 * p; im = c.resize((int(940 * sc), int(560 * sc)))
    paste(fr, im, (W - im.width) / 2, 520 + (560 - im.height) / 2, p)

def s_problem(fr, t, D):
    head(fr, t, [("AI 코딩, ", WHITE), ("이런 적 있죠?", ACC)])
    u = bubble(["할 일 관리 앱 만들어줘"], True, 620); paste(fr, u, W - 70 - u.width, 520, fade(t, .4))
    if t > 1.1:  # 묻지도 않고 코드부터 쏟아내는 AI
        p = clamp((t - 1.1) / 2.0); box = card_el(900, 560, fill=(10, 12, 16), outline=(70, 78, 88), r=28); bd = ImageDraw.Draw(box)
        cols = [BLUE, WHITE, GREEN, GREY, YEL, WHITE, BLUE, GREY, GREEN, WHITE]
        for i in range(int(10 * p) + 1):
            if i >= 10: break
            ind = [0, 1, 2, 2, 1, 2, 3, 3, 2, 0][i] * 40; bd.rounded_rectangle((40 + ind, 40 + i * 50, 40 + ind + [520, 420, 600, 380, 500, 640, 300, 450, 560, 200][i], 62 + i * 50), 11, fill=cols[i])
        paste(fr, box, 70, 680, ease((t - 1.1) / .3))
        lbl = text_el("묻지도 않고 코드 300줄", F("ExtraBold", 50), RED); paste(fr, lbl, cx(lbl), 1270, fade(t, 2.0))
    if t > 3.2:
        st = card_el(640, 140, fill=(40, 12, 12, 240), outline=RED, r=20, width=10); sd = ImageDraw.Draw(st)
        s = "내가 원한 거 아닌데…"; sd.text(((640 - tw(s, F("Black", 64))) / 2, 28), s, font=F("Black", 64), fill=RED)
        st = st.rotate(-6, expand=True, resample=Image.BICUBIC); p = ease((t - 3.2) / .25); sc = 1.5 - .5 * p
        im = st.resize((int(st.width * sc), int(st.height * sc))); paste(fr, im, (W - im.width) / 2, 860 - (im.height - st.height) / 2, p)

def s_solution(fr, t, D):
    a = text_el("superpowers를 깔면", F("ExtraBold", 70), GREY); paste(fr, a, cx(a), 560, fade(t, 0))
    b = rich_el([("AI가 ", WHITE), ("일하는 순서", ACC), ("가", WHITE)], BIG); paste(fr, b, cx(b), 690, fade(t, .3))
    c = text_el("바뀌어요", BIG); paste(fr, c, cx(c), 830, fade(t, .5))
    e = text_el("묻고 → 설계하고 → 테스트하고 → 만든다", F("Bold", 46), YEL); paste(fr, e, cx(e), 1060, fade(t, 1.2))

FLOW = [("브레인스토밍", "질문부터. 한 번에 하나씩", BLUE), ("설계 문서", "승인 전엔 코드 0줄", (210, 120, 255)),
        ("작업 계획", "작은 단위로 쪼개기", YEL), ("테스트 먼저 (TDD)", "실패하는 테스트 → 코드", GREEN), ("코드 리뷰", "계획대로 됐는지 검사", ACC)]
def s_flow(fr, t, D):
    head(fr, t, [("자동으로 돌아가는 ", WHITE), ("5단계", ACC)])
    d = ImageDraw.Draw(fr)
    for i, (h, sub, col) in enumerate(FLOW):
        at = .6 + i * 1.9; p = fade(t, at, .45)
        if p <= 0: continue
        y = 500 + i * 190
        if i: d.line([(140, y - 100), (140, y - 10)], fill=LINE, width=6)
        c = card_el(860, 160, outline=col if t < at + 1.9 or i == 4 else LINE, width=4); cdd = ImageDraw.Draw(c)
        cdd.ellipse((30, 35, 120, 125), fill=col); n = str(i + 1); cdd.text((75 - tw(n, F("Black", 54)) / 2, 40), n, font=F("Black", 54), fill=(20, 20, 20))
        cdd.text((150, 28), h, font=F("ExtraBold", 52), fill=WHITE); cdd.text((150, 96), sub, font=F("SemiBold", 38), fill=GREY)
        paste(fr, c, 110 - 100 * (1 - p), y, p)

def s_demo(fr, t, D):
    head(fr, t, [("깔고 나면 ", WHITE), ("이렇게 달라져요", ACC)])
    tag = text_el("예시 화면", F("Bold", 32), GREY); paste(fr, tag, cx(tag), 455, fade(t, 0))
    u = bubble(["할 일 관리 앱 만들어줘"], True, 620); paste(fr, u, W - 70 - u.width, 530, fade(t, .4))
    a = bubble(["만들기 전에 하나만 여쭤볼게요.", "혼자 쓰시나요, 팀이 같이 쓰나요?"], False, 880); paste(fr, a, 70, 690, fade(t, 1.5))
    u2 = bubble(["팀 3명이 같이 써요"], True, 560); paste(fr, u2, W - 70 - u2.width, 930, fade(t, 3.4))
    if t > 4.8:
        ch = card_el(880, 200, fill=(18, 40, 28), outline=GREEN, r=30, width=4); cd = ImageDraw.Draw(ch)
        cd.text((40, 30), "설계 문서 작성 완료", font=F("ExtraBold", 48), fill=WHITE)
        cd.text((40, 100), "docs/superpowers/specs/…-design.md", font=ImageFont.truetype(MONO_PATH, 30), fill=GREEN)
        cd.text((40, 145), "승인하시면 계획 → 테스트 → 구현 시작", font=F("SemiBold", 34), fill=GREY)
        paste(fr, ch, 70, 1100 + 30 * (1 - fade(t, 4.8)), fade(t, 4.8))

def s_install(fr, t, D):
    head(fr, t, [("설치는 ", WHITE), ("딱 한 줄", ACC)])
    s = text_el("Claude Code 공식 플러그인 마켓에서", F("Bold", 44), GREY); paste(fr, s, cx(s), 455, fade(t, .2))
    term = card_el(960, 460, fill=(10, 12, 16), outline=(70, 78, 88)); td = ImageDraw.Draw(term)
    td.rectangle((3, 3, 956, 70), fill=(30, 36, 44)); [td.ellipse((28 + i * 40, 24, 50 + i * 40, 46), fill=c) for i, c in enumerate([RED, YEL, GREEN])]
    td.text((170, 18), "claude", font=MONO, fill=GREY)
    paste(fr, term, 60, 580, fade(t, .3))
    if t > .7:
        d = ImageDraw.Draw(fr); lines = ["> /plugin install", "  superpowers", "  @claude-plugins-official"]
        k = int(sum(map(len, lines)) * clamp((t - .9) / 2.6)); y = 700; f = ImageFont.truetype(MONO_PATH, 44)
        for ln in lines:
            part = ln[:max(0, k)]; k -= len(ln); d.text((110, y), part, font=f, fill=GREEN if ln.startswith(">") else WHITE); y += 66
        if t > 3.7: d.text((110, y + 10), "✓ installed", font=f, fill=GREEN)
    n = text_el("Codex · Cursor 등은 저장소 README 참고", F("SemiBold", 36), GREY); paste(fr, n, cx(n), 1100, fade(t, 4.2))

TIPS = [("명령어 필요 없음", "평소처럼 \"~ 만들자\"라고 말하면 자동 작동"), ("질문엔 꼼꼼히 답하기", "답이 구체적일수록 결과가 좋아져요"),
        ("설계 문서는 꼭 읽고 승인", "여기서 방향을 잡아야 나중에 안 꼬여요")]
def s_tips(fr, t, D):
    head(fr, t, [("사용법 ", WHITE), ("꿀팁 3", ACC)])
    for i, (h, ex) in enumerate(TIPS):
        at = .7 + i * 2.6; p = fade(t, at, .45)
        if p <= 0: continue
        c = card_el(940, 250, outline=ACC if t < at + 2.6 or i == 2 else LINE, width=4); cd = ImageDraw.Draw(c)
        n = str(i + 1); cd.ellipse((40, 44, 130, 134), fill=ACC); cd.text((85 - tw(n, F("Black", 56)) / 2, 50), n, font=F("Black", 56), fill=(20, 20, 20))
        cd.text((160, 48), h, font=F("ExtraBold", 54), fill=WHITE); cd.text((160, 148), ex, font=F("SemiBold", 38), fill=YEL)
        paste(fr, c, 70 - 120 * (1 - p), 500 + i * 290, p)

def s_review(fr, t, D):
    head(fr, t, "솔직 평가")
    g = card_el(940, 330, outline=GREEN, width=4); gd = ImageDraw.Draw(g); gd.text((40, 34), "이런 분께 강추", font=F("Black", 52), fill=GREEN)
    for i, s in enumerate(["바이브코딩하다 코드가 자꾸 엉키는 분", "AI가 만든 코드를 믿기 어려운 분"]):
        check(gd, 46, 140 + i * 90, 40, GREEN, 8); gd.text((110, 132 + i * 90), s, font=F("Bold", 44), fill=WHITE)
    paste(fr, g, 70, 500 + 30 * (1 - fade(t, .4)), fade(t, .4))
    r = card_el(940, 300, outline=ACC, width=4); rd = ImageDraw.Draw(r); rd.text((40, 34), "아쉬운 점", font=F("Black", 52), fill=ACC)
    rd.text((40, 132), "질문·설계 단계가 있어서", font=F("Bold", 44), fill=WHITE); rd.text((40, 200), "1줄짜리 빠른 수정엔 과할 수 있어요", font=F("Bold", 44), fill=WHITE)
    paste(fr, r, 70, 880 + 30 * (1 - fade(t, 2.2)), fade(t, 2.2))

def s_outro(fr, t, D):
    a = text_el("저장해두고 써보세요", F("Black", 84)); paste(fr, a, cx(a), 380 + 30 * (1 - fade(t, 0)), fade(t, 0))
    c = card_el(940, 320, outline=BLUE, width=4); cd = ImageDraw.Draw(c)
    cd.text((50, 40), "NEXT  EP.02", font=F("Black", 44), fill=BLUE); cd.text((50, 110), "caveman", font=F("Black", 80), fill=WHITE)
    cd.text((50, 225), "원시인 말투로 토큰을 줄인다고?", font=F("SemiBold", 44), fill=GREY)
    paste(fr, c, 70, 600 + 40 * (1 - fade(t, .5)), fade(t, .5))
    for i, (s, col) in enumerate([("저장", BLUE), ("팔로우", ACC)]):
        p = fade(t, 1.2 + i * .25); bt = card_el(430, 130, fill=col, outline=col, r=65); bd = ImageDraw.Draw(bt)
        bd.text(((430 - tw(s, F("Black", 60))) / 2, 26), s, font=F("Black", 60), fill=WHITE); paste(fr, bt, 70 + i * 510, 1020 + 30 * (1 - p), p)

SCENES = [(s_hook, 4.5), (s_intro, 5.5), (s_problem, 5.5), (s_solution, 4.5), (s_flow, 11.0), (s_demo, 8.5), (s_install, 6.5), (s_tips, 9.0), (s_review, 6.0), (s_outro, 5.0)]
TOTAL = sum(d for _, d in SCENES)
proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                         "-c:a", "aac", "-b:a", "128k", "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", f"{OUT}/EP01_superpowers.mp4"], stdin=subprocess.PIPE)
start = 0.0; si = 0
for i in range(int(TOTAL * FPS)):
    gt = i / FPS
    while gt >= start + SCENES[si][1]: start += SCENES[si][1]; si += 1
    fn, dur = SCENES[si]; lt = gt - start; fr = BG1.copy(); fn(fr, lt, dur)
    if lt > dur - 0.2:
        o = layer(W, H); o.paste((13, 17, 23, int(255 * (lt - (dur - .2)) / .2)), (0, 0, W, H)); fr.alpha_composite(o)
    ImageDraw.Draw(fr).rectangle((0, 0, int(W * gt / TOTAL), 8), fill=ACC)
    if abs(lt - (dur - 0.6)) < 0.5 / FPS: fr.convert("RGB").resize((360, 640)).save(f"{S}/build/c_{si:02}.png")
    proc.stdin.write(fr.tobytes())
proc.stdin.close(); proc.wait()

cv = BG1.copy(); d = ImageDraw.Draw(cv)
s = f"{STARS:,}"; fb = F("Black", 130); star(d, W / 2 - tw(s, fb) / 2 - 10, 560, 62, YEL); d.text((W / 2 - tw(s, fb) / 2 + 70, 480), s, font=fb, fill=WHITE)
for i, (s, c) in enumerate([("개발자들이", WHITE), ("열광한 스킬", ACC)]):
    d.text(((W - tw(s, F("Black", 160))) / 2, 720 + i * 190), s, font=F("Black", 160), fill=c)
s = "superpowers 사용법"; d.text(((W - tw(s, F("ExtraBold", 72))) / 2, 1160), s, font=F("ExtraBold", 72), fill=YEL)
cv.convert("RGB").save(f"{OUT}/cover.png")
print("done", TOTAL)
