# Catatan Tambahan RAB dan Riset Teknis
*(Temuan Diskusi September 2026)*

Dokumen ini merangkum poin-poin krusial terkait Rencana Anggaran Biaya (RAB) dan klarifikasi teknis yang tidak secara eksplisit dicantumkan di Spesifikasi Utama, namun sangat penting untuk penyusunan proposal penelitian (Hibah Dosen) dan negosiasi.

---

## 1. Analisis Biaya Pengembangan Software (Jasa Engine)

### 1.1 Konteks Lisensi Software (100% Gratis)
Seluruh *stack* teknologi yang digunakan dalam proyek ini bersifat Open-Source. Klien tidak perlu membayar biaya lisensi, royalti, atau langganan API cloud.
* **MediaPipe BlazePose & OpenCV**: Lisensi Apache 2.0 (Gratis untuk komersial).
* **Python, FastAPI, C++, Arduino IDE**: Open Source (Gratis).
* Pemrosesan sepenuhnya berjalan di lokal (Edge Computing di laptop/PC), sehingga **bebas dari biaya server bulanan**.

### 1.2 RAB Software Khusus Riset Dosen (Engine Terminal-Based)
Karena proyek ini berbasis hibah penelitian dosen yang biasanya memiliki keterbatasan pagu anggaran, dan sistem hanya berjalan di terminal (tanpa pembuatan UI/UX Web atau Mobile App), maka estimasi biaya untuk seorang *Computer Vision Engineer* (selama 1 - 1.5 bulan) adalah sebagai berikut:

| Tahap Pengembangan Engine Khusus | Estimasi Biaya |
|---|---|
| Pengembangan Skrip Kalibrasi & Rekonstruksi 3D Multi-Kamera | Rp 5.000.000 |
| Logika Pose Estimation & Hitungan Olahraga (5 Gerakan) | Rp 5.000.000 |
| Firmware Kamera IoT & Deteksi Sensor Warna (HSV) | Rp 3.000.000 |
| Pengujian Akurasi Algoritma & Debugging Terminal | Rp 2.000.000 |
| **TOTAL BIAYA ENGINE (Tanpa UI/UX)** | **Rp 15.000.000** |

*Catatan: Jika di kemudian hari sistem ingin dibuatkan Web Dashboard komersial dengan UI/UX premium (tanpa Figma mockup amatir, melainkan Direct-to-Code CSS), maka biaya pengembangan penuh akan berkisar di Rp 50.000.000 (sesuai standar industri).*

---

## 2. Revisi dan Klarifikasi Hardware Kamera

### 2.1 Kekurangan pada RAB Hardware Awal
Hardware list yang ada sudah 95% benar, namun **wajib ditambahkan budget Casing 3D Printed** (sekitar Rp 100.000 - Rp 150.000 untuk 4 unit). 
Papan sirkuit XIAO ESP32-S3 Sense berbentuk telanjang (PCB murni) dan tidak memiliki lubang sekrup untuk tripod (1/4 inch thread). Tanpa casing, kamera tidak akan bisa dipasang ke tripod.

### 2.2 Fakta Penjualan XIAO ESP32-S3 Sense
* Modul XIAO ESP32-S3 "Sense" **selalu dijual sepaket (bundled) dengan lensa OV2640**. Anda tidak bisa membeli papan konektor kameranya saja tanpa lensa.
* Jika Anda bersikeras ingin memakai lensa **OV5640**, Anda tetap harus membeli paket Sense (mendapat OV2640), menyingkirkan lensa tersebut, dan membeli lensa OV5640 secara terpisah, yang mana ini adalah pemborosan biaya.

### 2.3 Mengapa Lensa OV2640 Justru Lebih Ideal dari OV5640?
Kegagalan membaca QR Code dengan lensa OV2640 di masa lalu disebabkan oleh kebutuhan fokus jarak sangat dekat (*macro focus*). Untuk *Pose Estimation*, OV2640 justru jauh lebih optimal karena:
1. **Titik Fokus:** Jarak subjek olahraga adalah 1.5 hingga 3 meter, yang merupakan *sweet spot* tertajam untuk lensa *fixed focus* OV2640.
2. **Keterbatasan AI:** Sebesar apapun resolusi sensornya, arsitektur *neural network* MediaPipe akan meremas (*downscale*) input gambar menjadi bujur sangkar **256x256 pixel**. Lensa OV5640 tidak akan memberikan detail lebih untuk MediaPipe.
3. **Bottleneck Bandwidth (Penting!):** Kita melakukan streaming 4 kamera serentak via WiFi. Memaksakan resolusi dari OV5640 akan menyebabkan lag, delay, dan *frame drop* parah. Resolusi VGA (640x480) dari OV2640 pada 30 FPS adalah titik seimbang sempurna antara kualitas gambar dan kelancaran jaringan WiFi lokal.

### 2.4 Mengapa XIAO S3 Berbeda dengan ESP32-CAM Lama?
Jika ESP32-CAM lawas (AI-Thinker) menghasilkan gambar yang sangat buruk (mirip kamera HP lawas) penuh *noise* dan tersendat, XIAO ESP32-S3 Sense memberikan hasil yang sangat bersih meskipun menggunakan sensor OV2640 yang sama. Alasannya:
* **Chip Lebih Cepat:** Chip S3 memiliki instruksi komputasi Vektor untuk memproses kompresi JPEG tanpa ngadat.
* **PSRAM Octal-SPI:** Kecepatan dan kapasitas memori jauh lebih tinggi, menghilangkan masalah *frame tearing*.
* **Antena Eksternal (U.FL):** Sinyal WiFi jauh lebih kuat dibanding antena internal murahan, sehingga data gambar tidak rusak di tengah transmisi.
* **Kelistrikan Stabil:** Komponen kelistrikan yang bersih pada board Seeed Studio menghilangkan bintik-bintik *noise* pada sensor gambar.
