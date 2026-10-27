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
