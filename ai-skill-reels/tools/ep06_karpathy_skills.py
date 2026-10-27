# EP.06 forrestchang/andrej-karpathy-skills (⭐ 225.4k, MIT · 2026-10-27 저장소 페이지 기준, 현재 multica-ai 이름으로 표시)
import sys
from episode import *
import card_style; card_style.COSTUME = "professor"

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #6"; FOOT = "EP.06 · andrej-karpathy-skills"
HOOK_HEAD = [[("파일 하나로", False)], [("AI 코딩 실수", True), (" 줄이기", False)]]

FILES = ["src/Button.tsx", "src/theme.ts", "src/App.tsx", "src/utils/color.ts", "package.json", "... +7 files"]
def problem(fr, t):
    u = chat(["버튼 색만 파란색으로 바꿔줘"], True); rise(fr, u, W - 70 - u.width, 340, t, .3)
    if t > 1.1:
        c = card_el(900, 560, fill=(10, 12, 16), outline=(70, 78, 88), r=28); d = ImageDraw.Draw(c)
        d.text((40, 30), "12 files changed", font=MONO44, fill=WHITE)
        d.text((520, 34), "+348", font=MONO44, fill=GREEN); d.text((690, 34), "−120", font=MONO44, fill=RED)
        for i, f in enumerate(FILES[:int(clamp((t - 1.3) / 1.4) * 6) + 1]): d.text((40, 120 + i * 68), f, font=MONO34, fill=GREY if i == 5 else YEL)
        paste(fr, c, 90, 520, fade(t, 1.1, .3))
    if t > 3.4:
        st = card_el(660, 140, fill=(40, 12, 12, 240), outline=RED, r=20, width=10); sd = ImageDraw.Draw(st)
        s = "버튼 색만 바꾸랬는데…"; sd.text(((660 - tw(s, F("Black", 58))) / 2, 32), s, font=F("Black", 58), fill=RED)
        pop(fr, st.rotate(-5, expand=True, resample=Image.BICUBIC), 200, 760, t, 3.4, 1.5)

SCENES = [
    hook(["AI 코딩 실수,", "파일 하나로 끝냥?"], 225400, HOOK_HEAD, "GitHub 별 22만 개 · CLAUDE.md 한 장"),
    intro("forrestchang", "andrej-karpathy-skills", "카파시가 짚은 AI 코딩 실수를 규칙 4개로",
          [("라이선스", "MIT · 무료"), ("주의", "카파시 본인이 만든 저장소는 아니에요")],
          [[("오늘의 스킬은", False)], [("카파시 스킬", True)]], "Andrej Karpathy의 관찰을 정리한 커뮤니티 저장소", ["유명인 이름", "빌렸다냥"]),
    custom(problem, [[("AI 코딩,", False)], [("이런 적 있죠?", True)]], "시킨 것보다 훨씬 많이 고쳐버림", 6.5),
    rows([("1", "생각하고 코딩하기", "가정을 말하고, 모르면 물어보기", BLUE), ("2", "단순함이 먼저", "문제를 푸는 최소한의 코드만", GREEN),
          ("3", "수술하듯 고치기", "요청한 부분만 수정하기", YEL), ("4", "목표로 검증하기", "성공 기준을 정하고 통과할 때까지", PURPLE)],
         [[("규칙은", False)], [("딱 4개", True)]], "원문: Think Before Coding 외 3개", 10.0, top=340, row_h=170, gap=26, step=1.9),
    custom(info_card("CLAUDE.md 한 장이 전부", [("Claude Code가 작업 전에 읽는 규칙 파일", "프로젝트 폴더에 두면 매번 자동으로 적용"), ("규칙 4개가 파일 하나에", "길지 않아서 직접 읽어봐도 금방이에요"), ("플러그인으로도 설치 가능", "둘 중 편한 방법으로")], "MD"),
           [[("원리는", False)], [("규칙 파일 하나", True)]], "그래서 가볍고 빨라요", 6.5),
    install(["> /plugin marketplace add", "  forrestchang/", "  andrej-karpathy-skills", "> /plugin install", "  andrej-karpathy-skills", "  @karpathy-skills"],
            [[("설치는", False)], [("명령어 두 줄", True)]], "CLAUDE.md 파일만 받아서 써도 돼요", ["교수님 모셔", "왔다냥"], dur=7.0),
    tips([("플러그인 대신 파일만", "curl로 CLAUDE.md 받아 프로젝트에 두기"), ("기존 CLAUDE.md가 있으면", "덮어쓰지 말고 뒤에 이어 붙이기"),
          ("내 입맛대로 고쳐 쓰기", "그냥 텍스트 파일이라 수정해도 돼요")],
         [[("사용법", False)], [("꿀팁 3", True)]], "설치 방법은 모두 저장소 README 기준"),
    review(["AI가 자꾸 일을 크게 벌리는 분", "파일 하나로 가볍게 시작하고 싶은 분"],
           ["카파시 공식 저장소가 아니에요", "규칙 안내라서 단계별 절차는 없어요"]),
    outro(["다음 편도", "저장하라냥"], "NEXT EP.07", "humanizer", "AI 말투 지우기",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 편: AI가 쓴 티 나는 글 고치기"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP06_karpathy-skills.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["AI 코딩 실수,", "파일 하나로 끝냥?"], "225,400", HOOK_HEAD, FOOT)
