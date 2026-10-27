# AI 스킬 릴스

GitHub에서 인기 있는 AI 에이전트 스킬을 하나씩 골라 소개하고 사용법을 알려주는 인스타 릴스 채널 자료예요.

## 에피소드
| 편 | 스킬 | 폴더 |
|---|---|---|
| EP.01 | [obra/superpowers](https://github.com/obra/superpowers) | `ep01_superpowers/` (영상, 커버, 캡션, 대본) |

## 영상 다시 만들기 (`tools/`)
무료 도구만 사용해요 (Python + Pillow + ffmpeg). 유료 생성 서비스는 쓰지 않아요.

```bash
pip install pillow
cd tools
python3 ep01_superpowers.py <출력폴더>   # → EP01_superpowers.mp4, cover.png
```

- `common.py`: 배경, 카드, 애니메이션 같은 공통 그리기 도구
- `ep01_superpowers.py`: EP.01 장면 구성
- `fonts/`: Pretendard, JetBrains Mono (둘 다 SIL Open Font License, 라이선스 파일 포함)

출력은 1080×1920, 30fps, 무음이에요. 배경음악은 인스타 앱에서 넣어요.
