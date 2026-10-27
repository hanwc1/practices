# AI 스킬 릴스

GitHub에서 인기 있는 AI 에이전트 스킬을 하나씩 골라 소개하고 사용법을 알려주는 인스타 릴스 채널 자료예요.

## 에피소드
| 편 | 스킬 | 폴더 |
|---|---|---|
| EP.01 | [obra/superpowers](https://github.com/obra/superpowers) | `ep01_superpowers/` |
| EP.02 | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `ep02_caveman/` |
| EP.03 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `ep03_ui_ux_pro_max/` |
| EP.04 | [mattpocock/skills](https://github.com/mattpocock/skills) | `ep04_mattpocock_skills/` |
| EP.05 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | `ep05_agent_skills/` |

각 폴더에 영상(무음 `*.mp4`, 배경음악 포함 `*_bgm.mp4`), 썸네일(`thumbnail_4x5.png`), 릴스 커버(`cover_9x16.png`), 캡션(`caption.txt`, @aimateur.lab 집사 말투)이 있어요. 캡션의 `[키워드]`는 댓글 이벤트 키워드로 바꿔 쓰세요. 확인 근거는 `SOURCES.md`에 정리했어요.

## 영상 다시 만들기 (`tools/`)
무료 도구만 사용해요 (Python + Pillow + ffmpeg). 유료 생성 서비스는 쓰지 않아요.

```bash
pip install pillow
cd tools
python3 ep01_superpowers.py <출력폴더>   # → EP01_superpowers.mp4
python3 thumb_ep01.py <출력폴더>         # → thumbnail_4x5.png, cover_9x16.png
python3 ep02_caveman.py ../ep02_caveman  # EP.02부터는 영상+썸네일+커버를 한 번에 (ep03~05도 같은 방식)
```

- `common.py`: 배경, 카드, 애니메이션 같은 공통 그리기 도구
- `card_style.py`: @aimateur.lab 카드 스타일 (손글씨 태그, 고양이 스티커, 말풍선, 헤드라인 패널)
- `costumes.py`: 후추 코스튬 합성 (EP.01 히어로, EP.02 원시인, EP.03 화가, EP.04 탐정, EP.05 개발자)
- `ep01_superpowers.py`: EP.01 장면 구성
- `thumb_ep01.py`: EP.01 썸네일·커버
- `episode.py`: EP.02부터 쓰는 공통 엔진 (장면 틀, 렌더러, 썸네일·커버)
- `ep02_caveman.py` ~ `ep05_agent_skills.py`: 편별 내용
- `fonts/`: Pretendard, Gaegu, JetBrains Mono (모두 SIL Open Font License, 라이선스 파일 포함)
- `../assets/cat.webp`: 마스코트 고양이 사진

출력은 1080×1920, 30fps예요. 무음 영상에 배경음악을 입히려면:

```bash
pip install numpy scipy soundfile
python3 add_bgm.py            # 모든 편 → *_bgm.mp4
python3 add_bgm.py ep02_caveman   # 한 편만
```

배경음악은 `music.py`가 코드로 직접 합성한 업비트 팝(112~124 BPM)이라 저작권 걱정이 없어요. 편마다 템포와 코드 진행이 달라요. 잔잔한 로파이 버전(`generate`)도 남겨 뒀어요.
