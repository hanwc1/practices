# EP.05 addyosmani/agent-skills (⭐ 110.8k, MIT · 2026-10-27 저장소 페이지 기준)
import sys
from episode import *

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #5"; FOOT = "EP.05 · addyosmani/agent-skills"
HOOK_HEAD = [[("시니어의 일하는 법,", False)], [("통째로", True), (" 설치하기", False)]]

LIFE = [("/spec", "무엇을 만들지 정의", BLUE), ("/plan", "작은 작업으로 쪼개기", YEL), ("/build", "한 조각씩 구현", GREEN),
        ("/test", "제대로 되는지 증명", PURPLE), ("/review", "머지 전 리뷰", ACC), ("/ship", "배포", RED)]

def auto(fr, t):
    c = card_el(940, 640, fill=(45, 30, 18), outline=ACC, width=5); d = ImageDraw.Draw(c)
    d.text((50, 50), "/build auto", font=ImageFont.truetype(MONO_PATH, 80), fill=YEL)
    d.text((50, 175), "계획을 한 번 승인하면 전부 구현", font=F("ExtraBold", 50), fill=WHITE)
    for i, s in enumerate(["작업마다 테스트 먼저 (TDD)", "작업마다 따로 커밋", "실패하거나 위험하면 멈춤"]):
        if t > 1.2 + i * .7:
            check(d, 56, 300 + i * 100, 46, GREEN, 9); d.text((130, 292 + i * 100), s, font=F("Bold", 46), fill=WHITE)
    pop(fr, c, 70, 360, t, .2)

CAT = tiles([("4", "정의", BLUE), ("1", "계획", YEL), ("7", "구현", GREEN), ("2", "검증", PURPLE), ("4", "리뷰", ACC), ("6", "출시", RED)],
            top=330, th=220, gap=36)

SCENES = [
    hook(["시니어 개발자", "복붙이냥?"], 110800, HOOK_HEAD, "GitHub 별 11만 개 · 스킬 25개"),
    intro("addyosmani", "agent-skills", "AI 코딩 에이전트용 실무 엔지니어링 스킬",
          [("라이선스", "MIT · 무료"), ("만든 사람", "웹 성능 분야로 유명한 Addy Osmani")],
          [[("오늘의 스킬은", False)], [("agent-skills", True)]], "시니어의 작업 습관을 스킬로 패키징", ["족보 같은", "스킬이냥"]),
    rows([(str(i + 1), c, s, col) for i, (c, s, col) in enumerate(LIFE)],
         [[("개발 전 과정이", False)], [("명령어 6개", True)]], "Claude Code 리뷰는 /agent-skills:review", 9.5, top=330, row_h=110, gap=20, step=1.3),
    custom(auto, [[("끝판왕 명령어", False)], [("/build auto", True)]], "그래도 결과는 꼭 직접 확인하기", 7.0),
    custom(CAT, [[("단계별 스킬", False)], [("총 25개", True)]], "+ 알맞은 스킬을 골라주는 메타 스킬 1개", 6.5),
    install(["> /plugin marketplace add", "  addyosmani/agent-skills", "> /plugin install", "  agent-skills@addy-agent-skills"],
            [[("설치는", False)], [("명령어 두 줄", True)]], "Claude Code 기준 · 다른 도구는 npx skills add", ["두 줄이면", "시니어다냥"]),
    tips([("리뷰는 /agent-skills:review", "기본 /review와 이름이 겹쳐서"), ("필요한 스킬만 골라 설치", "npx skills add … --skill 이름"),
          ("SSH 오류가 나면", "https:// 전체 주소로 marketplace add")],
         [[("사용법", False)], [("꿀팁 3", True)]], "모두 저장소 README에 나온 방법이에요"),
    review(["혼자 개발해도 팀처럼 체계적으로 하고 싶은 분", "보안·성능·배포까지 챙기고 싶은 분"],
           ["1화 superpowers와 겹치는 부분이 많아요", "둘 중 하나만 골라 쓰는 걸 추천해요"]),
    outro(["시즌 1 끝!", "추천은 댓글로냥"], "SEASON 2", "추천 받아요", "다음에 볼 스킬은?",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 시즌: 여러분이 댓글로 추천한 스킬"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP05_agent-skills.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["시니어 개발자", "복붙이냥?"], "110,800", HOOK_HEAD, FOOT)
