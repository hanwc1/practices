# 에피소드별 확인 근거 (각 GitHub 저장소 페이지, 2026-10-26~27 확인)

| 편 | 저장소 | ⭐ / 포크 | 라이선스 | 설치 (Claude Code) |
|---|---|---|---|---|
| EP.01 | obra/superpowers | 305.6k / 27.2k | MIT | `/plugin install superpowers@claude-plugins-official` |
| EP.02 | JuliusBrussee/caveman | 115.3k / 6.7k | Apache-2.0 | `/plugin marketplace add JuliusBrussee/caveman` → `/plugin install caveman@caveman` |
| EP.03 | nextlevelbuilder/ui-ux-pro-max-skill | 140.9k / 14.9k | MIT | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` → `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill` |
| EP.04 | mattpocock/skills | 304.1k / 25.6k | MIT | `claude plugin install mattpocock-skills@claude-plugins-official` → `/setup-matt-pocock-skills` |
| EP.05 | addyosmani/agent-skills | 110.8k / 11.6k | MIT | `/plugin marketplace add addyosmani/agent-skills` → `/plugin install agent-skills@addy-agent-skills` |

## 영상 속 숫자와 주장
- EP.02: 63 → 20토큰은 README의 React 리렌더 예시 (tiktoken o200k). /ultracave 14, /megacave 13. 규칙이 입력 토큰을 약 1,160개 추가. 요청 단위 과금은 절약 없음. CLI는 기본으로 사용 통계 전송 (`caveman telemetry off`).
- EP.03: 스타일 79 (활성 50) · 팔레트 192 · 폰트 조합 74 · 차트 25 · 스택 22 · UX 가이드 119. 검색 엔진은 Python 표준 라이브러리만 쓰고 네트워크를 호출하지 않음.
- EP.04: /grill-me = "Interviews you about a plan until every branch is resolved".
- EP.05: 스킬 25개 (메타 1 · 정의 4 · 계획 1 · 구현 7 · 검증 2 · 리뷰 4 · 출시 6). /build auto는 승인 한 번 후 전부 구현하고, 작업마다 TDD와 개별 커밋, 실패나 위험 단계에선 멈춤.
- 대화 장면("예시 화면")은 이해를 돕기 위한 연출이에요.
- 별 수는 계속 바뀌니 업로드 당일 다시 확인하세요.
