# Video Animasi: Dari Pasif Menjadi Proaktif

Video animasi untuk presentasi makalah *"Analisis Hukum Telematika terhadap Penonaktifan Peserta PBI Jaminan Kesehatan Tahun 2026 dan Peran Aplikasi Mobile JKN sebagai Layanan Publik Digital"* (Kelompok 2, Hukum Telematika Kelas E, FH Universitas Jember).

Video ini berfokus pada **solusi** yang ditawarkan dalam makalah (BAB III Saran).

## Berkas

| Berkas | Isi |
|---|---|
| `output/Animasi_Solusi_PBI_JKN.mp4` | **Video utama**: narasi suara Bahasa Indonesia + musik latar (1080p, 6:08) |
| `output/Animasi_Solusi_PBI_JKN_tanpa_suara.mp4` | Video bertempo narasi tanpa audio, untuk direkam ulang dengan suara sendiri |
| `output/Animasi_Solusi_PBI_JKN_singkat_tanpa_narasi.mp4` | Versi singkat (3:29) hanya dengan musik, tanpa narasi |
| `NASKAH_NARASI.md` | Teks narasi per adegan beserta penanda waktu |
| `src/animasi.html` | Sumber animasi (Canvas). Buka di peramban untuk pratinjau; tambahkan `?t=60` untuk membekukan pada detik ke-60 |
| `src/narasi.json` | Kalimat narasi per adegan (ejaan disesuaikan untuk TTS) |
| `src/narasi.py` | Pembuat trek narasi (Piper TTS offline) dan faktor sinkronisasi adegan |
| `src/render.js` | Perekam frame menjadi MP4 (Playwright + ffmpeg) |
| `src/musik.py` | Pembuat musik latar sintetis (bebas hak cipta) |

## Struktur video (versi bernarasi)

| Waktu | Adegan |
|---|---|
| 0:00 | Pembuka |
| 0:12 | Latar masalah (singkat) |
| 0:49 | Peta: 3 akar masalah → 3 solusi |
| 1:05 | Solusi 1: pemberitahuan langsung H-30 (pull → push) |
| 1:31 | Solusi 1: multikanal + dasar hukum |
| 2:08 | Solusi 2: DPIA + pengecualian otomatis pasien katastropik |
| 3:31 | Solusi 3: interoperabilitas data + lembaga PDP |
| 4:28 | Alur sebelum vs sesudah solusi |
| 4:57 | 6 tips praktis bagi masyarakat |
| 5:53 | Penutup |

## Membuat ulang video

Model suara: `vits-piper-id_ID-news_tts-medium` dari rilis `tts-models` di GitHub k2-fsa/sherpa-onnx (diekstrak, dipakai berkas `.onnx`-nya).

```bash
pip install piper-tts
python3 src/narasi.py <path>/id_ID-news_tts-medium.onnx kerja/      # -> kerja/narasi.wav, kerja/skala.txt
SKALA=$(cat kerja/skala.txt) node src/render.js video output/_video.mp4 30 4
python3 src/musik.py 368.5 kerja/musik.wav
ffmpeg -i output/_video.mp4 -i kerja/narasi.wav -i kerja/musik.wav \
  -filter_complex "[1]volume=1.0[n];[2]volume=0.22[m];[n][m]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k output/Animasi_Solusi_PBI_JKN.mp4
```

Agar adegan sinkron dengan narasi, setiap adegan diperlambat secara proporsional dengan faktor `k` (lihat `skala.txt`). Teks di video bisa diubah di `src/animasi.html`, dan kalimat narasi di `src/narasi.json`, lalu render ulang.
