"""Membuat trek suara narasi (TTS offline Piper, suara Bahasa Indonesia).

Setiap adegan punya beberapa "cue" (detik mulai + kalimat) di src/narasi.json.
Jika narasi lebih panjang dari jendela waktunya, adegan diperlambat dengan
faktor k (animasi diregangkan secara proporsional) agar suara dan gambar tetap
sinkron. Faktor k disimpan ke berkas agar dipakai saat merender video.

Pemakaian:
  python3 src/narasi.py <model.onnx> <folder_kerja>
Keluaran di folder_kerja: narasi.wav, skala.txt (faktor k per adegan), jadwal.txt
"""
import json
import re
import os
import subprocess
import sys
import wave

import numpy as np

BASE = [9, 22, 13, 15, 20, 34, 34, 22, 30, 10]  # harus sama dengan SCENES di animasi.html
NAMA = ['Pembuka', 'Latar masalah', 'Peta solusi', 'Solusi 1: pemberitahuan H-30',
        'Solusi 1: multikanal + dasar hukum', 'Solusi 2: DPIA + pengecualian otomatis',
        'Solusi 3: interoperabilitas data + lembaga PDP', 'Alur sebelum vs sesudah',
        'Tips masyarakat', 'Penutup']
SR = 22050
model, work = sys.argv[1], sys.argv[2]
os.makedirs(work, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
cues = json.load(open(os.path.join(here, 'narasi.json'), encoding='utf-8'))
assert len(cues) == len(BASE)
subs = json.load(open(os.path.join(here, 'subtitle.json'), encoding='utf-8'))
assert [len(x) for x in subs] == [len(x) for x in cues]


def tts(text, path):
    subprocess.run([sys.executable, '-m', 'piper', '-m', model, '-f', path,
                    '--length-scale', '0.92', '--sentence-silence', '0.3'],
                   input=text.encode('utf-8'), check=True, capture_output=True)
    with wave.open(path) as w:
        assert w.getframerate() == SR
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


clips, ks = [], []
for si, sc in enumerate(cues):
    D = BASE[si]
    row, k = [], 1.0
    for ci, (off, text) in enumerate(sc):
        a = tts(text, os.path.join(work, f'cue_{si:02d}_{ci:02d}.wav'))
        # buang hening di awal/akhir
        nz = np.nonzero(np.abs(a) > 0.01)[0]
        a = a[max(0, nz[0] - 200): nz[-1] + 2000] if len(nz) else a
        dur = len(a) / SR
        end = sc[ci + 1][0] if ci + 1 < len(sc) else D - (1.6 if si == len(BASE) - 1 else 0.7)
        k = max(k, (dur + 0.35) / (end - off))
        row.append((off, a, dur, text))
    k = round(k, 3)
    ks.append(k)
    clips.append(row)

total = sum(d * k for d, k in zip(BASE, ks))
track = np.zeros(int(total * SR) + SR)
jadwal = []
waktu = []
start = 0.0
for si, row in enumerate(clips):
    k = ks[si]
    jadwal.append(f'{int(start // 60)}:{int(start % 60):02d}  {NAMA[si]}  (k={k})')
    for off, a, dur, text in row:
        i0 = int((start + off * k) * SR)
        track[i0:i0 + len(a)] += a
        # subtitle: bagi kalimat secara proporsional terhadap jumlah karakter
        teks = subs[si][row.index((off, a, dur, text))]
        kal = [k_.strip() for k_ in re.split(r'(?<=[.?!])\s+', teks) if k_.strip()]
        n_all = sum(len(k_) for k_ in kal)
        t0 = start + off * k
        for k_ in kal:
            d_ = dur * len(k_) / n_all
            waktu.append([round(t0, 3), round(t0 + d_ + .15, 3), k_])
            t0 += d_
    start += BASE[si] * k

track = track / max(1e-6, np.max(np.abs(track))) * 0.9
with wave.open(os.path.join(work, 'narasi.wav'), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((track * 32767).astype(np.int16).tobytes())
json.dump(waktu, open(os.path.join(work, 'subtitle_waktu.json'), 'w', encoding='utf-8'), ensure_ascii=False)
open(os.path.join(work, 'skala.txt'), 'w').write(','.join(str(k) for k in ks))
open(os.path.join(work, 'jadwal.txt'), 'w').write('\n'.join(jadwal) + f'\nTOTAL {total:.2f}\n')
print(','.join(str(k) for k in ks))
print('\n'.join(jadwal))
print(f'TOTAL {total:.2f} detik')
