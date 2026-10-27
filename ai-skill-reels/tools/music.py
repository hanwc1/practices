# 저작권 걱정 없는 로파이 배경음악을 코드로 합성 (일렉 피아노 코드, 베이스, 드럼, 멜로디, LP 잡음)
import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100

PROGS = {  # 코드 진행 (C 기준 MIDI 음)
    "iv-iii-ii-I": [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]],
    "ii-V-I-vi":   [[50, 53, 57, 60, 64], [55, 59, 62, 64, 65], [48, 52, 55, 59, 62], [57, 60, 64, 67]],
    "vi-IV-I-V":   [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]],
    "minor-jazz":  [[51, 55, 58, 62], [50, 53, 57, 60], [48, 51, 55, 58], [46, 50, 53, 57]],
}
PENTA = [0, 2, 4, 7, 9]

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, f, order=2): return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)

def add(buf, sig, t0):
    i = int(t0 * SR)
    if i >= len(buf) or i < 0: return
    n = min(len(sig), len(buf) - i); buf[i:i + n] += sig[:n]

def rhodes(m, dur, vel, rng):
    t = np.arange(int((dur + 1.2) * SR)) / SR; f = hz(m)
    env = np.minimum(t / .008, 1) * np.exp(-t / 1.3); rel = np.clip((dur + .25 - t) / .25, 0, 1); env *= rel
    tone = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.004 * t)
    tone += .22 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / .25) + .06 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / .12)
    return vel * .14 * tone * env * (1 + .07 * np.sin(2 * np.pi * 4.8 * t + rng.uniform(0, 6)))

def bass(m, dur, vel):
    t = np.arange(int((dur + .1) * SR)) / SR; f = hz(m)
    env = np.minimum(t / .006, 1) * np.exp(-t / .7) * np.clip((dur + .05 - t) / .05, 0, 1)
    return vel * .42 * (np.sin(2 * np.pi * f * t) + .18 * np.sin(4 * np.pi * f * t)) * env

def kick(vel):
    t = np.arange(int(.45 * SR)) / SR; f = 46 + 85 * np.exp(-t / .035); ph = 2 * np.pi * np.cumsum(f) / SR
    return vel * .9 * np.sin(ph) * np.exp(-t / .22)

def snare(vel, rng):
    t = np.arange(int(.3 * SR)) / SR; n = bp(rng.standard_normal(len(t)), 1200, 5200)
    return vel * (.35 * n * np.exp(-t / .11) + .25 * np.sin(2 * np.pi * 185 * t) * np.exp(-t / .045))

def hat(vel, rng, open_=False):
    t = np.arange(int((.25 if open_ else .07) * SR)) / SR
    return vel * .22 * hp(rng.standard_normal(len(t)), 7000) * np.exp(-t / (.09 if open_ else .022))

def bell(m, vel):
    t = np.arange(int(1.4 * SR)) / SR; f = hz(m)
    return vel * .12 * (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / .2)) * np.minimum(t / .004, 1) * np.exp(-t / .45)

def generate(seconds, bpm=84, prog="iv-iii-ii-I", key=0, seed=1):
    rng = np.random.default_rng(seed); beat = 60 / bpm; bar = 4 * beat
    n = int((seconds + 2) * SR); keys, bassb, drums, mel = (np.zeros(n) for _ in range(4))
    chords = [[m + key for m in c] for c in PROGS[prog]]; nbars = int(np.ceil(seconds / bar)) + 1
    kicks = []; sw = lambda b: b + (.08 if (b * 2) % 2 == 1 else 0)  # 8분음 스윙 (박 단위)
    for bi in range(nbars):
        t0 = bi * bar; ch = chords[bi % len(chords)]; full = 2 <= bi < nbars - 2 and bi != nbars // 2
        for j, m in enumerate(ch):  # 코드: 살짝 흩뿌려 치기
            add(keys, rhodes(m, bar * (.62 if rng.random() < .5 else .95), rng.uniform(.65, .85), rng), t0 + j * .014)
        if rng.random() < .55:
            for j, m in enumerate(ch[1:]): add(keys, rhodes(m, beat * 1.3, rng.uniform(.4, .55), rng), t0 + 2.5 * beat + j * .012)
        if bi >= 1:
            root = ch[0] - 24 if ch[0] - 24 >= 33 else ch[0] - 12
            add(bassb, bass(root, beat * 1.6, .9), t0); add(bassb, bass(root + (7 if rng.random() < .5 else 0), beat * .9, .75), t0 + 2.5 * beat)
            if rng.random() < .4: add(bassb, bass(root + 12, beat * .25, .5), t0 + 3.75 * beat)
        for k in range(8):  # 하이햇 8분음
            if bi >= 1: add(drums, hat(rng.uniform(.5, .8) * (1 if k % 2 == 0 else .7), rng, open_=(k == 7 and rng.random() < .3)), t0 + sw(k / 2) * beat)
        if full:
            for b in [0, 2.5] + ([1.75] if rng.random() < .3 else []): add(drums, kick(.95), t0 + sw(b) * beat); kicks.append(t0 + sw(b) * beat)
            for b in (1, 3): add(drums, snare(.8, rng), t0 + b * beat + .012)
            if bi % 2 == 0:  # 멜로디: 2마디마다 짧은 펜타토닉 동기
                pos = sorted(rng.choice(np.arange(16), size=rng.integers(3, 6), replace=False))
                for p in pos: add(mel, bell(72 + key + rng.choice(PENTA) + (12 if rng.random() < .2 else 0), rng.uniform(.6, .9)), t0 + sw(p / 2) * beat)
    # 킥에 맞춰 코드·베이스를 살짝 눌러주기
    t = np.arange(n) / SR; duck = np.ones(n)
    for tk in kicks:
        i = int(tk * SR); seg = t[i:i + int(.3 * SR)] - tk; duck[i:i + len(seg)] = np.minimum(duck[i:i + len(seg)], 1 - .3 * np.exp(-seg / .12))
    keys, bassb = lp(keys, 3800) * duck, lp(bassb, 900) * duck
    d = int(beat * .75 * SR); echo = np.zeros(n); echo[d:] = mel[:-d] * .35; echo[2 * d:] += mel[:-2 * d] * .12; mel = lp(mel + echo, 5000)
    vinyl = lp(rng.standard_normal(n), 2500) * .004
    for i in rng.integers(0, n, int(seconds * 6)): vinyl[i:i + 40] += rng.uniform(.02, .06) * np.exp(-np.arange(min(40, n - i)) / 6)
    def level(x, db):  # 악기별 음량을 RMS 기준으로 맞춤 (코드가 주인공, 드럼은 뒤로)
        r = np.sqrt(np.mean(x[x != 0] ** 2)) if np.any(x) else 1; return x * (10 ** (db / 20) / max(r, 1e-9))
    drums = lp(drums, 6000)
    keys, bassb, drums, mel = level(keys, -17), level(bassb, -19), level(drums, -22), level(mel, -24)
    left = keys + bassb + drums + mel * .9 + vinyl
    hz_ = int(.012 * SR); kr = np.zeros(n); kr[hz_:] = keys[:-hz_]  # 코드는 살짝 넓게
    right = keys * .6 + kr * .45 + bassb + drums + np.roll(mel, int(.004 * SR)) + vinyl
    st = np.tanh(np.stack([left, right], 1) * 1.1)
    st = st[:int(seconds * SR)]; fi, fo = int(.4 * SR), int(2.5 * SR)
    st[:fi] *= np.linspace(0, 1, fi)[:, None]; st[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    return (st / max(1e-9, np.abs(st).max()) * .89).astype(np.float32)


# ---------- 업비트 팝 (밝고 통통 튀는 버전) ----------
POP_PROGS = {  # C 기준
    "I-V-vi-IV":  [[60, 64, 67, 72], [59, 62, 67, 71], [57, 60, 64, 69], [57, 60, 65, 69]],
    "vi-IV-I-V":  [[57, 60, 64, 69], [57, 60, 65, 69], [60, 64, 67, 72], [59, 62, 67, 71]],
    "I-vi-IV-V":  [[60, 64, 67, 72], [57, 60, 64, 69], [57, 60, 65, 69], [59, 62, 67, 71]],
    "IV-V-iii-vi": [[57, 60, 65, 69], [59, 62, 67, 71], [59, 64, 67, 71], [57, 60, 64, 69]],
}
POP_ROOTS = {"I-V-vi-IV": [48, 43, 45, 41], "vi-IV-I-V": [45, 41, 48, 43], "I-vi-IV-V": [48, 45, 41, 43], "IV-V-iii-vi": [41, 43, 40, 45]}

def pluck(m, vel, dur=.22):
    t = np.arange(int((dur + .05) * SR)) / SR; f = hz(m); tone = np.zeros_like(t)
    for k in range(1, 9): tone += np.sin(2 * np.pi * f * k * t * (1 + .0015 * (k % 2))) / k  # 톱니파 비슷하게
    return vel * .1 * tone * np.minimum(t / .003, 1) * np.exp(-t / (dur * .45))

def pad(ms, dur):
    t = np.arange(int(dur * SR)) / SR; out = np.zeros_like(t)
    for m in ms:
        for det in (-.004, 0, .004): out += np.sin(2 * np.pi * hz(m) * (1 + det) * t) + .3 * np.sin(4 * np.pi * hz(m) * (1 + det) * t)
    env = np.minimum(t / .15, 1) * np.clip((dur - t) / .15, 0, 1); return out * env * .02

def pop_bass(m, vel, dur):
    t = np.arange(int((dur + .03) * SR)) / SR; f = hz(m)
    tone = np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) + .15 * np.sin(6 * np.pi * f * t)
    return vel * .4 * tone * np.minimum(t / .003, 1) * np.exp(-t / (dur * .7))

def marimba(m, vel):
    t = np.arange(int(.6 * SR)) / SR; f = hz(m)
    return vel * .2 * (np.sin(2 * np.pi * f * t) * np.exp(-t / .22) + .35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / .03)) * np.minimum(t / .002, 1)

def punch_kick(vel):
    t = np.arange(int(.35 * SR)) / SR; f = 52 + 120 * np.exp(-t / .025); ph = 2 * np.pi * np.cumsum(f) / SR
    return vel * (np.sin(ph) * np.exp(-t / .16) + .3 * np.exp(-t / .002) * np.random.default_rng(0).standard_normal(len(t)))

def clap(vel, rng):
    out = np.zeros(int(.25 * SR))
    for k, dt in enumerate((0, .009, .018)):
        t = np.arange(int(.2 * SR)) / SR; burst = bp(rng.standard_normal(len(t)), 900, 5000) * np.exp(-t / (.012 if k < 2 else .09))
        i = int(dt * SR); out[i:i + len(burst)] += burst[:len(out) - i]
    return vel * .5 * out

def generate_pop(seconds, bpm=118, prog="I-V-vi-IV", key=0, seed=1):
    rng = np.random.default_rng(seed); beat = 60 / bpm; bar = 4 * beat; e8 = beat / 2; s16 = beat / 4
    n = int((seconds + 2) * SR); chords_b, bass_b, drum_b, lead_b, pad_b = (np.zeros(n) for _ in range(5))
    chords = [[m + key for m in c] for c in POP_PROGS[prog]]; roots = [r + key for r in POP_ROOTS[prog]]
    nbars = int(np.ceil(seconds / bar)) + 1; brk = nbars // 2 + (nbars // 2) % 2  # 중간에 1마디 쉬어가기
    scale = [0, 2, 4, 7, 9, 12, 14, 16]
    motif = [(0, 4), (1, 4), (3, 5), (4, 4), (6, 2), (7, 3), (10, 4), (12, 5), (14, 7)]  # (8분음 위치, 음계 위치) 2마디 후크
    alt = [(p, min(len(scale) - 1, s + rng.integers(-1, 2))) for p, s in motif]
    kicks = []
    for bi in range(nbars):
        t0 = bi * bar; ch = chords[bi % 4]; root = roots[bi % 4]
        intro, full = bi < 2, 2 <= bi < nbars - 1 and bi != brk
        add(pad_b, pad(ch[:3], bar), t0)
        for k in range(8):  # 플럭 코드: 엇박 위주로 통통
            if k % 2 == 1 or k == 0 or (k == 4 and rng.random() < .5):
                for j, m in enumerate(ch): add(chords_b, pluck(m, (.95 if k % 2 else .7) * rng.uniform(.85, 1)), t0 + k * e8 + j * .003)
        if not intro:
            for k in range(8): add(bass_b, pop_bass(root + (12 if k % 2 else 0), .9 if k % 2 == 0 else .7, e8 * .9), t0 + k * e8)
        for k in range(16):  # 하이햇 16분음
            if intro and k % 2: continue
            add(drum_b, hat(.9 if k % 4 == 2 else .45, rng, open_=(k % 4 == 2 and full)), t0 + k * s16)
        if full:
            for b in range(4): add(drum_b, punch_kick(1.0), t0 + b * beat); kicks.append(t0 + b * beat)
            for b in (1, 3): add(drum_b, clap(.9, rng), t0 + b * beat)
            if bi % 2 == 0:
                for p, sidx in (motif if (bi // 2) % 2 == 0 else alt): add(lead_b, marimba(72 + key + scale[sidx], rng.uniform(.8, 1)), t0 + p * e8)
        if bi == 1 or bi == brk:  # 다음 마디로 끌어올리는 스네어 롤
            for k in range(8): add(drum_b, clap(.25 + .08 * k, rng), t0 + 2 * beat + k * s16)
    t = np.arange(n) / SR; duck = np.ones(n)
    for tk in kicks:  # 킥에 맞춰 펌핑
        i = int(tk * SR); seg = t[i:i + int(beat * SR)] - tk; duck[i:i + len(seg)] = np.minimum(duck[i:i + len(seg)], 1 - .45 * np.exp(-seg / .09))
    def level(x, db):
        r = np.sqrt(np.mean(x[x != 0] ** 2)) if np.any(x) else 1; return x * (10 ** (db / 20) / max(r, 1e-9))
    chords_b = level(lp(chords_b, 5500), -19) * duck; pad_b = level(lp(pad_b, 3000), -27) * duck
    bass_b = level(lp(bass_b, 1400), -18) * duck; drum_b = level(drum_b, -17); lead_b = level(lead_b, -20)
    d = int(e8 * 3 * SR); echo = np.zeros(n); echo[d:] = lead_b[:-d] * .3; lead_b = lead_b + echo
    left = chords_b + pad_b + bass_b + drum_b + lead_b
    w = int(.010 * SR); cr = np.zeros(n); cr[w:] = chords_b[:-w]
    right = chords_b * .55 + cr * .5 + pad_b + bass_b + drum_b + np.roll(lead_b, int(.003 * SR))
    st = np.tanh(np.stack([left, right], 1) * 1.2)[:int(seconds * SR)]
    fi, fo = int(.05 * SR), int(2.0 * SR)
    st[:fi] *= np.linspace(0, 1, fi)[:, None]; st[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.3
    return (st / max(1e-9, np.abs(st).max()) * .9).astype(np.float32)
