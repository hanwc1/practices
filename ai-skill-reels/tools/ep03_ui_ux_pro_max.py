# EP.03 nextlevelbuilder/ui-ux-pro-max-skill (⭐ 140.9k, MIT · 2026-10-27 저장소 페이지 기준)
import sys
from episode import *
import card_style; card_style.COSTUME = "artist"

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TAG = "GitHub 인기 스킬 #3"; FOOT = "EP.03 · ui-ux-pro-max-skill"
HOOK_HEAD = [[("AI가 만든 화면,", False)], [("왜 다 ", False), ("똑같을까?", True)]]

def generic_ui():  # 흔한 "AI 기본 디자인" 목업
    c = card_el(900, 640, fill=(245, 245, 250), outline=(70, 78, 88), r=28); d = ImageDraw.Draw(c)
    hero = Image.new("RGBA", (860, 300)); hd = ImageDraw.Draw(hero)
    for x in range(860): hd.line([(x, 0), (x, 300)], fill=(int(120 + 60 * x / 860), int(80 + 20 * x / 860), int(230 - 30 * x / 860), 255))
    m = Image.new("L", hero.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 859, 299), 20, fill=255); c.paste(hero, (20, 20), m)
    d.rounded_rectangle((230, 90, 670, 130), 12, fill=(255, 255, 255)); d.rounded_rectangle((300, 150, 600, 175), 10, fill=(230, 225, 255))
    d.rounded_rectangle((360, 210, 540, 260), 25, fill=(255, 255, 255))
    for i in range(3):
        x = 40 + i * 280; d.rounded_rectangle((x, 350, x + 260, 610), 18, fill=(255, 255, 255), outline=(225, 225, 235), width=2)
        d.ellipse((x + 100, 380, x + 160, 440), fill=(180, 150, 255)); d.rounded_rectangle((x + 40, 470, x + 220, 492), 8, fill=(200, 200, 215))
        d.rounded_rectangle((x + 60, 510, x + 200, 528), 8, fill=(225, 225, 235))
    return c

UI = generic_ui()
def problem(fr, t):
    rise(fr, UI, 90, 330, t, .3)
    lab = chip("AI 기본 디자인", GREY); rise(fr, lab, 90, 990, t, .8)
    if t > 2.4:
        st = card_el(660, 140, fill=(40, 12, 12, 240), outline=RED, r=20, width=10); sd = ImageDraw.Draw(st)
        s = "또 보라색 그라데이션…"; sd.text(((660 - tw(s, F("Black", 60))) / 2, 30), s, font=F("Black", 60), fill=RED)
        pop(fr, st.rotate(-5, expand=True, resample=Image.BICUBIC), 200, 560, t, 2.4, 1.5)

DB = tiles([("79", "UI 스타일", BLUE), ("192", "컬러 팔레트", ACC), ("74", "폰트 조합", YEL), ("119", "UX 가이드라인", GREEN), ("25", "차트 종류", PURPLE), ("22", "기술 스택", RED)],
           top=330, th=220, gap=36)

SCENES = [
    hook(["AI 디자인", "촌스럽다냥?"], 140900, HOOK_HEAD, "GitHub 별 14만 개 디자인 스킬"),
    intro("nextlevelbuilder", "ui-ux-pro-max", "AI에게 디자인 감각을 주는 스킬",
          [("라이선스", "MIT · 무료"), ("지원", "Claude Code · Cursor · Windsurf 등 20개+")],
          [[("오늘의 스킬은", False)], [("UI UX Pro Max", True)]], "디자이너 없이도 그럴듯한 화면", ["이름이", "프로맥스냥"]),
    custom(problem, [[("AI 디자인,", False)], [("어디서 본 듯한?", True)]], "가운데 정렬, 보라색, 똑같은 카드 3개", 6.0),
    custom(DB, [[("안에 든", False)], [("디자인 데이터베이스", True)]], "제품 종류에 맞춰 골라 써요", 8.0),
    rows([("1", "화면 요청", "\"랜딩 페이지 만들어줘\"", BLUE), ("2", "5가지 동시 검색", "제품·스타일·색·레이아웃·폰트", YEL),
          ("3", "디자인 시스템 생성", "색·폰트·효과·피해야 할 것까지", PURPLE), ("4", "구현 + 최종 점검", "출시 전 체크리스트로 확인", GREEN)],
         [[("이렇게", False)], [("작동해요", True)]], "검색은 인터넷 없이 내 컴퓨터에서", 9.0, top=340, row_h=170, gap=26, step=1.8),
    install(["> /plugin marketplace add", "  nextlevelbuilder/", "  ui-ux-pro-max-skill", "> /plugin install", "  ui-ux-pro-max@", "  ui-ux-pro-max-skill"],
            [[("설치는", False)], [("명령어 두 줄", True)]], "Claude Code 기준 · CLI 설치도 있어요", ["복붙하면", "끝이다냥"]),
    tips([("\"SaaS 랜딩 페이지 만들어줘\"", "Build a landing page for my SaaS product"), ("\"헬스케어 분석 대시보드\"", "Create a dashboard for healthcare analytics"),
          ("\"다크모드 포트폴리오 사이트\"", "Design a portfolio website with dark mode")],
         [[("이렇게", False)], [("말하면 돼요", True)]], "저장소 예시 프롬프트 · 한국어로 해도 OK"),
    review(["디자이너 없이 화면 만드는 1인 개발자", "랜딩·대시보드 자주 만드는 분"],
           ["웹·앱 화면(프론트엔드) 전용이에요", "결과물은 직접 보고 다듬어야 해요"]),
    outro(["다음 편도", "저장하라냥"], "NEXT EP.04", "mattpocock/skills", "AI가 나를 심문한다?",
          [[("저장하고", False)], [("팔로우", True), (" 해두라냥!", False)]], "다음 편: 별 30만 개, /grill-me의 정체"),
]

if __name__ == "__main__":
    snap = sys.argv[2] if len(sys.argv) > 2 else None
    print("video", render(SCENES, f"{OUT}/EP03_ui-ux-pro-max.mp4", TAG, FOOT, snap))
    thumbnails(OUT, TAG, ["AI 디자인", "촌스럽다냥?"], "140,900", HOOK_HEAD, FOOT)
