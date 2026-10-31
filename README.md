# Video Animasi: Dari Pasif Menjadi Proaktif

Video animasi untuk presentasi makalah *"Analisis Hukum Telematika terhadap Penonaktifan Peserta PBI Jaminan Kesehatan Tahun 2026 dan Peran Aplikasi Mobile JKN sebagai Layanan Publik Digital"* (Kelompok 2, Hukum Telematika Kelas E, FH Universitas Jember).

Video ini berfokus pada **solusi** yang ditawarkan dalam makalah (BAB III Saran).

## Berkas

| Berkas | Isi |
|---|---|
| `output/Animasi_Kartun_Solusi_PBI_JKN.mp4` | **Video utama (kartun)**: narasi suara, subtitle, dan musik latar (1080p, 6:08) |
| `output/Animasi_Kartun_Solusi_PBI_JKN_tanpa_suara.mp4` | Versi kartun tanpa audio (subtitle tetap ada), untuk direkam ulang dengan suara sendiri |
| `output/Animasi_Solusi_PBI_JKN.mp4` | Versi infografis (non-kartun) dengan narasi dan musik |
| `output/Animasi_Solusi_PBI_JKN_tanpa_suara.mp4` | Versi infografis tanpa audio |
| `output/Animasi_Solusi_PBI_JKN_singkat_tanpa_narasi.mp4` | Versi infografis singkat (3:29), hanya musik |
| `NASKAH_NARASI.md` | Teks narasi per adegan beserta penanda waktu |
| `src/kartun.html` | Sumber animasi kartun (Canvas). Buka di peramban untuk pratinjau; tambahkan `?t=60` untuk membekukan pada detik ke-60 |
| `src/animasi.html` | Sumber animasi versi infografis |
| `src/narasi.json` / `src/subtitle.json` | Kalimat narasi (ejaan untuk TTS) dan teks subtitle yang ditampilkan |
| `src/narasi.py` | Pembuat trek narasi (Piper TTS offline), faktor sinkronisasi adegan, dan waktu subtitle |
| `src/render.js` | Perekam frame menjadi MP4 (Playwright + ffmpeg) |
| `src/musik.py` | Pembuat musik latar sintetis (bebas hak cipta) |
| `src/fonts/` | Font Fredoka (SIL Open Font License) |

## Tokoh dalam versi kartun

- **Pak Darmo**: peserta PBI (tokoh fiktif) yang mengalami masalah lalu merasakan solusinya.
- **Bu Sari**: kader/petugas desa yang membantu perbaikan data dan mengantar surat.
- **Si Mobile JKN**: maskot ponsel. Ia tertidur saat aplikasi pasif, lalu "berdering" saat proaktif.
- **Mesin DPIA**, **robot Data Terpadu**, dan **Pengawas PDP** (pahlawan berjubah) untuk Solusi 2 dan 3.

## Struktur video

| Waktu | Adegan |
|---|---|
| 0:00 | Pembuka |
| 0:12 | Latar masalah (singkat) |
| 0:47 | Peta: 3 akar masalah → 3 solusi |
| 1:03 | Solusi 1: pemberitahuan langsung H-30 (pull → push) |
| 1:30 | Solusi 1: tiga kanal + dasar hukum |
| 2:07 | Solusi 2: mesin DPIA + pengecualian otomatis pasien katastropik |
| 3:30 | Solusi 3: data terpadu + lembaga pengawas PDP |
| 4:27 | Alur sebelum vs sesudah solusi |
| 4:57 | 6 tips praktis bagi masyarakat |
| 5:53 | Penutup |

## Membuat ulang video

Model suara: `vits-piper-id_ID-news_tts-medium` dari rilis `tts-models` di GitHub k2-fsa/sherpa-onnx (diekstrak, dipakai berkas `.onnx`-nya).

```bash
pip install piper-tts
python3 src/narasi.py <path>/id_ID-news_tts-medium.onnx kerja/      # -> kerja/narasi.wav, kerja/skala.txt
PAGE=kartun.html SUBS=kerja/subtitle_waktu.json SKALA=$(cat kerja/skala.txt) node src/render.js video output/_video.mp4 30 4
python3 src/musik.py 368.5 kerja/musik.wav
ffmpeg -i output/_video.mp4 -i kerja/narasi.wav -i kerja/musik.wav \
  -filter_complex "[1]volume=1.0[n];[2]volume=0.22[m];[n][m]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k output/Animasi_Kartun_Solusi_PBI_JKN.mp4
```

Agar adegan sinkron dengan narasi, setiap adegan diperlambat secara proporsional dengan faktor `k` (lihat `skala.txt`). Teks di video bisa diubah di `src/kartun.html`, dan kalimat narasi di `src/narasi.json`, lalu render ulang.
