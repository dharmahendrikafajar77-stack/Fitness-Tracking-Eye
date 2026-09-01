SPECIFICATION DOCUMENT
FITNESS TRACKING EYE
Multi-Camera Wireless Motion Capture System untuk Pelacakan dan Analisis Gerakan Fitness

Versi Dokumen: 1.0
Tanggal: 1 September 2026
Status: Final Research — Siap untuk Pengembangan Proposal
Klasifikasi: Internal — Untuk Tim Proposal


DAFTAR ISI

BAB 1 — RINGKASAN EKSEKUTIF
BAB 2 — LATAR BELAKANG DAN KEBUTUHAN PROYEK
BAB 3 — RUANG LINGKUP PROYEK
BAB 4 — ARSITEKTUR SISTEM
BAB 5 — KOMPONEN HARDWARE: MODUL KAMERA
BAB 6 — DESAIN FISIK PERANGKAT
BAB 7 — KOMPONEN SOFTWARE: POSE ESTIMATION ENGINE
BAB 8 — STRATEGI PEMROSESAN DATA
BAB 9 — PROTOKOL KOMUNIKASI DAN JARINGAN
BAB 10 — SINKRONISASI MULTI-KAMERA
BAB 11 — REKONSTRUKSI 3D
BAB 12 — KALIBRASI KAMERA
BAB 13 — ALGORITMA DETEKSI EXERCISE
BAB 14 — TRACKING BAND SYSTEM
BAB 15 — SENSOR IMU TAMBAHAN (OPSIONAL)
BAB 16 — PLATFORM DAN ANTARMUKA PENGGUNA
BAB 17 — SPESIFIKASI PER EXERCISE
BAB 18 — OPERASIONAL: INDOOR DAN OUTDOOR
BAB 19 — ANALISIS RISIKO DAN MITIGASI
BAB 20 — ANALISIS KOMPETITOR
BAB 21 — OPSI PAKET UNTUK KLIEN
BAB 22 — ESTIMASI BIAYA
BAB 23 — ROADMAP PENGEMBANGAN
BAB 24 — VERIFIKASI DAN PENGUJIAN
BAB 25 — REFERENSI AKADEMIK DAN TEKNIS
BAB 26 — LAMPIRAN
BAB 27 — REKOMENDASI KONFIGURASI FINAL UNTUK KLIEN


================================================================================
BAB 1 — RINGKASAN EKSEKUTIF
================================================================================

1.1 Tentang Proyek

Fitness Tracking Eye adalah sistem pelacakan fitness yang menggunakan teknologi motion capture berbasis multiple wireless camera untuk mendeteksi, menghitung repetisi, dan menganalisis form gerakan dari pengguna. Sistem ini dirancang untuk satu pengguna (single user), bersifat portable sehingga dapat dibawa dan di-setup di lokasi yang berbeda-beda, serta dioptimalkan untuk penggunaan indoor dengan kemampuan untuk tetap berfungsi di outdoor.

Sistem ini mampu memantau lima jenis exercise yaitu Push Up, Pull Up, Sit Up, Squat Jump, dan Vertical Jump. Untuk setiap exercise, sistem tidak hanya menghitung jumlah repetisi tetapi juga menganalisis kualitas form gerakan dan memberikan metrik performa yang relevan.

1.2 Tujuan Utama

Tujuan pertama adalah membangun sistem multi-kamera wireless yang mampu menangkap gerakan pengguna dari berbagai sudut secara real-time. Tujuan kedua adalah mengimplementasikan algoritma pose estimation dan exercise detection yang akurat untuk kelima exercise target. Tujuan ketiga adalah menyediakan feedback real-time mengenai jumlah repetisi dan kualitas form gerakan. Tujuan keempat adalah memastikan sistem bersifat portable dan dapat di-setup dalam waktu kurang dari 15 menit di lokasi manapun.

1.3 Pendekatan Teknologi

Sistem menggunakan empat unit modul kamera berbasis mikrokontroler XIAO ESP32-S3 Sense yang ditempatkan di sekitar area latihan membentuk coverage 360 derajat. Keempat kamera ini mengirimkan video stream melalui jaringan WiFi ke satu laptop atau PC yang menjadi unit pemrosesan utama. Di laptop inilah semua proses pose estimation, rekonstruksi 3D, deteksi exercise, dan analisis form dilakukan.

Selain itu, sistem ini dilengkapi dengan inovasi berupa Tracking Band, yaitu gelang berwarna neon yang dipakai di beberapa titik tubuh untuk membantu identifikasi bagian tubuh dan meningkatkan akurasi deteksi. Tracking band ini terinspirasi dari teknologi motion capture yang digunakan dalam industri pembuatan film dan VFX, namun disederhanakan agar mudah digunakan oleh pengguna awam.

1.4 Constraint yang Ditetapkan

Proyek ini beroperasi dalam beberapa constraint penting. Pertama, sistem dirancang untuk single user saja, yaitu hanya satu orang yang di-track pada satu waktu. Kedua, sistem harus bersifat portable sehingga seluruh perangkat harus bisa dimuat dalam satu backpack dan di-setup dengan cepat di lokasi berbeda. Ketiga, sistem dioptimalkan untuk indoor namun harus tetap berfungsi di outdoor. Keempat, budget bersifat fleksibel dan tidak menjadi faktor eliminasi utama dalam pemilihan teknologi.


================================================================================
BAB 2 — LATAR BELAKANG DAN KEBUTUHAN PROYEK
================================================================================

2.1 Permasalahan yang Dihadapi

Dalam dunia fitness, kemampuan untuk melakukan exercise dengan form yang benar sangat penting. Form yang buruk tidak hanya mengurangi efektivitas latihan tetapi juga meningkatkan risiko cedera. Sayangnya, tidak semua orang memiliki akses ke personal trainer yang bisa memantau dan mengoreksi form mereka secara real-time.

Teknologi fitness tracking yang ada saat ini umumnya hanya berfokus pada counting berbasis akselerometer sederhana seperti yang ada di smartwatch, atau menggunakan single camera yang memiliki keterbatasan sudut pandang dan rentan terhadap masalah occlusion dimana bagian tubuh tertutupi dari sudut kamera.

2.2 Solusi yang Diusulkan

Fitness Tracking Eye menjawab permasalahan ini dengan menggabungkan beberapa teknologi. Multi-camera coverage dari empat sudut berbeda mengatasi masalah occlusion yang menjadi kelemahan utama single camera system. Pose estimation berbasis AI menggunakan MediaPipe BlazePose memberikan 33 keypoints 3D dari tubuh pengguna. Algoritma state machine dan joint angle calculation yang dikembangkan khusus untuk masing-masing dari lima exercise target memberikan deteksi yang spesifik dan akurat.

Yang membuat sistem ini unik adalah penambahan Tracking Band, sebuah konsep yang terinspirasi dari industri motion capture dalam pembuatan film VFX. Dalam industri film, aktor menggunakan bodysuit penuh yang dilengkapi marker reflektif. Konsep ini kami adaptasi menjadi gelang warna neon sederhana yang dipakai di beberapa titik tubuh kunci. Gelang ini membantu kamera dan software untuk lebih akurat mengidentifikasi bagian-bagian tubuh, terutama saat terjadi gerakan cepat atau occlusion.

2.3 Landscape Teknologi Saat Ini

Berdasarkan riset mendalam yang dilakukan, terdapat sepuluh pilar teknologi yang masing-masing memiliki beberapa opsi implementasi. Pilar-pilar tersebut meliputi Pose Estimation Engine, Hardware Kamera, Processing Strategy, Sensor Pendukung, Communication Protocol, Sinkronisasi Multi-Kamera, Metode 3D Reconstruction, Algoritma Exercise Detection, Platform dan Antarmuka Pengguna, serta Kalibrasi Kamera.

Setiap pilar telah dianalisis secara mendalam dengan mempertimbangkan akurasi, biaya, kompleksitas implementasi, scalability, dan kesesuaian dengan constraint proyek. Hasil analisis ini menghasilkan satu konfigurasi optimal yang disebut "Balanced Kit" yang menjadi acuan utama dalam dokumen spesifikasi ini.


================================================================================
BAB 3 — RUANG LINGKUP PROYEK
================================================================================

3.1 Yang Termasuk dalam Ruang Lingkup

Sistem multi-kamera wireless menggunakan empat unit modul kamera mikrokontroler XIAO ESP32-S3 Sense yang terhubung melalui WiFi ke satu unit pemrosesan utama berupa laptop atau PC. Pose estimation menggunakan MediaPipe BlazePose dengan 33 keypoints 3D. Deteksi dan counting otomatis untuk lima exercise yaitu Push Up, Pull Up, Sit Up, Squat Jump, dan Vertical Jump. Analisis form gerakan real-time dengan scoring dan feedback koreksi. Rekonstruksi 3D menggunakan multi-view triangulation dari empat kamera yang telah dikalibrasi. Tracking Band system berupa gelang berwarna neon yang bisa dipindah-pindah sesuai exercise untuk meningkatkan akurasi deteksi. Web Dashboard untuk menampilkan hasil tracking secara real-time. Kalibrasi kamera menggunakan ChArUco board. Portable kit yang muat dalam satu backpack.

3.2 Yang Tidak Termasuk dalam Ruang Lingkup Fase Pertama

Multi-user tracking yaitu tracking lebih dari satu orang secara bersamaan. Mobile application native untuk Android atau iOS. Machine learning classifier untuk exercise detection yang akan menjadi upgrade dari state machine di fase berikutnya. Force plate atau jump mat hardware. EMG sensor untuk analisis aktivasi otot. Cloud-based processing atau storage. Integrasi dengan platform fitness pihak ketiga seperti Strava atau Google Fit.

3.3 Target Exercise

Lima exercise yang menjadi target sistem ini dipilih karena mencakup berbagai jenis gerakan fundamental dalam fitness. Push Up mewakili gerakan dorong horizontal. Pull Up mewakili gerakan tarik vertikal. Sit Up mewakili gerakan fleksi trunk. Squat Jump mewakili gerakan eksplosif lower body dengan fase airborne. Vertical Jump mewakili gerakan lompatan vertikal maksimal.


================================================================================
BAB 4 — ARSITEKTUR SISTEM
================================================================================

4.1 Arsitektur Umum

Arsitektur sistem terdiri dari tiga tier utama. Tier pertama adalah Camera Node Layer yang terdiri dari empat unit XIAO ESP32-S3 Sense yang berfungsi sebagai mata sistem. Setiap camera node bertugas menangkap frame video dan mengkompresinya menjadi format JPEG, kemudian mengirimkannya sebagai MJPEG stream melalui WiFi. Camera node tidak melakukan processing apapun selain capture dan compress karena mikrokontroler tidak memiliki kemampuan komputasi untuk menjalankan pose estimation.

Tier kedua adalah Network Layer yang terdiri dari satu unit dedicated WiFi router 5GHz atau travel router yang menghubungkan keempat camera node dengan unit pemrosesan utama. Jaringan ini bersifat dedicated, artinya tidak digunakan untuk keperluan internet atau traffic lainnya, sehingga bandwidth sepenuhnya tersedia untuk streaming kamera.

Tier ketiga adalah Central Processing Layer yang merupakan satu unit laptop atau PC yang menjalankan seluruh pipeline pemrosesan. Pipeline ini dimulai dari menerima MJPEG stream dari keempat kamera, mendecode frame, menjalankan MediaPipe BlazePose untuk mengekstrak 33 keypoints 3D dari setiap frame setiap kamera, melakukan rekonstruksi 3D melalui triangulation dari multi-view, menjalankan algoritma exercise detection dan rep counting, melakukan form analysis dan scoring, hingga menampilkan hasilnya di web dashboard secara real-time.

4.2 Aliran Data

Aliran data dalam sistem dimulai dari camera node yang menangkap frame pada resolusi VGA yaitu 640 kali 480 piksel dengan frame rate 15 hingga 20 FPS. Frame ini dikompresi menjadi JPEG dengan quality setting 15 hingga 20, menghasilkan file berukuran sekitar 30 hingga 50 kilobyte per frame. Frame yang sudah dikompresi dikirim sebagai MJPEG stream melalui HTTP over WiFi 5GHz ke unit pemrosesan utama.

Di unit pemrosesan utama, setiap stream diterima oleh OpenCV menggunakan fungsi VideoCapture yang mengakses URL stream dari masing-masing camera node. Frame yang diterima di-decode dari JPEG ke format BGR, dikonversi ke RGB, lalu dikirim ke MediaPipe BlazePose untuk proses pose estimation. Hasilnya berupa 33 landmark coordinates dalam format 3D yang meliputi posisi x, y, z serta visibility score untuk setiap landmark.

Landmark dari keempat kamera kemudian diproses oleh modul rekonstruksi 3D yang melakukan triangulation untuk mendapatkan posisi 3D sebenarnya dari setiap sendi tubuh. Posisi 3D ini menjadi input bagi modul exercise detection yang menjalankan state machine dan menghitung sudut sendi untuk menentukan fase gerakan, menghitung repetisi, dan mengevaluasi kualitas form.

Hasil akhir berupa data repetisi, form score, dan metrik performa dikirim melalui WebSocket ke web dashboard yang menampilkannya secara real-time di browser.

4.3 Bandwidth dan Latency

Setiap camera node menghasilkan stream dengan bandwidth sekitar 2 hingga 3 Mbps pada setting resolusi VGA dan frame rate 15 hingga 20 FPS. Dengan empat kamera, total bandwidth yang dibutuhkan adalah sekitar 10 hingga 12 Mbps. Ini berada dalam kapasitas WiFi 5GHz yang umumnya mampu menyediakan throughput 50 Mbps atau lebih dalam kondisi baik.

Latency total dari capture hingga ditampilkan di dashboard diperkirakan berada di kisaran 150 hingga 300 milidetik. Ini terdiri dari latency capture dan compress di camera node sekitar 30 hingga 50 milidetik, latency network sekitar 20 hingga 50 milidetik, latency decode dan pose estimation sekitar 50 hingga 100 milidetik, serta latency exercise detection dan rendering sekitar 20 hingga 50 milidetik. Latency ini acceptable untuk fitness tracking karena gerakan exercise paling cepat seperti jump masih memiliki durasi lebih dari 200 milidetik.


================================================================================
BAB 5 — KOMPONEN HARDWARE: MODUL KAMERA
================================================================================

5.1 Pemilihan Hardware: XIAO ESP32-S3 Sense

Setelah mengevaluasi lima opsi hardware kamera yang meliputi ESP32-CAM AI-Thinker, XIAO ESP32-S3 Sense, Raspberry Pi 4 dengan Camera Module, Smartphone, dan IP Camera, keputusan jatuh pada XIAO ESP32-S3 Sense dari Seeed Studio sebagai camera node utama.

XIAO ESP32-S3 Sense dipilih sebagai satu-satunya opsi hardware kamera yang ditawarkan karena beberapa alasan fundamental. Opsi ini menggunakan mikrokontroler sebagai camera node yang sesuai dengan visi proyek, bukan Single Board Computer seperti Raspberry Pi maupun smartphone.

5.2 Spesifikasi Teknis XIAO ESP32-S3 Sense

Prosesor yang digunakan adalah ESP32-S3 dual-core Xtensa LX7 dengan clock speed 240MHz. Yang membedakan ESP32-S3 dari pendahulunya ESP32 adalah kehadiran vector instructions yang memberikan akselerasi hingga 30 kali lipat untuk operasi AI dan machine learning. Meskipun dalam arsitektur ini camera node tidak menjalankan pose estimation, vector instructions ini memberikan potensi untuk future upgrade dimana pre-processing ringan bisa dilakukan di edge.

Memori yang tersedia meliputi 8MB PSRAM dan 8MB Flash. PSRAM berukuran dua kali lipat dari ESP32-CAM yang hanya memiliki 4MB. Kapasitas PSRAM yang lebih besar ini krusial untuk buffering frame di resolusi tinggi dan mencegah frame drop yang sering terjadi pada ESP32-CAM karena keterbatasan buffer.

Modul kamera default adalah OV2640 dengan resolusi maksimal 2 megapiksel yaitu 1600 kali 1200 piksel. Namun board ini juga mendukung sensor OV5640 dengan resolusi 5 megapiksel jika diperlukan upgrade kualitas gambar di masa depan. Untuk keperluan pose estimation, resolusi VGA yaitu 640 kali 480 piksel sudah lebih dari cukup dan merupakan sweet spot antara kualitas dan bandwidth.

Konektivitas WiFi menggunakan standar 802.11 b/g/n pada frekuensi 2.4GHz. WiFi pada ESP32-S3 diketahui lebih stabil dibandingkan ESP32 original berkat perbaikan pada firmware dan stack jaringan. Board ini juga mendukung Bluetooth 5.0 LE yang bisa dimanfaatkan untuk konfigurasi awal atau komunikasi dengan sensor IMU.

Form factor XIAO ESP32-S3 Sense sangat compact dengan dimensi hanya 21 kali 17.5 milimeter, menjadikannya sekitar 60 persen lebih kecil dari ESP32-CAM yang berukuran 27 kali 40.5 milimeter. Ukuran yang sangat kecil ini memudahkan mounting dan meminimalkan visual footprint saat dipasang di mini tripod.

5.3 Alasan Tidak Memilih ESP32-CAM

ESP32-CAM dari AI-Thinker pernah menjadi standard untuk proyek kamera berbasis mikrokontroler, namun di tahun 2025 hingga 2026 sudah dianggap sebagai produk legacy. Perbedaan utama terletak pada prosesor dimana ESP32-CAM menggunakan ESP32 tanpa vector instructions sementara XIAO ESP32-S3 Sense menggunakan ESP32-S3 dengan vector instructions. PSRAM pada ESP32-CAM hanya 4MB dibandingkan 8MB pada XIAO ESP32-S3 Sense. Stabilitas WiFi ESP32-CAM dikenal bermasalah terutama saat multi-stream, sementara ESP32-S3 lebih stabil. Form factor ESP32-CAM lebih besar. Selisih harga hanya sekitar Rp 120.000 per unit atau Rp 480.000 untuk empat unit, yang sangat worth it mengingat peningkatan signifikan di semua aspek.

5.4 Alasan Tidak Memilih Raspberry Pi

Raspberry Pi 4 atau 5 dengan Camera Module sebenarnya merupakan opsi yang secara teknis lebih powerful karena bisa menjalankan edge processing dengan MediaPipe di setiap node. Namun opsi ini tidak dipilih karena beberapa alasan. Pertama, biaya empat unit Raspberry Pi 4 dengan Camera Module berkisar Rp 3.900.000 hingga Rp 4.800.000, jauh lebih mahal dari empat unit XIAO ESP32-S3 Sense yang hanya sekitar Rp 780.000 hingga Rp 900.000. Kedua, visi proyek ini adalah menggunakan mikrokontroler dan modul kamera, bukan Single Board Computer. Ketiga, konsumsi daya Raspberry Pi jauh lebih tinggi yaitu 6 hingga 12 watt per unit dibandingkan ESP32-S3 yang hanya sekitar 1.25 watt. Keempat, form factor Raspberry Pi lebih besar sehingga kurang portable.

5.5 Alasan Tidak Memilih Smartphone dan IP Camera

Smartphone tidak dipilih karena meskipun gratis dan memiliki kualitas kamera terbaik, masalah stabilitas aplikasi, baterai yang cepat habis, dan ketidakkonsistenan performa antar model HP menjadikannya tidak reliable untuk deployment. IP Camera tidak dipilih karena latency RTSP yang terlalu tinggi yaitu 1 hingga 3 detik, firmware yang locked sehingga tidak bisa dikustomisasi, serta tidak portable karena umumnya membutuhkan power over ethernet atau mounting permanen.

5.6 Konfigurasi Penempatan Kamera

Empat kamera ditempatkan membentuk konfigurasi 360 derajat di sekitar area latihan. Penempatan idealnya adalah di empat sisi yaitu depan, belakang, kiri, dan kanan pada jarak sekitar 2 hingga 4 meter dari pengguna dan ketinggian sekitar 1 hingga 1.5 meter dari lantai. Setiap kamera dipasang di mini tripod yang foldable untuk kemudahan transport dan setup.

Konfigurasi ini memastikan bahwa setidaknya dua kamera selalu memiliki pandangan yang jelas ke setiap bagian tubuh pengguna, bahkan saat terjadi occlusion dari satu sudut. Untuk exercise tertentu, sudut kamera tertentu lebih penting dari yang lain. Untuk Push Up dan Sit Up, kamera samping atau sagittal view menjadi kamera primer. Untuk Pull Up, kamera depan menjadi primer. Untuk Squat Jump dan Vertical Jump, kombinasi kamera depan dan samping menjadi kritis.

5.7 Spesifikasi Streaming

Resolusi streaming ditetapkan pada VGA yaitu 640 kali 480 piksel. Resolusi ini merupakan sweet spot yang memberikan detail cukup untuk pose estimation tanpa membebani bandwidth dan processing secara berlebihan. Frame rate target adalah 15 hingga 20 FPS yang cukup untuk menangkap gerakan fitness dengan akurat. JPEG quality setting ditetapkan antara 15 hingga 20 yang memberikan keseimbangan antara ukuran file dan kualitas gambar. Protocol streaming menggunakan MJPEG over HTTP yang merupakan protocol paling stabil dan mature di ekosistem ESP32. Estimasi bandwidth per kamera adalah 2 hingga 3 Mbps, dan total bandwidth untuk empat kamera adalah 10 hingga 12 Mbps.

5.8 Power Supply

Setiap camera node membutuhkan power supply 5V dengan arus minimum 500mA. Untuk penggunaan indoor, power adapter USB standar sudah cukup. Untuk penggunaan outdoor dimana akses listrik terbatas, powerbank dengan kapasitas 10000mAh dapat menyuplai satu camera node selama kurang lebih 30 hingga 40 jam operasi terus-menerus, berkat konsumsi daya ESP32-S3 yang sangat rendah yaitu sekitar 250 hingga 350 miliampere saat streaming aktif.


================================================================================
BAB 6 — DESAIN FISIK PERANGKAT
================================================================================

Bab ini menjelaskan gambaran fisik dari setiap perangkat keras yang harus dirakit untuk sistem Fitness Tracking Eye. Informasi ini penting bagi tim proposal untuk memvisualisasikan produk akhir yang akan diterima klien, serta bagi tim engineering untuk memahami kebutuhan perakitan, material, dan form factor.

6.1 Gambaran Umum Perangkat

Sistem Fitness Tracking Eye terdiri dari beberapa perangkat fisik yang terpisah namun bekerja sebagai satu kesatuan. Perangkat utama adalah empat unit Camera Node yang berfungsi sebagai mata sistem. Setiap Camera Node adalah sebuah device kecil mandiri yang berisi mikrokontroler, modul kamera, dan sumber daya listrik, semuanya dikemas dalam satu casing compact. Selain Camera Node, terdapat Tracking Band berupa gelang neon yang dipakai di tubuh pengguna, serta opsional IMU Wristband yang berupa gelang sensor gerak di pergelangan tangan. Semua perangkat ini, beserta mini tripod, router, kabel, dan ChArUco board, dikemas dalam satu backpack untuk portability.

6.2 Camera Node — Komponen Penyusun

Setiap Camera Node terdiri dari tiga komponen utama yang dirakit menjadi satu unit.

Komponen pertama adalah board mikrokontroler XIAO ESP32-S3 Sense dari Seeed Studio. Board ini berukuran sangat kecil yaitu 21 kali 17.5 milimeter, kira-kira seukuran kuku jempol orang dewasa. Board ini sudah dilengkapi dengan slot kamera, antena WiFi, konektor USB-C untuk programming dan power, serta pad untuk koneksi baterai LiPo. Board inilah yang menjalankan firmware untuk menangkap frame dari kamera, mengkompresinya menjadi JPEG, dan mengirimkannya sebagai MJPEG stream melalui WiFi.

Komponen kedua adalah modul kamera OV2640 yang terhubung ke board melalui flex cable pendek. Modul kamera ini berukuran sangat kecil yaitu sekitar 8 kali 8 milimeter untuk sensor dan lens assembly. Pada XIAO ESP32-S3 Sense, modul kamera ini dipasang di slot khusus di bagian belakang board menggunakan konektor FPC. Pemasangan sangat mudah yaitu buka kunci konektor FPC, masukkan flex cable, lalu kunci kembali. Tidak diperlukan soldering.

Komponen ketiga adalah sumber daya listrik. Ada tiga opsi yang bisa dipilih tergantung skenario penggunaan.

6.3 Camera Node — Opsi Sumber Daya

Opsi pertama adalah USB-C power adapter dengan kabel. Ini merupakan opsi paling sederhana dan stabil untuk penggunaan indoor. Setiap Camera Node dihubungkan ke power adapter USB standar 5V 1A melalui kabel USB-C. Kelebihannya adalah power unlimited sehingga tidak perlu khawatir baterai habis, paling stabil karena tidak ada fluktuasi tegangan, dan paling murah karena adapter USB 5V sudah sangat umum. Kekurangannya adalah setiap Camera Node memiliki kabel power yang terhubung ke outlet listrik, sehingga kurang rapi dan membutuhkan akses ke empat colokan listrik. Estimasi biaya per unit adalah Rp 45.000 hingga Rp 75.000 untuk adapter dan kabel.

Opsi kedua adalah powerbank mini. Setiap Camera Node dipasangkan dengan powerbank kecil berkapasitas 5000 hingga 10000 mAh yang ditempatkan di dasar tripod atau diikat ke tripod. Kelebihannya adalah wireless sehingga tidak ada kabel power yang mengganggu, mudah didapatkan karena powerbank sudah sangat umum, dan bisa diganti dengan powerbank apapun yang ada. Kekurangannya adalah menambah bulk pada setiap camera node, perlu di-charge sebelum sesi, dan posisi powerbank di tripod perlu diperhatikan agar tidak mengganggu keseimbangan. Estimasi daya tahan dengan powerbank 5000mAh adalah sekitar 15 hingga 20 jam continuous streaming karena ESP32-S3 hanya mengkonsumsi sekitar 250 hingga 350 miliampere. Estimasi biaya per unit adalah Rp 75.000 hingga Rp 150.000.

Opsi ketiga adalah baterai LiPo yang terintegrasi di dalam casing. Baterai LiPo berkapasitas 500 hingga 1000 mAh disolder langsung ke battery pad di board XIAO ESP32-S3 dan dikemas bersama board di dalam casing. Ini menghasilkan device yang paling compact dan clean karena semua komponen berada dalam satu unit kecil. XIAO ESP32-S3 memiliki built-in battery charging circuit sehingga baterai bisa di-charge langsung melalui port USB-C tanpa perlu charger terpisah. Kelebihannya adalah form factor paling kecil dan rapi, truly wireless, dan charging terintegrasi melalui USB-C. Kekurangannya adalah memerlukan soldering untuk menghubungkan baterai ke board, daya tahan lebih terbatas yaitu sekitar 2 hingga 4 jam dengan baterai 1000mAh, dan memerlukan casing custom yang mengakomodasi board dan baterai. Estimasi biaya per unit adalah Rp 45.000 hingga Rp 90.000 untuk baterai LiPo.

6.4 Camera Node — Casing dan Enclosure

Setiap Camera Node memerlukan casing atau enclosure untuk melindungi komponen elektronik dan memudahkan mounting ke tripod. Ada beberapa opsi casing.

Opsi pertama adalah casing 3D printed custom. Casing dirancang menggunakan software CAD seperti Fusion 360 atau TinkerCAD dan dicetak menggunakan 3D printer dengan material PLA atau PETG. Desain casing harus mengakomodasi lubang untuk lensa kamera di sisi depan, ventilasi untuk pembuangan panas, akses ke port USB-C untuk charging dan programming, mount thread standar seperempat inci di bagian bawah untuk kompatibilitas dengan tripod standar, serta ruang untuk baterai LiPo jika menggunakan opsi baterai terintegrasi. Ukuran casing diperkirakan sekitar 35 kali 30 kali 20 milimeter tanpa baterai atau 35 kali 30 kali 35 milimeter dengan baterai LiPo terintegrasi. Estimasi biaya cetak per unit adalah Rp 15.000 hingga Rp 45.000 untuk material.

Opsi kedua adalah casing off-the-shelf berupa project box atau junction box kecil yang tersedia di toko elektronik. Project box berukuran sekitar 50 kali 35 kali 20 milimeter bisa dimodifikasi dengan mengebor lubang untuk lensa dan USB-C. Lebih cepat dan mudah daripada 3D printing namun hasilnya kurang presisi dan kurang estetis. Estimasi biaya per unit adalah Rp 15.000 hingga Rp 30.000.

Opsi ketiga adalah tanpa casing dimana board ditempel langsung ke tripod menggunakan double-sided tape atau velcro. Ini merupakan opsi tercepat dan termurah untuk prototyping namun tidak direkomendasikan untuk deployment karena komponen tidak terlindungi.

Rekomendasi untuk produk akhir adalah casing 3D printed custom karena memberikan hasil paling presisi, profesional, dan bisa didesain khusus untuk kebutuhan proyek ini.

6.5 Camera Node — Dimensi dan Form Factor Final

Dengan casing 3D printed dan baterai LiPo terintegrasi, setiap Camera Node memiliki perkiraan dimensi akhir sekitar 40 kali 35 kali 35 milimeter. Untuk memberikan gambaran, ukuran ini kira-kira seukuran kotak korek api atau sedikit lebih kecil. Berat total per unit diperkirakan sekitar 25 hingga 40 gram tergantung kapasitas baterai dan material casing. Ini sangat ringan dan tidak akan membebani mini tripod.

Dengan opsi USB-C power adapter tanpa baterai terintegrasi, dimensi bisa lebih kecil lagi yaitu sekitar 35 kali 30 kali 20 milimeter karena tidak perlu ruang untuk baterai.

6.6 Camera Node — Perakitan

Proses perakitan setiap Camera Node relatif sederhana dan tidak memerlukan keahlian elektronik tingkat lanjut.

Langkah pertama adalah memasang modul kamera OV2640 ke board XIAO ESP32-S3 Sense. Buka kunci konektor FPC di board dengan cara mengangkat tab pengunci ke atas. Masukkan flex cable modul kamera ke konektor dengan orientasi yang benar yaitu kontak tembaga menghadap ke bawah. Tekan tab pengunci kembali ke bawah untuk mengunci flex cable. Proses ini memakan waktu sekitar 30 detik.

Langkah kedua khusus untuk opsi baterai terintegrasi adalah menyolder kabel baterai LiPo ke battery pad positif dan negatif di board. Pad ini sudah ditandai dengan jelas di board. Perlu kehati-hatian untuk tidak membalik polaritas karena bisa merusak board. Proses ini memakan waktu sekitar 5 menit bagi yang berpengalaman soldering.

Langkah ketiga adalah memasukkan board dan baterai ke dalam casing. Pastikan lensa kamera sejajar dengan lubang di casing. Pastikan port USB-C accessible dari luar casing. Tutup casing.

Langkah keempat adalah flashing firmware ke board melalui USB-C menggunakan Arduino IDE atau PlatformIO. Firmware berisi konfigurasi WiFi yaitu SSID dan password serta konfigurasi streaming yaitu resolusi, frame rate, dan quality. Proses flash memakan waktu sekitar 1 hingga 2 menit per board.

Langkah kelima adalah mounting Camera Node ke mini tripod menggunakan thread mount di bagian bawah casing.

Total waktu perakitan per unit diperkirakan 10 hingga 15 menit untuk opsi USB adapter atau 20 hingga 25 menit untuk opsi baterai terintegrasi yang memerlukan soldering.

6.7 Camera Node — Ringkasan Bill of Materials per Unit

Berikut adalah daftar komponen lengkap untuk satu unit Camera Node.

XIAO ESP32-S3 Sense board sudah termasuk modul kamera OV2640 dan antena WiFi dengan harga sekitar Rp 195.000 hingga Rp 225.000. Casing 3D printed atau project box dengan harga sekitar Rp 15.000 hingga Rp 45.000. Mini tripod foldable dengan thread mount seperempat inci seharga sekitar Rp 75.000 hingga Rp 120.000.

Untuk opsi USB power, diperlukan USB-C cable panjang 1 hingga 2 meter seharga sekitar Rp 30.000 hingga Rp 45.000 dan USB power adapter 5V 1A seharga sekitar Rp 30.000 hingga Rp 45.000.

Untuk opsi baterai terintegrasi, diperlukan baterai LiPo 3.7V kapasitas 500 hingga 1000 mAh seharga sekitar Rp 45.000 hingga Rp 90.000.

Total biaya per Camera Node berkisar Rp 345.000 hingga Rp 435.000 untuk opsi USB power atau Rp 330.000 hingga Rp 480.000 untuk opsi baterai terintegrasi.

Total biaya empat Camera Node berkisar Rp 1.380.000 hingga Rp 1.920.000.

6.8 Tracking Band — Gambaran Fisik

Tracking Band adalah gelang elastis berwarna neon yang dipakai di tubuh pengguna. Secara fisik, setiap band terlihat seperti gelang olahraga biasa atau sweatband yang sering dipakai atlet, namun dengan warna neon yang sangat mencolok agar mudah dideteksi oleh kamera.

Band Size S untuk pergelangan tangan dan kaki berbentuk strip neoprene dengan lebar 4 hingga 5 sentimeter dan panjang total sekitar 30 sentimeter sebelum dililitkan. Satu sisi memiliki lapisan velcro hook dan sisi lainnya velcro loop sehingga bisa dililitkan dan direkatkan di berbagai ukuran lingkar. Sisi dalam yang menempel ke kulit dilapisi silicone dots atau strip untuk mencegah band bergeser saat berkeringat atau bergerak. Warnanya adalah hijau neon dan biru neon yang sangat mencolok bahkan dari jarak jauh.

Band Size M untuk paha dan lengan atas memiliki bentuk serupa namun lebih panjang yaitu sekitar 65 sentimeter dan lebih lebar yaitu 5 hingga 7 sentimeter untuk mengakomodasi lingkar paha yang jauh lebih besar. Strip velcro juga lebih panjang untuk memberikan range adjustable yang cukup. Warnanya adalah kuning neon dan merah neon.

Band Size L untuk dada memiliki desain yang sedikit berbeda yaitu menggunakan elastic webbing yang lebih kokoh dengan buckle quick-release di bagian depan, mirip dengan strap heart rate monitor. Panjang total sekitar 130 sentimeter dengan lebar 5 hingga 8 sentimeter. Buckle memudahkan pemasangan dan pelepasan cepat tanpa perlu melepas baju. Warnanya adalah putih atau silver reflective.

Semua band terbuat dari material yang tahan air dan keringat sehingga bisa dicuci setelah digunakan.

6.9 IMU Wristband — Gambaran Fisik (Opsional)

IMU Wristband merupakan komponen opsional yang hanya ada di Paket Pro. Secara fisik, IMU Wristband terlihat seperti jam tangan kecil atau fitness tracker sederhana. Device ini terdiri dari board XIAO ESP32-S3 berukuran 21 kali 17.5 milimeter, sensor BMI270 berukuran sangat kecil yaitu 2.5 kali 3 milimeter yang disolder atau dihubungkan melalui breakout board ke pin I2C board ESP32-S3, serta baterai LiPo berkapasitas 200 hingga 400 mAh.

Ketiga komponen ini dikemas dalam casing kecil berukuran perkiraan 40 kali 25 kali 15 milimeter yang dipasang pada strap velcro yang dipakai di pergelangan tangan. Casing bisa dibuat menggunakan 3D printing dengan material PETG yang lebih tahan panas dan impact dibandingkan PLA. Casing harus memiliki lubang ventilasi kecil dan akses ke port USB-C untuk charging.

Berat total per unit IMU Wristband diperkirakan sekitar 20 hingga 30 gram termasuk baterai dan strap, yang sangat ringan dan tidak akan mengganggu gerakan pengguna saat exercise.

Daya tahan baterai diperkirakan 6 hingga 10 jam continuous operation karena BMI270 sangat hemat daya yaitu kurang dari 1 miliampere saat active tracking.

6.10 Portable Kit — Isi Backpack

Seluruh sistem dikemas dalam satu backpack ukuran standar 20 hingga 30 liter. Berikut adalah daftar lengkap isi backpack.

Empat unit Camera Node yang masing-masing sudah dirakit dalam casing lengkap dengan tripod terlipat. Satu unit travel WiFi router. Empat unit kabel USB-C jika menggunakan opsi USB power atau empat unit powerbank mini jika menggunakan opsi baterai powerbank. Satu set Tracking Band yaitu 5 buah gelang neon dalam pouch kecil. Opsional dua unit IMU Wristband. Satu unit ChArUco calibration board yang dicetak pada papan rigid berukuran A3. Satu buah pouch aksesoris berisi power adapter, kabel cadangan, dan manual setup singkat.

Total berat seluruh kit diperkirakan 2 hingga 3 kilogram tergantung opsi power yang dipilih dan apakah menyertakan IMU Wristband atau tidak. Berat ini sangat ringan dan mudah dibawa kemana-mana.

Waktu setup dari membuka backpack hingga sistem siap tracking diperkirakan 10 hingga 15 menit. Ini mencakup menempatkan empat tripod dan Camera Node di sekitar area latihan sekitar 3 hingga 5 menit, menyalakan router dan menunggu Camera Node terhubung sekitar 1 hingga 2 menit, menjalankan software di laptop dan memastikan semua stream aktif sekitar 2 hingga 3 menit, serta melakukan kalibrasi kamera jika diperlukan sekitar 3 hingga 5 menit.


================================================================================
BAB 7 — KOMPONEN SOFTWARE: POSE ESTIMATION ENGINE
================================================================================

7.1 Pemilihan Engine: MediaPipe BlazePose

Setelah mengevaluasi lima pose estimation engine utama yaitu MediaPipe BlazePose, MoveNet, OpenPose, YOLOv8 Pose, dan RTMPose, keputusan jatuh pada MediaPipe BlazePose dari Google. Keputusan ini bersifat teknis internal dan tidak perlu dikomunikasikan ke klien.

7.2 Spesifikasi MediaPipe BlazePose

MediaPipe BlazePose menggunakan arsitektur two-stage yang terdiri dari detector stage menggunakan model yang terinspirasi BlazeFace untuk mendeteksi keberadaan orang dalam frame, dilanjutkan dengan landmark model yang memprediksi posisi 33 keypoints. Arsitektur ini dioptimalkan untuk single person detection sehingga tidak ada overhead dari multi-person tracking yang tidak diperlukan dalam proyek ini.

Output berupa 33 keypoints dalam format 3D. Setiap keypoint memiliki koordinat x dan y dalam normalized image coordinates yaitu 0 hingga 1, koordinat z yang merepresentasikan depth relatif, serta visibility score yang menunjukkan seberapa yakin model bahwa keypoint tersebut terlihat di frame.

Tiga puluh tiga keypoints ini mencakup area kepala yaitu nose, left eye inner, left eye, left eye outer, right eye inner, right eye, right eye outer, left ear, right ear, mouth left, dan mouth right. Area upper body meliputi left shoulder, right shoulder, left elbow, right elbow, left wrist, right wrist, left pinky, right pinky, left index, right index, left thumb, dan right thumb. Area lower body meliputi left hip, right hip, left knee, right knee, left ankle, right ankle, left heel, right heel, left foot index, dan right foot index.

Jumlah 33 keypoints ini jauh lebih banyak dibandingkan COCO-17 format yang hanya 17 keypoints dan digunakan oleh MoveNet, YOLO Pose, dan RTMPose. Keypoints tambahan seperti pergelangan kaki, tumit, dan ujung kaki sangat bermanfaat untuk analisis exercise yang melibatkan kaki seperti squat jump dan vertical jump.

7.3 Alasan Pemilihan MediaPipe BlazePose

Alasan utama pemilihan adalah native 3D support. MediaPipe BlazePose adalah satu-satunya engine di antara kelima kandidat yang memberikan estimasi depth yaitu koordinat z secara native dari single camera. Meskipun depth ini bersifat pseudo-3D dan tidak seakurat depth camera, informasi ini sangat membantu sebagai initial estimate sebelum dilakukan triangulation dari multi-view.

Alasan kedua adalah optimasi single person. Karena proyek ini hanya membutuhkan tracking satu orang, engine yang dirancang khusus untuk single person lebih efisien. Engine lain seperti YOLO Pose, RTMPose, dan OpenPose dirancang untuk multi-person sehingga memiliki overhead berupa person detector yang tidak diperlukan.

Alasan ketiga adalah performa yang ringan. MediaPipe BlazePose mampu berjalan pada 30 FPS atau lebih pada CPU laptop biasa tanpa GPU. Ini penting karena laptop juga harus memproses empat stream kamera secara bersamaan. Model Lite berukuran hanya 3MB dan model Full berukuran 6MB.

Alasan keempat adalah built-in landmark smoothing yang mengurangi jitter pada keypoints. Jitter ini jika tidak di-handle akan menyebabkan fluktuasi pada perhitungan sudut sendi yang berujung pada false counting.

Alasan kelima adalah lisensi Apache 2.0 yang memungkinkan penggunaan komersial secara bebas tanpa biaya lisensi tambahan.

7.4 Alasan Tidak Memilih Engine Lain

MoveNet dari Google TensorFlow tidak dipilih karena hanya menyediakan 17 keypoints 2D tanpa depth estimation. Meskipun lebih cepat dari MediaPipe, kurangnya detail keypoints terutama di area kaki dan tangan membatasi kemampuan analisis form.

OpenPose dari CMU tidak dipilih karena membutuhkan GPU powerful untuk berjalan yang bertentangan dengan target portability. Selain itu lisensi AGPL membatasi penggunaan komersial dan model berukuran lebih dari 200MB. Meskipun menyediakan keypoints paling detail termasuk jari tangan dan wajah, detail tersebut tidak diperlukan untuk fitness tracking.

YOLOv8 Pose dari Ultralytics tidak dipilih karena lisensi AGPL yang sama dengan OpenPose, hanya menyediakan 17 keypoints, dan dirancang sebagai unified detect plus pose yang merupakan fitur overkill untuk single person tracking.

RTMPose dari OpenMMLab sebenarnya merupakan kandidat kuat dengan akurasi tertinggi di antara semua engine yaitu AP 76.3 pada COCO dan kecepatan 90 FPS pada CPU. Namun RTMPose tidak dipilih karena tidak memiliki native 3D support, membutuhkan separate person detector, dan ekosistem MMPose yang lebih kompleks untuk di-setup dibandingkan MediaPipe.

7.5 Benchmark Performa

Berdasarkan data benchmark yang dikumpulkan dari berbagai sumber, berikut performa MediaPipe BlazePose pada berbagai hardware. Pada PC dengan prosesor Intel i7 dan GPU, model Lite mencapai lebih dari 120 FPS dan model Full mencapai lebih dari 80 FPS. Pada PC dengan CPU only, model Lite mencapai lebih dari 50 FPS dan model Full mencapai lebih dari 30 FPS. Pada Raspberry Pi 4, model Lite mencapai 12 hingga 15 FPS dan model Full mencapai 8 hingga 12 FPS. Pada Raspberry Pi 5, model Lite mencapai 20 hingga 25 FPS dan model Full mencapai 15 hingga 20 FPS.

Untuk proyek ini, target adalah menjalankan empat instance MediaPipe secara bersamaan di laptop. Dengan model Lite pada CPU, diperkirakan setiap instance dapat mencapai 12 hingga 15 FPS jika dijalankan secara sequential, atau lebih tinggi jika dijalankan secara parallel menggunakan multi-threading. FPS minimum yang acceptable untuk fitness tracking adalah 15 FPS.


================================================================================
BAB 8 — STRATEGI PEMROSESAN DATA
================================================================================

8.1 Pemilihan: Central Processing

Strategi pemrosesan yang dipilih adalah Central Processing dimana semua pose estimation dan logic dijalankan di satu unit pemrosesan utama yaitu laptop atau PC. Keputusan ini bersifat teknis internal.

8.2 Alasan Pemilihan Central Processing

Alasan utama adalah keterbatasan hardware camera node. XIAO ESP32-S3 Sense sebagai mikrokontroler tidak memiliki kemampuan komputasi untuk menjalankan MediaPipe BlazePose. Meskipun ESP32-S3 memiliki vector instructions untuk AI, model MediaPipe membutuhkan TensorFlow Lite runtime dengan minimum RAM beberapa ratus megabyte yang jauh melebihi kapasitas ESP32-S3. Oleh karena itu camera node hanya berfungsi sebagai capture device yang menangkap frame dan mengirimkannya sebagai MJPEG stream.

Alasan kedua adalah kemudahan development dan debugging. Dengan semua logic terpusat di satu tempat, developer hanya perlu mengurus satu codebase Python. Debugging menjadi jauh lebih mudah karena tidak perlu remote debug ke empat device edge yang terpisah. Update algoritma bisa dilakukan langsung tanpa perlu re-flash firmware empat camera node.

Alasan ketiga adalah konsistensi processing. Semua frame diproses oleh model MediaPipe yang sama di hardware yang sama, sehingga tidak ada variasi hasil yang disebabkan oleh perbedaan hardware atau versi model di setiap edge device.

Alasan keempat adalah kemampuan recording. Dengan central processing, raw video dari semua kamera bisa direkam untuk analisis offline di kemudian hari. Ini tidak mungkin dilakukan jika processing dilakukan di edge karena edge device tidak memiliki storage yang cukup.

8.3 Trade-off Central Processing

Trade-off utama dari central processing dibandingkan edge processing adalah kebutuhan bandwidth yang jauh lebih tinggi. Central processing membutuhkan pengiriman raw JPEG frame yang berukuran 30 hingga 50 kilobyte per frame, sementara edge processing hanya mengirim skeleton data berukuran sekitar 1 kilobyte per frame. Untuk empat kamera pada 15 FPS, central processing membutuhkan bandwidth sekitar 10 hingga 12 Mbps sementara edge processing hanya membutuhkan sekitar 60 kilobyte per detik.

Trade-off kedua adalah beban pada unit pemrosesan utama. Laptop harus mampu menjalankan empat instance MediaPipe secara bersamaan ditambah logic exercise detection dan web dashboard. Ini membutuhkan laptop dengan spesifikasi minimum prosesor Intel i5 generasi 10 atau setara, RAM 8GB, dan idealnya memiliki GPU discrete untuk akselerasi.

Trade-off ketiga adalah single point of failure. Jika laptop mengalami masalah, seluruh sistem berhenti. Berbeda dengan edge processing dimana jika satu node crash, node lainnya tetap berjalan.

Meskipun demikian, trade-off ini acceptable karena bandwidth 10 hingga 12 Mbps masih dalam kapasitas WiFi 5GHz, laptop modern sudah cukup powerful untuk menangani beban ini, dan single point of failure bisa dimitigasi dengan monitoring dan restart otomatis.


================================================================================
BAB 9 — PROTOKOL KOMUNIKASI DAN JARINGAN
================================================================================

9.1 Protocol Stack

Sistem menggunakan dua protocol komunikasi utama. Protocol pertama adalah MJPEG over HTTP yang digunakan untuk streaming video dari camera node ke unit pemrosesan utama. MJPEG atau Motion JPEG adalah format streaming dimana setiap frame video dikodekan secara independen sebagai gambar JPEG dan dikirim berurutan melalui HTTP. Protocol ini dipilih karena merupakan satu-satunya format streaming yang didukung secara native dan stabil oleh ESP32 camera library. Tidak diperlukan codec video seperti H.264 atau H.265 yang membutuhkan hardware encoder yang tidak tersedia di ESP32.

Protocol kedua adalah WebSocket yang digunakan untuk dua keperluan. Pertama, untuk mengirim hasil processing berupa data skeleton, repetisi, form score, dan metrik dari backend Python ke web dashboard frontend. Kedua, untuk komunikasi real-time bidirectional antara frontend dan backend misalnya untuk mengirim perintah start, stop, atau mengubah exercise mode.

9.2 Jaringan

Seluruh komunikasi berjalan di jaringan WiFi lokal yang dedicated. Dedicated berarti router yang digunakan tidak terhubung ke internet dan hanya melayani traffic antara camera node dan unit pemrosesan utama. Ini penting untuk memastikan tidak ada kompetisi bandwidth dengan traffic internet lainnya.

Untuk penggunaan indoor, direkomendasikan menggunakan dedicated WiFi router dengan dukungan 5GHz. Router travel seperti GL.iNet Slate AX merupakan pilihan yang baik karena compact, mendukung 5GHz, dan memiliki throughput yang cukup. Meskipun ESP32-S3 hanya mendukung WiFi 2.4GHz, router 5GHz tetap direkomendasikan agar laptop terhubung melalui 5GHz untuk throughput lebih tinggi, sementara camera node terhubung melalui 2.4GHz.

Untuk penggunaan outdoor dimana tidak ada akses WiFi, salah satu opsi adalah menggunakan laptop sebagai WiFi hotspot dimana keempat camera node terhubung langsung ke hotspot laptop. Opsi lainnya adalah menggunakan travel router yang ditenagai oleh powerbank.

9.3 Konfigurasi Jaringan Teknis

Setiap camera node akan memiliki IP address statis yang di-assign melalui konfigurasi firmware. Misalnya Camera Node 1 pada IP 192.168.1.101, Camera Node 2 pada IP 192.168.1.102, Camera Node 3 pada IP 192.168.1.103, dan Camera Node 4 pada IP 192.168.1.104. Unit pemrosesan utama mengakses stream dari masing-masing camera node melalui URL HTTP standar yaitu http://IP_ADDRESS:81/stream.

Backend Python menggunakan framework FastAPI atau Flask yang menyediakan WebSocket endpoint untuk komunikasi dengan web dashboard. Web dashboard diakses melalui browser di laptop pada alamat localhost.


================================================================================
BAB 10 — SINKRONISASI MULTI-KAMERA
================================================================================

10.1 Metode Sinkronisasi: NTP dengan Software Timestamp Matching

Sinkronisasi antar kamera menggunakan Network Time Protocol atau NTP untuk menyamakan clock di semua device, ditambah dengan software timestamp matching pada setiap frame. Metode ini dipilih karena memberikan akurasi 1 hingga 10 milidetik yang sudah lebih dari cukup untuk fitness tracking dimana gerakan exercise paling cepat masih memiliki durasi lebih dari 200 milidetik.

10.2 Alternatif yang Dievaluasi

PTP atau Precision Time Protocol IEEE 1588 memberikan akurasi sub-microsecond namun membutuhkan hardware support khusus dan koneksi kabel sehingga tidak sesuai dengan constraint wireless dan portability.

Hardware GPIO Trigger memberikan sinkronisasi paling presisi namun membutuhkan kabel trigger antar semua camera node yang mengalahkan tujuan wireless.

Software Sync Library seperti libsoftwaresync memberikan akurasi sekitar 250 microsecond dan berjalan di atas WiFi, namun membutuhkan library khusus yang belum tentu kompatibel dengan ESP32.

Visual Sync menggunakan LED flash memberikan akurasi satu frame sekitar 33 hingga 66 milidetik dan sangat simple namun membutuhkan kamera melihat LED yang sama.

10.3 Implementasi

Setiap camera node menyertakan timestamp dalam metadata frame yang dikirim. Di sisi unit pemrosesan utama, frame dari keempat kamera dicocokkan berdasarkan timestamp terdekat. Frame yang timestamp-nya terlalu jauh dari frame referensi yaitu lebih dari 50 milidetik akan di-drop atau di-interpolasi.

Untuk kalibrasi awal sinkronisasi, digunakan metode visual sync dimana sebuah LED yang terlihat oleh semua kamera dinyalakan secara bersamaan. Offset waktu antara frame dimana LED pertama kali terdeteksi di setiap kamera dihitung dan digunakan sebagai koreksi offset.


================================================================================
BAB 11 — REKONSTRUKSI 3D
================================================================================

11.1 Metode: Multi-View Triangulation

Rekonstruksi 3D menggunakan metode Direct Linear Transform atau DLT triangulation yang diimplementasikan melalui fungsi cv2.triangulatePoints dari library OpenCV. Metode ini mengambil keypoints 2D dari minimal dua kamera yang sudah dikalibrasi dan menghitung posisi 3D sebenarnya melalui proses triangulasi geometris.

11.2 Prasyarat

Triangulation membutuhkan kalibrasi kamera yang lengkap mencakup intrinsic parameters yaitu focal length, optical center, dan distortion coefficients dari setiap kamera, serta extrinsic parameters yaitu posisi dan orientasi relatif setiap kamera terhadap satu sistem koordinat referensi yang sama.

Kalibrasi intrinsic dilakukan satu kali per camera node menggunakan ChArUco board dan hasilnya disimpan sebagai file konfigurasi. Kalibrasi extrinsic dilakukan setiap kali kamera dipindahkan ke lokasi baru menggunakan ChArUco board yang sama yang diletakkan di area latihan dan terlihat oleh semua kamera secara bersamaan.

11.3 Pipeline Rekonstruksi 3D

Langkah pertama adalah undistort yaitu menghilangkan distorsi lensa dari keypoints 2D menggunakan intrinsic parameters. Langkah kedua adalah matching yaitu mencocokkan keypoints yang sama dari kamera yang berbeda berdasarkan ID keypoint dari MediaPipe. Langkah ketiga adalah triangulation yaitu menghitung posisi 3D dari setiap keypoint yang terdeteksi di minimal dua kamera. Langkah keempat adalah kinematic constraint yaitu memvalidasi hasil triangulasi terhadap batasan anatomis tubuh manusia seperti panjang tulang yang konsisten dan range of motion yang wajar. Langkah kelima adalah temporal smoothing menggunakan Kalman filter untuk menghaluskan trajectory 3D dan mengurangi jitter.

11.4 Handling Occlusion

Jika sebuah keypoint hanya terdeteksi di satu kamera dan tidak terdeteksi atau visibility rendah di kamera lainnya, sistem akan menggunakan pseudo-3D estimate dari MediaPipe pada kamera tersebut sebagai fallback. Jika keypoint tidak terdeteksi di kamera manapun, sistem menggunakan posisi terakhir yang diketahui dengan prediction berbasis velocity dari frame sebelumnya.

Tracking band yang dipakai pengguna membantu mengatasi occlusion karena warna neon dari band lebih mudah dideteksi dibandingkan bare skin atau pakaian biasa yang mungkin berwarna mirip dengan background.

11.5 Alternatif yang Dievaluasi

2D-to-3D Lifting menggunakan model neural network seperti MotionAGFormer atau VideoPose3D yang memprediksi posisi 3D dari keypoints 2D single camera. Metode ini tidak membutuhkan multi-camera dan kalibrasi namun akurasi depth-nya terbatas karena bersifat estimasi dari model yang di-train pada dataset tertentu.

Best-View Selection yang memilih kamera dengan confidence tertinggi untuk setiap keypoint pada setiap frame. Metode ini paling simple dan robust terhadap occlusion namun tidak menghasilkan true 3D sehingga analisis depth dan form 3D tidak memungkinkan.

Kedua alternatif ini tidak dipilih sebagai metode utama namun bisa digunakan sebagai fallback. Best-View Selection digunakan saat hanya satu kamera mendeteksi keypoint tertentu. 2D-to-3D Lifting bisa digunakan sebagai initial estimate sebelum di-refine oleh triangulation.


================================================================================
BAB 12 — KALIBRASI KAMERA
================================================================================

12.1 Metode: ChArUco Board

Kalibrasi kamera menggunakan ChArUco board yang merupakan kombinasi dari Charuco checkerboard dan ArUco markers. ChArUco board dipilih sebagai gold standard karena beberapa keunggulan dibandingkan checkerboard biasa.

Keunggulan pertama adalah toleransi terhadap occlusion parsial. Tidak seperti checkerboard standar yang membutuhkan seluruh pattern terlihat untuk deteksi, ChArUco board tetap bisa digunakan meskipun sebagian pattern tertutupi atau berada di luar frame kamera. Ini dimungkinkan karena setiap ArUco marker memiliki ID unik sehingga corner mana pun yang terdeteksi bisa langsung diidentifikasi posisinya di board.

Keunggulan kedua adalah eliminasi ambiguitas rotasi. Checkerboard simetris bisa menyebabkan ambiguitas dimana orientasi board terdeteksi terbalik. ArUco markers yang asimetris menghilangkan ambiguitas ini.

Keunggulan ketiga adalah akurasi sub-pixel melalui sub-pixel corner refinement yang memberikan presisi tinggi pada penentuan posisi corner.

12.2 Workflow Kalibrasi

Langkah pertama adalah mencetak ChArUco board. Board dicetak pada material rigid seperti papan akrilik, karton tebal, atau aluminium composite panel. Material harus benar-benar datar karena warping pada board akan menyebabkan error kalibrasi yang signifikan. Ukuran board yang direkomendasikan adalah A3 atau lebih besar.

Langkah kedua adalah kalibrasi intrinsic. Setiap kamera dikalibrasi secara individual dengan menangkap 20 atau lebih gambar ChArUco board dari berbagai posisi dan orientasi. Posisi board harus bervariasi di seluruh area frame dan mencakup berbagai sudut tilting. Hasil kalibrasi berupa focal length, optical center, dan distortion coefficients disimpan sebagai file YAML atau JSON.

Langkah ketiga adalah kalibrasi extrinsic. ChArUco board diletakkan di area latihan pada posisi yang terlihat oleh semua kamera secara bersamaan. Sistem menangkap frame dari semua kamera dan menghitung posisi dan orientasi relatif setiap kamera terhadap board. Hasilnya berupa rotation matrix dan translation vector antar kamera.

Langkah keempat adalah validasi. Reprojection error dihitung untuk memvalidasi kualitas kalibrasi. Target reprojection error adalah kurang dari 0.5 piksel. Jika error terlalu tinggi, kalibrasi diulang.

12.3 Kalibrasi Portable

Karena sistem bersifat portable dan kamera akan di-setup ulang di lokasi berbeda, kalibrasi extrinsic perlu dilakukan setiap kali setup baru. Untuk mempercepat proses, sistem menyediakan guided calibration mode di aplikasi yang memandu pengguna melalui langkah-langkah kalibrasi dengan instruksi visual.

ChArUco board bisa dicetak dan dilaminasi pada papan rigid berukuran A3 yang cukup ringan untuk dibawa dalam backpack bersama peralatan lainnya.


================================================================================
BAB 13 — ALGORITMA DETEKSI EXERCISE
================================================================================

13.1 Pendekatan: State Machine dengan Joint Angle Calculation

Algoritma deteksi exercise menggunakan pendekatan state machine yang dikombinasikan dengan joint angle calculation. Setiap exercise dimodelkan sebagai sequence of states dimana transisi antar state ditentukan oleh nilai sudut sendi tertentu yang melewati threshold yang telah ditetapkan.

Pendekatan ini dipilih karena beberapa alasan. Pertama, transparansi dan explainability dimana setiap keputusan counting bisa di-trace dan di-explain mengapa repetisi dihitung atau tidak. Kedua, kecepatan development karena rule-based approach bisa dibangun dan di-tune dalam hitungan hari. Ketiga, akurasi yang sudah cukup tinggi yaitu 90 hingga 95 persen untuk fase awal. Keempat, upgrade path yang jelas dimana setelah data cukup terkumpul, model machine learning seperti LSTM atau GRU bisa di-train untuk menggantikan atau melengkapi state machine.

13.2 Formula Perhitungan Sudut Sendi

Sudut sendi dihitung menggunakan trigonometri dari tiga titik landmark. Diberikan tiga titik A, B, dan C dimana B adalah sendi yang sudutnya dihitung, sudut dihitung menggunakan formula arctan2 dari selisih koordinat. Sudut yang dihasilkan kemudian dikonversi ke derajat. Misalnya untuk menghitung sudut siku, titik A adalah shoulder, titik B adalah elbow, dan titik C adalah wrist.

13.3 Teknik Anti-False Counting

Hysteresis thresholding digunakan dimana threshold untuk transisi dari state UP ke DOWN berbeda dari threshold transisi DOWN ke UP. Misalnya elbow angle harus turun di bawah 100 derajat untuk dianggap DOWN, tapi harus naik di atas 160 derajat untuk dianggap kembali UP. Gap antara threshold ini mencegah oscillation dimana sudut yang berfluktuasi di sekitar satu threshold menyebabkan false counting.

Minimum transition time mensyaratkan bahwa transisi antar state hanya valid jika waktu sejak transisi terakhir melebihi minimum tertentu, misalnya 200 milidetik. Ini mencegah counting yang disebabkan oleh jitter atau gerakan involunter yang sangat cepat.

Moving average smoothing pada nilai sudut sendi menggunakan window 3 hingga 5 frame untuk mengurangi jitter dari pose estimation. Smoothing ini dilakukan sebelum nilai sudut dibandingkan dengan threshold.

Visibility check memastikan bahwa semua keypoints yang diperlukan untuk perhitungan sudut memiliki visibility score di atas threshold minimum sebelum sudut dihitung. Jika visibility rendah, frame tersebut di-skip dan posisi terakhir yang valid digunakan.

13.4 Spesifikasi Deteksi per Exercise

Spesifikasi lengkap untuk masing-masing exercise dijelaskan di Bab 16 dokumen ini.


================================================================================
BAB 14 — TRACKING BAND SYSTEM
================================================================================

14.1 Latar Belakang dan Inspirasi

Tracking Band System terinspirasi dari teknologi motion capture yang digunakan dalam industri pembuatan film dan Visual Effects atau VFX. Dalam produksi film seperti Avatar, Planet of the Apes, dan berbagai film Marvel, aktor menggunakan bodysuit yang dilengkapi puluhan hingga ratusan marker reflektif kecil berbentuk bola. Kamera infrared khusus dari merk seperti Vicon atau OptiTrack mendeteksi marker-marker ini untuk merekam gerakan aktor dengan presisi milimeter. Sistem profesional ini berharga ratusan juta hingga miliaran rupiah.

Konsep Tracking Band mengadaptasi prinsip dasar marker-assisted tracking ini namun menyederhanakannya secara drastis agar sesuai dengan konteks fitness tracking. Alih-alih bodysuit penuh dengan marker reflektif yang mahal, kita menggunakan gelang elastis berwarna neon yang dipakai di beberapa titik kunci tubuh. Alih-alih kamera infrared khusus, kita menggunakan RGB camera standar dengan deteksi warna berbasis HSV color space.

14.2 Konsep Kerja

Tracking Band bekerja sebagai lapisan deteksi tambahan yang melengkapi pose estimation dari MediaPipe BlazePose. Setiap band berwarna neon berbeda yang dipakai di bagian tubuh tertentu terdeteksi oleh kamera melalui color segmentation dalam HSV color space. Posisi centroid dari setiap band yang terdeteksi kemudian di-fuse dengan keypoints dari MediaPipe untuk meningkatkan akurasi identifikasi bagian tubuh.

Proses fusion berjalan sebagai berikut. Pertama, MediaPipe menghasilkan 33 keypoints dengan posisi dan visibility score masing-masing. Secara bersamaan, color detection mengidentifikasi posisi centroid dari setiap band berwarna. Kedua, sistem membandingkan posisi keypoint MediaPipe dengan posisi centroid band yang sesuai. Ketiga, jika jarak antara keduanya melebihi threshold tertentu yang menandakan kemungkinan misdetection oleh MediaPipe, posisi keypoint dikoreksi menggunakan weighted average dari kedua sumber data. Keempat, jika MediaPipe kehilangan tracking pada keypoint tertentu misalnya karena occlusion, posisi band yang masih terdeteksi digunakan sebagai fallback.

14.3 Sistem Ukuran Band: 3 Kategori

Berdasarkan analisis data antropometri rata-rata orang dewasa, ditemukan bahwa ukuran lingkar bagian tubuh memiliki variasi yang signifikan. Pergelangan tangan memiliki lingkar rata-rata 14 hingga 20 sentimeter. Pergelangan kaki memiliki lingkar rata-rata 19 hingga 24 sentimeter. Paha memiliki lingkar rata-rata 48 hingga 62 sentimeter. Dada memiliki lingkar rata-rata 80 hingga 115 sentimeter.

Temuan penting adalah bahwa pergelangan tangan dan pergelangan kaki memiliki lingkar yang cukup dekat sehingga satu ukuran velcro band dengan range adjustable bisa fit di kedua bagian tubuh. Namun paha memiliki lingkar yang jauh lebih besar yaitu sekitar tiga kali lipat dari pergelangan sehingga membutuhkan ukuran band yang terpisah. Dada memiliki lingkar terbesar dan membutuhkan band ukuran tersendiri.

Berdasarkan temuan ini, sistem tracking band dirancang dengan tiga kategori ukuran.

Size S berjumlah dua buah dengan range adjustable 14 hingga 26 sentimeter. Band ini fit untuk pergelangan tangan dan pergelangan kaki serta forearm. Material menggunakan neoprene 2 milimeter dengan penutup velcro dan lebar 4 hingga 5 sentimeter. Sisi dalam dilengkapi grip dots atau silicone strips untuk mencegah band bergeser. Material neoprene tahan air dan keringat. Warna yang ditetapkan adalah Hijau Neon untuk band pertama dan Biru Neon untuk band kedua. Estimasi berat per band adalah 15 hingga 20 gram dan estimasi harga adalah Rp 15.000 hingga Rp 30.000 per band.

Size M berjumlah dua buah dengan range adjustable 28 hingga 58 sentimeter. Band ini fit untuk paha, upper arm atau bicep, dan betis. Material menggunakan neoprene 2 milimeter dengan penutup velcro panjang dan lebar 5 hingga 7 sentimeter. Strip velcro harus cukup panjang untuk mengakomodasi range 30 sentimeter dari terkecil ke terbesar. Sisi dalam dilengkapi silicone strips karena area paha cenderung lebih berkeringat. Warna yang ditetapkan adalah Kuning Neon untuk band pertama dan Merah Neon untuk band kedua. Estimasi berat per band adalah 25 hingga 35 gram dan estimasi harga adalah Rp 30.000 hingga Rp 45.000 per band.

Size L berjumlah satu buah dengan range adjustable 60 hingga 120 sentimeter. Band ini fit untuk dada dan perut. Material menggunakan elastic webbing dengan penutup velcro dan buckle quick-release serta lebar 5 hingga 8 sentimeter. Desain mirip dengan heart rate monitor strap dengan buckle untuk kemudahan pemakaian dan pelepasan cepat. Warna yang ditetapkan adalah Putih atau Silver Reflective. Estimasi berat adalah 40 hingga 60 gram dan estimasi harga adalah Rp 45.000 hingga Rp 75.000 per band.

Total kit tracking band terdiri dari 5 band dalam 3 ukuran dengan total estimasi biaya Rp 150.000 hingga Rp 225.000.

14.4 Konsep Repositionable Band

Salah satu inovasi kunci dari sistem tracking band ini adalah konsep repositionable dimana band bisa dipindah-pindahkan sesuai dengan exercise yang dilakukan. Tidak semua exercise membutuhkan band di semua lokasi tubuh, dan beberapa exercise membutuhkan band di lokasi yang berbeda.

Konsep ini memungkinkan penggunaan hanya lima band untuk cover semua lima exercise. Band Size S yang dipakai di pergelangan tangan untuk Push Up dan Pull Up bisa dipindahkan ke pergelangan kaki untuk Squat Jump dan Vertical Jump. Band Size M yang dipakai di paha untuk Sit Up dan Squat Jump bisa dilepas saat tidak diperlukan untuk Push Up, Pull Up, dan Vertical Jump. Band Size L selalu berada di dada untuk semua exercise sehingga tidak pernah perlu dipindahkan.

14.5 Mapping Band per Exercise

Untuk Push Up, pengguna memasang dua band Size S di pergelangan tangan kiri dan kanan serta satu band Size L di dada. Band Size S di pergelangan tangan membantu track posisi dan lebar hand placement. Band Size L di dada krusial untuk tracking kedalaman gerakan yaitu seberapa rendah dada turun. Dua band Size M tidak diperlukan karena posisi kaki relatif statis. Total band yang dipakai adalah tiga buah.

Untuk Pull Up, konfigurasi sama dengan Push Up yaitu dua band Size S di pergelangan tangan kiri dan kanan serta satu band Size L di dada. Band Size S di pergelangan tangan membantu track posisi grip dan referensi apakah dagu melewati bar. Band Size L di dada menjadi referensi untuk deteksi kipping yaitu ayunan hip yang berlebihan. Total band yang dipakai adalah tiga buah.

Untuk Sit Up, pengguna memasang dua band Size M di paha kiri dan kanan serta satu band Size L di dada. Band Size M di paha berfungsi sebagai anchor point atau referensi statis karena paha relatif tidak banyak bergerak saat sit up. Band Size L di dada adalah bagian yang paling banyak bergerak sehingga tracking trunk flexion menjadi lebih akurat. Band Size S tidak diperlukan karena pergelangan tangan dan kaki tidak relevan. Total band yang dipakai adalah tiga buah.

Untuk Squat Jump, pengguna memasang dua band Size S di pergelangan kaki kiri dan kanan, dua band Size M di paha kiri dan kanan, serta satu band Size L di dada. Ini adalah satu-satunya exercise yang membutuhkan semua lima band. Band Size S di ankle krusial untuk deteksi jump height yaitu displacement ankle dari ground saat takeoff dan landing. Band Size M di paha penting untuk tracking squat depth yaitu seberapa dalam pengguna squat sebelum melompat. Band Size L di dada menjadi referensi postur torso dan center of mass. Total band yang dipakai adalah lima buah.

Untuk Vertical Jump, pengguna memasang dua band Size S di pergelangan kaki kiri dan kanan serta satu band Size L di dada. Band Size S di ankle berfungsi sama dengan Squat Jump yaitu untuk deteksi jump height. Band Size L di dada untuk tracking center of mass. Band Size M tidak diperlukan karena tidak ada analisis squat depth seperti pada Squat Jump. Total band yang dipakai adalah tiga buah.

14.6 Dynamic Color Mapping

Karena band dipindah-pindah posisi antar exercise, warna band tidak lagi mewakili satu bagian tubuh tertentu secara fixed. Sebagai gantinya, warna mewakili ukuran band. Hijau Neon dan Biru Neon selalu merupakan band Size S. Kuning Neon dan Merah Neon selalu merupakan band Size M. Putih selalu merupakan band Size L.

Sistem mengetahui exercise apa yang sedang aktif karena pengguna memilih exercise sebelum memulai. Berdasarkan exercise yang dipilih, sistem secara otomatis melakukan mapping warna ke bagian tubuh yang sesuai. Misalnya untuk Push Up, Hijau Neon di-map ke Left Wrist dan Biru Neon di-map ke Right Wrist. Untuk Squat Jump, Hijau Neon di-map ke Left Ankle dan Biru Neon di-map ke Right Ankle. Mapping ini transparan bagi pengguna, mereka hanya perlu mengikuti instruksi pemasangan yang ditampilkan di aplikasi.

14.7 User Flow Pemasangan Band

Saat pengguna membuka aplikasi dan memilih exercise yang ingin dilakukan, aplikasi menampilkan instruksi visual yang menunjukkan di mana setiap band harus dipasang. Instruksi mencakup gambar atau diagram sederhana yang menunjukkan posisi pemasangan dan warna band yang sesuai. Pengguna memasang band sesuai instruksi yang memakan waktu sekitar 30 detik untuk tiga band atau 60 detik untuk lima band. Setelah band terpasang, pengguna menekan tombol mulai dan sistem memulai tracking.

Saat pengguna ingin beralih ke exercise lain, aplikasi menampilkan instruksi transisi yang menunjukkan band mana yang perlu dipindahkan, dilepas, atau ditambahkan. Band Size L di dada tidak pernah perlu dipindahkan sehingga mempercepat transisi. Waktu transisi antara exercise diperkirakan 30 hingga 60 detik.

14.8 Pipeline Deteksi Teknis

Deteksi color band menggunakan OpenCV HSV color segmentation. Setiap frame yang diterima dari kamera dikonversi dari color space BGR ke HSV. Untuk setiap warna band, fungsi cv2.inRange digunakan dengan parameter HSV lower dan upper bound yang telah dikalibrasi untuk memfilter piksel yang sesuai warna band. Hasilnya berupa binary mask yang kemudian di-proses dengan morphological operations yaitu erode untuk menghilangkan noise kecil dan dilate untuk mengisi gap. Contour detection menggunakan cv2.findContours untuk menemukan blob terbesar yang merupakan band. Centroid dari blob terbesar dihitung menggunakan cv2.moments.

Proses ini secara komputasi sangat ringan karena color segmentation di HSV hanya melibatkan operasi perbandingan sederhana per-pixel, jauh lebih ringan dibandingkan neural network inference. Overhead tambahan dari tracking band detection diperkirakan kurang dari 5 milidetik per frame.

14.9 Kalibrasi Warna

Karena warna yang terlihat oleh kamera dipengaruhi oleh kondisi pencahayaan, kalibrasi HSV threshold perlu dilakukan saat setup. Sistem menyediakan calibration wizard dimana pengguna diminta menunjukkan setiap band ke kamera satu per satu. Sistem mendeteksi histogram HSV dari area band dan secara otomatis menghitung optimal lower dan upper bound. Untuk penggunaan indoor dengan pencahayaan konsisten, kalibrasi hanya perlu dilakukan sekali. Untuk penggunaan outdoor dimana pencahayaan berubah, re-kalibrasi mungkin diperlukan atau sistem bisa menggunakan adaptive thresholding yang secara otomatis menyesuaikan threshold berdasarkan kondisi pencahayaan.

14.10 Peningkatan Akurasi yang Diharapkan

Berdasarkan studi dan riset yang dilakukan, penambahan color band diperkirakan meningkatkan akurasi overall sistem dari sekitar 85 hingga 90 persen menjadi 90 hingga 95 persen. Peningkatan paling signifikan terjadi pada body part identification dimana band memberikan identitas warna yang jelas untuk setiap segmen tubuh, dan occlusion handling dimana saat MediaPipe kehilangan tracking karena occlusion, band yang masih terdeteksi menjadi fallback yang reliable.


================================================================================
BAB 15 — SENSOR IMU TAMBAHAN (OPSIONAL)
================================================================================

15.1 Deskripsi

Sebagai opsi upgrade, sistem dapat dilengkapi dengan sensor Inertial Measurement Unit atau IMU yang berupa modul kecil berisi accelerometer dan gyroscope yang dipakai di pergelangan tangan. Sensor ini memberikan data gerakan dengan frekuensi sampling 100 hingga 1000 kali per detik, jauh lebih tinggi dibandingkan kamera yang hanya 15 hingga 20 frame per detik.

15.2 Pemilihan Sensor: BMI270

Berdasarkan riset terbaru, sensor IMU yang sebelumnya populer yaitu MPU6050 dan BNO055 sudah dianggap obsolete untuk proyek baru di tahun 2025 hingga 2026. MPU6050 hanya memiliki 6 axis tanpa magnetometer, tidak memiliki on-board sensor fusion yang memadai, dan mengalami drift yang signifikan. BNO055 meskipun memiliki built-in sensor fusion sering mengalami error kalibrasi dan boros daya.

Sensor yang direkomendasikan adalah BMI270 dari Bosch yang merupakan sensor generasi modern yang dirancang khusus untuk wearable dan fitness tracking. Keunggulan BMI270 meliputi built-in step counter dan gesture detection di level hardware sehingga ESP32 bisa tetap dalam mode deep sleep. Konsumsi daya kurang dari 1 miliampere saat active tracking yang jauh lebih hemat dibandingkan BNO055. Ukuran sangat kecil cocok untuk form factor wristband. Harga terjangkau yaitu sekitar Rp 75.000 hingga Rp 120.000 per modul.

Alternatif lainnya adalah ICM-20948 dari InvenSense TDK yang merupakan sensor 9 axis dengan magnetometer built-in. Sensor ini direkomendasikan jika orientasi 3D absolut diperlukan misalnya untuk mengetahui arah hadap pengguna.

15.3 Arsitektur IMU Wristband

Setiap IMU wristband terdiri dari satu board XIAO ESP32-S3 yang sama dengan camera node untuk konsistensi ekosistem, satu sensor BMI270 yang terhubung melalui I2C, satu baterai LiPo berkapasitas 200 hingga 400 mAh, dan casing kecil yang terintegrasi ke strap velcro yang dipakai di pergelangan tangan.

Data sensor dikirim melalui WiFi atau Bluetooth Low Energy ke unit pemrosesan utama dengan frekuensi 100Hz. Format data berupa JSON atau binary compact yang berisi timestamp, nilai accelerometer 3 axis, dan nilai gyroscope 3 axis.

15.4 Sensor Fusion Camera plus IMU

Data dari IMU di-fuse dengan data dari kamera menggunakan metode adaptive trust weighting. Prinsipnya adalah sistem mempercayai kamera lebih saat kondisi pencahayaan baik dan pengguna bergerak lambat, namun mempercayai IMU lebih saat terjadi gerakan cepat seperti saat fase jump atau saat terjadi occlusion dimana kamera kehilangan tracking.

Fusion dilakukan menggunakan Extended Kalman Filter yang menggabungkan measurement dari kedua sumber dengan weight yang dinamis berdasarkan confidence score MediaPipe dan noise level IMU.

15.5 Apa yang IMU Bisa dan Tidak Bisa Ukur

IMU sangat akurat untuk repetition counting melalui peak detection dari sinyal akselerasi. IMU juga akurat untuk exercise classification yaitu membedakan jenis exercise berdasarkan pola akselerasi dan rotasi. Movement speed dan tempo juga bisa diukur dengan baik. Body orientation yaitu apakah pengguna berbaring, berdiri, atau terbalik juga reliabel.

Namun IMU tidak akurat untuk mengukur displacement atau jarak pergerakan karena double integration dari akselerasi menghasilkan error kumulatif lebih dari 50 persen dalam hitungan detik. IMU juga tidak bisa mengukur joint angle secara absolut karena hanya mengetahui orientasi segmen tubuh dimana sensor terpasang, bukan sudut antar segmen. Untuk kedua measurement ini, kamera tetap menjadi sumber data primer.


================================================================================
BAB 16 — PLATFORM DAN ANTARMUKA PENGGUNA
================================================================================

16.1 Backend: Python

Backend menggunakan Python sebagai bahasa pemrograman utama dengan beberapa library kunci. OpenCV digunakan untuk camera handling, image processing, dan kalibrasi. MediaPipe digunakan untuk pose estimation. NumPy dan SciPy digunakan untuk angle calculation, signal processing, dan mathematical operations. FastAPI atau Flask digunakan sebagai web server yang menyediakan WebSocket endpoint. filterpy digunakan untuk implementasi Kalman filter pada temporal smoothing.

Python dipilih karena semua library yang dibutuhkan tersedia secara native, ekosistem Python untuk computer vision dan machine learning adalah yang paling mature, dan development speed menjadi yang tercepat dibandingkan bahasa lain.

16.2 Frontend: Web Dashboard

Frontend menggunakan web application berbasis HTML, CSS, dan JavaScript yang berjalan di browser. Web dashboard dipilih karena cross-platform sehingga bisa diakses dari device apapun yang memiliki browser, tidak memerlukan instalasi, dan modern UI framework memungkinkan tampilan yang profesional dan responsif.

Fitur dashboard meliputi tampilan multi-camera view yang menunjukkan feed dari empat kamera secara bersamaan. Visualisasi skeleton overlay di atas video feed. Exercise mode selector untuk memilih exercise yang akan dilakukan. Real-time rep counter yang menampilkan jumlah repetisi saat ini. Form score gauge yang menunjukkan kualitas form dari 0 hingga 100 persen. Correction tips yang memberikan feedback koreksi form secara real-time misalnya "pinggul terlalu turun" atau "lutut melewati ujung kaki". Session analytics berupa chart dan statistik dari sesi latihan. Sensor status panel yang menunjukkan status koneksi setiap kamera dan sensor.

Komunikasi antara backend dan frontend menggunakan WebSocket yang memungkinkan update data secara real-time tanpa perlu polling.


================================================================================
BAB 17 — SPESIFIKASI PER EXERCISE
================================================================================

17.1 Push Up

Keypoints utama yang digunakan adalah Shoulder dengan indeks 11 dan 12, Elbow dengan indeks 13 dan 14, Wrist dengan indeks 15 dan 16, Hip dengan indeks 23 dan 24, serta Ankle dengan indeks 27 dan 28.

Sudut kunci yang dihitung adalah elbow angle yaitu sudut yang dibentuk oleh shoulder, elbow, dan wrist. Saat posisi atas atau arms extended, sudut ini mendekati 180 derajat. Saat posisi bawah atau lowest point, sudut ini mendekati 90 derajat.

State machine terdiri dari dua state yaitu UP dan DOWN. Transisi dari UP ke DOWN terjadi ketika elbow angle turun di bawah 100 derajat. Transisi dari DOWN ke UP terjadi ketika elbow angle naik di atas 160 derajat. Satu siklus lengkap UP ke DOWN ke UP dihitung sebagai satu repetisi.

Form analysis meliputi hip alignment check yang memastikan bahwa garis dari shoulder ke hip ke ankle mendekati lurus yaitu sekitar 180 derajat. Jika hip angle menyimpang lebih dari 15 derajat dari 180, sistem memberikan warning "hip sagging" atau "hip terlalu tinggi". Depth check memastikan bahwa pengguna turun cukup dalam yaitu elbow angle mencapai minimum di bawah threshold tertentu. Hand width check menggunakan tracking band di pergelangan tangan untuk memastikan jarak antar tangan sesuai dengan lebar bahu.

Kamera primer untuk Push Up adalah kamera samping atau sagittal view karena memberikan pandangan terbaik untuk elbow angle dan hip alignment.

Tracking band yang digunakan adalah Size S di kedua pergelangan tangan untuk membantu track hand placement dan Size L di dada untuk depth tracking.

17.2 Pull Up

Keypoints utama adalah Shoulder dengan indeks 11 dan 12, Elbow dengan indeks 13 dan 14, Wrist dengan indeks 15 dan 16, serta Nose dengan indeks 0 sebagai referensi posisi dagu.

Sudut kunci adalah elbow angle dan posisi vertikal nose relatif terhadap wrist. Saat hanging position, elbow angle mendekati 180 derajat dan nose berada di bawah wrist. Saat posisi atas, nose berada di atas atau sejajar dengan wrist yang menandakan chin di atas bar.

State machine terdiri dari dua state yaitu HANG dan UP. Transisi dari HANG ke UP terjadi ketika nose Y-coordinate lebih kecil atau lebih tinggi dari wrist Y-coordinate. Transisi dari UP ke HANG terjadi ketika elbow angle melebihi 160 derajat. Satu siklus HANG ke UP ke HANG dihitung sebagai satu repetisi.

Form analysis meliputi kipping detection yang mengukur perubahan sudut hip per frame. Jika hip swing melebihi 20 derajat per transisi, sistem memberikan warning "kipping detected". Full extension check memastikan lengan benar-benar lurus di posisi hang.

Kamera primer adalah kamera depan atau frontal view ditambah kamera samping untuk kipping detection.

Tracking band yang digunakan adalah Size S di kedua pergelangan tangan untuk track grip position dan Size L di dada untuk kipping detection.

17.3 Sit Up

Keypoints utama adalah Shoulder dengan indeks 11 dan 12, Hip dengan indeks 23 dan 24, serta Knee dengan indeks 25 dan 26.

Sudut kunci adalah hip angle yaitu sudut yang dibentuk oleh shoulder, hip, dan knee. Saat posisi lying down, sudut ini mendekati atau melebihi 140 derajat. Saat posisi duduk, sudut ini berkurang hingga di bawah 70 derajat.

State machine terdiri dari dua state yaitu DOWN dan UP. Transisi dari DOWN ke UP terjadi ketika hip angle turun di bawah 70 derajat. Transisi dari UP ke DOWN terjadi ketika hip angle naik di atas 140 derajat. Satu siklus DOWN ke UP ke DOWN dihitung sebagai satu repetisi.

Form analysis meliputi feet planted check yang memastikan posisi ankle tetap stabil dengan varians posisi yang rendah. Full range of motion verification memastikan pengguna benar-benar turun hingga lying position dan naik hingga sitting position.

Kamera primer adalah kamera samping atau sagittal view.

Tracking band yang digunakan adalah Size M di kedua paha sebagai anchor point referensi dan Size L di dada untuk trunk flexion tracking.

17.4 Squat Jump

Keypoints utama adalah Hip dengan indeks 23 dan 24, Knee dengan indeks 25 dan 26, Ankle dengan indeks 27 dan 28, serta Shoulder dengan indeks 11 dan 12.

Sudut kunci meliputi knee angle yaitu sudut yang dibentuk oleh hip, knee, dan ankle, serta vertical displacement dari ankle Y-coordinate untuk deteksi fase airborne.

State machine terdiri dari empat state yaitu STAND, SQUAT, JUMP, dan LAND. Transisi dari STAND ke SQUAT terjadi ketika knee angle turun di bawah 90 derajat. Transisi dari SQUAT ke JUMP terjadi ketika ankle Y-coordinate menunjukkan displacement ke atas yang signifikan yaitu kedua kaki terangkat dari ground. Transisi dari JUMP ke LAND terjadi ketika ankle Y-coordinate kembali ke level ground. Transisi dari LAND ke STAND terjadi ketika knee angle kembali di atas 160 derajat. Satu siklus lengkap dihitung sebagai satu repetisi.

Form analysis meliputi squat depth check yang memastikan knee angle mencapai minimum di bawah threshold. Knee-over-toe check menggunakan kamera samping untuk memastikan lutut tidak melewati ujung kaki saat squat. Landing mechanics analysis memeriksa knee angle saat landing yang seharusnya sedikit flexed untuk menyerap impact bukan locked straight. Torso angle check memastikan torso tetap relatif tegak saat squat.

Metrik tambahan meliputi estimasi jump height dari pixel displacement dan power estimation dari akselerasi data jika IMU tersedia.

Kamera primer adalah kombinasi kamera depan dan samping karena exercise ini membutuhkan analisis dari multiple angle.

Tracking band yang digunakan adalah Size S di kedua ankle untuk jump detection, Size M di kedua paha untuk squat depth, dan Size L di dada untuk torso reference. Ini adalah satu-satunya exercise yang menggunakan semua lima band.

17.5 Vertical Jump

Keypoints utama adalah Hip dengan indeks 23 dan 24, Ankle dengan indeks 27 dan 28, serta Shoulder dengan indeks 11 dan 12.

Tracking utama adalah hip Y-coordinate atau ankle Y-coordinate yang dipantau dari waktu ke waktu untuk mengukur jump height.

State machine terdiri dari empat state yaitu STAND, CROUCH, JUMP, dan LAND. Transisi dari STAND ke CROUCH terjadi saat knee bend terdeteksi sebagai counter-movement sebelum jump. Transisi dari CROUCH ke JUMP terjadi saat kedua kaki terangkat dari ground. Transisi JUMP berlanjut hingga mencapai PEAK yaitu titik tertinggi. Transisi dari PEAK ke LAND terjadi saat pengguna mulai turun dan mendarat.

Metrik utama meliputi maximum jump height yang dihitung dari selisih posisi Y hip atau ankle di peak versus standing position. Metrik ini perlu dikalibrasi dari pixel ke sentimeter menggunakan referensi jarak yang diketahui. Flight time yaitu durasi pengguna berada di udara dari takeoff hingga landing. Hang time yaitu durasi pengguna berada di atas 80 persen dari peak height. Counter-movement depth yaitu seberapa dalam crouch sebelum jump.

Kamera primer adalah kamera samping yang esensial untuk pengukuran ketinggian yang akurat.

Tracking band yang digunakan adalah Size S di kedua ankle untuk jump height detection dan Size L di dada untuk center of mass tracking.


================================================================================
BAB 18 — OPERASIONAL: INDOOR DAN OUTDOOR
================================================================================

18.1 Optimasi Indoor

Penggunaan indoor merupakan kondisi ideal untuk sistem ini. Pencahayaan yang konsisten dan terkontrol memberikan kualitas gambar terbaik untuk pose estimation dan color band detection. WiFi interference minimal jika menggunakan dedicated router. Power supply tersedia dari outlet listrik. Permukaan lantai rata untuk penempatan tripod yang stabil.

Rekomendasi setup indoor meliputi penggunaan pencahayaan yang merata tanpa shadow yang keras. Pengguna sebaiknya mengenakan pakaian yang kontras dengan background. Background sebaiknya plain dan tidak terlalu ramai pattern. Jarak kamera ke pengguna optimal adalah 2 hingga 4 meter.

18.2 Kemampuan Outdoor

Sistem dirancang untuk tetap berfungsi di outdoor meskipun dengan beberapa keterbatasan. Constraint outdoor yang dipertimbangkan meliputi pencahayaan yang berubah-ubah dan berpotensi terlalu terang di bawah sinar matahari langsung, tidak ada akses WiFi router sehingga perlu menggunakan laptop hotspot atau travel router portable, power supply bergantung pada powerbank, serta kondisi angin dan permukaan yang tidak rata dapat mempengaruhi stabilitas tripod.

Rekomendasi setup outdoor meliputi memposisikan pengguna agar matahari tidak berada di belakang pengguna untuk menghindari backlight yang menyulitkan pose estimation. Menggunakan area yang teduh seperti di bawah pohon atau gazebo jika memungkinkan. Mengatur kamera ke manual exposure untuk menghindari auto-adjust flickering. Menggunakan powerbank minimum 10000mAh per camera node. Mengamankan tripod dengan beban tambahan jika angin kencang. Re-kalibrasi warna tracking band karena pencahayaan outdoor berbeda dari indoor.

18.3 Dampak Lingkungan per Teknologi

RGB Camera dengan MediaPipe memiliki performa excellent di indoor dan baik di outdoor dengan catatan perlu menghindari backlight. IMU sensor tidak terpengaruh lingkungan sama sekali karena tidak bergantung pada cahaya. WiFi sangat stabil di indoor namun di outdoor membutuhkan portable router dengan jangkauan yang mungkin terbatas. Power supply di indoor bisa menggunakan outlet listrik sepanjang waktu namun di outdoor bergantung pada kapasitas powerbank.

Perlu dicatat bahwa depth camera berbasis infrared seperti Intel RealSense atau Azure Kinect telah dieliminasi dari pertimbangan karena gagal di outdoor. Sensor infrared menggunakan wavelength yang sama dengan sinar matahari sehingga di outdoor, sensor kebanjiran ambient infrared yang menyebabkan signal-to-noise ratio turun drastis dan menghasilkan depth map yang penuh noise atau gagal total.


================================================================================
BAB 19 — ANALISIS RISIKO DAN MITIGASI
================================================================================

19.1 Risiko Teknis

WiFi instability yang menyebabkan frame drop merupakan risiko dengan probabilitas tinggi dan impact medium. Mitigasi utama adalah penggunaan dedicated router yang tidak dibagi dengan traffic lain dan penggunaan band 5GHz dimana memungkinkan. Monitoring frame rate secara real-time dengan alert jika FPS turun di bawah threshold juga menjadi bagian dari mitigasi.

Occlusion dimana bagian tubuh tertutupi merupakan risiko dengan probabilitas tinggi dan impact tinggi. Mitigasi utama adalah multi-camera coverage dari 360 derajat dan penggunaan tracking band sebagai fallback detection. Confidence-based view selection yang memilih kamera terbaik untuk setiap keypoint juga membantu mengatasi occlusion.

Variasi pencahayaan merupakan risiko dengan probabilitas medium dan impact medium. Mitigasi meliputi histogram equalization dan gamma correction sebagai pre-processing, manual exposure setting pada kamera, serta adaptive HSV threshold untuk color band detection.

Kalibrasi kamera drift seiring waktu merupakan risiko dengan probabilitas medium dan impact tinggi karena langsung mempengaruhi akurasi 3D reconstruction. Mitigasi berupa kalibrasi ulang saat setiap setup baru dan potensi self-calibration menggunakan pose prior sebagai maintenance berkala.

Pose estimation jitter merupakan risiko dengan probabilitas tinggi dan impact medium. Mitigasi menggunakan landmark smoothing bawaan MediaPipe ditambah moving average filter tambahan dan Kalman filter pada 3D trajectory.

False rep counting merupakan risiko dengan probabilitas medium dan impact tinggi karena merupakan output utama yang dilihat pengguna. Mitigasi menggunakan hysteresis thresholding, minimum transition time, visibility check, dan validasi full cycle sebelum increment counter.

Variasi tipe tubuh pengguna merupakan risiko dengan probabilitas medium dan impact medium. Mitigasi menggunakan normalized angles yang tidak bergantung pada ukuran tubuh absolut, serta potensi adaptive thresholds yang bisa di-tune per pengguna.

Overheating pada camera node saat streaming kontinu merupakan risiko dengan probabilitas medium dan impact rendah. Mitigasi menggunakan heatsink kecil jika diperlukan dan monitoring suhu melalui sensor internal ESP32-S3.

19.2 Risiko Non-Teknis

Keterlambatan pengiriman komponen hardware merupakan risiko yang perlu diperhitungkan dalam timeline proyek. Mitigasi berupa procurement komponen di awal proyek dan identifikasi vendor alternatif.

Penolakan pengguna terhadap tracking band merupakan risiko dimana pengguna merasa terganggu harus memasang band sebelum exercise. Mitigasi berupa desain band yang nyaman dan cepat dipasang, serta menjadikan tracking band sebagai opsi tambahan bukan keharusan karena sistem tetap berfungsi tanpa band meskipun dengan akurasi lebih rendah.


================================================================================
BAB 20 — ANALISIS KOMPETITOR
================================================================================

20.1 Produk Komersial Existing

Tempo Studio menggunakan 3D Time-of-Flight sensor dengan AI. Harganya berkisar Rp 30.000.000 hingga Rp 75.000.000 ditambah langganan bulanan Rp 585.000. Tempo menyediakan real-time form tracking dan auto rep counting untuk berbagai exercise. Target marketnya adalah home gym premium.

Lululemon Mirror sebelumnya bernama Mirror menggunakan kamera dan instruktur virtual. Harganya sekitar Rp 22.500.000 ditambah langganan bulanan Rp 585.000. Form tracking hanya tersedia melalui instruktur yang memantau melalui video, bukan melalui AI otomatis. Target marketnya adalah lifestyle fitness.

Tonal menggunakan electromagnetic resistance dengan sensor built-in. Harganya sekitar Rp 52.500.000 ditambah langganan bulanan Rp 735.000. Form tracking dilakukan melalui data resistance motor dan bukan computer vision. Target marketnya adalah serious strength training.

GymCam merupakan proyek riset dari Carnegie Mellon University yang menggunakan single stationary camera dengan AI. Proyek ini mencapai 93.6 persen accuracy untuk exercise recognition. Target penggunaannya adalah penelitian dan gym monitoring.

20.2 Diferensiasi Fitness Tracking Eye

Sistem yang dibangun berbeda dari produk existing dalam beberapa aspek fundamental. Pertama, multi-camera wireless yang memberikan coverage 360 derajat dimana produk komersial umumnya menggunakan satu sensor atau kamera dari satu sudut saja. Kedua, biaya yang jauh lebih rendah yaitu Rp 1.500.000 hingga Rp 3.000.000 versus Rp 30.000.000 hingga Rp 75.000.000 untuk produk komersial. Ketiga, modular dan upgradeable dimana pengguna bisa mulai dari kamera saja dan menambahkan tracking band atau IMU sensor di kemudian hari tanpa mengubah hardware kamera. Keempat, portable dimana seluruh sistem muat dalam satu backpack sementara produk komersial umumnya merupakan instalasi permanen. Kelima, fokus pada lima exercise spesifik dengan analisis mendalam alih-alih mencoba cover semua exercise secara generik.


================================================================================
BAB 21 — OPSI PAKET UNTUK KLIEN
================================================================================

21.1 Filosofi Penawaran

Mengingat klien bukan orang teknis, penawaran disederhanakan menjadi tiga paket yang mudah dipahami. Klien tidak perlu mengetahui detail teknis seperti pose estimation engine, processing strategy, atau protocol komunikasi. Semua keputusan teknis telah ditentukan oleh tim teknis sebagai konfigurasi optimal.

Yang ditawarkan sebagai opsi kepada klien hanyalah level aksesoris tambahan yang mempengaruhi akurasi dan user experience. Semua paket menggunakan hardware kamera dan software yang sama.

21.2 Paket Basic — Camera Only

Paket ini terdiri dari empat unit modul kamera XIAO ESP32-S3 Sense dengan modul kamera OV2640. Empat unit mini tripod foldable untuk penempatan kamera. Satu unit travel WiFi router. Power adapter atau powerbank untuk setiap kamera. Satu unit ChArUco calibration board. Software aplikasi backend Python dan web dashboard.

Pengguna cukup menempatkan empat kamera di sekitar area latihan, menghubungkannya ke WiFi, melakukan kalibrasi sekali, dan mulai berlatih. Sistem mendeteksi exercise dan menghitung repetisi menggunakan computer vision saja tanpa aksesoris tambahan.

Estimasi biaya hardware adalah Rp 1.500.000 hingga Rp 2.250.000. Akurasi diperkirakan 85 hingga 90 persen. Waktu setup adalah 5 hingga 10 menit. Ini merupakan paket yang direkomendasikan untuk memulai karena paling simple dan sudah memberikan hasil yang baik.

Kelebihannya adalah paling mudah di-setup, paling murah, dan pengguna tidak perlu memakai aksesoris apapun di tubuh. Kekurangannya adalah akurasi bisa menurun saat terjadi occlusion dan saat gerakan sangat cepat.

21.3 Paket Tracking Band — Camera plus Color Band

Paket ini mencakup semua komponen dari Paket Basic ditambah lima buah tracking band berwarna neon dengan tiga ukuran yang berbeda. Dua band Size S berwarna hijau neon dan biru neon untuk pergelangan tangan atau kaki. Dua band Size M berwarna kuning neon dan merah neon untuk paha atau lengan atas. Satu band Size L berwarna putih untuk dada.

Pengguna memasang band sesuai instruksi yang ditampilkan di aplikasi sebelum memulai exercise. Band bisa dipindahkan antar posisi sesuai exercise yang dilakukan. Sistem menggunakan warna band sebagai referensi tambahan untuk meningkatkan akurasi identifikasi bagian tubuh.

Estimasi biaya tambahan adalah Rp 150.000 hingga Rp 225.000 sehingga total menjadi Rp 1.650.000 hingga Rp 2.475.000. Akurasi diperkirakan meningkat menjadi 90 hingga 95 persen. Waktu setup menjadi 7 hingga 12 menit termasuk pemasangan band.

Paket ini merupakan rekomendasi best value karena peningkatan akurasi yang signifikan dengan biaya tambahan yang minimal.

21.4 Paket Pro — Camera plus Tracking Band plus IMU Sensor

Paket ini mencakup semua komponen dari Paket Tracking Band ditambah dua unit IMU sensor wristband yang terdiri dari XIAO ESP32-S3 dengan sensor BMI270 dalam casing wristband. IMU sensor ini dipakai di pergelangan tangan dan memberikan data gerakan 100 kali per detik yang melengkapi data dari kamera.

IMU sensor mendeteksi gerakan bahkan saat kamera tidak bisa melihat karena occlusion, memberikan data gerakan cepat yang mungkin terlewat oleh kamera karena frame rate terbatas, dan meningkatkan akurasi counting terutama untuk gerakan cepat seperti jump.

Estimasi biaya tambahan adalah Rp 300.000 hingga Rp 600.000 sehingga total menjadi Rp 1.950.000 hingga Rp 3.075.000. Akurasi diperkirakan mencapai 95 hingga 98 persen. Waktu setup menjadi 10 hingga 15 menit termasuk pemasangan band dan IMU.

Paket ini direkomendasikan untuk pengguna yang membutuhkan akurasi maksimal. Kekurangannya adalah IMU sensor perlu di-charge secara berkala dan menambah sedikit kerumitan setup.

21.5 Upgrade Path

Arsitektur sistem dirancang modular sehingga pengguna bisa memulai dari Paket Basic dan melakukan upgrade ke paket yang lebih tinggi kapan saja tanpa mengubah hardware kamera atau setup yang sudah ada. Tracking band bisa ditambahkan kapan saja karena hanya membutuhkan update software untuk mengaktifkan fitur color detection. IMU sensor juga bisa ditambahkan belakangan karena arsitektur backend sudah disiapkan untuk menerima data sensor fusion.


================================================================================
BAB 22 — ESTIMASI BIAYA
================================================================================

22.1 Biaya Hardware per Paket

Paket Basic memiliki rincian biaya sebagai berikut. Empat unit XIAO ESP32-S3 Sense dengan harga per unit sekitar Rp 195.000 hingga Rp 225.000 sehingga subtotal Rp 780.000 hingga Rp 900.000. Empat unit mini tripod foldable dengan harga per unit sekitar Rp 75.000 hingga Rp 120.000 sehingga subtotal Rp 300.000 hingga Rp 480.000. Satu unit travel WiFi router seharga sekitar Rp 375.000 hingga Rp 600.000. Empat unit USB-C power adapter atau kabel dengan subtotal sekitar Rp 150.000 hingga Rp 225.000. Satu unit ChArUco calibration board yang dicetak sendiri dengan biaya cetak sekitar Rp 75.000. Total biaya hardware Paket Basic adalah sekitar Rp 1.680.000 hingga Rp 2.280.000.

Paket Tracking Band menambahkan biaya lima unit tracking band neon velcro dengan tiga ukuran seharga total sekitar Rp 150.000 hingga Rp 225.000. Total biaya hardware Paket Tracking Band menjadi sekitar Rp 1.830.000 hingga Rp 2.505.000.

Paket Pro menambahkan biaya dua unit XIAO ESP32-S3 dengan harga per unit sekitar Rp 150.000 hingga Rp 195.000 sehingga subtotal Rp 300.000 hingga Rp 390.000. Dua unit sensor BMI270 breakout board dengan harga per unit sekitar Rp 75.000 hingga Rp 120.000 sehingga subtotal Rp 150.000 hingga Rp 240.000. Dua unit baterai LiPo dan casing wristband dengan subtotal sekitar Rp 150.000 hingga Rp 225.000. Total biaya hardware tambahan Pro sekitar Rp 600.000 hingga Rp 855.000. Total biaya hardware Paket Pro menjadi sekitar Rp 2.430.000 hingga Rp 3.360.000.

22.2 Biaya Recurring

Tidak ada biaya langganan bulanan. Semua software berjalan secara lokal dan tidak membutuhkan layanan cloud berbayar. Biaya recurring hanya meliputi penggantian komponen yang rusak jika diperlukan dan listrik untuk charging perangkat.

22.3 Kebutuhan Hardware yang Sudah Dimiliki

Sistem mengasumsikan pengguna sudah memiliki laptop atau PC sebagai unit pemrosesan utama. Spesifikasi minimum laptop yang direkomendasikan adalah prosesor Intel i5 generasi 10 atau AMD Ryzen 5 3000 series atau yang setara, RAM 8GB atau lebih, WiFi adapter, dan browser modern seperti Chrome, Firefox, atau Edge.


================================================================================
BAB 23 — ROADMAP PENGEMBANGAN
================================================================================

23.1 Fase 1: Core Engine (Minggu 1 hingga 2)

Setup project structure dan environment. Implementasi single webcam dengan MediaPipe pose estimation. Build angle calculator dan smoothing utilities. Implementasi Push Up detection sebagai proof-of-concept dengan terminal-based rep counter. Validasi akurasi counting pada Push Up dengan target error kurang dari 5 persen.

23.2 Fase 2: Semua Exercise (Minggu 3 hingga 4)

Implementasi exercise detector untuk semua lima exercise. Build form analysis untuk setiap exercise dengan scoring system. Implementasi jump metrics calculation untuk Squat Jump dan Vertical Jump. Buat exercise configuration system menggunakan YAML atau JSON untuk menyimpan threshold dan parameter per exercise.

23.3 Fase 3: Multi-Camera (Minggu 5 hingga 7)

Setup XIAO ESP32-S3 Sense firmware untuk MJPEG streaming. Implementasi multi-camera stream manager di backend. Kalibrasi kamera menggunakan ChArUco board. Multi-view 3D reconstruction menggunakan triangulation. Timestamp synchronization antar kamera. Portable kit assembly dan testing.

23.4 Fase 4: Tracking Band (Minggu 8 hingga 9)

Implementasi HSV color detection pipeline. Calibration wizard untuk threshold warna. Fusion logic antara MediaPipe landmarks dan color band centroids. Testing accuracy improvement dengan dan tanpa tracking band. Dokumentasi instruksi pemasangan band per exercise.

23.5 Fase 5: Dashboard dan Polish (Minggu 10 hingga 12)

Web dashboard dengan real-time visualization. Analytics dan session history. Performance optimization. Outdoor testing dan optimization. Dokumentasi pengguna dan hardware setup guide. Comprehensive testing dan validation.

23.6 Fase Opsional: IMU Integration

Setup ESP32-S3 dengan BMI270 untuk IMU wristband. Implementasi BLE atau WiFi data transmission dari IMU ke backend. Sensor fusion engine menggunakan Extended Kalman Filter. Testing accuracy improvement dengan IMU.


================================================================================
BAB 24 — VERIFIKASI DAN PENGUJIAN
================================================================================

24.1 Pengujian Unit

Pengujian unit meliputi test untuk angle calculator yang memvalidasi perhitungan sudut dari berbagai konfigurasi tiga titik. Test untuk exercise detector yang memvalidasi state machine transition dan counting logic menggunakan data keypoint yang disimulasikan. Test untuk pose estimator adapter yang memvalidasi output format konsisten. Test untuk sensor fusion yang memvalidasi weighted average dan Kalman filter output.

24.2 Pengujian Integrasi

Pengujian integrasi meliputi test single camera end-to-end dari capture hingga rep counting. Test multi-camera streaming dengan empat kamera simultan. Test kalibrasi dan 3D reconstruction accuracy. Test tracking band detection dalam berbagai kondisi pencahayaan.

24.3 Pengujian Performa

Benchmark FPS dan latency untuk setiap komponen pipeline. Benchmark total system latency dari capture hingga dashboard display. Stress test dengan streaming empat kamera selama minimal satu jam continuous. Memory usage monitoring untuk memastikan tidak ada memory leak.

24.4 Pengujian Akurasi

Setiap exercise ditest dengan video sample dan real-time webcam. Rep counting accuracy divalidasi manual dengan target error kurang dari 5 persen. Form analysis divalidasi dengan known good form dan bad form videos. Jump height dibandingkan dengan pengukuran manual menggunakan referensi yang diketahui. Test dilakukan pada minimal tiga orang dengan tipe tubuh berbeda untuk memvalidasi robustness.

24.5 Pengujian Lapangan

Test setup di tiga lokasi indoor berbeda untuk memvalidasi portability. Test setup di satu lokasi outdoor untuk memvalidasi outdoor capability. Measurement waktu setup dari backpack hingga ready-to-track. User acceptance testing dengan minimal satu orang non-teknis.


================================================================================
BAB 25 — REFERENSI AKADEMIK DAN TEKNIS
================================================================================

25.1 Riset dan Paper Akademik

GymCam: Detecting, Recognizing and Tracking Simultaneous Exercises in Unconstrained Scenes. Khurana et al. Carnegie Mellon University. UbiComp 2019. Paper ini mendemonstrasikan deteksi exercise dari kamera statis dengan accuracy 93.6 persen.

mmFiT: mmWave Fitness Tracking. TechRxiv. Paper ini mengeksplorasi fitness tracking contactless menggunakan millimeter wave radar.

SmartEdgeSensor3DHumanPose. AIS-Bonn. Framework multi-view 3D pose estimation yang berjalan di edge device.

SelfPose3d. Choi et al. Self-supervised multi-view 3D human pose estimation dari multi-camera.

M3GYM Dataset. Dataset multi-view multi-person gym yang terdiri dari 8 kamera dan 500 lebih aksi.

TotalCapture Dataset. BMVA. Dataset hybrid yang menggabungkan multi-view video, IMU data, dan skeletal ground truth.

BlazePose. Google Research. Paper yang mendeskripsikan arsitektur underlying dari MediaPipe Pose.

RTMPose. OpenMMLab. High-efficiency real-time multi-person pose estimation.

25.2 Library dan Framework

MediaPipe dari Google untuk pose estimation dengan 33 keypoints 3D. OpenCV untuk camera handling, image processing, calibration, dan triangulation. NumPy dan SciPy untuk mathematical operations dan signal processing. filterpy untuk implementasi Kalman filter. FastAPI untuk web server backend dengan WebSocket support. TensorFlow Lite sebagai runtime untuk model MediaPipe.

25.3 Proyek Open Source Referensi

nicknochnack/MediaPipePoseEstimation untuk referensi implementasi basic exercise counter menggunakan MediaPipe.

AIS-Bonn/SmartEdgeSensor3DHumanPose untuk referensi arsitektur multi-view 3D pose estimation.

hongsukchoi/SelfPose3d untuk referensi self-supervised multi-view reconstruction.

Pushtogithub23/Tracking-Physical-Activities-with-MediaPipe-and-OpenCV untuk referensi activity tracking.

FreeMoCap untuk referensi open-source markerless motion capture menggunakan computer vision.


================================================================================
BAB 26 — LAMPIRAN
================================================================================

Lampiran A: Daftar 33 Keypoints MediaPipe BlazePose

Indeks 0 adalah Nose. Indeks 1 adalah Left Eye Inner. Indeks 2 adalah Left Eye. Indeks 3 adalah Left Eye Outer. Indeks 4 adalah Right Eye Inner. Indeks 5 adalah Right Eye. Indeks 6 adalah Right Eye Outer. Indeks 7 adalah Left Ear. Indeks 8 adalah Right Ear. Indeks 9 adalah Mouth Left. Indeks 10 adalah Mouth Right. Indeks 11 adalah Left Shoulder. Indeks 12 adalah Right Shoulder. Indeks 13 adalah Left Elbow. Indeks 14 adalah Right Elbow. Indeks 15 adalah Left Wrist. Indeks 16 adalah Right Wrist. Indeks 17 adalah Left Pinky. Indeks 18 adalah Right Pinky. Indeks 19 adalah Left Index. Indeks 20 adalah Right Index. Indeks 21 adalah Left Thumb. Indeks 22 adalah Right Thumb. Indeks 23 adalah Left Hip. Indeks 24 adalah Right Hip. Indeks 25 adalah Left Knee. Indeks 26 adalah Right Knee. Indeks 27 adalah Left Ankle. Indeks 28 adalah Right Ankle. Indeks 29 adalah Left Heel. Indeks 30 adalah Right Heel. Indeks 31 adalah Left Foot Index. Indeks 32 adalah Right Foot Index.

Lampiran B: Tracking Band Color Mapping per Exercise

Push Up: Hijau Neon di-map ke Left Wrist, Biru Neon di-map ke Right Wrist, Putih di-map ke Chest. Kuning Neon dan Merah Neon tidak digunakan.

Pull Up: Hijau Neon di-map ke Left Wrist, Biru Neon di-map ke Right Wrist, Putih di-map ke Chest. Kuning Neon dan Merah Neon tidak digunakan.

Sit Up: Kuning Neon di-map ke Left Thigh, Merah Neon di-map ke Right Thigh, Putih di-map ke Chest. Hijau Neon dan Biru Neon tidak digunakan.

Squat Jump: Hijau Neon di-map ke Left Ankle, Biru Neon di-map ke Right Ankle, Kuning Neon di-map ke Left Thigh, Merah Neon di-map ke Right Thigh, Putih di-map ke Chest. Semua band digunakan.

Vertical Jump: Hijau Neon di-map ke Left Ankle, Biru Neon di-map ke Right Ankle, Putih di-map ke Chest. Kuning Neon dan Merah Neon tidak digunakan.

Lampiran C: Ringkasan State Machine per Exercise

Push Up memiliki dua state yaitu UP dan DOWN. Threshold DOWN adalah elbow angle kurang dari 100 derajat. Threshold UP adalah elbow angle lebih dari 160 derajat.

Pull Up memiliki dua state yaitu HANG dan UP. Threshold UP adalah nose Y kurang dari wrist Y. Threshold HANG adalah elbow angle lebih dari 160 derajat.

Sit Up memiliki dua state yaitu DOWN dan UP. Threshold UP adalah hip angle kurang dari 70 derajat. Threshold DOWN adalah hip angle lebih dari 140 derajat.

Squat Jump memiliki empat state yaitu STAND, SQUAT, JUMP, dan LAND. Threshold SQUAT adalah knee angle kurang dari 90 derajat. Threshold JUMP adalah ankle Y displacement positif signifikan. Threshold LAND adalah ankle Y kembali ke ground level. Threshold STAND adalah knee angle lebih dari 160 derajat.

Vertical Jump memiliki empat state yaitu STAND, CROUCH, JUMP, dan LAND. Threshold CROUCH adalah knee bend detected. Threshold JUMP adalah ankle Y displacement positif signifikan. Threshold LAND adalah ankle Y kembali ke ground level. Satu repetisi dihitung setelah satu siklus lengkap.

Lampiran D: Daftar Komponen Hardware Paket Lengkap

Komponen kamera terdiri dari empat unit Seeed Studio XIAO ESP32-S3 Sense, empat unit modul kamera OV2640, empat unit mini tripod foldable, empat unit USB-C cable, empat unit USB power adapter 5V 1A, dan satu unit travel WiFi router 5GHz.

Komponen tracking band terdiri dari dua unit neoprene velcro band Size S warna hijau neon dan biru neon, dua unit neoprene velcro band Size M warna kuning neon dan merah neon, dan satu unit elastic strap band Size L warna putih.

Komponen IMU opsional terdiri dari dua unit Seeed Studio XIAO ESP32-S3, dua unit sensor BMI270 breakout board, dua unit baterai LiPo 300mAh, dan dua unit wristband case 3D printed.

Komponen kalibrasi terdiri dari satu unit ChArUco board cetak pada material rigid ukuran A3.

Komponen processing terdiri dari satu unit laptop atau PC dengan spesifikasi minimum Intel i5 Gen 10 atau setara, RAM 8GB, WiFi adapter, dan browser modern. Laptop tidak termasuk dalam paket dan diasumsikan sudah dimiliki pengguna.


================================================================================
BAB 27 — REKOMENDASI KONFIGURASI FINAL UNTUK KLIEN
================================================================================

Untuk menghindari kebingungan klien akibat terlalu banyak opsi teknis, bab ini menyederhanakan seluruh hasil riset menjadi 3 Konfigurasi Final (Fixed Configurations). Klien hanya perlu memilih salah satu dari tiga konfigurasi ini tanpa perlu memikirkan detail komponen di dalamnya.

27.1 Konfigurasi 1: BASIC STUDIO KIT (Indoor/Fixed Setup)
Konfigurasi ini dirancang untuk studio gym atau penggunaan dalam ruangan di mana akses listrik selalu tersedia. Ini adalah opsi termurah dan paling bebas perawatan (maintenance-free).
- Mata Kamera: 4x XIAO ESP32-S3 Sense + Lensa OV2640.
- Sumber Daya: USB-C Power Adapter 5V 1A. (Dicolok langsung ke listrik). Kelebihannya, sistem bisa menyala 24/7 tanpa perlu repot mengisi daya baterai.
- Mount: 4x Mini Tripod.
- Aksesoris Tubuh: Tidak ada. Sistem sepenuhnya bergantung pada AI MediaPipe untuk mendeteksi tubuh (Markerless).
- Target Pengguna: Klien yang ingin setup permanen di ruangan terang.

27.2 Konfigurasi 2: PORTABLE TRACKING KIT (Outdoor/Mobile Setup)
Konfigurasi ini dirancang untuk pelatih yang sering berpindah lokasi (taman, rumah klien) di mana akses listrik sulit didapatkan, namun membutuhkan akurasi tinggi.
- Mata Kamera: 4x XIAO ESP32-S3 Sense + Lensa OV2640.
- Sumber Daya: Mini Powerbank 5000mAh per kamera. Kami merekomendasikan powerbank mini berukuran tabung/lipstik (harga sekitar Rp 75.000 - Rp 120.000) yang sangat praktis dan murah. Powerbank ini cukup untuk menyuplai daya selama 15-20 jam nonstop, dan sangat mudah diganti (plug-and-play) jika rusak, tanpa perlu membongkar casing kamera.
- Aksesoris Tubuh: 1 Set Tracking Band (Gelang warna neon).
- Target Pengguna: Pelatih keliling atau event fitness outdoor.

27.3 Konfigurasi 3: PRO KIT (Max Accuracy & Max Battery)
Konfigurasi tertinggi yang menggabungkan semua sensor untuk akurasi level profesional, dengan sistem power custom yang dirancang untuk ketahanan maksimal dengan biaya sangat rendah.
- Mata Kamera: 4x XIAO ESP32-S3 Sense + Lensa OV2640.
- Sumber Daya Custom: Baterai 18650 2P (Parallel). Alih-alih powerbank, kita menggunakan casing khusus yang memuat 2 buah baterai lithium 18650 yang disusun secara paralel (3.7V). 
  - Alasan menggunakan 2P: Board XIAO memiliki chip manajemen daya bawaan yang mendukung baterai 3.7V. Dengan susunan 2P, kita mendapatkan kapasitas masif (sekitar 6000mAh - 7000mAh) hanya dengan biaya Rp 90.000 - Rp 120.000 untuk dua baterai + holder.
  - Alasan TIDAK menggunakan 2S: Konfigurasi 2S (Series) menghasilkan 7.4V, yang akan membakar board XIAO secara langsung kecuali kita menambahkan modul penurun tegangan (Buck Converter) ke 5V. Konfigurasi 2P jauh lebih simpel, murah, aman, dan bisa di-charge langsung dari port USB-C di board XIAO.
- Aksesoris Tubuh: 1 Set Tracking Band (Gelang warna neon).
- Sensor Tambahan: 2x IMU Wristband (Sensor gerak di pergelangan tangan).
- Target Pengguna: Atlet profesional, analis olahraga, dan klien premium yang menuntut akurasi tertinggi tanpa kompromi.


AKHIR DOKUMEN

Dokumen ini disusun berdasarkan riset mendalam yang dilakukan pada September 2026. Semua data teknis dan rekomendasi telah divalidasi melalui studi literatur akademik, dokumentasi teknis vendor, dan benchmark dari komunitas open source. Dokumen ini menjadi acuan utama untuk pengembangan proposal yang akan diajukan kepada klien.
