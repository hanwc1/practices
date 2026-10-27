# EP.08 garrytan/gstack (⭐ 137.9k, MIT · 2026-10-27 저장소 페이지 기준)
import sys
from episode import *
import card_style; card_style.COSTUME = "ceo"

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #8"; FOOT = "EP.08 · garrytan/gstack"
HOOK_HEAD = [[("YC 대표의 개발 세팅,", False)], [("그대로", True), (" 가져오기", False)]]

TEAM = tiles([("CEO", "제품 방향 다시 잡기", ACC), ("EM", "설계·엣지 케이스 확정", BLUE), ("디자인", "디자인 시스템 만들기", PURPLE),
              ("리뷰", "CI 통과해도 터질 버그", YEL), ("QA", "진짜 브라우저로 테스트", GREEN), ("보안", "OWASP·STRIDE 점검", RED)], top=330, th=220, gap=36)

SCENES = [
    hook(["YC 대표가", "쓰는 거냥?"], 137900, HOOK_HEAD, "GitHub 별 13.8만 개 · gstack"),
    intro("garrytan", "gstack", "Claude Code를 가상 개발팀으로 만드는 도구 23개",
          [("라이선스", "MIT · 무료"), ("만든 사람", "Y Combinator 대표 Garry Tan")],
          [[("오늘의 스킬은", False)], [("gstack", True)]], "본인이 매일 쓰는 세팅을 공개", ["사장님 스킬", "이다냥"]),
    custom(stamp_card("혼자 개발할 때 체크리스트", ["☐ 기획이 맞는지 검토", "☐ 설계 리뷰", "☐ 코드 리뷰", "☐ 브라우저로 QA", "☐ 보안 점검"], "다 챙길 수 있을까…"),
           [[("혼자 개발하면", False)], [("다 빼먹죠?", True)]], "만들기 바빠서 리뷰·QA·보안은 뒷전", 6.0),
    custom(TEAM, [[("AI 팀원이", False)], [("역할별로", True), (" 있어요", False)]], "생각 → 계획 → 구현 → 리뷰 → 테스트 → 배포", 7.5),
    rows([("1", "/office-hours", "여기서 시작: 아이디어 점검 + 설계 문서", BLUE), ("2", "/review", "배포 전에 터질 버그 찾기", YEL),
          ("3", "/qa", "진짜 브라우저로 버그 재현·수정", GREEN), ("4", "/ship", "테스트·리뷰 후 PR 만들기", ACC)],
         [[("꼭 알아야 할", False)], [("명령어 4개", True)]], "전체 도구는 23개", 9.0, top=340, row_h=170, gap=26, step=1.8),
    install(["$ git clone --single-branch \\", "  --depth 1 https://github.com/", "  garrytan/gstack.git \\", "  ~/.claude/skills/gstack", "$ cd ~/.claude/skills/gstack", "$ ./setup"],
            [[("설치는", False)], [("터미널에서", True)]], "Git과 Bun(1.4.2 이상 권장)이 필요해요", ["팀장님 출근", "했다냥"], title="terminal", dur=7.0),
    tips([("처음엔 /office-hours부터", "만들 것을 설명하면 설계 문서가 나와요"), ("한 번에: /autoplan → /ship", "CEO·디자인·개발 리뷰를 한 명령으로"),
          ("안전장치 /careful", "위험한 명령 전에 경고해줘요")],
         [[("사용법", False)], [("꿀팁 3", True)]], "모두 저장소 README에 나온 방법이에요"),
    review(["혼자서 팀처럼 일하고 싶은 창업자", "리뷰·QA를 자주 빼먹는 분"],
           ["명령어가 23개라 처음엔 많아요", "Bun 설치 등 준비가 조금 필요해요"]),
    outro(["다음 편도", "저장하라냥"], "NEXT EP.09", "marketingskills", "마케팅 스킬 52개",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 편: 마케터 없이 마케팅하기"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP08_gstack.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["YC 대표가", "쓰는 거냥?"], "137,900", HOOK_HEAD, FOOT)
