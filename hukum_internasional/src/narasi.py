"""Membuat narasi (Piper TTS offline, suara Bahasa Indonesia) dan jadwal adegan.

Setiap kalimat (cue) disuarakan terpisah lalu diletakkan berurutan di dalam adegannya.
Durasi adegan = durasi panduan, kecuali bila narasinya lebih panjang (adegan diperpanjang seperlunya).

Pemakaian: python3 narasi.py <model.onnx> <folder_kerja> [length_scale]
Keluaran: narasi.wav, jadwal.json (mulai/durasi adegan dan waktu tiap cue),
          subtitle_waktu.json, jadwal.txt
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

SR = 22050
model, work = sys.argv[1], sys.argv[2]
LS = sys.argv[3] if len(sys.argv) > 3 else '0.86'
os.makedirs(work, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(here, 'narasi.json'), encoding='utf-8'))['adegan']

LEAD, GAP, TAIL = 0.5, 0.3, 0.5


def tts(text, path):
    subprocess.run([sys.executable, '-m', 'piper', '-m', model, '-f', path,
                    '--length-scale', LS, '--sentence-silence', '0.2'],
                   input=text.encode('utf-8'), check=True, capture_output=True)
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    nz = np.nonzero(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 200): nz[-1] + 1500] if len(nz) else a


jadwal, subs, clips = [], [], []
start = 0.0
for si, sc in enumerate(data):
    t = LEAD
    cues = []
    for ci, c in enumerate(sc['cue']):
        a = tts(c['tts'], os.path.join(work, f'cue_{si}_{ci}.wav'))
        d = len(a) / SR
        cues.append({'t': round(t, 3), 'dur': round(d, 3)})
        clips.append((start + t, a))
        # subtitle: bagi per kalimat secara proporsional
        kal = [k.strip() + ('' if k.strip()[-1:] in '.?!' else '.') for k in c['sub'].replace('? ', '?|').replace('. ', '.|').split('|') if k.strip()]
        n = sum(len(k) for k in kal); t0 = start + t
        for k in kal:
            dd = d * len(k) / n
            subs.append([round(t0, 3), round(t0 + dd + .15, 3), k]); t0 += dd
        t += d + GAP
    dur = max(sc['durasi'], t - GAP + TAIL)
    jadwal.append({'nama': sc['nama'], 'mulai': round(start, 3), 'dur': round(dur, 3), 'panduan': sc['durasi'], 'cue': cues})
    start += dur

total = start
track = np.zeros(int(total * SR) + SR)
for t0, a in clips:
    i0 = int(t0 * SR); track[i0:i0 + len(a)] += a
track = track[:int(round(total * 30) / 30 * SR)]
track = track / max(1e-6, np.max(np.abs(track))) * 0.9
with wave.open(os.path.join(work, 'narasi.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype(np.int16).tobytes())
json.dump({'total': round(total, 3), 'adegan': jadwal}, open(os.path.join(work, 'jadwal.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(subs, open(os.path.join(work, 'subtitle_waktu.json'), 'w', encoding='utf-8'), ensure_ascii=False)
rows = [f"{int(j['mulai'] // 60)}:{j['mulai'] % 60:05.2f}  {j['nama']:<26} {j['dur']:6.2f} dtk (panduan {j['panduan']})" for j in jadwal]
open(os.path.join(work, 'jadwal.txt'), 'w').write('\n'.join(rows) + f'\nTOTAL {total:.2f}\n')
print('\n'.join(rows)); print(f'TOTAL {total:.2f} detik')
