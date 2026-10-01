"""
Generate a professional .docx comparison document
harmonized with the original Proposal Fitness Tracking Eye style.
"""
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

doc = Document()

# ── Page Setup ──
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2.5)

# ── Styles ──
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

def add_heading_styled(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)
    return h

def add_table_with_style(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(9)
    # Rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return table

def add_bold_para(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(11)
    return p

# ═══════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════
doc.add_paragraph()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('LAMPIRAN TEKNIS')
run.bold = True
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x5C)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Analisis Perbandingan Arsitektur Sistem')
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0x44, 0x72, 0xC4)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Rancangan v1 (4× XIAO ESP32-S3 Sense)\nvs\nRancangan v2 (2× Raspberry Pi AI Camera)')
run.font.size = Pt(13)

doc.add_paragraph()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Dokumen Pendukung Proposal\nPengembangan Sistem Fitness Tracking Eye Terintegrasi')
run.font.size = Pt(11)
run.italic = True

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('HowArts Technology')
run.bold = True
run.font.size = Pt(14)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Padang, Oktober 2026')
run.font.size = Pt(11)

doc.add_page_break()

# ═══════════════════════════════════════════════
# DAFTAR ISI
# ═══════════════════════════════════════════════
add_heading_styled('DAFTAR ISI', level=1)
toc_items = [
    'BAB 1  Pendahuluan & Latar Belakang Revisi',
    'BAB 2  Perbandingan Arsitektur Inti',
    'BAB 3  Perbandingan Spesifikasi Hardware',
    'BAB 4  Perbandingan Rincian Anggaran Biaya (RAB)',
    'BAB 5  Perbandingan Arsitektur Software & Kompleksitas Koding',
    'BAB 6  Perbandingan Keandalan Sistem (Reliability)',
    'BAB 7  Perbandingan Performa & Latency',
    'BAB 8  Perbandingan Portabilitas & Coverage per Exercise',
    'BAB 9  Temuan Kritis pada Rancangan v1',
    'BAB 10 Matriks Keputusan Final (Weighted Scoring)',
    'BAB 11 Rekomendasi & Langkah Selanjutnya',
]
for item in toc_items:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(2)
doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 1
# ═══════════════════════════════════════════════
add_heading_styled('BAB 1  PENDAHULUAN & LATAR BELAKANG REVISI', level=1)

add_heading_styled('1.1 Tujuan Dokumen', level=2)
doc.add_paragraph(
    'Dokumen ini merupakan lampiran teknis dari Proposal Pengembangan Sistem '
    'Fitness Tracking Eye Terintegrasi. Dokumen ini menyajikan hasil analisis '
    'perbandingan mendalam antara dua alternatif arsitektur perangkat keras '
    'yang dapat digunakan sebagai fondasi sistem, beserta dampaknya terhadap '
    'biaya, keandalan, performa, kompleksitas pengembangan, dan portabilitas.'
)

add_heading_styled('1.2 Latar Belakang Revisi', level=2)
doc.add_paragraph(
    'Dalam proses riset dan validasi teknis pasca-penyusunan proposal awal, '
    'ditemukan beberapa celah kritis pada rancangan perangkat keras yang '
    'berpotensi menghambat keberhasilan sistem di lapangan. Temuan utama '
    'meliputi:'
)
findings = [
    'Mikrokontroler XIAO ESP32-S3 Sense hanya mendukung WiFi 2.4GHz, '
    'bukan 5GHz seperti yang tertulis di proposal awal.',
    'Pengiriman 4 aliran video MJPEG secara simultan melalui WiFi 2.4GHz '
    'berisiko tinggi mengalami congestion (kemacetan) dan frame drop.',
    'Beban komputasi AI (4 instance MediaPipe paralel) di perangkat utama '
    '(Laptop) tidak disebutkan secara eksplisit di proposal, padahal '
    'membutuhkan spesifikasi GPU dedicated.',
    'Tersedianya teknologi Raspberry Pi AI Camera (Sony IMX500) yang mampu '
    'menjalankan AI langsung di dalam sensor kamera, mengeliminasi kebutuhan '
    'pengiriman video dan pemrosesan AI terpusat.',
]
for f in findings:
    doc.add_paragraph(f, style='List Bullet')

add_heading_styled('1.3 Dua Alternatif yang Dibandingkan', level=2)
add_table_with_style(
    ['Aspek', 'Rancangan v1 (Proposal Asli)', 'Rancangan v2 (Revisi Baru)'],
    [
        ['Nama Kode', 'Central Processing', 'Edge AI Processing'],
        ['Jumlah Kamera', '4 unit', '2 unit'],
        ['Hardware Kamera', 'XIAO ESP32-S3 Sense + OV5640', 'Raspberry Pi AI Camera (Sony IMX500)'],
        ['Host/Pengontrol', 'ESP32-S3 (built-in)', 'Raspberry Pi Zero 2 W'],
        ['Lokasi AI Processing', 'Central (di Laptop/PC)', 'Edge (di dalam sensor kamera)'],
        ['Data via WiFi', 'Video mentah MJPEG (~3 Mbps/kamera)', 'Teks JSON skeleton (~1 KB/frame)'],
        ['Frekuensi WiFi', '2.4 GHz saja (BUKAN 5GHz)', '2.4 GHz (cukup untuk teks)'],
        ['Coverage Sudut Pandang', '360° (4 titik)', '~180° (2 titik orthogonal 90°)'],
    ]
)

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 2
# ═══════════════════════════════════════════════
add_heading_styled('BAB 2  PERBANDINGAN ARSITEKTUR INTI', level=1)

add_heading_styled('2.1 Aliran Data Rancangan v1 (Central Processing)', level=2)
doc.add_paragraph(
    'Dalam arsitektur v1, keempat kamera ESP32-S3 mengirimkan aliran video '
    'mentah (format MJPEG, resolusi VGA 640×480, 15–20 FPS) melalui jaringan '
    'WiFi 2.4GHz ke perangkat utama (Laptop). Laptop kemudian menjalankan '
    'empat instance MediaPipe BlazePose secara paralel untuk mengekstrak '
    'koordinat 33 keypoints tubuh dari masing-masing aliran video.'
)
doc.add_paragraph('Bandwidth WiFi yang dibutuhkan: ~8–12 Mbps (4 video sekaligus)')
doc.add_paragraph('Beban CPU Laptop: SANGAT TINGGI (4 instance MediaPipe paralel)')
doc.add_paragraph('Titik kegagalan: WiFi congestion, frame drop, CPU overload')

add_heading_styled('2.2 Aliran Data Rancangan v2 (Edge AI Processing)', level=2)
doc.add_paragraph(
    'Dalam arsitektur v2, kedua kamera Raspberry Pi AI Camera menjalankan '
    'Neural Network langsung di dalam sensor Sony IMX500. Kamera menghasilkan '
    'koordinat skeleton (bukan gambar video), yang kemudian diteruskan oleh '
    'Raspberry Pi Zero 2 W dalam format JSON ringan melalui WiFi.'
)
doc.add_paragraph('Bandwidth WiFi yang dibutuhkan: ~0.1–0.5 Mbps (hanya teks JSON)')
doc.add_paragraph('Beban CPU Laptop/HP: SANGAT RINGAN (hanya matematika sudut)')
doc.add_paragraph('Titik kegagalan: Minimal')

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 3
# ═══════════════════════════════════════════════
add_heading_styled('BAB 3  PERBANDINGAN SPESIFIKASI HARDWARE', level=1)

add_heading_styled('3.1 Spesifikasi Sensor Kamera', level=2)
add_table_with_style(
    ['Spesifikasi', 'OV5640 (v1)', 'Sony IMX500 (v2)'],
    [
        ['Resolusi Maksimum', '5 MP (2592×1944)', '12.3 MP (4056×3040)'],
        ['FPS Efektif Proyek', '15–20 FPS (VGA, MJPEG)', '30 FPS (binned 2028×1520)'],
        ['AI On-Chip', '❌ Tidak ada', '✅ Neural Network Accelerator'],
        ['Ukuran Modul', '~20×20 mm', '~25×24×12 mm'],
        ['Kualitas Gambar', 'Standar', 'Profesional (sensor Sony)'],
        ['Harga per Unit (Lokal)', '~Rp 225.000 (incl. ESP32)', '~Rp 2.000.000'],
    ]
)

add_heading_styled('3.2 Spesifikasi Mikrokontroler / Host', level=2)
add_table_with_style(
    ['Spesifikasi', 'XIAO ESP32-S3 (v1)', 'RPi Zero 2 W (v2)'],
    [
        ['Klasifikasi', 'Mikrokontroler', 'Single Board Computer (SBC)'],
        ['Prosesor', 'Xtensa LX7, 2-core 240MHz', 'ARM Cortex-A53, 4-core 1GHz'],
        ['RAM', '8 MB PSRAM', '512 MB LPDDR2'],
        ['Sistem Operasi', 'Bare-metal / RTOS', 'Linux (Raspberry Pi OS)'],
        ['WiFi', '2.4 GHz SAJA', '2.4 GHz SAJA'],
        ['Port Kamera', 'DVP (OV series)', 'CSI (RPi Camera series)'],
        ['Konsumsi Daya', '~1–2 Watt', '~2–3 Watt'],
        ['Harga (Lokal)', 'Termasuk modul kamera', '~Rp 1.000.000'],
        ['Ukuran', '21×17.5 mm', '65×30 mm'],
    ]
)

add_heading_styled('3.3 Komponen per Titik Kamera', level=2)
add_bold_para('Rancangan v1:')
doc.add_paragraph('Lensa OV5640 → (kabel pita) → XIAO ESP32-S3 Sense → (WiFi) → Video MJPEG ke Laptop')
add_bold_para('Rancangan v2:')
doc.add_paragraph('RPi AI Camera (Sony IMX500) → (kabel pita CSI) → RPi Zero 2 W → (WiFi) → JSON Skeleton ke Laptop/HP')

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 4
# ═══════════════════════════════════════════════
add_heading_styled('BAB 4  PERBANDINGAN RINCIAN ANGGARAN BIAYA (RAB)', level=1)

add_heading_styled('4.1 RAB Rancangan v1 — 4 Kamera ESP32-S3', level=2)
add_table_with_style(
    ['Komponen', 'Qty', 'Harga Satuan', 'Total'],
    [
        ['XIAO ESP32-S3 Sense + OV5640', '4', 'Rp 225.000', 'Rp 900.000'],
        ['Custom 3D Printed Casing', '4', 'Rp 150.000', 'Rp 600.000'],
        ['Enclosure Mounting Bracket', '4', 'Rp 200.000', 'Rp 800.000'],
        ['Mini Tripod Foldable', '4', 'Rp 120.000', 'Rp 480.000'],
        ['USB-C Power Adapter & Kabel', '4', 'Rp 56.250', 'Rp 225.000'],
        ['Travel WiFi Router', '1', 'Rp 600.000', 'Rp 600.000'],
        ['Sensor IMU BMI270', '2', 'Rp 120.000', 'Rp 240.000'],
        ['Baterai LiPo IMU', '2', 'Rp 112.500', 'Rp 225.000'],
        ['Tracking Band Neon Velcro', '1 set', 'Rp 200.000', 'Rp 200.000'],
        ['', '', 'TOTAL v1', 'Rp 4.270.000'],
    ]
)

add_heading_styled('4.2 RAB Rancangan v2 — 2 Kamera AI Raspberry Pi', level=2)
add_table_with_style(
    ['Komponen', 'Qty', 'Harga Satuan', 'Total'],
    [
        ['Raspberry Pi AI Camera (IMX500)', '2', 'Rp 2.000.000', 'Rp 4.000.000'],
        ['Raspberry Pi Zero 2 W', '2', 'Rp 1.000.000', 'Rp 2.000.000'],
        ['MicroSD Card 32GB Class 10', '2', 'Rp 75.000', 'Rp 150.000'],
        ['Custom 3D Printed Casing', '2', 'Rp 150.000', 'Rp 300.000'],
        ['Mini Tripod Foldable', '2', 'Rp 120.000', 'Rp 240.000'],
        ['Powerbank 10Ah 5V/3A + Kabel', '2', 'Rp 250.000', 'Rp 500.000'],
        ['Travel WiFi Router (opsional)', '1', 'Rp 600.000', 'Rp 600.000'],
        ['', '', 'TOTAL v2', 'Rp 7.790.000'],
    ]
)

add_heading_styled('4.3 Analisis Selisih', level=2)
add_table_with_style(
    ['Metrik', 'v1', 'v2', 'Selisih'],
    [
        ['Total Biaya Hardware', 'Rp 4.270.000', 'Rp 7.790.000', '+Rp 3.520.000 (+82%)'],
        ['Biaya per Titik Kamera', 'Rp 556.250', 'Rp 3.345.000', '+Rp 2.788.750'],
        ['Jumlah Komponen Dirakit', '~20 bagian', '~10 bagian', '50% lebih sedikit'],
        ['Komponen Perlu Solder', '0', '0', 'Sama'],
    ]
)

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 5
# ═══════════════════════════════════════════════
add_heading_styled('BAB 5  PERBANDINGAN ARSITEKTUR SOFTWARE & KOMPLEKSITAS KODING', level=1)

add_heading_styled('5.1 Tabel Kompleksitas per Modul', level=2)
add_table_with_style(
    ['Modul', 'v1 (Kesulitan)', 'v2 (Kesulitan)'],
    [
        ['Firmware Kamera', 'SULIT — C/C++ MJPEG streaming, buffer, WiFi reconnect', 'MUDAH — Load model AI via SDK RPi'],
        ['Video/Data Receiver', 'SANGAT SULIT — 4 stream paralel, sinkronisasi timestamp', 'MUDAH — 2 stream teks JSON via WebSocket'],
        ['Pose Estimation', 'SULIT — 4x MediaPipe multiprocessing', 'TIDAK PERLU — Otomatis di cip Sony'],
        ['Sinkronisasi Kamera', 'SANGAT SULIT — 4 sumber async, drift 50–200ms', 'MUDAH — 2 sumber, drift terkontrol'],
        ['Triangulasi 3D', 'SEDANG — OpenCV DLT 4 view', 'SEDANG — OpenCV DLT 2 view (lebih simpel)'],
        ['Exercise Engine', 'SEDANG', 'SEDANG — Identik'],
        ['Web Dashboard', 'SEDANG', 'SEDANG — Identik'],
        ['Mobile App', 'SEDANG', 'SEDANG — Identik'],
        ['Cloud Sync', 'MUDAH', 'MUDAH — Identik'],
        ['TOTAL', 'Kesulitan: 9/10', 'Kesulitan: 5/10'],
    ]
)

doc.add_paragraph(
    'Rancangan v2 mengurangi beban pengembangan software (software engineering) '
    'hingga hampir 50%, karena modul-modul tersulit — yaitu Video Streaming '
    'paralel, AI Processing paralel, dan Sinkronisasi 4 Kamera — telah '
    'sepenuhnya ditangani oleh perangkat keras (hardware-accelerated).'
)

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 6
# ═══════════════════════════════════════════════
add_heading_styled('BAB 6  PERBANDINGAN KEANDALAN SISTEM (RELIABILITY)', level=1)

add_table_with_style(
    ['Aspek Keandalan', 'v1 (4× ESP32)', 'v2 (2× RPi AI Cam)', 'Pemenang'],
    [
        ['Stabilitas WiFi', 'KRITIS — 4 video @ 2.4GHz', 'AMAN — hanya teks', 'v2'],
        ['Konsistensi FPS', 'TIDAK TERJAMIN — drop saat WiFi sibuk', 'KONSISTEN — 30 FPS on-chip', 'v2'],
        ['Sinkronisasi Waktu', 'SANGAT SULIT — 4 sumber async', 'MUDAH — 2 sumber', 'v2'],
        ['Ketahanan Panas', 'BAIK — ESP32 hemat daya', 'SEDANG — RPi perlu ventilasi', 'v1'],
        ['Ketahanan Baterai', 'UNGGUL — >15 jam', 'CUKUP — 6–8 jam', 'v1'],
        ['Waktu Boot/Startup', 'INSTAN — <1 detik', 'LAMBAT — 30–45 detik booting', 'v1'],
        ['Recovery dari Error', 'MANUAL — cabut & colok ulang', 'OTOMATIS — auto-restart via Linux', 'v2'],
    ]
)

doc.add_paragraph('Skor Keandalan v1: 3 menang dari 7 metrik (43%)')
doc.add_paragraph('Skor Keandalan v2: 4 menang dari 7 metrik (57%)')

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 7
# ═══════════════════════════════════════════════
add_heading_styled('BAB 7  PERBANDINGAN PERFORMA & LATENCY', level=1)

add_table_with_style(
    ['Metrik Performa', 'v1 (4× ESP32)', 'v2 (2× RPi AI Cam)'],
    [
        ['Resolusi Input AI', 'VGA 640×480', 'Full HD 2028×1520'],
        ['FPS AI Processing', '15–20 FPS (bottleneck WiFi)', '30 FPS (on-chip, konsisten)'],
        ['Total Latency E2E', '150–300 ms (optimis), 500ms+ realistis', '50–100 ms'],
        ['Beban CPU Main Device', '70–90%', '5–15%'],
        ['Main Device Minimum', 'Laptop + GPU dedicated', 'Laptop biasa / Smartphone'],
        ['Akurasi Pose', 'Baik (33 keypoints 3D)', 'Sangat Baik (sensor Sony, NPU presisi)'],
    ]
)

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 8
# ═══════════════════════════════════════════════
add_heading_styled('BAB 8  PERBANDINGAN PORTABILITAS & COVERAGE PER EXERCISE', level=1)

add_heading_styled('8.1 Portabilitas', level=2)
add_table_with_style(
    ['Aspek', 'v1 (4× ESP32)', 'v2 (2× RPi AI Cam)'],
    [
        ['Jumlah Tiang/Tripod', '4 buah', '2 buah'],
        ['Berat Total Kit', '~3–4 kg', '~2–3 kg'],
        ['Waktu Setup', '10–15 menit', '5–8 menit'],
        ['Waktu Bongkar', '~5 menit', '~3 menit'],
        ['Main Device', 'Laptop performa tinggi (besar)', 'Laptop biasa / HP Android'],
        ['Kapasitas Ransel', 'Penuh', 'Setengah kosong'],
    ]
)

add_heading_styled('8.2 Coverage per Exercise', level=2)
add_table_with_style(
    ['Exercise', 'v1: 4 Kamera 360°', 'v2: 2 Kamera 90°', 'Dampak Pengurangan'],
    [
        ['Push Up', 'Depan, Belakang, Kiri, Kanan', 'Samping + Depan-Serong', 'Minimal'],
        ['Pull Up', 'Depan, Belakang, Kiri, Kanan', 'Samping + Depan-Serong', 'Minimal'],
        ['Sit Up', 'Depan, Belakang, Kiri, Kanan', 'Samping + Depan-Serong', 'Minimal'],
        ['Squat Jump', 'Depan, Belakang, Kiri, Kanan', 'Samping + Depan-Serong', 'Sedang (simetri lutut)'],
        ['Vertical Jump', 'Depan, Belakang, Kiri, Kanan', 'Samping + Depan-Serong', 'Minimal'],
    ]
)

doc.add_paragraph(
    'Untuk kelima exercise target (semuanya gerakan linear pada sagittal plane), '
    'pengurangan dari 4 ke 2 kamera hanya berdampak sedikit pada deteksi Squat Jump '
    '(kehilangan kemampuan melihat knee valgus dari belakang). Semua exercise lain '
    'tidak terdampak signifikan.'
)

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 9
# ═══════════════════════════════════════════════
add_heading_styled('BAB 9  TEMUAN KRITIS PADA RANCANGAN v1', level=1)

add_heading_styled('9.1 Temuan #1: WiFi 5GHz yang Tidak Mungkin', level=2)
doc.add_paragraph('Lokasi di Proposal: BAB 4.1, baris "1x Travel WiFi Router 5GHz"')
doc.add_paragraph(
    'Masalah: Mikrokontroler XIAO ESP32-S3 Sense hanya mendukung WiFi frekuensi '
    '2.4GHz. Chip ESP32-S3 secara fisik tidak memiliki radio 5GHz. Menulis '
    '"5GHz" di proposal merupakan klaim teknis yang tidak dapat dipenuhi.'
)
doc.add_paragraph(
    'Dampak: Jika klien atau penguji melakukan verifikasi teknis, ini menjadi '
    'cacat faktual yang merusak kredibilitas proposal secara keseluruhan.'
)

add_heading_styled('9.2 Temuan #2: Latency yang Menyesatkan', level=2)
doc.add_paragraph('Lokasi di Proposal: BAB 3.2, "Total Latency Sistem: 150–300 ms"')
doc.add_paragraph(
    'Masalah: Estimasi latency 150–300 ms mengasumsikan 4 aliran video MJPEG '
    'berjalan mulus tanpa hambatan melalui jaringan WiFi 2.4GHz. Pada realita '
    'lingkungan gym/indoor yang padat sinyal WiFi (dari HP pengunjung, Bluetooth, '
    'microwave), latency dapat membengkak hingga 500 ms sampai 2 detik.'
)
doc.add_paragraph(
    'Dampak: Klaim "real-time" dalam proposal menjadi tidak akurat dan berpotensi '
    'menyesatkan ekspektasi klien.'
)

add_heading_styled('9.3 Temuan #3: Main Device Tidak Tercantum di RAB', level=2)
doc.add_paragraph('Lokasi di Proposal: BAB 4 (Kebutuhan Teknis) dan BAB 9 (RAB)')
doc.add_paragraph(
    'Masalah: Proposal tidak menyebutkan kebutuhan Laptop/PC lokal sebagai '
    'mesin pemroses AI. Dalam arsitektur v1, Laptop dengan GPU dedicated '
    '(spesifikasi gaming) adalah kebutuhan WAJIB yang tidak masuk di daftar '
    'kebutuhan teknis maupun di Rincian Anggaran Biaya.'
)
doc.add_paragraph(
    'Dampak: Klien dapat berasumsi bahwa sistem berjalan mandiri tanpa Laptop '
    'tambahan, dan merasa dirugikan saat mengetahui harus menyediakan perangkat '
    'komputasi sendiri.'
)

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 10
# ═══════════════════════════════════════════════
add_heading_styled('BAB 10  MATRIKS KEPUTUSAN FINAL (WEIGHTED SCORING)', level=1)

doc.add_paragraph(
    'Matriks berikut memberikan skor tertimbang (weighted score) berdasarkan '
    'bobot kepentingan setiap kriteria terhadap keberhasilan proyek di lapangan.'
)

add_table_with_style(
    ['Kriteria', 'Bobot', 'v1: 4× ESP32', 'v2: 2× RPi AI', 'Pemenang'],
    [
        ['Biaya Hardware', '15%', '⭐⭐⭐⭐⭐ (Rp 4,2 Jt)', '⭐⭐ (Rp 7,8 Jt)', 'v1'],
        ['Keandalan Jaringan', '20%', '⭐⭐', '⭐⭐⭐⭐⭐', 'v2'],
        ['Kemudahan Koding', '20%', '⭐⭐ (9/10)', '⭐⭐⭐⭐ (5/10)', 'v2'],
        ['Akurasi Real-Time', '15%', '⭐⭐⭐', '⭐⭐⭐⭐⭐', 'v2'],
        ['Portabilitas', '10%', '⭐⭐⭐', '⭐⭐⭐⭐⭐', 'v2'],
        ['Coverage 360°', '10%', '⭐⭐⭐⭐⭐', '⭐⭐⭐', 'v1'],
        ['Ketahanan Baterai', '5%', '⭐⭐⭐⭐⭐', '⭐⭐⭐', 'v1'],
        ['Fleksibilitas Main Device', '5%', '⭐⭐', '⭐⭐⭐⭐⭐', 'v2'],
        ['', '', '', '', ''],
        ['SKOR TOTAL', '100%', '2.95 / 5', '4.15 / 5', 'v2 🏆'],
    ]
)

doc.add_page_break()

# ═══════════════════════════════════════════════
# BAB 11
# ═══════════════════════════════════════════════
add_heading_styled('BAB 11  REKOMENDASI & LANGKAH SELANJUTNYA', level=1)

add_heading_styled('11.1 Rekomendasi Arsitektur', level=2)

add_bold_para('Gunakan Rancangan v2 (2× Raspberry Pi AI Camera) jika:')
recs_v2 = [
    'Tim memiliki anggaran hardware dalam rentang Rp 7–8 Juta.',
    'Prioritas utama adalah keandalan sistem di lapangan (gym, outdoor).',
    'Tim ingin fokus mengembangkan fitur (Exercise Engine, Dashboard), bukan men-debug masalah jaringan.',
    'Produk ingin bisa berjalan di HP biasa tanpa memerlukan Laptop ber-GPU.',
]
for r in recs_v2:
    doc.add_paragraph(r, style='List Bullet')

add_bold_para('Pertahankan Rancangan v1 (4× XIAO ESP32-S3) jika:')
recs_v1 = [
    'Anggaran hardware maksimal Rp 4,5 Juta dan tidak dapat dinaikkan.',
    'Coverage 360° merupakan keharusan mutlak (misal: untuk olahraga berputar).',
    'Tim bersedia mengalokasikan 60–70% waktu pengembangan untuk mengatasi masalah teknis jaringan dan sinkronisasi video.',
]
for r in recs_v1:
    doc.add_paragraph(r, style='List Bullet')

add_heading_styled('11.2 Langkah Selanjutnya', level=2)

steps = [
    ('Keputusan Tim', 'Diskusikan dokumen ini bersama seluruh anggota tim (2 Teknisi, 2 Web Developer, 1 Project Manager) dan tetapkan arsitektur final.'),
    ('Revisi Proposal', 'Setelah keputusan diambil, perbarui dokumen Proposal resmi sesuai arsitektur terpilih.'),
    ('Fase Prototipe (Biaya Rp 0)', 'Mulai pengembangan Exercise Engine menggunakan webcam Laptop untuk memvalidasi logika AI sebelum membeli hardware apapun.'),
    ('Procurement', 'Pesan hardware setelah prototipe webcam terbukti berhasil mendeteksi repetisi dan menilai form gerakan.'),
]
for title, desc in steps:
    add_bold_para(f'{title}:')
    doc.add_paragraph(desc)

# ═══════════════════════════════════════════════
# LEMBAR PENGESAHAN
# ═══════════════════════════════════════════════
doc.add_page_break()
add_heading_styled('LEMBAR PENGESAHAN', level=1)
doc.add_paragraph()
doc.add_paragraph('Dokumen lampiran teknis ini disusun dan disahkan sebagai bagian tidak terpisahkan dari Proposal Pengembangan Sistem Fitness Tracking Eye Terintegrasi.')
doc.add_paragraph()
doc.add_paragraph('Dibuat di Padang, pada tanggal Oktober 2026.')
doc.add_paragraph()
doc.add_paragraph()

sign_table = doc.add_table(rows=3, cols=2)
sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
sign_table.cell(0, 0).text = 'PIHAK KLIEN'
sign_table.cell(0, 1).text = 'PIHAK PENGEMBANG'
sign_table.cell(1, 0).text = '\n\n\n'
sign_table.cell(1, 1).text = '\n\n\n'
sign_table.cell(2, 0).text = '(________________________)'
sign_table.cell(2, 1).text = '(________________________)'
for row in sign_table.rows:
    for cell in row.cells:
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ── Save ──
output_path = r'D:\Aaa\Fitness-Tracking-Eye\docs\Lampiran_Teknis_Perbandingan_Arsitektur_v1_vs_v2.docx'
doc.save(output_path)
print(f'Document saved to: {output_path}')
