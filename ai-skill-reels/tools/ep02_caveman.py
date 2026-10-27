# EP.02 JuliusBrussee/caveman (⭐ 115.3k, Apache-2.0 · 2026-10-27 저장소 페이지 기준)
import sys
from episode import *
import card_style; card_style.COSTUME = "caveman"

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #2"; FOOT = "EP.02 · JuliusBrussee/caveman"

def problem(fr, t):
    u = chat(["useEffect가 왜 계속 다시 실행돼?"], True); rise(fr, u, W - 70 - u.width, 340, t, .3)
    if t > 1.0:
        p = clamp((t - 1.0) / 1.8); box = card_el(900, 560, fill=(36, 42, 52), outline=(70, 78, 88), r=34); bd = ImageDraw.Draw(box)
        for i in range(min(9, int(9 * p) + 1)):
            bd.rounded_rectangle((40, 44 + i * 56, 40 + [780, 740, 800, 690, 770, 720, 800, 650, 420][i], 68 + i * 56), 12, fill=(70, 78, 88))
        paste(fr, box, 90, 500, fade(t, 1.0, .3))
    if t > 3.0:
        st = card_el(560, 140, fill=(40, 12, 12, 240), outline=RED, r=20, width=10); sd = ImageDraw.Draw(st)
        s = "그래서 결론이 뭔데…"; sd.text(((560 - tw(s, F("Black", 60))) / 2, 30), s, font=F("Black", 60), fill=RED)
        pop(fr, st.rotate(-5, expand=True, resample=Image.BICUBIC), 250, 760, t, 3.0, 1.5)

NORMAL_W = [800, 760, 820, 700, 790, 740, 600]
def compare(fr, t):
    a = card_el(940, 430, outline=LINE, width=3); ad = ImageDraw.Draw(a)
    ad.text((40, 30), "일반 답변", font=F("Black", 48), fill=GREY); ad.text((700, 36), "63 토큰", font=F("ExtraBold", 42), fill=GREY)
    for i, w in enumerate(NORMAL_W): ad.rounded_rectangle((40, 120 + i * 42, 40 + w * .95, 140 + i * 42), 10, fill=(60, 68, 78))
    rise(fr, a, 70, 330, t, .3)
    b = card_el(940, 300, fill=(45, 30, 18), outline=ACC, width=5); bd = ImageDraw.Draw(b)
    bd.text((40, 30), "caveman", font=F("Black", 48), fill=ACC); bd.text((700, 36), "20 토큰", font=F("ExtraBold", 42), fill=YEL)
    bd.text((40, 115), "New object ref each render,", font=MONO34, fill=WHITE)
    bd.text((40, 165), "so React re-renders.", font=MONO34, fill=WHITE)
    bd.text((40, 215), "Wrap the prop in useMemo.", font=MONO34, fill=GREEN)
    rise(fr, b, 70, 800, t, 2.2)

SCENES = [
    hook(["토큰 아끼려고", "원시인 된다냥?"], 115300, [[("원시인처럼 말하면", False)], [("AI 비용", True), ("이 준다?", False)]], "GitHub 별 11.5만 개 스킬"),
    intro("JuliusBrussee", "caveman", "AI 답변을 원시인 말투로 확 줄이는 스킬",
          [("라이선스", "Apache-2.0 · 무료"), ("지원", "Claude Code · Codex · Gemini CLI 등")],
          [[("오늘의 스킬은", False)], [("caveman", True)]], "\"적은 말로 되면 왜 많이 말함\"", ["우가우가", "알아듣겠냥?"]),
    custom(problem, [[("AI 답변,", False)], [("너무 길죠?", True)]], "한 줄이면 될 걸 한 페이지로…", 6.0),
    custom(compare, [[("같은 답인데", False)], [("토큰은 1/3", True)]], "저장소 예시 · React 리렌더 질문", 10.0),
    rows([("1", "/caveman", "기본 원시인 · 20토큰", BLUE), ("2", "/ultracave", "더 짧게, 끙 · 14토큰", YEL), ("3", "/megacave", "한문 모드 · 13토큰", PURPLE)],
         [[("말투 강도는", False)], [("3단계", True)]], "끌 때는 /caveman off", 7.5, top=360, row_h=200, gap=40, step=1.6),
    install(["> /plugin marketplace add", "  JuliusBrussee/caveman", "> /plugin install", "  caveman@caveman"],
            [[("설치는", False)], [("명령어 두 줄", True)]], "Claude Code 기준 · 다른 도구는 README 참고", ["두 줄이면", "원시인이다냥"]),
    tips([("/caveman-commit", "커밋 메시지도 짧고 굵게"), ("/caveman-stats", "얼마나 아꼈는지 숫자로 확인"), ("caveman telemetry off", "CLI는 기본으로 사용 통계 전송")],
         [[("같이 쓰면 좋은", False)], [("꿀팁 3", True)]], "3번은 CLI로 설치했을 때만 해당"),
    review(["긴 AI 답변 읽기 귀찮은 분", "API 토큰 비용 아끼고 싶은 분"],
           ["규칙 때문에 입력 토큰이 약 1,160개 늘어요", "요청 단위 과금(Copilot 등)은 절약 효과 없음"]),
    outro(["다음 편도", "저장하라냥"], "NEXT EP.03", "UI UX Pro Max", "AI 디자인 퀄리티 올리기",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 편: AI 디자인이 촌스러울 때"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP02_caveman.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["토큰 아끼려고", "원시인 된다냥?"], "115,300",
               [[("원시인처럼 말하면", False)], [("AI 비용", True), ("이 준다?", False)]], FOOT)
