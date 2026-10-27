# AI 스킬 릴스

GitHub에서 인기 있는 AI 에이전트 스킬을 하나씩 골라 소개하고 사용법을 알려주는 인스타 릴스 채널 자료예요.

## 에피소드
| 편 | 스킬 | 폴더 |
|---|---|---|
| EP.01 | [obra/superpowers](https://github.com/obra/superpowers) | `ep01_superpowers/` (영상, 썸네일 4:5, 커버 9:16, 캡션, 대본) |

## 영상 다시 만들기 (`tools/`)
무료 도구만 사용해요 (Python + Pillow + ffmpeg). 유료 생성 서비스는 쓰지 않아요.

```bash
pip install pillow
cd tools
python3 ep01_superpowers.py <출력폴더>   # → EP01_superpowers.mp4
python3 thumb_ep01.py <출력폴더>         # → thumbnail_4x5.png, cover_9x16.png
```

- `common.py`: 배경, 카드, 애니메이션 같은 공통 그리기 도구
- `card_style.py`: @aimateur.lab 카드 스타일 (손글씨 태그, 고양이 스티커, 말풍선, 헤드라인 패널)
- `ep01_superpowers.py`: EP.01 장면 구성
- `thumb_ep01.py`: EP.01 썸네일·커버
- `fonts/`: Pretendard, Gaegu, JetBrains Mono (모두 SIL Open Font License, 라이선스 파일 포함)
- `../assets/cat.webp`: 마스코트 고양이 사진

출력은 1080×1920, 30fps, 무음이에요. 배경음악은 인스타 앱에서 넣어요.
