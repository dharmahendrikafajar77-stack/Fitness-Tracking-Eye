# Instrumen Lengkap & Rubrik Konsultasi Pakar FIK (Sports Science & Kinesiology)
## Proyek: Fitness Tracking Eye - Edge AI Motion Capture & Biomechanical Analysis

> **Tujuan Dokumen**:
> Dokumen ini dirancang sebagai lembar kerja instrumen teknis saat berkonsultasi dengan dosen, akademisi, atau mahasiswa **Fakultas Ilmu Keolahragaan (FIK)**. Tujuannya adalah mengekstraksi parameter numerik definitif (derajat sudut sendi, toleransi *Range of Motion*, serta kriteria pembatalan repetisi/*No-Rep*) untuk 5 gerakan uji kebugaran jasmani.
>
> Data numerik dari rubrik ini akan langsung ditransformasikan menjadi logika ambang batas (*threshold hysteresis*) pada file sistem [config/exercise_config.yaml](file:///d:/Aaa/Repo/Fitness-Tracking-Eye/config/exercise_config.yaml).

---

## DAFTAR ISI
1. [Standar Protokol Uji Kebugaran yang Digunakan](#1-standar-protokol-uji-kebugaran-yang-digunakan)
2. [Siklus Fase Gerakan (State Machine Lifecycle)](#2-siklus-fase-gerakan-state-machine-lifecycle)
3. [Rubrik Rinci Gerakan 1: PUSH UP](#3-rubrik-rinci-gerakan-1-push-up)
4. [Rubrik Rinci Gerakan 2: SIT UP](#4-rubrik-rinci-gerakan-2-sit-up)
5. [Rubrik Rinci Gerakan 3: SQUAT JUMP](#5-rubrik-rinci-gerakan-3-squat-jump)
6. [Rubrik Rinci Gerakan 4: VERTICAL JUMP](#6-rubrik-rinci-gerakan-4-vertical-jump)
7. [Rubrik Rinci Gerakan 5: PULL UP](#7-rubrik-rinci-gerakan-5-pull-up)
8. [Matriks Klasifikasi Kesalahan (Minor Fault vs Major No-Rep vs Disqualification)](#8-matriks-klasifikasi-kesalahan)
9. [Pedoman Geometri Kamera & Tata Ruang Lapangan (Sweet Spot 2 Kamera)](#9-pedoman-geometri-kamera--tata-ruang-lapangan)

---

## 1. Standar Protokol Uji Kebugaran yang Digunakan

Sebelum memulai pengujian teknis, mintalah narasumber FIK mengonfirmasi standar operasional prosedur (SOP) acuan utama:

* [ ] **Standar Tes Kesamaptaan Jasmani TNI (AD/AL/AU)** (Siklus 1 menit, aturan strict).
* [ ] **Standar Tes Kesamaptaan Jasmani POLRI** (Siklus 1 menit, kriteria kelulusan komprehensif).
* [ ] **Standar Tes Kebugaran Jasmani Indonesia (TKJI) / Kemenpora** (Standar umum pelajar/mahasiswa/atlet daerah).
* [ ] **Standar American College of Sports Medicine (ACSM) / NSCA** (Standar internasional *strength & conditioning*).

> **Catatan untuk Pewawancara**: Catat jika ada variasi standar antara pengujian militer/kedinasan dengan kebugaran sipil. Sistem kita dirancang modular sehingga profil threshold dapat dialihkan melalui file konfigurasi YAML.

---

## 2. Siklus Fase Gerakan (State Machine Lifecycle)

Setiap gerakan dalam sistem AI dimodelkan sebagai mesin status (*Finite State Machine*) 6 fase:

```
[Fase 0: Entry/Standby] -> [Fase 1: Postur Awal Sah] -> [Fase 2: Eksentrik (Turun/Turun)]
                                                                  |
[Fase 5: Sah 1 Repetisi] <- [Fase 4: Konsentrik (Naik)] <- [Fase 3: Titik Puncak ROM (Inflection)]
```

* **Fase 0 (Standby / Readiness)**: Atlet berdiri atau bersiap memasuki zona pandang kamera.
* **Fase 1 (Starting Posture Locked)**: Tubuh dalam posisi awal yang sah selama minimal 1.0 detik sebelum hitungan dimulai.
* **Fase 2 (Eccentric Phase)**: Gerakan menuju titik beban maksimal (turun pada push up/squat, rebah pada sit up).
* **Fase 3 (Inflection Point / Peak Depth)**: Titik ekstrem *Range of Motion* (ROM). Kunci validitas repetisi.
* **Fase 4 (Concentric Phase)**: Usaha mengangkat/mendorong kembali ke posisi awal.
* **Fase 5 (Lockout / Rep Completed)**: Penguncian sendi di posisi awal; 1 poin repetisi ditambahkan ke papan skor.

---

## 3. Rubrik Rinci Gerakan 1: PUSH UP

### A. Anatomi & Sendi Utama yang Dilacak AI
* **Siku (*Elbow*)**: Sudut antara Bahu (*Shoulder*) - Siku (*Elbow*) - Pergelangan Tangan (*Wrist*).
* **Garis Tulang Punggung (*Body Line*)**: Sudut antara Bahu (*Shoulder*) - Panggul (*Hip*) - Pergelangan Kaki (*Ankle*).
* **Keseimbangan Bahu (*Shoulder Tilt*)**: Sudut kemiringan horizontal garis Bahu Kiri ke Bahu Kanan.
* **Bukaan Telapak Tangan (*Hand Stance*)**: Rasio jarak pergelangan tangan (*wrist-to-wrist*) terhadap lebar bahu (*shoulder-to-shoulder*).

### B. Lembar Isian Pertanyaan Konsultasi FIK

| No | Parameter Biomekanik | Opsi Standar / Nilai Default AI | Jawaban / Ketetapan Pakar FIK |
| :---: | :--- | :--- | :--- |
| **1.1** | **Posisi Awal Lengan (*Lockout*)** | Siku lurus penuh $\ge 160^\circ$. | Sudut minimal: `.......` derajat |
| **1.2** | **Kedalaman Siku Minimum (*Down Threshold*)** | Sudut siku $\le 90^\circ$ (paha & dada tidak menyentuh lantai). | Sudut maksimal siku di bawah: `.......` derajat |
| **1.3** | **Jarak Dada ke Lantai** | Sekitar 1 kepalan tangan (~8–10 cm dari lantai). | Standar jarak dada: `.......` cm |
| **1.4** | **Kelurusan Tulang Belakang (*Plank Line*)** | Garis bahu-panggul-tumit $\ge 155^\circ$ (toleransi sag $15^\circ$). | Sudut minimal garis tubuh: `.......` derajat |
| **1.5** | **Batas Pelanggaran Pinggul Melorot (*Hip Sag*)** | Sudut bahu-panggul-lutut $< 150^\circ$. | Batas sudut hip sag: `.......` derajat |
| **1.6** | **Batas Pelanggaran Pantat Menungging (*Pike*)** | Sudut bahu-panggul-lutut $< 145^\circ$ ke arah atas. | Batas sudut hip pike: `.......` derajat |
| **1.7** | **Bukaan Telapak Tangan** | $1.0\times - 1.5\times$ lebar bahu. | Toleransi bukaan: `.......` $\times$ lebar bahu |
| **1.8** | **Orientasi Jari Tangan** | Menghadap lurus ke depan (toleransi serong luar $15^\circ$). | Standar jari tangan: `....................` |
| **1.9** | **Posisi Kepala & Leher** | Netral memandang lantai 20 cm di depan tangan. | Standar posisi kepala: `....................` |
| **1.10** | **Posisi Kaki & Jari Kaki** | Rapat atau terbuka maksimal selebar panggul (10–20 cm). | Jarak maksimal antar kaki: `.......` cm |
| **1.11** | **Aturan Istirahat (*Resting Rule*)** | Hanya boleh istirahat di posisi plank atas (lengan lurus). | Maksimal waktu istirahat: `.......` detik |
| **1.12** | **Diskualifikasi Instan (*Foul/DQ*)** | Lutut menyentuh lantai, atau merebahkan badan penuh. | Kriteria DQ: `................................` |

---

## 4. Rubrik Rinci Gerakan 2: SIT UP

### A. Anatomi & Sendi Utama yang Dilacak AI
* **Sudut Panggul (*Hip Flexion Angle*)**: Sudut antara Bahu (*Shoulder*) - Panggul (*Hip*) - Lutut (*Knee*).
* **Sudut Fleksi Lutut (*Knee Angle*)**: Sudut antara Panggul (*Hip*) - Lutut (*Knee*) - Pergelangan Kaki (*Ankle*).
* **Stabilitas Tumit (*Heel Anchoring*)**: Perpindahan vertikal koordinat tumit (*ankle landmark y-displacement*).
* **Simetri Bukaan Lutut**: Jarak horizontal lutut kiri terhadap lutut kanan dari kamera depan.

### B. Lembar Isian Pertanyaan Konsultasi FIK

| No | Parameter Biomekanik | Opsi Standar / Nilai Default AI | Jawaban / Ketetapan Pakar FIK |
| :---: | :--- | :--- | :--- |
| **2.1** | **Posisi Awal Telentang (*Down Threshold*)** | Punggung & tulang belikat (*scapula*) menempel matras, sudut panggul $\ge 130^\circ$. | Sudut minimal posisi bawah: `.......` derajat |
| **2.2** | **Posisi Puncak Sah (*Up Threshold*)** | Sudut panggul $\le 70^\circ$ (badan tegak mendekati paha). | Sudut maksimal posisi atas: `.......` derajat |
| **2.3** | **Sentuhan Titik Puncak** | Siku menyentuh lutut atau melewati garis paha atas. | Syarat sentuhan puncak: `....................` |
| **2.4** | **Posisi Tangan Resmi** | *Opsi A*: Jari saling mengunci di belakang kepala.<br>*Opsi B*: Menempel di pelipis (*temple*).<br>*Opsi C*: Menyilang di depan dada (*arms crossed*). | Opsi resmi yang dipilih: `Opsi A / B / C` |
| **2.5** | **Pelanggaran Tangan Terlepas** | Tangan terlepas dari kepala/pelipis saat menarik tubuh. | Apakah membatalkan rep? `Ya / Tidak` |
| **2.6** | **Sudut Tekukan Lutut** | Fleksi lutut membentuk sudut $80^\circ - 100^\circ$ (nominal $90^\circ$). | Rentang sudut lutut: `.......` s/d `.......` derajat |
| **2.7** | **Bantuan Penahan Kaki (*Feet Anchored*)** | Apakah kaki dipegang partner / penahan kaki, atau bebas? | Kondisi kaki: `Dipegang / Mandiri Bebas` |
| **2.8** | **Toleransi Tumit Terangkat (*Heel Lift*)** | Tumit terangkat dari lantai maksimal 5 cm / pergeseran 10%. | Batas toleransi angkat tumit: `.......` cm |
| **2.9** | **Pelanggaran Mengayun Pantat (*Hip Thrusting*)** | Mengangkat pantat dari matras untuk mendapat momentum pantulan. | Apakah membatalkan rep? `Ya / Tidak` |
| **2.10** | **Posisi Istirahat yang Sah** | Boleh istirahat di posisi duduk tegak (*UP*) atau telentang (*DOWN*)? | Posisi istirahat sah: `Atas / Bawah / Keduanya` |
| **2.11** | **Batas Waktu Jeda Diam** | Berhenti bergerak maksimal 3 detik sebelum hitungan disetop. | Maksimal waktu jeda diam: `.......` detik |

---

## 5. Rubrik Rinci Gerakan 3: SQUAT JUMP

### A. Anatomi & Sendi Utama yang Dilacak AI
* **Kedalaman Lutut (*Knee Flexion Angle*)**: Sudut antara Panggul (*Hip*) - Lutut (*Knee*) - Pergelangan Kaki (*Ankle*).
* **Sudut Panggul (*Hip Hinge Angle*)**: Sudut antara Bahu (*Shoulder*) - Panggul (*Hip*) - Lutut (*Knee*).
* **Penyimpangan Lutut (*Knee Valgus / Varus*)**: Rasio jarak antar-lutut terhadap jarak antar-pergelangan kaki dari kamera depan.
* **Tinggi Lompatan (*Airborne Clearance*)**: Jarak terangkatnya ujung jari kaki (*toe landmark*) dari lantai.

### B. Lembar Isian Pertanyaan Konsultasi FIK

| No | Parameter Biomekanik | Opsi Standar / Nilai Default AI | Jawaban / Ketetapan Pakar FIK |
| :---: | :--- | :--- | :--- |
| **3.1** | **Posisi Berdiri Tegak (*Starting Stand*)** | Lutut & panggul lurus $\ge 160^\circ$. | Sudut minimal berdiri: `.......` derajat |
| **3.2** | **Kedalaman Jongkok Minimal (*Squat Threshold*)** | Sudut lutut $\le 95^\circ$ (paha minimal sejajar lantai/*parallel squat*). | Sudut maksimal lutut di bawah: `.......` derajat |
| **3.3** | **Posisi Lutut vs Jari Kaki (*Knee Over Toe*)** | Lutut tidak boleh maju melebihi 5 cm di depan ujung jari kaki. | Toleransi lutut maju: `.......` cm |
| **3.4** | **Posisi Tangan** | Tangan saling mengunci di belakang tengkuk leher. | Posisi tangan yang diakui: `....................` |
| **3.5** | **Kelurusan Tulang Belakang (*Torso Lean*)** | Dada condong ke depan maksimal $35^\circ - 45^\circ$, tidak membungkuk. | Batas condong dada: `.......` derajat |
| **3.6** | **Fase Melayang (*Airborne Clearance*)** | Kaki harus lepas kontak penuh dari lantai minimal 5–10 cm. | Tinggi lompatan minimal: `.......` cm |
| **3.7** | **Pendaratan Aman (*Soft Landing Cushion*)** | Lutut wajib langsung menekuk lentur ($\le 140^\circ$) saat mendarat. | Batas sudut lutut mendarat: `.......` derajat |
| **3.8** | **Pelanggaran Lutut Masuk (*Knee Valgus*)** | Jarak kedua lutut $< 70\%$ dari jarak kedua pergelangan kaki. | Toleransi penyempitan lutut: `.......` % |
| **3.9** | **Asimetri Pendaratan** | Selisih waktu atau ketinggian pendaratan kaki kiri vs kanan. | Toleransi selisih landing: `.......` ms / cm |

---

## 6. Rubrik Rinci Gerakan 4: VERTICAL JUMP

### A. Anatomi & Sendi Utama yang Dilacak AI
* **Perpindahan Panggul Vertikal ($\Delta Y_{hip}$)**: Mengukur selisih ketinggian titik panggul berdiri netral vs titik tertinggi di udara.
* **Waktu Melayang (*Flight Time $t$*)**: Menggunakan rumus fisika balistik: $h = \frac{1}{8} g t^2$.
* **Sudut Jongkok Persiapan (*Countermovement Crouch*)**: Sudut fleksi lutut sesaat sebelum tolakan.
* **Simetri Ayunan Lengan (*Arm Swing Clearance*)**: Ketinggian dan sinkronisasi kedua pergelangan tangan.

### B. Lembar Isian Pertanyaan Konsultasi FIK

| No | Parameter Biomekanik | Opsi Standar / Nilai Default AI | Jawaban / Ketetapan Pakar FIK |
| :---: | :--- | :--- | :--- |
| **4.1** | **Metode Pengujian yang Sah** | *Opsi A*: Countermovement Jump / CMJ (awalan ayunan bebas).<br>*Opsi B*: Squat Jump / SJ (statis dari jongkok tanpa awalan).<br>*Opsi C*: Sargent Jump Test (sentuhan papan skor dinding). | Protokol resmi yang dipakai: `Opsi A / B / C` |
| **4.2** | **Metode Komputasi AI yang Diakui** | *Metode 1*: *Flight Time Duration* ($h = \frac{1}{8} g t^2$).<br>*Metode 2*: *Landmark Peak Displacement* ($\Delta Y$ panggul dalam skala piksel ke cm). | Metode prioritas: `Metode 1 / 2 / Fusi` |
| **4.3** | **Persiapan Jongkok (*Crouch Angle*)** | Bebas sesuai kenyamanan atlet, rata-rata $100^\circ - 120^\circ$. | Apakah ada batas kedalaman awalan? `.......` |
| **4.4** | **Bantuan Ayunan Lengan (*Arm Swing*)** | Lengan diayun bebas ke atas kepala untuk tolakan maksimal. | Apakah tangan boleh bebas mengayun? `Ya / Tidak` |
| **4.5** | **Pelanggaran Menekuk Kaki di Udara (*Tucking Foul*)** | Menekuk lutut ke dada saat di udara untuk memanipulasi waktu melayang. | Apakah menekuk kaki membatalkan tes? `Ya / Tidak` |
| **4.6** | **Titik Pendaratan (*Landing Zone*)** | Kaki harus mendarat di area yang sama (tidak melompat maju/mundur $> 25\text{ cm}$). | Toleransi pergeseran titik jatuh: `.......` cm |
| **4.7** | **Jumlah Percobaan Sah (*Trial Policy*)** | Atlet diberikan 2 atau 3 kali percobaan, nilai tertinggi yang diambil. | Jumlah percobaan resmi: `.......` kali |

---

## 7. Rubrik Rinci Gerakan 5: PULL UP

### A. Anatomi & Sendi Utama yang Dilacak AI
* **Sudut Siku (*Elbow Angle*)**: Sudut antara Bahu (*Shoulder*) - Siku (*Elbow*) - Pergelangan Tangan (*Wrist*).
* **Posisi Dagu vs Mistar (*Chin Over Bar*)**: Koordinat Y dagu (*chin*) melampaui koordinat Y palang horizontal (*bar*).
* **Ayunan Panggul / Kipping (*Hip Sway Deviation*)**: Pergeseran horizontal panggul dari sumbu gravitasi lurus.

### B. Lembar Isian Pertanyaan Konsultasi FIK

| No | Parameter Biomekanik | Opsi Standar / Nilai Default AI | Jawaban / Ketetapan Pakar FIK |
| :---: | :--- | :--- | :--- |
| **5.1** | **Jenis Pegangan Palang (*Grip Style*)** | *Opsi A*: Pronated / Overhand (Telapak tangan menghadap depan - Pull Up murni).<br>*Opsi B*: Supinated / Underhand (Telapak tangan menghadap wajah - Chin Up). | Standar pegangan resmi: `Overhand / Bebas` |
| **5.2** | **Posisi Menggantung Penuh (*Dead Hang*)** | Lengan lurus penuh $\ge 165^\circ - 180^\circ$. | Sudut minimal lengan posisi bawah: `.......` derajat |
| **5.3** | **Ketinggian Angkat Sah (*Chin Clearance*)** | Dagu harus melewati bidang atas palang (*chin fully above bar*). | Syarat puncak: `Dagu lewat palang / Dada sentuh` |
| **5.4** | **Pelanggaran Mendongakkan Dagu (*Head Tilting Cheat*)** | Mendongakkan kepala ke atas secara berlebihan padahal bahu belum naik. | Batas toleransi kemiringan leher: `.......` derajat |
| **5.5** | **Pelanggaran Ayunan Kaki / Kipping (*Kipping Foul*)** | Mengayunkan kaki atau pinggul untuk menciptakan momentum dorongan. | Toleransi ayunan tubuh: `.......` derajat deviasi |
| **5.6** | **Posisi Kaki yang Sah** | Lurus ke bawah atau boleh disilangkan di belakang lutut? | Standar posisi kaki: `Lurus / Bebas` |
| **5.7** | **Kaki Menyentuh Tanah/Tiang** | Kaki tidak boleh menyentuh lantai atau tiang penyangga kapan pun. | Apakah otomatis foul? `Ya / Tidak` |
| **5.8** | **Istirahat Menggantung** | Atlet hanya boleh istirahat di posisi dead hang (tidak boleh melepas pegangan). | Maksimal waktu menggantung diam: `.......` detik |

---

## 8. Matriks Klasifikasi Kesalahan

Berdasarkan kesepakatan dengan FIK, bagi jenis kesalahan ke dalam 3 tingkatan keparahan (*severity levels*):

```
+-----------------------------------------------------------------------------------+
| LEVEL 1: PENALTI FORM (MINOR FAULT)                                               |
| Repetisi TETAP DIHITUNG, namun skor kualitas biomekanik (*form score*) berkurang. |
| Contoh: Bukaan tangan sedikit terlalu lebar, tempo sedikit tersentak.             |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| LEVEL 2: REPETISI BATAL (MAJOR NO-REP)                                            |
| Repetisi TIDAK DIHITUNG sama sekali karena tidak memenuhi syarat rentang gerak.   |
| Contoh: Siku push up tidak mencapai 90 derajat, dagu tidak melewati palang pull up|
| pantat terangkat saat sit up.                                                     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| LEVEL 3: DISKUALIFIKASI / SELESAI (SESSION TERMINATION)                           |
| Sesi pengujian otomatis DIHENTIKAN karena melanggar aturan integritas tes fisik.  |
| Contoh: Lutut menyentuh lantai saat push-up, melepas palang pull-up, atau         |
| berhenti diam melebihi batas waktu istirahat yang diizinkan (misal > 5 detik).   |
+-----------------------------------------------------------------------------------+
```

---

## 9. Pedoman Geometri Kamera & Tata Ruang Lapangan

Bagikan diagram tata letak ini kepada tim FIK untuk memvalidasi arena pengujian:

```
                          [ KAMERA 1: FRONTAL / PV1 ]
                               (Tinggi: 75-85 cm)
                               (Tilt: 12-18 derajat ke bawah)
                                      |
                                      | Jarak: 2.5 - 2.8 Meter
                                      v
                             +-----------------+
                             |   [ KEPALA ]    |
                             |        |        |
[ KAMERA 2: SAGITTAL / PV2 ] |    [ BADAN ]    | <--- MATRAS LATIHAN (1.8m x 0.6m)
  (Tinggi: 45-55 cm)         |        |        |
  (Tilt: 0-5 derajat datar)  |    [ KAKI ]     |
  (Jarak: 2.8 - 3.2 Meter)   +-----------------+
```

### Check-list Persiapan Pengambilan Data Uji Coba:
1. [ ] Matras tidak licin dan berwarna kontras dengan lantai/dinding.
2. [ ] Pakaian atlet: Celana pendek/training pas di badan (*slim-fit*) dan kaos kontras (hindari pakaian gombrong/longgar yang menutupi sendi lutut dan siku).
3. [ ] Pencahayaan ruangan minimal 300 lux (terang merata tanpa bayangan gelap ekstrem).
4. [ ] Tandai lantai dengan selotip penanda (*cross mark*) untuk posisi tripod Kamera 1 dan Kamera 2 agar replikasi pengujian presisi di setiap sesi.
