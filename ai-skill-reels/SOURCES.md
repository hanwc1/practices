# 에피소드별 확인 근거 (각 GitHub 저장소 페이지, 2026-10-26~27 확인)

| 편 | 저장소 | ⭐ / 포크 | 라이선스 | 설치 (Claude Code) |
|---|---|---|---|---|
| EP.01 | obra/superpowers | 305.6k / 27.2k | MIT | `/plugin install superpowers@claude-plugins-official` |
| EP.02 | JuliusBrussee/caveman | 115.3k / 6.7k | Apache-2.0 | `/plugin marketplace add JuliusBrussee/caveman` → `/plugin install caveman@caveman` |
| EP.03 | nextlevelbuilder/ui-ux-pro-max-skill | 140.9k / 14.9k | MIT | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` → `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill` |
| EP.04 | mattpocock/skills | 304.1k / 25.6k | MIT | `claude plugin install mattpocock-skills@claude-plugins-official` → `/setup-matt-pocock-skills` |
| EP.05 | addyosmani/agent-skills | 110.8k / 11.6k | MIT | `/plugin marketplace add addyosmani/agent-skills` → `/plugin install agent-skills@addy-agent-skills` |
| EP.06 | forrestchang/andrej-karpathy-skills (페이지에는 multica-ai로 표시) | 225.4k / 22.5k | MIT | `/plugin marketplace add forrestchang/andrej-karpathy-skills` → `/plugin install andrej-karpathy-skills@karpathy-skills` |
| EP.07 | blader/humanizer | 61.4k / 4.9k | MIT | `/plugin marketplace add blader/humanizer` → `/plugin install humanizer@humanizer` (Claude Code 2.1.142+) |
| EP.08 | garrytan/gstack | 137.9k / 20.5k | MIT | `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` |
| EP.09 | coreyhaines31/marketingskills | 56.9k / 8.4k | MIT | `/plugin marketplace add coreyhaines31/marketingskills` → `/plugin install marketing-skills` |
| EP.10 | thedotmack/claude-mem | 103.7k / 9.1k | Apache-2.0 | `/plugin marketplace add thedotmack/claude-mem` → `/plugin install claude-mem` (또는 `npx claude-mem install`) |

## 영상 속 숫자와 주장
- EP.02: 63 → 20토큰은 README의 React 리렌더 예시 (tiktoken o200k). /ultracave 14, /megacave 13. 규칙이 입력 토큰을 약 1,160개 추가. 요청 단위 과금은 절약 없음. CLI는 기본으로 사용 통계 전송 (`caveman telemetry off`).
- EP.03: 스타일 79 (활성 50) · 팔레트 192 · 폰트 조합 74 · 차트 25 · 스택 22 · UX 가이드 119. 검색 엔진은 Python 표준 라이브러리만 쓰고 네트워크를 호출하지 않음.
- EP.04: /grill-me = "Interviews you about a plan until every branch is resolved".
- EP.05: 스킬 25개 (메타 1 · 정의 4 · 계획 1 · 구현 7 · 검증 2 · 리뷰 4 · 출시 6). /build auto는 승인 한 번 후 전부 구현하고, 작업마다 TDD와 개별 커밋, 실패나 위험 단계에선 멈춤.
- EP.06: 규칙 4개 Think Before Coding · Simplicity First · Surgical Changes · Goal-Driven Execution. 카파시 본인이 만들거나 보증한 저장소가 아님.
- EP.07: 위키백과 "Signs of AI writing" 기반, 패턴 26개 · 6개 묶음. 첫 고쳐쓰기 → 비평 → 최종본. AI 탐지기 회피 목적이 아니라고 명시.
- EP.08: Garry Tan (Y Combinator 대표), 도구 23개, Bun 1.4.2+ 필요. /office-hours · /review · /qa · /ship · /autoplan · /careful.
- EP.09: 스킬 52개. 영상 속 6개 분야 묶음은 이해를 돕기 위해 직접 나눈 것 (README 공식 분류 아님).
- EP.10: 로컬 SQLite + Chroma 저장, <private> 태그, 설치 시 클라우드 로그인 단계 (CLAUDE_MEM_ONLINE_OPTIN=false 또는 --provider로 생략 가능), 클라우드 동기화는 선택.
- EP.07·08·09의 체크리스트·예시 문장, 대화 장면("예시 화면")은 이해를 돕기 위한 연출이에요.
- 별 수는 계속 바뀌니 업로드 당일 다시 확인하세요.
