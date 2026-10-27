# EP.04 mattpocock/skills (⭐ 304.1k, MIT · 2026-10-27 저장소 페이지 기준)
import sys
from episode import *

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #4"; FOOT = "EP.04 · mattpocock/skills"
HOOK_HEAD = [[("코딩 전에", False)], [("AI가 나를 ", False), ("심문", True), ("한다?", False)]]

COMBO = [("/to-spec", "지금 대화를 스펙 문서로"), ("/to-tickets", "작은 작업 티켓으로 쪼개기"), ("/implement", "테스트 먼저 → 코드 리뷰까지")]
def combo(fr, t):
    for i, (cmd, desc) in enumerate(COMBO):
        at = .4 + i * 1.3; p = fade(t, at)
        if p <= 0: continue
        c = card_el(940, 190, fill=(45, 30, 18) if i == 2 else CARD, outline=ACC if i == 2 else LINE, width=4); d = ImageDraw.Draw(c)
        d.text((40, 36), cmd, font=MONO44, fill=YEL if i == 2 else WHITE); d.text((40, 110), desc, font=F("SemiBold", 40), fill=GREY)
        paste(fr, c, 70, 330 + i * 270 + 30 * (1 - p), p)
        if i < 2 and t > at + .5:
            dd = ImageDraw.Draw(fr); x = W / 2; y = 330 + i * 270 + 198
            dd.polygon([(x - 26, y + 14), (x + 26, y + 14), (x, y + 60)], fill=ACC)

SCENES = [
    hook(["별이 또", "30만 개냥?"], 304100, HOOK_HEAD, "GitHub 별 30만 개 · Matt Pocock의 스킬"),
    intro("mattpocock", "skills", "\"Skills for Real Engineers\"",
          [("라이선스", "MIT · 무료"), ("지원", "Claude Code · Codex · Copilot · Gemini CLI")],
          [[("오늘의 스킬은", False)], [("mattpocock/skills", True)]], "TypeScript 강사 Matt Pocock이 직접 쓰는 스킬", ["유명 강사의", "비밀 무기냥"]),
    chat_demo([(["/grill-me 사내 할 일 앱 만들 계획이야"], True, .3), (["로그인은 사내 계정으로 하나요,", "따로 만드나요?"], False, 1.4),
               (["사내 계정으로요"], True, 3.0), (["좋아요. 마감 알림도 필요한가요?"], False, 4.2)],
              [[("대표 스킬", False)], [("/grill-me", True)]], "계획의 모든 갈래가 정리될 때까지 질문", 8.0),
    rows([("1", "/tdd", "테스트 먼저 쓰고 구현", GREEN), ("2", "/diagnosing-bugs", "재현 → 최소화 → 회귀 테스트", RED),
          ("3", "/handoff", "대화를 문서로 정리해 넘기기", BLUE), ("4", "/teach", "개념을 여러 번에 나눠 가르쳐줌", YEL)],
         [[("같이 쓰면 좋은", False)], [("스킬 4개", True)]], "전체 스킬은 25개가 넘어요", 9.0, top=340, row_h=170, gap=26, step=1.8),
    custom(combo, [[("기획부터 구현까지", False)], [("3단 콤보", True)]], "순서대로 실행하면 끝", 6.5),
    install(["$ claude plugin install", "  mattpocock-skills", "  @claude-plugins-official", "> /setup-matt-pocock-skills"],
            [[("설치 한 줄 +", False)], [("처음 한 번 설정", True)]], "설정에선 이슈 트래커와 문서 위치를 물어봐요", ["셋업까지", "하라냥"], title="terminal", dur=7.0),
    tips([("저장소마다 한 번 셋업", "/setup-matt-pocock-skills"), ("코딩 전엔 /grill-me", "방향부터 맞추고 시작하기"), ("뭘 쓸지 모르면 /ask-matt", "상황에 맞는 스킬을 골라줘요")],
         [[("사용법", False)], [("꿀팁 3", True)]], "슬래시(/)로 직접 부르는 스킬이 많아요"),
    review(["계획 없이 코딩부터 하다 꼬이는 분", "팀에서 이슈·스펙을 관리하는 분"],
           ["스킬이 많아서 처음엔 헷갈려요", "이슈 트래커 연동 설정이 필요해요"]),
    outro(["다음 편도", "저장하라냥"], "NEXT EP.05", "agent-skills", "개발 전 과정을 명령어 6개로",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 편: addyosmani/agent-skills"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP04_mattpocock-skills.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["별이 또", "30만 개냥?"], "304,100", HOOK_HEAD, FOOT)
