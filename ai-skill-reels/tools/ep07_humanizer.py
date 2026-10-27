# EP.07 blader/humanizer (⭐ 61.4k, MIT · 2026-10-27 저장소 페이지 기준)
import sys
from episode import *
import card_style; card_style.COSTUME = "writer"

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #7"; FOOT = "EP.07 · blader/humanizer"
HOOK_HEAD = [[("AI가 쓴 티 나는 글,", False)], [("사람 말투로", True), (" 바꾸기", False)]]

PATTERNS = tiles([("A", "연출된 문장", BLUE), ("B", "기계적인 리듬", YEL), ("C", "과장과 남의 권위", ACC),
                  ("D", "꾸밈용 서식", GREEN), ("E", "챗봇·초안 흔적", PURPLE), ("F", "엉뚱한 독자 설정", RED)], top=330, th=220, gap=36)

SCENES = [
    hook(["AI가 쓴 티", "팍팍 난다냥?"], 61400, HOOK_HEAD, "GitHub 별 6만 개 · humanizer"),
    intro("blader", "humanizer", "AI가 쓴 티를 글에서 지워주는 스킬",
          [("라이선스", "MIT · 무료"), ("근거", "위키백과 'AI 글쓰기 징후' 가이드")],
          [[("오늘의 스킬은", False)], [("humanizer", True)]], "뜻은 그대로, 말투만 사람처럼", ["글쓰기 과외", "선생님이냥"]),
    custom(stamp_card("AI가 쓴 글", ["이것은 단순한 도구가 아닙니다.", "하나의 혁신입니다.", "빠르고, 쉽고, 강력합니다.", "결론적으로, 미래는 지금입니다."], "AI 티 난다…", tag="예시 문장"),
           [[("AI가 쓴 글,", False)], [("어딘가 어색하죠?", True)]], "\"A가 아니라 B\", 세 개씩 나열, 과한 결론", 6.5),
    custom(PATTERNS, [[("찾아내는", False)], [("AI 패턴 26개", True)]], "6개 묶음 · \"A가 아니라 B\" 같은 말버릇까지", 7.5),
    rows([("1", "첫 번째 고쳐쓰기", "의미는 그대로 두고", BLUE), ("2", "스스로 비평하기", "아직 AI 같은 부분 찾기", YEL), ("3", "최종본", "한 번 더 다듬어서 완성", GREEN)],
         [[("이렇게", False)], [("고쳐줘요", True)]], "파일을 주면 글만 고치고 코드는 그대로", 8.5, top=360, row_h=200, gap=40, step=1.8),
    install(["> /plugin marketplace add", "  blader/humanizer", "> /plugin install", "  humanizer@humanizer"],
            [[("설치는", False)], [("명령어 두 줄", True)]], "Claude Code 2.1.142 이상 · Claude.ai는 ZIP 업로드", ["두 줄이면", "작가다냥"]),
    tips([("/humanizer + 글 붙여넣기", "가장 기본 사용법"), ("내 글 샘플을 같이 주기", "2~3문단 주면 내 말투에 맞춰요"),
          ("파일도 바로 고쳐요", "\"docs/launch-post.md 다듬어줘\"")],
         [[("사용법", False)], [("꿀팁 3", True)]], "AI 탐지기 피하기용은 아니에요", 9.5),
    review(["블로그·뉴스레터 초안을 AI로 쓰는 분", "AI 글이 딱딱하게 느껴지는 분"],
           ["영어 글 기준 가이드라 한국어는 직접 확인", "AI 탐지기는 여전히 잡아낼 수 있어요"]),
    outro(["다음 편도", "저장하라냥"], "NEXT EP.08", "gstack", "YC 대표의 개발 세팅",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 편: AI 가상 개발팀 만들기"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP07_humanizer.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["AI가 쓴 티", "팍팍 난다냥?"], "61,400", HOOK_HEAD, FOOT)
