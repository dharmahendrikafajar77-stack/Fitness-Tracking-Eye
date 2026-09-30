PROPOSAL
Pengembangan Sistem Fitness Tracking Eye Terintegrasi
HowArts Technology
Padang, September 2026
BAB 1 RINGKASAN EKSEKUTIF & LATAR BELAKANG
1.1 Ringkasan Eksekutif
Proposal ini memaparkan rancangan komprehensif pengembangan Fitness Tracking Eye, sebuah sistem 
motion capture multi-camera wireless
 yang mengintegrasikan perangkat keras Internet of Things (IoT), platform 
computer vision
 berbasis AI, 
real-time Web Dashboard
, dan 
Mobile Companion Application
, didukung infrastruktur Cloud Server mandiri. Sistem ini dirancang khusus untuk mengotomasi proses pemantauan latihan fitness mendeteksi jenis exercise, menghitung repetisi, dan menganalisis kualitas form gerakan secara 
real-time
 
guna memberikan feedback objektif, terstandarisasi, dan portabel kepada pengguna maupun pelatih.
Sistem ini dibangun di atas fondasi teknologi mutakhir:
Empat unit mikrokontroler kamera XIAO ESP32-S3 Sense
 dengan 
custom 3D printed enclosure
 yang membentuk 
coverage
 360 derajat di sekitar area latihan.
Engine pose estimation MediaPipe BlazePose
 untuk mengekstrak 33 titik 
keypoints
 3D tubuh pengguna secara presisi.
Exercise Engine berbasis State Machine & Triangulasi 3D
 untuk mendeteksi repetisi dan kualitas form pada lima jenis exercise target: 
Push Up, Pull Up, Sit Up, Squat Jump, dan Vertical Jump
.
Integrated Platform Ecosystem:
 Web Dashboard interaktif untuk visualisasi layar lebar, Mobile App untuk kontrol cepat dan riwayat latihan, serta Cloud Server & Domain kustom selama 1 tahun penuh.
1.2 Latar Belakang & Urgensi Masalah
Form gerakan yang benar merupakan faktor penentu utama efektivitas dan keamanan latihan fitness. Form yang buruk tidak hanya mengurangi hasil latihan, 
tetapi juga meningkatkan risiko cedera otot dan sendi secara signifikan. Sayangnya, akses terhadap 
personal trainer
 yang mampu memantau dan mengoreksi form secara 
real-time
 masih terbatas dan berbiaya tinggi.
Teknologi fitness tracking yang tersedia di pasaran saat ini memiliki kelemahan:
a. Keterbatasan Sensor Wearable: Smartwatch hanya mengandalkan 
accelerometer
 untuk menghitung repetisi tanpa kemampuan menganalisis kualitas form dan postur sendi.
b. Kelemahan Single Camera: Solusi kamera tunggal sangat rentan terhadap masalah 
occlusion
 (bagian tubuh tertutup sudut kamera) yang menyebabkan hilangnya pelacakan sendi.
c. Biaya Solusi Komersial Sangat Tinggi: Produk premium komersial dibanderol puluhan juta rupiah ditambah biaya langganan bulanan (
recurring fee
) yang memberatkan.
d. Tidak Portabel: Mayoritas perangkat premium merupakan instalasi permanen di satu tempat.
Fitness Tracking Eye
 menghadirkan solusi terlengkap: portabel dalam satu backpack, multi-sudut 360°, ekosistem Web & Mobile App terintegrasi, Cloud server mandiri, dan efisiensi biaya tanpa biaya langganan aplikasi bulanan.
BAB 2
 
DESKRIPSI & ALUR KERJA SISTEM
2.1 Deskripsi Umum Ekosistem Sistem
Fitness Tracking Eye dirancang sebagai satu kesatuan ekosistem teknologi terpadu yang menghubungkan:
Modul IoT Portable Kit (Standar Hardware Proposal 2):
 4 unit Camera Node XIAO ESP32-S3 Sense (lensa OV5640 5MP) dalam 
casing 3D print custom
, mini tripod, dedicated WiFi router 5GHz, dan 
Tracking Band
 neon.
Core Exercise & AI Vision Engine:
 Backend komputasi yang menjalankan pose estimation (MediaPipe BlazePose 33 titik 3D), rekonstruksi 3D multi-kamera (Triangulasi OpenCV DLT), Kalman filter, dan algoritma 
state machine
.
Web Dashboard Real-Time:
 Antarmuka layar lebar berbasis WebSocket untuk 
skeletal overlay
, 
rep counter
, 
form score gauge (0–100%)
, dan analitik sesi.
Mobile Companion Application (Android / iOS):
 Aplikasi mobile untuk kontrol sesi latihan, panduan penempatan kamera/band, profil atlet, dan rekaman riwayat performa.
Infrastruktur Cloud Server & Domain (1 Tahun Penuh):
 VPS Cloud berkecepatan tinggi, Domain kustom (.com/.tech), managed SSL, dan database sinkronisasi data online.
2.2 Alur Kerja Otomatis (5 Langkah End-to-End)
Langkah
Nama Tahapan
Deskripsi Operasional
1
Setup & Kalibrasi Kamera
Pengguna menempatkan 4 kamera mini tripod di sekeliling area latihan dan terhubung ke router WiFi 5GHz. Kalibrasi ChArUco board dilakukan kilat (< 15 menit total setup).
2
Pemilihan Exercise & Tracking Band
Pengguna memilih menu exercise di Web Dashboard atau Mobile App. Sistem memandu pemasangan Tracking Band neon (30–60 detik).
3
Streaming & Rekonstruksi 3D
Keempat kamera menyiarkan MJPEG stream via WiFi ke server pemrosesan. MediaPipe mengekstrak 33 landmark per sudut, lalu direkonstruksi menjadi posisi koordinat 3D nyata via triangulasi multi-view.
4
Deteksi Repetisi & Form Scoring
Exercise Engine menghitung dinamika sudut sendi (
joint angles
), mendeteksi repetisi valid via state machine, dan mengevaluasi kualitas postur serta sudut kritis.
5
Visualisasi Real-Time & Sinkronisasi Cloud
Hasil repetisi, skor form, dan grafik analitik langsung tampil di Web Dashboard / Mobile App secara instan (~150–300 ms), serta tersimpan otomatis ke Cloud Database.
BAB 3 ARSITEKTUR SISTEM (TOPOLOGI)
3.1 Diagram Arsitektur Sistem
Berikut representasi aliran data end-to-end dari lapisan perangkat keras (
hardware
), pemrosesan lokal AI, hingga lapisan layanan cloud dan aplikasi antarmuka:
Gambar Topologi Arsitektur
3.2 Penjelasan
 Alur Teknis
4x Camera Nodes: Video VGA (640x480) 15–20 FPS dikompresi MJPEG (
latency: 30–50 ms
).
Dedicated WiFi 5GHz: Throughput stabil 10–12 Mbps tanpa interferensi publik (
latency: 20–50 ms
).
MediaPipe BlazePose & 3D Triangulation: Ekstraksi 33 keypoints 3D paralel & Kalman Filter (
latency: 50–100 ms
).
Exercise Engine & WebSocket Push: Evaluasi state machine & push JSON real-time (
latency: 20–50 ms
).
Total Latency Sistem: 150 – 300 ms (sangat mulus dan responsif).
BAB 4 KEBUTUHAN TEKNIS (HARDWARE DAN SOFTWARE)
4.1 Kebutuhan Hardware (1 Unit Prototipe)
Spesifikasi komponen perangkat keras yang dibutuhkan untuk membangun satu unit prototipe fungsional sistem Fitness Tracking Eye:
Komponen / Perangkat
Spesifikasi & Fungsi
4x XIAO ESP32-S3 Sense + OV5640
Unit kamera wireless ultra-compact (Xtensa LX7 dual-core 240MHz, 8MB PSRAM, kamera 5MP).
4x Custom 3D Printed Casing
Enclosure presisi berbahan PETG/PLA dengan ventilasi panas & dudukan thread 1/4" tripod.
4x Mini Tripod Foldable
Penyangga kamera fleksibel yang kokoh, stabil, dan dapat dilipat untuk mobilitas.
1x Travel WiFi Router 5GHz
Jaringan nirkabel dedicated berkecepatan tinggi tanpa hambatan traffic internet luar.
4x Power Supply System
Opsi adapter USB-C / powerbank mini untuk fleksibilitas operasional indoor & outdoor.
1x ChArUco Calibration Board (A3)
Papan kalibrasi presisi pada material rigid untuk kalibrasi multi-kamera instan.
1 Set Tracking Band (5 pcs, 3 ukuran)
Gelang neon repositionable tahan keringat (Size S, M, L) untuk akurasi pelacakan sendi.
4.2 Software
 
& Cloud Technology
 Stack
Tumpukan teknologi perangkat lunak yang digunakan dalam pengembangan sistem ini 
dipilih berdasarkan kriteria akurasi, performa, dan kemudahan pemeliharaan jangka panjang:
Komponen Teknologi
Deskripsi & Peran Arsitektur
MediaPipe BlazePose (Google)
Engine pose estimation AI tercanggih untuk ekstraksi 33 keypoints 3D real-time.
OpenCV
Pemrosesan citra, kalibrasi multi-kamera, dan algoritma triangulasi 3D Direct Linear Transform (DLT).
Python (FastAPI Backend)
High-performance backend server yang menjalankan Exercise Engine dan endpoint WebSocket.
Modern Web (
Nextjs
)
Antarmuka dashboard responsif dan interaktif untuk visualisasi layar lebar.
Mobile App (Flutter / React Native)
Aplikasi mobile Android/iOS untuk monitoring sesi, profil atlet, dan kontrol cepat.
Cloud VPS & Custom Domain (1 Thn)
Infrastruktur server daring dedicated, domain kustom, SSL, dan penyimpanan database cloud.
NumPy, SciPy & filterpy
Perhitungan vektor sudut sendi, signal processing, dan implementasi Kalman smoothing.
BAB 5 KEUNGGULAN SISTEM
5.1 Efisiensi Biaya Berbasis Intellectual Property (IP Scaling)
Keunggulan terbesar sistem ini terletak pada model investasi berbasis 
Intellectual Property (IP). Biaya rekayasa perangkat lunak (
software engine, mobile app, dashboard, cloud setup
) hanya perlu dibangun satu kali. Setelah software selesai, penambahan unit alat baru (unit 2, 3, dst.) hanya membutuhkan biaya hardware saja tanpa biaya software ulang.
5.2 Opsi Konfigurasi Kit Perangkat (Skalabilitas Produksi)
Sistem dirancang modular sehingga unit hardware tambahan dapat dipesan dalam 3 tingkatan kit sesuai kebutuhan operasional klien:
Konfigurasi Kit
Peruntukan & Skenario
Fitur Hardware & Daya
Estimasi Biaya Hardware/Unit
1. Basic Studio Kit
Gym / Studio Indoor (Fixed Setup)
4x Kamera ESP32-S3 + Casing 3D + Tripod + Router 5GHz + USB-C Adapter (Markerless AI).
Rp 2.800.000 – Rp 3.000.000
2. Portable Tracking Kit
Pelatih Mobile / Outdoor Event
Basic Studio Kit + 1 Set Tracking Band Neon (5 pcs) + Powerbank Kit + Tas Ransel Portable.
Rp 3.500.000 – Rp 3.800.000
3. Pro Kit (Max Accuracy)
 
(Standar Prototipe)
Analisis Atlet & High-Performance
Portable Kit + Dual IMU 6-axis Wristband + Baterai LiPo + Heavy Duty Mounting Bracket (Akurasi 95–98%).
Rp 4.200.000 – Rp 4.500.000
(BOM Riil: 
Rp 4.270.000
)
BAB 
6
 
SPESIFIKASI DETEKSI PER EXERCISE
Sistem mendeteksi repetisi dan fase gerakan pada masing-m
asing dari lima exercise target menggunakan pendekatan state machine yang menghitung sudut sendi (joint angle) dari keypoints tubuh. Setiap keputusan counting bersifat transparan dan dapat ditelusuri, dengan akurasi 90
-
95% pada fase awal 
implementasi. Berikut ringkasan state, transisi, dan threshold kunci yang digunakan untuk setiap exercise.
6.1 Ringkasan State Machine per Exercise
Exercise
State
Threshold Kunci
Fokus Form Analysis
Push Up
UP, DOWN
DOWN: elbow angle < 100°. UP: elbow angle > 160°.
Kelurusan tulang belakang (hip sag/pike), kedalaman dada.
Pull Up
HANG, UP
UP: dagu melewati bar. HANG: elbow angle > 160°.
Full extension lengan, minimalisasi ayunan tubuh (
kipping
).
Sit Up
DOWN, UP
UP: hip angle < 70°. DOWN: hip angle > 140°.
Rentang fleksi trunk, posisi punggung saat menyentuh matras.
Squat Jump
STAND, SQUAT, JUMP, LAND
SQUAT: knee angle < 90°. JUMP–LAND: displacement ankle vertikal.
Kedalaman squat ($<90^\circ$), simetri lutut, soft landing mechanics.
Vertical Jump
STAND, CROUCH, JUMP, LAND
Diukur dari displacement hip/ankle vertikal maksimum.
Pengukuran estimasi tinggi lompatan vertikal (
flight time
).
6.2 Teknik Anti-False Counting
Untuk mencegah kesalahan penghitungan repetisi, sistem 
menerapkan hysteresis thresholding (ambang berbeda untuk transisi naik dan turun), minimum transition time antar state, moving average smoothing pada nilai sudut sendi, serta visibility check untuk memastikan keypoints yang digunakan benar-benar terlihat o
leh kamera sebelum dihitung.
BAB 7 ANALISIS RISIKO
7.1 Risiko Teknis Utama
Berikut adalah risiko teknis utama yang teridentifikasi dalam pengembangan dan pengoperasian sistem beserta strategi mitigasinya.
Risiko Teknis & Operasional
Tingkat
Strategi Mitigasi Terintegrasi
Occlusion (Tubuh Tertutup Sudut)
Sedang
Sudut pandang 360° dari 4 kamera + Tracking Band neon sebagai verifikasi multi-view.
Instabilitas Jaringan WiFi
Rendah
Menggunakan dedicated router WiFi 5GHz terisolasi dari traffic publik + buffer stream.
Variasi Cahaya Lingkungan
Sedang
Manual exposure control
, 
adaptive HSV thresholding
, dan kalibrasi cepat awal.
Keamanan Data & Server
Rendah
Cloud VPS dengan enkripsi SSL/TLS, otentikasi JWT token, dan backup harian otomatis.
7.2 Risiko Non-Teknis
Keterlambatan pengiriman komponen dimitigasi melalui procurement di awal proyek dan identifikasi vendor alternatif. Potensi penolakan pengguna terhadap pemakaian Tracking Band 
dimitigasi dengan menjadikannya opsi tambahan
 
sistem tetap berfungsi tanpa band meski dengan akurasi yang sedikit lebih rendah.
BAB 8 POSISI KOMPETITIF
8.1 Perbandingan dengan Produk Existing
Berikut perbandingan Fitness Tracking Eye dengan beberapa produ
k fitness tracking komersial yang tersedia di pasaran saat ini.
Solusi / Produk
Teknologi Sensor
Estimasi Harga Perangkat
Biaya Langganan
Kelemahan Utama
Tempo Studio
3D Time-of-Flight + AI
Rp 30 – 75 Juta
Rp 585.000 / bln
Sangat mahal, instalasi fixed indoor.
Lululemon Mirror
Single Camera + Coach
± Rp 22,5 Juta
Rp 585.000 / bln
Manual coach, bukan AI otomatis 360°.
Tonal
Motor Resistance Sensor
± Rp 52,5 Juta
Rp 735.000 / bln
Permanen di dinding, tidak portable.
Fitness Tracking Eye
4x AI Camera + Web + Mobile
Rp 2,8 – 4,2 Jt (Unit Tambahan)
Rp 0 (Termasuk Server 1 Thn)
Portabel, 360°, Web & App, Terjangkau
8.2 Diferensiasi Utama
Coverage 360° dari 4 kamera vs. satu sensor/kamera pada kompetitor.
Biaya jauh lebih rendah tanpa biaya 
langganan bulanan.
Modular dan upgradeable mulai dari kamera saja, tambahkan aksesoris kapan saja.
Portable dalam satu backpack, sementara kompetitor umumnya instalasi permanen.
BAB 9 RINCIAN ANGGARAN BIAYA (RAB)
9.1 Tabel Rincian Anggaran Pengembangan Sistem Lengkap
Kategori / Komponen Pekerjaan
Deskripsi & Deliverable
Nilai Investasi (Rp)
A. PERANGKAT KERAS (HARDWARE & PORTABLE KIT)
4.270.000
4x XIAO ESP32-S3 Sense + Kamera OV5640
Modul mikrokontroler kamera 5MP (4 unit @ Rp 225.000)
900.000
4x Mini Tripod Foldable
Penyangga kamera portabel fleksibel (4 unit @ Rp 120.000)
480.000
1x Travel WiFi Router 5GHz
Jaringan nirkabel dedicated lokal kecepatan tinggi
600.000
4x USB-C Power Adapter & Kabel Set
Sistem daya operasional kamera (4 unit @ Rp 56.250)
225.000
4x Custom 3D Printed Casing
Casing presisi tahan panas kamera (4 unit @ Rp 150.000)
600.000
4x Enclosure Mounting Bracket
Bracket dudukan & pengaman tripod (4 unit @ Rp 200.000)
800.000
2x Sensor IMU BMI270 Breakout Board
Modul sensor inersial 6-axis gerak cepat (2 unit @ Rp 120.000)
240.000
2x Baterai LiPo IMU Wristband
Sumber daya mandiri wristband (2 unit @ Rp 112.500)
225.000
1 Set Tracking Band Neon Velcro (5 pcs)
Gelang neon identifikasi sendi 3 ukuran tahan keringat
200.000
B. PENGEMBANGAN SISTEM, PLATFORM & CLOUD
21.730.000
Core AI Vision & 5 Exercise Motion Engine
Integrasi MediaPipe 33-point 3D, triangulasi multi-kamera, firmware IoT, state machine 5 exercise & form scoring real-time
9.500.000
Web Dashboard & Mobile Application (Android/iOS)
Desain UI/UX Figma, Web Dashboard WebSocket real-time, Mobile App atlet, skeletal visualizer & analitik performa
7.500.000
Infrastruktur Cloud Server & Domain (1 Tahun)
Cloud VPS Dedicated High-Performance, Domain Kustom (.com/.tech), Managed SSL & Cloud Database Sync
2.000.000
Integrasi Sistem, QA, Testing Lapangan & UAT
Pengujian end-to-end (Hardware + Web + App + Cloud), validasi lapangan indoor/outdoor, onboarding & manual book
2.730.000
TOTAL KESELURUHAN ANGGARAN PROYEK
Rp 26.000.000
BAB 10
 -
 JADWAL PELAKSANAAN (
60
 HARI)
10.1 Roadmap & Fase Pelaksanaan (8 Minggu Kerja)
Fase
Periode
Tahapan
Deliverable Kunci
FASE 1
Minggu 1–2
(Hari 1–14)
Desain UI/UX, Hardware & PoC
Finalisasi UI Figma (Web & App), perakitan hardware, PoC pose estimation single-cam, & Exercise Engine dasar.
FASE 2
Minggu 3–4
(Hari 15–28)
All 5 Exercise Engines & Firmware
Penyelesaian algoritma seluruh 5 exercise, form scoring system, firmware 4 kamera ESP32-S3, & struktur Mobile App.
FASE 3
Minggu 5–6
(Hari 29–42)
3D Triangulation, Band & Cloud
Kalibrasi ChArUco, triangulasi 3D, modul HSV Tracking Band, setup VPS Cloud Server, Domain & Database.
FASE 4
Minggu 7–8
(Hari 43–60)
Web/Mobile Integration, QA & UAT
Integrasi penuh Web Dashboard & Mobile App real-time, pengujian lapangan (indoor/outdoor), UAT resmi, & Handover.
10.2 Masa Stabilisasi & Garansi
Masa Stabilisasi & Buffer (7–10 Hari Kalender)
Garansi Pemeliharaan Pasca-Handover (6 Bulan Penuh)
Alokasi waktu khusus pasca-Fase 4 untuk adaptasi lingkungan operasional riil klien, fine-tuning threshold, dan penyesuaian minor.
Layanan purna jual gratis selama 6 bulan mencakup pemeliharaan software/app, perbaikan 
bug
, kalibrasi ulang, dan konsultasi teknis.
BAB 11 GARANSI  & KONTROL KUALITAS
11.1 Garansi & Layanan Purna Jual
HowArts Technology berkomitmen memberikan jaminan kualitas terbaik:
Garansi Software & Aplikasi 6 Bulan: Perbaikan bebas biaya terhadap setiap 
error
, 
bug
, atau isu teknis pada Web Dashboard maupun Mobile App.
Dukungan Teknis Prioritas: Layanan bantuan teknis melalui saluran komunikasi prioritas (WhatsApp/Email/Remote).
11.2 Standar Kontrol Kualitas (QA Standards)
Akurasi Rep Counting: Target margin of error < 5% pada seluruh 5 jenis exercise.
Reprojection Error Kalibrasi: Nilai error reprojection 
<5% 
 pada triangulasi 3D.
Konektivitas & Load Testing: Pengujian 
continuous streaming
 4 kamera selama minimal 60 menit nonstop tanpa gangguan.
User Acceptance Testing (UAT): Verifikasi fungsi menyeluruh bersama pihak klien sebelum serah terima.
BAB 12
 
SKEMA DAN TERMIN PEMBAYARAN
12.1 Rincian Tahapan Pembayaran (Milestone-Based)
Pembayaran dilakukan secara bertahap dalam 
tiga (3) termin
 yang mengikat pada pencapaian 
milestone
 yang terukur secara transparan:
TERMIN I
 
Down Payment 30% (Rp 7.800.000)
Waktu:
 Saat penandatanganan Surat Perintah Kerja (SPK) / Kontrak Kerja Sama (Hari ke-1).
Peruntukan:
 Inisiasi proyek, pengadaan seluruh unit komponen hardware, perancangan UI/UX Figma Web & Mobile, dan setup lingkungan dev.
TERMIN II Milestone Fase 2 (Akhir Bulan ke-1) 30% (Rp 7.800.000)
Waktu:
 Setelah penyelesaian Fase 2 (Hari ke-28: Desain Figma disetujui, Core 5 Exercise Engine tervalidasi, dan firmware 4-kamera teruji).
Peruntukan:
 Rekonstruksi 3D multi-kamera, integrasi Tracking Band, setup Cloud VPS Server & Domain, dan pengembangan Mobile App.
TERMIN III Pelunasan (Akhir Bulan ke-2) 40% (Rp 10.400.000)
Waktu:
 Setelah seluruh sistem selesai (Hari ke-60: Web & Mobile App terintegrasi dengan Cloud Server, UAT berhasil disetujui, dan serah terima resmi).
12.2 Ringkasan Jadwal Pembayaran
Tahapan Termin
Persentase
Nilai Pembayaran (IDR)
Pemicu Pembayaran (Trigger Milestone)
Termin I (DP)
30%
Rp 7.800.000
Penandatanganan SPK / Kontrak Kerja Sama (Hari 1)
Termin II
30%
Rp 7.800.000
Milestone Fase 2 diverifikasi & disetujui (Hari 28 / Bulan 1)
Termin III (Pelunasan)
40%
Rp 10.400.000
Final UAT, Serah Terima Sistem, Web/App & Cloud (Hari 60 / Bulan 2)
TOTAL
100%
Rp 26.000.000
3 Tahapan Pembayaran (2 Bulan)
12.3 Lembar Pengesahan Proposal
Dibuat dan disetujui di 
Padang
, pada tanggal 
September 2026
.
PIHAK KLIEN
PIHAK PENGEMBANG
Direktur/kepala divisi