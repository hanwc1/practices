import math

def star(d, x, y, r, fill):
    pts = [(x + (r if i % 2 == 0 else r * .45) * math.cos(-math.pi / 2 + i * math.pi / 5),
            y + (r if i % 2 == 0 else r * .45) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
    d.polygon(pts, fill=fill)
