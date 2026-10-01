# 🔬 Fitness Tracking Eye — Analisis Perbandingan Arsitektur

> **Dokumen Temuan Teknis**
> Tanggal: 1 Oktober 2026
> Status: Draft untuk Diskusi Tim

---

## 1. Ringkasan Eksekutif

Setelah melakukan riset mendalam dan diskusi teknis selama beberapa sesi, ditemukan **celah-celah kritis** pada rancangan awal (Proposal v1) yang berpotensi menyebabkan kegagalan sistem di lapangan. Dokumen ini membandingkan **Rancangan Awal (v1)** dengan **Rancangan Revisi (v2)** secara menyeluruh dari segala aspek yang bisa dibandingkan.

### Perubahan Arsitektur Inti

| Aspek | Rancangan v1 (Proposal Asli) | Rancangan v2 (Revisi Baru) |
|:---|:---|:---|
| **Jumlah Kamera** | 4 unit | 2 unit |
| **Hardware Kamera** | XIAO ESP32-S3 Sense + OV5640 | Raspberry Pi AI Camera (Sony IMX500) |
| **Host/Pengontrol** | ESP32-S3 (built-in) | Raspberry Pi Zero 2 W |
| **Lokasi AI Processing** | Central (di Laptop/PC) | Edge (di dalam kamera itu sendiri) |
| **Data yang Dikirim via WiFi** | Video mentah MJPEG (berat) | Teks JSON skeleton (ringan) |
| **WiFi** | 2.4 GHz (salah tulis 5GHz) | 2.4 GHz (cukup untuk teks) |
| **Coverage** | 360° (4 sudut pandang) | ~180° (2 sudut orthogonal 90°) |

---

## 2. Perbandingan Hardware

### 2.1 Komponen per Titik Kamera

**Rancangan v1 — Satu titik kamera terdiri dari:**
```
┌──────────────────────────────────┐
│  Lensa OV5640 (5MP)              │
│         ↓ (kabel pita)           │
│  XIAO ESP32-S3 Sense             │
│  • Xtensa LX7 240MHz             │
│  • 8MB PSRAM                     │
│  • WiFi 2.4GHz ONLY ⚠️           │
│  • Tugas: Tangkap gambar →       │
│    Kompresi MJPEG → Kirim Video  │
│         ↓ (WiFi)                 │
│  [VIDEO MENTAH ke Laptop]        │
└──────────────────────────────────┘
```

**Rancangan v2 — Satu titik kamera terdiri dari:**
```
┌──────────────────────────────────┐
│  RPi AI Camera (Sony IMX500)     │
│  • 12.3MP sensor                 │
│  • Built-in AI Accelerator (NPU) │
│  • Tugas: Tangkap gambar →       │
│    Deteksi 33 keypoints →        │
│    Output koordinat skeleton     │
│         ↓ (kabel pita CSI)       │
│  Raspberry Pi Zero 2 W           │
│  • BCM2710A1 1GHz quad-core      │
│  • 512MB RAM                     │
│  • WiFi 2.4GHz                   │
│  • Tugas: Terima skeleton data → │
│    Format ke JSON → Kirim Teks   │
│         ↓ (WiFi)                 │
│  [TEKS JSON ke Laptop/HP]        │
└──────────────────────────────────┘
```

### 2.2 Spesifikasi Kamera Head-to-Head

| Spesifikasi | OV5640 (v1) | Sony IMX500 (v2) |
|:---|:---|:---|
| Resolusi Maksimum | 5 Megapiksel (2592×1944) | 12.3 Megapiksel (4056×3040) |
| FPS Efektif untuk Proyek | 15-20 FPS (VGA, MJPEG) | 30 FPS (binned 2028×1520) |
| AI On-Chip | ❌ Tidak ada | ✅ Neural Network Accelerator |
| Ukuran Fisik Modul | ~20×20 mm (sangat kecil) | ~25×24×12 mm (kecil) |
| Kualitas Gambar | Standar (warna agak pucat) | Profesional (Sony sensor) |
| Harga per Unit (Lokal) | ~Rp 225.000 (termasuk ESP32) | ~Rp 2.000.000 (kamera saja) |

### 2.3 Spesifikasi Mikrokontroler/Host Head-to-Head

| Spesifikasi | XIAO ESP32-S3 (v1) | RPi Zero 2 W (v2) |
|:---|:---|:---|
| Klasifikasi | Mikrokontroler | Single Board Computer (SBC) |
| Prosesor | Xtensa LX7, Dual-core 240MHz | ARM Cortex-A53, Quad-core 1GHz |
| RAM | 8MB PSRAM | 512MB LPDDR2 |
| Sistem Operasi | Tidak ada (bare-metal/RTOS) | Linux (Raspberry Pi OS) |
| WiFi | 2.4GHz **SAJA** | 2.4GHz **SAJA** |
| Port Kamera | DVP (untuk OV series) | CSI (untuk RPi Camera series) |
| Penyimpanan | Flash internal | MicroSD (perlu dibeli terpisah) |
| Konsumsi Daya | ~1-2 Watt (sangat hemat) | ~2-3 Watt (lebih boros) |
| Harga per Unit (Lokal) | Sudah termasuk di OV5640 | ~Rp 1.000.000 |
| Ukuran | 21×17.5 mm (sekecil koin) | 65×30 mm (seukuran flashdisk besar) |

---

## 3. Perbandingan Biaya (RAB)

### 3.1 Rincian Biaya Hardware Lengkap

**Rancangan v1 — 4 Kamera ESP32-S3**

| Komponen | Qty | Harga Satuan | Total |
|:---|:---:|:---:|:---|
| XIAO ESP32-S3 Sense + OV5640 | 4 | Rp 225.000 | Rp 900.000 |
| Custom 3D Printed Casing | 4 | Rp 150.000 | Rp 600.000 |
| Enclosure Mounting Bracket | 4 | Rp 200.000 | Rp 800.000 |
| Mini Tripod Foldable | 4 | Rp 120.000 | Rp 480.000 |
| USB-C Power Adapter & Kabel | 4 | Rp 56.250 | Rp 225.000 |
| Travel WiFi Router 5GHz | 1 | Rp 600.000 | Rp 600.000 |
| Sensor IMU BMI270 | 2 | Rp 120.000 | Rp 240.000 |
| Baterai LiPo IMU | 2 | Rp 112.500 | Rp 225.000 |
| Tracking Band Neon | 1 set | Rp 200.000 | Rp 200.000 |
| **TOTAL v1** | | | **Rp 4.270.000** |

**Rancangan v2 — 2 Kamera AI Raspberry Pi**

| Komponen | Qty | Harga Satuan | Total |
|:---|:---:|:---:|:---|
| Raspberry Pi AI Camera (Sony IMX500) | 2 | Rp 2.000.000 | Rp 4.000.000 |
| Raspberry Pi Zero 2 W | 2 | Rp 1.000.000 | Rp 2.000.000 |
| MicroSD Card 32GB (Class 10) | 2 | Rp 75.000 | Rp 150.000 |
| Custom 3D Printed Casing | 2 | Rp 150.000 | Rp 300.000 |
| Mini Tripod Foldable | 2 | Rp 120.000 | Rp 240.000 |
| Powerbank 10000mAh 5V/3A + Kabel | 2 | Rp 250.000 | Rp 500.000 |
| Travel WiFi Router (Opsional) | 1 | Rp 600.000 | Rp 600.000 |
| **TOTAL v2** | | | **Rp 7.790.000** |

### 3.2 Analisis Selisih Biaya

| Metrik | v1 | v2 | Selisih |
|:---|:---:|:---:|:---|
| **Total Biaya Hardware** | Rp 4.270.000 | Rp 7.790.000 | **+Rp 3.520.000 (82% lebih mahal)** |
| Biaya per Titik Kamera | Rp 556.250 | Rp 3.345.000 | +Rp 2.788.750 per titik |
| Jumlah Komponen yang Dirakit | ~20 bagian | ~10 bagian | 50% lebih sedikit |
| Komponen yang Perlu Disolder | 0 | 0 | Sama (tidak ada) |

> **Catatan:** Meskipun v2 82% lebih mahal, selisih Rp 3,5 Juta ini "membeli" kita:
> eliminasi risiko WiFi lag, eliminasi beban CPU di Laptop, dan arsitektur software yang 50% lebih sederhana.

---

## 4. Perbandingan Arsitektur Software

### 4.1 Aliran Data (Data Flow)

**Rancangan v1 — Central Processing**
```
4x ESP32 ──[Video MJPEG 640x480]──→ WiFi 2.4GHz ──→ Laptop
                                                         │
                                          ┌──────────────┤
                                          ↓              ↓
                                    MediaPipe x4    Triangulasi 3D
                                    (SANGAT BERAT)  (OpenCV DLT)
                                          ↓              ↓
                                    Exercise Engine ←────┘
                                          ↓
                                    WebSocket → Dashboard
```
- **Bandwidth WiFi yang dibutuhkan:** ~8-12 Mbps (4 video sekaligus)
- **Beban CPU Laptop:** SANGAT TINGGI (4 instance MediaPipe paralel)
- **Titik Kegagalan:** WiFi congestion, frame drop, CPU overload

**Rancangan v2 — Edge Processing**
```
2x RPi AI Camera ──[AI di dalam kamera]──→ RPi Zero 2W
                                               │
                                    [JSON ~1KB/frame]
                                               ↓
                                          WiFi 2.4GHz
                                               ↓
                                          Laptop / HP
                                               │
                                    ┌──────────┤
                                    ↓          ↓
                              Triangulasi   Exercise Engine
                              3D (ringan)   (State Machine)
                                    ↓          ↓
                              WebSocket → Dashboard
```
- **Bandwidth WiFi yang dibutuhkan:** ~0.1-0.5 Mbps (hanya teks JSON)
- **Beban CPU Laptop:** SANGAT RINGAN (hanya matematika sudut)
- **Titik Kegagalan:** Minimal

### 4.2 Kompleksitas Koding

| Modul yang Harus Dikoding | v1 (Kesulitan) | v2 (Kesulitan) |
|:---|:---|:---|
| **Firmware Kamera** | 🔥🔥🔥 Sulit — Koding C/C++ untuk MJPEG streaming di ESP32, buffer management, WiFi reconnect | ⭐ Mudah — Cukup load model AI ke kamera, SDK Raspberry Pi sudah tersedia |
| **Video Receiver di Laptop** | 🔥🔥🔥🔥 Sangat Sulit — Menerima 4 stream video MJPEG secara paralel, menjaga sinkronisasi timestamp, error handling saat frame drop | ⭐⭐ Mudah — Menerima 2 stream teks JSON kecil via WebSocket |
| **Pose Estimation** | 🔥🔥🔥 Sulit — Menjalankan 4 instance MediaPipe secara multiprocessing di Laptop tanpa crash | ✅ Tidak perlu dikoding — Sudah otomatis berjalan di dalam cip Sony IMX500 |
| **Sinkronisasi Antar Kamera** | 🔥🔥🔥🔥 Sangat Sulit — Mencocokkan frame dari 4 video yang datang dengan timing berbeda (async) | ⭐⭐ Mudah — Mencocokkan 2 paket JSON berdasarkan timestamp |
| **Triangulasi 3D** | 🔥🔥 Sedang — OpenCV DLT dari 4 sudut pandang, banyak edge case | 🔥🔥 Sedang — Sama, tapi hanya dari 2 sudut (lebih sederhana) |
| **Exercise Engine (State Machine)** | 🔥🔥 Sedang | 🔥🔥 Sedang — Identik, tidak berubah |
| **Web Dashboard** | 🔥🔥 Sedang | 🔥🔥 Sedang — Identik, tidak berubah |
| **Mobile App** | 🔥🔥 Sedang | 🔥🔥 Sedang — Identik, tidak berubah |
| **Cloud Sync** | ⭐ Mudah | ⭐ Mudah — Identik, tidak berubah |
| | | |
| **TOTAL ESTIMASI** | **🔥 Kesulitan: 9/10** | **⭐ Kesulitan: 5/10** |

> **Kesimpulan:** Rancangan v2 mengurangi beban koding (software engineering) hampir **50%** karena modul tersulit (Video Streaming + AI Paralel + Sinkronisasi 4 Kamera) sudah ditangani oleh hardware.

---

## 5. Perbandingan Keandalan (Reliability)

| Aspek Keandalan | v1 (4x ESP32) | v2 (2x RPi AI Cam) | Pemenang |
|:---|:---|:---|:---|
| **Stabilitas WiFi** | ⚠️ KRITIS — 4 video stream @ 2.4GHz = risiko congestion sangat tinggi, frame drop di lingkungan ramai | ✅ AMAN — Hanya mengirim teks ~1KB, bandwidth minimal | **v2** |
| **Konsistensi FPS** | ⚠️ TIDAK TERJAMIN — ESP32 MJPEG sering drop dari 20 ke 5 FPS saat WiFi sibuk | ✅ KONSISTEN — AI Camera selalu 30 FPS (processing on-chip) | **v2** |
| **Sinkronisasi Waktu** | ⚠️ SANGAT SULIT — 4 sumber async, drift bisa 50-200ms | ✅ MUDAH — 2 sumber saja, drift lebih terkontrol | **v2** |
| **Ketahanan Panas** | ✅ BAIK — ESP32 hemat daya, jarang overheat | ⚠️ SEDANG — RPi Zero 2W bisa hangat, perlu ventilasi di casing | **v1** |
| **Ketahanan Baterai** | ✅ UNGGUL — ~1-2W, powerbank kecil tahan >15 jam | ⚠️ CUKUP — ~2-3W per node, powerbank 10Ah tahan ~6-8 jam | **v1** |
| **Waktu Boot/Startup** | ✅ INSTAN — ESP32 nyala dalam <1 detik | ⚠️ LAMBAT — RPi butuh ~30-45 detik untuk booting Linux | **v1** |
| **Recovery dari Error** | ⚠️ MANUAL — Jika ESP32 hang, harus dicabut & colok ulang | ✅ OTOMATIS — Linux bisa di-script untuk auto-restart service | **v2** |

**Skor Keandalan:**
- v1: 3 menang, 4 kalah → **Keandalan: 43%**
- v2: 4 menang, 3 kalah → **Keandalan: 57%**

---

## 6. Perbandingan Performa Sistem

| Metrik Performa | v1 (4x ESP32) | v2 (2x RPi AI Cam) |
|:---|:---|:---|
| **Resolusi Input ke AI** | VGA 640×480 (limitasi bandwidth) | Full HD 2028×1520 (on-chip, no bandwidth issue) |
| **FPS AI Processing** | 15-20 FPS (bottleneck WiFi) | 30 FPS (on-chip, konsisten) |
| **Jumlah Keypoints** | 33 (MediaPipe BlazePose) | Tergantung model yang di-load (bisa 17 atau 33) |
| **Total Latency End-to-End** | 150-300 ms (optimistis), **500ms+ realistis** saat WiFi macet | **50-100 ms** (data teks sangat ringan) |
| **Beban CPU Main Device** | 70-90% (4x MediaPipe paralel) | 5-15% (hanya matematika sudut) |
| **Main Device Minimum** | Laptop dengan GPU dedicated (minimal GTX 1650) | Laptop kantoran biasa, atau bahkan Smartphone |
| **Akurasi Pose Estimation** | Baik (33 keypoints 3D) | Sangat Baik (Sony sensor lebih tajam, NPU lebih presisi) |

---

## 7. Perbandingan Portabilitas

| Aspek | v1 (4x ESP32) | v2 (2x RPi AI Cam) |
|:---|:---|:---|
| **Jumlah Tiang/Tripod** | 4 buah | 2 buah |
| **Berat Total Kit** | ~3-4 kg | ~2-3 kg |
| **Waktu Setup** | ~10-15 menit (pasang 4 tripod + kalibrasi 4 kamera) | ~5-8 menit (pasang 2 tripod + boot RPi) |
| **Waktu Bongkar** | ~5 menit | ~3 menit |
| **Main Device** | HARUS Laptop berperforma tinggi (berat, besar) | Bisa Laptop biasa atau bahkan HP Android |
| **Kapasitas Ransel** | Penuh (4 tripod + 4 node + router + laptop gaming) | Setengah kosong (2 tripod + 2 node + router) |

---

## 8. Perbandingan Coverage & Akurasi per Exercise

| Exercise | v1: 4 Kamera 360° | v2: 2 Kamera 90° | Dampak Pengurangan |
|:---|:---|:---|:---|
| **Push Up** | Depan, Belakang, Kiri, Kanan | Samping + Depan-Serong | ⚠️ Minimal — gerakan linear, 2 sudut sudah cukup melihat siku & punggung |
| **Pull Up** | Depan, Belakang, Kiri, Kanan | Samping + Depan-Serong | ⚠️ Minimal — gerakan naik-turun, 2 sudut cukup untuk mendeteksi dagu melewati bar |
| **Sit Up** | Depan, Belakang, Kiri, Kanan | Samping + Depan-Serong | ⚠️ Minimal — gerakan fleksi trunk terlihat jelas dari samping |
| **Squat Jump** | Depan, Belakang, Kiri, Kanan | Samping + Depan-Serong | ⚠️ Sedang — kehilangan kemampuan melihat simetri lutut dari belakang |
| **Vertical Jump** | Depan, Belakang, Kiri, Kanan | Samping + Depan-Serong | ⚠️ Minimal — tinggi lompatan terukur jelas dari samping |

> **Kesimpulan Coverage:** Untuk **5 exercise yang dipilih** (semuanya gerakan linear/sagittal plane), pengurangan dari 4 ke 2 kamera hanya sedikit mempengaruhi Squat Jump (kehilangan deteksi *knee valgus* dari belakang). Semua exercise lain **tidak terdampak signifikan**.

---

## 9. Temuan Kritis pada Rancangan v1

### 🚨 Temuan #1: WiFi 5GHz yang Tidak Mungkin
**Lokasi di Proposal:** BAB 4.1, baris "1x Travel WiFi Router 5GHz"
**Masalah:** XIAO ESP32-S3 Sense hanya mendukung WiFi 2.4GHz. Menulis "5GHz" di proposal adalah **klaim yang tidak bisa dipenuhi**.
**Dampak:** Jika klien/penguji memverifikasi, ini menjadi cacat faktual yang merusak kredibilitas proposal.

### 🚨 Temuan #2: Beban Komputasi Tersembunyi
**Lokasi di Proposal:** BAB 3.2, "Total Latency Sistem: 150–300 ms"
**Masalah:** Estimasi latency 150-300ms mengasumsikan 4 video stream berjalan mulus tanpa hambatan. Pada realita WiFi 2.4GHz yang padat (gym, co-working space), latency bisa membengkak ke **500ms hingga 2 detik**.
**Dampak:** Klaim "real-time" di proposal menjadi menyesatkan.

### 🚨 Temuan #3: Main Device Tidak Disebutkan
**Lokasi di Proposal:** BAB 4, BAB 9 (RAB)
**Masalah:** Proposal tidak menyebutkan kebutuhan **Laptop/PC lokal** sebagai mesin pemroses AI. Dalam arsitektur v1, Laptop dengan GPU dedicated adalah **kebutuhan WAJIB**, namun tidak masuk di RAB maupun di daftar kebutuhan teknis.
**Dampak:** Klien bisa berasumsi sistem berjalan tanpa Laptop tambahan, lalu merasa dirugikan saat mengetahui harus menyediakan Laptop sendiri.

---

## 10. Matriks Keputusan Final

| Kriteria (Bobot) | v1: 4x ESP32 | v2: 2x RPi AI Cam | Pemenang |
|:---|:---|:---|:---|
| Biaya Hardware (15%) | ⭐⭐⭐⭐⭐ (Rp 4,2 Jt) | ⭐⭐ (Rp 7,8 Jt) | **v1** |
| Keandalan Jaringan (20%) | ⭐⭐ (WiFi 2.4GHz, 4 video) | ⭐⭐⭐⭐⭐ (teks saja) | **v2** |
| Kemudahan Koding (20%) | ⭐⭐ (kesulitan 9/10) | ⭐⭐⭐⭐ (kesulitan 5/10) | **v2** |
| Akurasi Real-Time (15%) | ⭐⭐⭐ (tergantung WiFi) | ⭐⭐⭐⭐⭐ (30 FPS konsisten) | **v2** |
| Portabilitas (10%) | ⭐⭐⭐ (4 tiang) | ⭐⭐⭐⭐⭐ (2 tiang) | **v2** |
| Coverage 360° (10%) | ⭐⭐⭐⭐⭐ (4 sudut) | ⭐⭐⭐ (2 sudut) | **v1** |
| Ketahanan Baterai (5%) | ⭐⭐⭐⭐⭐ (>15 jam) | ⭐⭐⭐ (6-8 jam) | **v1** |
| Fleksibilitas Main Device (5%) | ⭐⭐ (butuh laptop GPU) | ⭐⭐⭐⭐⭐ (HP biasa pun cukup) | **v2** |
| | | | |
| **SKOR TOTAL TERTIMBANG** | **2.95 / 5** | **4.15 / 5** | **🏆 v2** |

---

## 11. Rekomendasi Akhir

### ✅ Gunakan Rancangan v2 (2x Raspberry Pi AI Camera) jika:
- Tim memiliki anggaran hardware Rp 7-8 Juta
- Prioritas utama adalah **keandalan sistem di lapangan**
- Tim ingin fokus koding fitur (Exercise Engine, Dashboard), bukan debugging masalah jaringan
- Produk ingin bisa berjalan di **HP biasa** (tanpa Laptop GPU)

### ✅ Pertahankan Rancangan v1 (4x XIAO ESP32-S3) jika:
- Anggaran hardware MAKSIMAL Rp 4,5 Juta dan tidak bisa dinaikkan
- Coverage 360° adalah keharusan mutlak
- Tim bersedia menghabiskan **60-70% waktu** untuk mengatasi masalah teknis jaringan dan sinkronisasi video

---

## 12. Langkah Selanjutnya

1. **Keputusan Tim:** Diskusikan dokumen ini bersama tim (2 Teknisi, 2 Web Dev, 1 PM) dan pilih arsitektur final
2. **Revisi Proposal:** Setelah keputusan diambil, perbarui dokumen proposal resmi
3. **Fase Prototipe:** Mulai koding Exercise Engine menggunakan webcam Laptop (biaya Rp 0) untuk memvalidasi logika AI sebelum membeli hardware apapun
4. **Procurement:** Pesan hardware setelah prototipe webcam terbukti berhasil
