# EP.01 썸네일(4:5, 1080x1350)과 릴스 커버(9:16, 1080x1920)
# 커버는 프로필 그리드가 가운데 4:5만 보여주므로, 썸네일 디자인을 그대로 가운데에 두고 위아래만 늘림
import sys
from card_style import *

OUT = sys.argv[1]
TAG = "GitHub 인기 스킬 #1"
HEAD = [[("GitHub 별 30만 개,", False)], [("이 스킬 ", False), ("뭐길래?", True)]]

def design(h, oy):
    im = background(W, h); split = oy + 930
    paste(im, pill(TAG), 70, oy + 60)
    c = cat(820); paste(im, c, W - c.width + 70, split - c.height + 40)
    panel(im, split, h)  # 고양이 아래쪽 잘린 부분을 패널이 덮음
    paste(im, bubble(["별이 30만 개", "실화냥?"], 60), 50, oy + 250)
    s = star_sticker("306,000", 5); paste(im, s, 40, oy + 600)
    hd = headline(HEAD, 86); paste(im, hd, 80, split + 70)
    footer(im, oy + 1270, "EP.01 · obra/superpowers")
    return im.convert("RGB")

design(1350, 0).save(f"{OUT}/thumbnail_4x5.png")
design(1920, 285).save(f"{OUT}/cover_9x16.png")
print("ok")
