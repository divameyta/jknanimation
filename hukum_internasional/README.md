# Video Animasi: Studi Kasus Sipadan-Ligitan (Indonesia/Malaysia)

Video animasi untuk Akademik Showcase Hukum Internasional, **Kelompok 7, Pengantar Hukum Indonesia Kelas C**, Fakultas Hukum Universitas Jember.
Video ini mengikuti *Panduan Video Animasi Sipadan-Ligitan Kelompok 7*: fokus pada contoh kasus, 8 adegan, narasi dan subtitle sesuai teks panduan.

## Berkas

| Berkas | Isi |
|---|---|
| `output/Video_Kasus_Sipadan_Ligitan_Kelompok7.mp4` | **Video utama**: narasi, subtitle, dan musik loop (16:9, 1920×1080) |
| `output/Video_Kasus_Sipadan_Ligitan_Kelompok7_tanpa_suara.mp4` | Versi tanpa audio (subtitle tetap ada) |
| `NASKAH_VIDEO.md` | Narasi per adegan beserta waktu tayang |
| `src/kasus.html` | Sumber animasi (Canvas). Buka di peramban untuk pratinjau; `?t=60` membekukan pada detik ke-60 |
| `src/narasi.json` | Narasi 8 adegan: `sub` = teks persis panduan (subtitle), `tts` = ejaan fonetis untuk suara |
| `src/narasi.py` | Pembuat suara (Piper TTS offline) dan jadwal adegan |
| `src/musik_loop.py` | Musik latar sintetis bebas royalti yang menyambung mulus saat diulang |
| `src/qr.png` | QR ke Google Drive materi lengkap (naskah induk, infografis, leaflet, video), melalui https://q.me-qr.com/udbutg0r |
| `src/render.js` | Perekam frame menjadi MP4 |
| `src/fonts/` | Fredoka (OFL) dan Luckiest Guy (Apache 2.0) |

## Gaya visual
Mengikuti Bagian 1 panduan: langit biru cerah berawan, garis paranada dan not musik melayang, huruf kartun tebal merah–biru–kuning, dan ikon ramah (globe, timbangan, palu hakim, gulungan perjanjian, pulau, balon udara, pesawat kertas).
**Tidak ada karakter, logo, atau kendaraan dari acara TV/film mana pun.** Nuansanya terinspirasi tema "Little Einstein", tetapi tidak memakai tokoh atau aset acara tersebut.

| Warna | Hex |
|---|---|
| Langit | `#3FA9EE` → `#BFE6FF` |
| Merah | `#E8262D` |
| Biru | `#1F4FA3` |
| Kuning | `#FFCE1F` |
| Navy (garis/teks) | `#14306B` |

## Membuat ulang

```bash
python3 src/narasi.py <path>/id_ID-news_tts-medium.onnx kerja/ 0.8
TIMING=kerja/jadwal.json SUBS=kerja/subtitle_waktu.json node src/render.js video output/_video.mp4 30 4
python3 src/musik_loop.py <durasi_video> kerja/musik.wav
ffmpeg -i output/_video.mp4 -i kerja/narasi.wav -i kerja/musik.wav \
  -filter_complex "[1]aresample=44100,apad[n];[2]volume=0.22[m];[n][m]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest output/Video_Kasus_Sipadan_Ligitan_Kelompok7.mp4
```

Kalau kelompok merekam narasi sendiri dengan durasi tepat sesuai panduan, isi `durasi` di `narasi.json` dan jadwal di `jadwal.json` bisa disesuaikan, lalu render ulang.
