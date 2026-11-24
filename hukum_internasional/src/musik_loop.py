"""Musik latar sintetis (bebas hak cipta) yang menyambung mulus saat diputar berulang.

Pemakaian: python3 musik_loop.py <durasi_detik> <keluaran.wav>
Ekor musik di-crossfade ke awalnya, sehingga sampel terakhir menyambung ke sampel pertama.
"""
import sys
import wave
import numpy as np

SR = 44100
dur = float(sys.argv[1])
out = sys.argv[2]
X = 4.0  # panjang crossfade (detik)
n = int(SR * (dur + X))
t = np.arange(n) / SR


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# progresi ceria: C - G - Am - F, 4 detik per akor (tempo 120, 2 birama)
CH = [[48, 55, 60, 64], [43, 50, 59, 62], [45, 52, 57, 60], [41, 48, 57, 60]]
BAR = 4.0
pad = np.zeros(n); pl = np.zeros(n); bass = np.zeros(n)
for k in range(int(np.ceil((dur + X) / BAR)) + 1):
    ch = CH[k % 4]
    s0 = k * BAR - .8
    i0, i1 = max(0, int(s0 * SR)), min(n, int((s0 + BAR + 1.6) * SR))
    if i0 >= i1:
        continue
    tt = t[i0:i1] - s0
    env = np.sin(np.pi * np.clip(tt / (BAR + 1.6), 0, 1)) ** 2
    for m in ch[1:]:
        pad[i0:i1] += env * np.sin(2 * np.pi * hz(m) * tt) / 3
    # bas: dua ketukan
    for b in range(4):
        st = k * BAR + b * 1.0
        a0 = int(st * SR)
        if a0 >= n:
            continue
        a1 = min(n, a0 + int(.9 * SR)); ta = t[a0:a1] - st
        bass[a0:a1] += np.exp(-ta * 4) * np.sin(2 * np.pi * hz(ch[0]) * ta) * (1 - np.exp(-ta * 300))
    # petikan (seperti marimba): pola 8 not per birama
    pat = [0, 2, 1, 3, 2, 1, 3, 2]
    for j in range(8):
        st = k * BAR + j * .5
        a0 = int(st * SR)
        if a0 >= n:
            continue
        a1 = min(n, a0 + int(.6 * SR)); ta = t[a0:a1] - st
        f = hz(ch[1:][pat[j] % 3] + 12 + (12 if pat[j] == 3 else 0))
        pl[a0:a1] += np.exp(-ta * 9) * (np.sin(2 * np.pi * f * ta) + .3 * np.sin(2 * np.pi * 4 * f * ta)) * (1 - np.exp(-ta * 400))

mix = .45 * pad + .35 * bass + .22 * pl
for d, g in [(.25, .25), (.5, .12)]:
    s = int(d * SR); mix[s:] += g * mix[:-s]
# crossfade ekor (dur..dur+X) ke awal (0..X) agar loop mulus
L, xs = int(dur * SR), int(X * SR)
fade = np.linspace(0, 1, xs)
head = mix[:xs] * fade + mix[L:L + xs] * (1 - fade)
loop = np.concatenate([head, mix[xs:L]])
loop = loop / np.max(np.abs(loop)) * .35
st = np.stack([loop, np.roll(loop, int(.011 * SR))], axis=1)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok', out, len(loop) / SR)
