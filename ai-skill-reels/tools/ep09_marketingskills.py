# EP.09 coreyhaines31/marketingskills (⭐ 56.9k, MIT · 2026-10-27 저장소 페이지 기준)
import sys
from episode import *
import card_style; card_style.COSTUME = "marketer"

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #9"; FOOT = "EP.09 · marketingskills"
HOOK_HEAD = [[("마케팅 스킬", False)], [("52개", True), ("를 한 번에", False)]]

FIELDS = tiles([("전환", "페이지·가입 전환율", BLUE), ("카피", "카피·이메일·SNS", ACC), ("SEO", "검색·AI 검색 노출", GREEN),
                ("광고", "광고·측정·A/B 테스트", YEL), ("성장", "추천·이탈 방지", PURPLE), ("전략", "가격·출시·플랜", RED)], top=330, th=220, gap=36)

SCENES = [
    hook(["마케터 없이", "마케팅한다냥?"], 56900, HOOK_HEAD, "GitHub 별 5.7만 개 · marketingskills"),
    intro("coreyhaines31", "marketingskills", "카피·SEO·광고·분석까지 마케팅 스킬 모음",
          [("라이선스", "MIT · 무료"), ("만든 사람", "마케팅 에이전시 대표 Corey Haines")],
          [[("오늘의 스킬은", False)], [("marketingskills", True)]], "개발자가 아니어도 쓰기 좋은 스킬", ["홍보는", "내가 한다냥"]),
    custom(stamp_card("서비스 오픈 체크리스트", ["✔ 기능 개발 완료", "✔ 디자인 완료", "☐ 랜딩 페이지 문구", "☐ 검색 노출(SEO)", "☐ 홍보·광고"], "홍보는 어떻게 하지…"),
           [[("만들기만 하고", False)], [("홍보는 막막?", True)]], "개발자에게 제일 어려운 마케팅", 6.0),
    custom(FIELDS, [[("분야별로", False)], [("다 들어 있어요", True)]], "52개 스킬을 분야별로 묶어 보면", 8.5),
    chat_demo([(["이 랜딩 페이지 전환율 좀 올려줘"], True, .3), (["cro 스킬로 페이지를 점검할게요."], False, 1.6),
               (["환영 이메일 5개 시퀀스 만들어줘"], True, 3.2), (["emails 스킬로 작성할게요."], False, 4.5)],
              [[("그냥 말하면", False)], [("알아서 골라 써요", True)]], "직접 부르기: /cro, /emails, /seo-audit", 8.5),
    install(["> /plugin marketplace add", "  coreyhaines31/marketingskills", "> /plugin install", "  marketing-skills"],
            [[("설치는", False)], [("명령어 두 줄", True)]], "Claude Code 기준 · 다른 도구는 npx skills add", ["두 줄이면", "마케터다냥"]),
    tips([("필요한 것만 골라 설치", "npx skills add … --skill cro copywriting"), ("product-marketing 먼저", "다른 스킬이 먼저 읽는 제품 정보"),
          ("/marketing-council", "여러 전문가 관점으로 의견 받기")],
         [[("사용법", False)], [("꿀팁 3", True)]], "모두 저장소 README에 나온 방법이에요"),
    review(["1인 창업자·사이드 프로젝트 운영자", "마케팅 기초를 배우고 싶은 분"],
           ["SaaS·영어권 마케팅 기준이에요", "스킬이 52개라 고르는 데 시간이 걸려요"]),
    outro(["다음 편도", "저장하라냥"], "NEXT EP.10", "claude-mem", "AI가 어제 일을 기억한다?",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 편: 시즌 2 마지막 편"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP09_marketingskills.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["마케터 없이", "마케팅한다냥?"], "56,900", HOOK_HEAD, FOOT)
