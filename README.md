# Video Animasi: Dari Pasif Menjadi Proaktif

Video animasi untuk presentasi makalah *"Analisis Hukum Telematika terhadap Penonaktifan Peserta PBI Jaminan Kesehatan Tahun 2026 dan Peran Aplikasi Mobile JKN sebagai Layanan Publik Digital"* (Kelompok 2, Hukum Telematika Kelas E, FH Universitas Jember).

Video ini berfokus pada **solusi** yang ditawarkan dalam makalah (BAB III Saran).

## Berkas

| Berkas | Isi |
|---|---|
| `output/Animasi_Solusi_PBI_JKN.mp4` | Video final dengan musik latar (1080p, ±3,5 menit) |
| `output/Animasi_Solusi_PBI_JKN_tanpa_musik.mp4` | Video yang sama tanpa audio, untuk diisi narasi sendiri |
| `NASKAH_NARASI.md` | Naskah narasi per adegan, lengkap dengan penanda waktu |
| `src/animasi.html` | Sumber animasi (Canvas). Buka di peramban untuk pratinjau; tambahkan `?t=60` untuk membekukan pada detik ke-60 |
| `src/render.js` | Perekam frame menjadi MP4 (Playwright + ffmpeg) |
| `src/musik.py` | Pembuat musik latar sintetis (bebas hak cipta) |

## Struktur video

| Waktu | Adegan |
|---|---|
| 0:00 | Pembuka |
| 0:09 | Latar masalah (singkat) |
| 0:31 | Peta: 3 akar masalah → 3 solusi |
| 0:44 | Solusi 1: pemberitahuan langsung H-30 (pull → push) |
| 0:59 | Solusi 1: multikanal + dasar hukum |
| 1:19 | Solusi 2: DPIA + pengecualian otomatis pasien katastropik |
| 1:53 | Solusi 3: interoperabilitas data + lembaga PDP |
| 2:27 | Alur sebelum vs sesudah solusi |
| 2:49 | 6 tips praktis bagi masyarakat |
| 3:19 | Penutup |

## Membuat ulang video

```bash
node src/render.js video output/_video_nosound.mp4 30 6
python3 src/musik.py 209 musik.wav
ffmpeg -i output/_video_nosound.mp4 -i musik.wav -c:v copy -c:a aac -b:a 160k -shortest output/Animasi_Solusi_PBI_JKN.mp4
```

Teks pada video bisa diubah langsung di `src/animasi.html`, lalu render ulang.
