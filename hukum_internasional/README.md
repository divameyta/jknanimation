# Video Animasi: Hukum Internasional & Kasus Sipadan-Ligitan

Video animasi kartun untuk **Akademik Showcase Hukum Internasional**, Kelompok 7, Kelas C, Fakultas Hukum Universitas Jember.
Seluruh isi diambil dari *Naskah Induk Hukum Internasional Kelompok 7*, dan susunannya mengikuti *Ketentuan Isi Media* (bagian 4, Video Animasi).

## Berkas

| Berkas | Isi |
|---|---|
| `output/Video_Hukum_Internasional_Kelompok7.mp4` | **Video utama**: narasi, subtitle, dan musik loop (16:9, 1080p, 2:54) |
| `output/Video_Hukum_Internasional_Kelompok7_tanpa_suara.mp4` | Versi tanpa audio (subtitle tetap ada) |
| `NASKAH_VIDEO.md` | Naskah narasi per adegan dengan penanda waktu |
| `src/video.html` | Sumber animasi (Canvas). Buka di peramban untuk pratinjau; `?t=60` membekukan pada detik ke-60 |
| `src/narasi.json` / `src/subtitle.json` | Kalimat narasi (ejaan fonetis untuk TTS) dan teks subtitle |
| `src/narasi.py` | Pembuat narasi (Piper TTS offline), faktor sinkronisasi, dan waktu subtitle |
| `src/musik_loop.py` | Musik latar sintetis bebas hak cipta yang menyambung mulus saat diulang |
| `src/render.js` | Perekam frame menjadi MP4 |

## Kesesuaian dengan ketentuan video

| Ketentuan | Rencana | Di video |
|---|---|---|
| Pembuka: pertanyaan pemantik | ±10 dtk | 0:00–0:09: "Mengapa Sipadan dan Ligitan kini milik Malaysia?" |
| Definisi & ruang lingkup: animasi subjek | ±20 dtk | 0:09–0:31: definisi lintas batas, 6 subjek muncul bergantian, 6 cabang |
| Prinsip & asas: istilah Latin satu per satu | ±20 dtk | 0:31–0:55: 4 prinsip (Pasal 2 Piagam PBB), lalu 6 kartu asas Latin beserta artinya |
| Tujuan & fungsi: ikon bergerak | ±15 dtk | 0:55–1:11: 4 ikon tujuan dan 4 roda gigi fungsi |
| Sumber hukum: diagram Pasal 38 bertahap | ±20 dtk | 1:11–1:31: a, b, c turun satu per satu (setara), lalu d sebagai sumber tambahan |
| Kasus: peta, kronologi, para pihak, sidang, putusan | ±60 dtk | 1:31–2:38: peta ilustrasi, 6 titik kronologi, Special Agreement dan tabel dalil, 17 hakim, 3 pertimbangan, palu 16:1 |
| Penutup: pelajaran, ajakan scan QR, sumber | ±10 dtk | 2:38–2:54: pelajaran, ajakan scan QR, daftar sumber |
| 16:9, subtitle wajib, musik bebas hak cipta | | 1920×1080, subtitle selalu tampil, musik sintetis buatan sendiri |
| Akhir menyambung mulus ke awal | | 1,8 detik terakhir melebur ke frame pertama, dan musik di-crossfade agar loop tanpa jeda |

## Konsistensi antarmedia (leaflet, infografis, video)

- **Font:** Fredoka (Google Fonts, gratis; tersedia juga di Canva).
- **Palet warna:**

| Nama | Hex | Dipakai untuk |
|---|---|---|
| Navy | `#1D3557` | judul, kotak penting |
| Biru laut | `#457B9D` | aksen, rujukan pasal |
| Biru muda | `#A8DADC` | latar kartu |
| Krem | `#F1FAEE` | latar halaman |
| Merah | `#E63946` | kasus, penekanan |
| Emas | `#FFB703` | label, sorotan |
| Toska | `#2A9D8F` | prinsip, tanda benar |

- **Istilah:** sama dengan naskah induk (mis. *effectivités*, *Special Agreement*, "Pasal 38 ayat (1) Statuta ICJ").
- **Maskot:** "Si Bumi" (bola dunia berwajah), bisa dipakai juga di leaflet dan infografis.

## Membuat ulang

```bash
python3 src/narasi.py <path>/id_ID-news_tts-medium.onnx kerja/
SUBS=kerja/subtitle_waktu.json SKALA=$(cat kerja/skala.txt) node src/render.js video output/_video.mp4 30 4
python3 src/musik_loop.py <durasi_video> kerja/musik.wav
ffmpeg -i output/_video.mp4 -i kerja/narasi.wav -i kerja/musik.wav \
  -filter_complex "[1]aresample=44100[n];[2]volume=0.25[m];[n][m]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest output/Video_Hukum_Internasional_Kelompok7.mp4
```
