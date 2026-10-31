"""Membuat musik latar ambient sederhana (sintesis, bebas hak cipta).

Pemakaian: python3 src/musik.py <durasi_detik> <keluaran.wav>
"""
import sys
import wave
import numpy as np

SR = 44100
dur = float(sys.argv[1])
out = sys.argv[2]
n = int(SR * dur)
t = np.arange(n) / SR

# progresi akor lembut: Am - F - C - G, masing-masing 8 detik
def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)

CHORDS = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]
BAR = 8.0
pad = np.zeros(n)
arp = np.zeros(n)
for k in range(int(np.ceil(dur / BAR)) + 1):
    ch = CHORDS[k % 4]
    s0 = k * BAR - 1.5
    e0 = s0 + BAR + 3.0
    i0, i1 = max(0, int(s0 * SR)), min(n, int(e0 * SR))
    if i0 >= i1:
        continue
    tt = t[i0:i1] - s0
    env = np.sin(np.pi * np.clip(tt / (BAR + 3.0), 0, 1)) ** 2
    for m in ch:
        f = hz(m)
        pad[i0:i1] += env * (np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * 2 * f * tt + .5)) / len(ch)
    # arpeggio pelan (8 not per bar)
    for j in range(8):
        st = k * BAR + j * 1.0
        a0 = int(st * SR)
        if a0 >= n or st < 0:
            continue
        a1 = min(n, a0 + int(1.8 * SR))
        ta = t[a0:a1] - st
        f = hz(ch[[0, 1, 2, 3, 2, 1, 2, 3][j]] + 12)
        arp[a0:a1] += np.exp(-ta * 3.0) * np.sin(2 * np.pi * f * ta) * (1 - np.exp(-ta * 200))

mix = .55 * pad + .18 * arp
# gema sederhana
for d, g in [(.31, .35), (.62, .2), (.93, .1)]:
    s = int(d * SR)
    mix[s:] += g * mix[:-s]
# fade in/out
fi, fo = int(3 * SR), int(4 * SR)
mix[:fi] *= np.linspace(0, 1, fi)
mix[-fo:] *= np.linspace(1, 0, fo)
mix = mix / np.max(np.abs(mix)) * .35
stereo = np.stack([mix, np.roll(mix, int(.012 * SR))], axis=1)
data = (stereo * 32767).astype(np.int16)
with wave.open(out, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print('ok', out, dur)
