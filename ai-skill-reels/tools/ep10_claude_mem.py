# EP.10 thedotmack/claude-mem (⭐ 103.7k, Apache-2.0 · 2026-10-27 저장소 페이지 기준)
import sys
from episode import *
import card_style; card_style.COSTUME = "memory"

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #10"; FOOT = "EP.10 · thedotmack/claude-mem"
HOOK_HEAD = [[("AI가 어제 한 일을", False)], [("기억", True), ("한다면?", False)]]

def problem(fr, t):
    u = chat(["어제 하던 거 이어서 해줘"], True); rise(fr, u, W - 70 - u.width, 360, t, .3)
    a = chat(["어떤 작업을 말씀하시는 건지", "알려주시겠어요?"], False); rise(fr, a, 70, 520, t, 1.3)
    if t > 2.8:
        st = card_el(560, 140, fill=(40, 12, 12, 240), outline=RED, r=20, width=10); sd = ImageDraw.Draw(st)
        s = "또 처음부터…"; sd.text(((560 - tw(s, F("Black", 64))) / 2, 28), s, font=F("Black", 64), fill=RED)
        pop(fr, st.rotate(-5, expand=True, resample=Image.BICUBIC), 260, 800, t, 2.8, 1.5)

SCENES = [
    hook(["어제 한 얘기", "또 하라냥?"], 103700, HOOK_HEAD, "GitHub 별 10만 개 · claude-mem"),
    intro("thedotmack", "claude-mem", "세션이 바뀌어도 맥락을 이어주는 메모리",
          [("라이선스", "Apache-2.0 · 무료"), ("지원", "Claude Code · Codex · Gemini 등")],
          [[("오늘의 스킬은", False)], [("claude-mem", True)]], "AI에게 일기장을 쥐여주는 플러그인", ["집사보다", "기억력 좋다냥"]),
    custom(problem, [[("새 세션마다", False)], [("처음부터 설명?", True)]], "대화를 새로 열면 AI는 전부 잊어버려요", 6.0),
    rows([("1", "작업 기록", "세션 중 한 일을 자동으로 수집", BLUE), ("2", "AI로 압축", "핵심만 요약해서", YEL),
          ("3", "내 컴퓨터에 저장", "SQLite + 벡터 검색 DB", GREEN), ("4", "다음 세션에 주입", "관련 있는 맥락만 골라서", ACC)],
         [[("이렇게", False)], [("기억해요", True)]], "검색 → 타임라인 → 상세 보기 3단계로 꺼내 써요", 10.0, top=340, row_h=170, gap=26, step=1.9),
    custom(info_card("내 기억은 어디에 저장될까?", [("기본 저장은 내 컴퓨터", "SQLite + Chroma 벡터 DB"), ("설정은 ~/.claude-mem/settings.json", None), ("클라우드 로그인·동기화는 선택", "설치 때 끌 수 있어요 (--provider 등)")], "DB"),
           [[("어디에", False)], [("저장될까?", True)]], "민감한 내용은 <private> 태그로 빼기", 7.0),
    install(["> /plugin marketplace add", "  thedotmack/claude-mem", "> /plugin install", "  claude-mem"],
            [[("설치는", False)], [("명령어 두 줄", True)]], "또는 터미널에서 npx claude-mem install", ["두 줄이면", "기억한다냥"]),
    tips([("설치 후 Claude Code 재시작", "그래야 지난 맥락이 보여요"), ("<private> 태그", "저장하면 안 될 내용은 감싸서 빼기"),
          ("문제 생기면 doctor", "npx claude-mem doctor")],
         [[("사용법", False)], [("꿀팁 3", True)]], "모두 저장소 README에 나온 방법이에요"),
    review(["긴 프로젝트를 여러 날 이어 하는 분", "매번 배경 설명하기 지친 분"],
           ["설치 때 클라우드 로그인 단계가 있어요 (끌 수 있음)", "클라우드 동기화는 문서 읽고 켜기"]),
    outro(["시즌 2 끝!", "추천은 댓글로냥"], "SEASON 3", "추천 받아요", "다음에 볼 스킬은?",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 시즌: 여러분이 댓글로 추천한 스킬"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP10_claude-mem.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["어제 한 얘기", "또 하라냥?"], "103,700", HOOK_HEAD, FOOT)
