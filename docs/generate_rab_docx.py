import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    """Sets padding for a cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_hyperlink(paragraph, url, text, color="0056B3", underline=True):
    """Adds a clickable hyperlink into a docx paragraph."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w", "r")} r:id="{r_id}"/>')
    new_run = parse_xml(f'<w:r {nsdecls("w")}><w:rPr/></w:r>')
    rPr = new_run.find(qn('w:rPr'))

    if color:
        c = parse_xml(f'<w:color {nsdecls("w")} w:val="{color}"/>')
        rPr.append(c)
    if underline:
        u = parse_xml(f'<w:u {nsdecls("w")} w:val="single"/>')
        rPr.append(u)

    text_node = parse_xml(f'<w:t {nsdecls("w")}>{text}</w:t>')
    new_run.append(text_node)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

def create_rab_document(output_path):
    doc = Document()

    # Margin 0.8 inch agar tabel 6 kolom muat sangat lega tanpa wrap berlebih
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # -------------------------------------------------------------
    # Document Header / Title
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(3)
    title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run("RENCANA ANGGARAN BIAYA (RAB) PENGADAAN HARDWARE")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(15)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(12)
    sub_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("Sistem Multi-Kamera Dual-View Edge AI — \"Fitness Tracking Eye\" (All-in Landed Cost)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Info Summary Box
    info_table = doc.add_table(rows=2, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False

    info_data = [
        [("Proyek:", " Fitness Tracking Eye (Dual-View Edge AI)"), ("Alokasi Pagu Hardware:", " Rp 8.000.000")],
        [("Target Sistem:", " 2 Unit Kamera (Frontal & Sagittal)"), ("Realisasi All-in:", " Rp 6.791.145 (Surplus Rp 1.208.855)")]
    ]

    for row_idx, row in enumerate(info_data):
        for col_idx, (label, val) in enumerate(row):
            cell = info_table.cell(row_idx, col_idx)
            set_cell_background(cell, "F0F4F8")
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r_l = p.add_run(label)
            r_l.font.name = "Calibri"
            r_l.font.size = Pt(9)
            r_l.font.bold = True
            r_v = p.add_run(val)
            r_v.font.name = "Calibri"
            r_v.font.size = Pt(9)
            if "Hemat" in val:
                r_v.font.bold = True
                r_v.font.color.rgb = RGBColor(0x1B, 0x7A, 0x3E)

    info_table.columns[0].width = Inches(3.45)
    info_table.columns[1].width = Inches(3.45)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # Main Hardware Procurement Table (6 Columns)
    # -------------------------------------------------------------
    # Kolom: No | Nama Komponen & Spesifikasi | Qty | Harga Satuan All-in | Total Harga All-in | Sumber Pengadaan
    table_items = [
        (
            "1",
            "Raspberry Pi 3 Model A+\n(Quad-Core 1.4GHz, 512MB RAM, Wi-Fi 2.4/5GHz)",
            "2 unit",
            "Rp 679.700",
            "Rp 1.359.400",
            ("Cytron Marketplace", "https://www.cytron.io/p-raspberry-pi-3-model-a-plus")
        ),
        (
            "2",
            "Raspberry Pi AI Camera\n(Sony IMX500 12.3MP with On-Chip NPU & CSI Cable)",
            "2 unit",
            "Rp 1.903.200",
            "Rp 3.806.400",
            ("Cytron Marketplace", "https://www.cytron.io/p-raspberry-pi-ai-camera")
        ),
        (
            "3",
            "MicroSDXC 64GB Class 10 / A1 / U3 / V30\n(Samsung Ovation Extreme - Read Up to 160MB/s)",
            "2 unit",
            "Rp 284.750",
            "Rp 569.500",
            ("Shopee - Samsung Official", "https://shopee.co.id/Samsung-Micro-SD-Evo-Plus-64GB-128GB-256GB-Memory-MicroSD-Kartu-Memori-HP-Card-Class10-Garansi-10thn-i.90333466.3663592211")
        ),
        (
            "4",
            "Baterai 18650 NMC 3.000mAh 3.7V\n(RakkiPanda Flat Top, Max 10.5A, C-Rate 3C)",
            "4 unit",
            "Rp 58.875",
            "Rp 235.500",
            ("Shopee - RakkiPanda", "https://shopee.co.id/RakkiPanda-Baterai-Cas-18650-Flat-Top-Button-Top-3000mAh-i.516471536.19072920314")
        ),
        (
            "5",
            "Modul Powerbank IP5310 Out 5V 3A\n(Type-C Step-Up Boost + Pass-Through UPS)",
            "2 unit",
            "Rp 21.917",
            "Rp 43.833",
            ("Shopee - Modul Elektronik", "https://shopee.co.id/IP5310-Module-Power-Bank-5V-3A-Power-Delivery-USB-Type-C-Boost-Convert-i.292092948.22187464156")
        ),
        (
            "6",
            "Holder Baterai 18650 2-Slot Parallel\n(Model Flush Mount Box Tanam Casing)",
            "2 unit",
            "Rp 16.244",
            "Rp 32.487",
            ("Shopee - Komponen Elektronik", "https://shopee.co.id/Holder-Dudukan-Baterai-Lithium-2x-18650-3-7V-8-4V-Bisa-Seri-Paralel-Model-Tanam-di-Box-Flush-Mount-Battery-Holder-i.2178321.51767387344")
        ),
        (
            "7",
            "Tripod Kamera Multifungsi + BallHead\n(TaffSTUDIO NC-26 Universal 1/4\" Mount)",
            "2 unit",
            "Rp 32.013",
            "Rp 64.025",
            ("Shopee - TaffSTUDIO Official", "https://shopee.co.id/TaffSTUDIO-Tripod-Kamera-Multifungsi-for-Smartphone-and-Studio-Light-NC-26-i.165737536.47450034424")
        ),
        (
            "8",
            "Saklar Mini ON/OFF Slide/Toggle Switch\n(Pemutus Jalur Arus Baterai Utama)",
            "2 unit",
            "Rp 5.000",
            "Rp 10.000",
            "Toko Komponen Offline"
        ),
        (
            "9",
            "Mini Aluminium Heatsink Passive Cooler\n(Pendingin Pasif CPU Pi 3A+)",
            "2 unit",
            "Rp 10.000",
            "Rp 20.000",
            "Toko Komponen Offline"
        ),
        (
            "10",
            "Custom Case 3D Print Enclosure (0.1mm)\n(Housing Dual Camera & Baterai Tanam)",
            "2 unit",
            "Rp 300.000",
            "Rp 600.000",
            "Jasa 3D Print (Tahap Riset)"
        ),
        (
            "11",
            "Baut, Mur, Spacer PCB, & Jumper Solid\n(M2 / M2.5 Spacer + Kabel Daya GPIO)",
            "1 set",
            "Rp 50.000",
            "Rp 50.000",
            "Toko Baut & Elektronik"
        ),
    ]

    table = doc.add_table(rows=len(table_items) + 2, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(0.4), Inches(2.2), Inches(0.7), Inches(1.1), Inches(1.2), Inches(1.3)]
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    # Header Row
    headers = ["No.", "Nama Komponen & Spesifikasi", "Jumlah", "Harga Satuan (All-in)", "Total Harga (All-in)", "Sumber Pengadaan"]
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        cell = hdr_cells[i]
        cell.width = col_widths[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=120, bottom=120, left=60, right=60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title)
        run.font.name = "Calibri"
        run.font.size = Pt(8.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Data Rows
    for row_idx, item in enumerate(table_items):
        row_cells = table.rows[row_idx + 1].cells
        bg_color = "F9FAFC" if row_idx % 2 == 1 else "FFFFFF"

        for col_idx in range(6):
            cell = row_cells[col_idx]
            cell.width = col_widths[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)

            if col_idx == 0:  # No
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(item[0])
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.bold = True
            elif col_idx == 1:  # Nama Komponen
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                lines = item[1].split("\n")
                r_main = p.add_run(lines[0])
                r_main.font.name = "Calibri"
                r_main.font.size = Pt(8.5)
                r_main.font.bold = True
                if len(lines) > 1:
                    r_sub = p.add_run("\n" + lines[1])
                    r_sub.font.name = "Calibri"
                    r_sub.font.size = Pt(7.5)
                    r_sub.font.italic = True
                    r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            elif col_idx == 2:  # Kuantitas
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(item[2])
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
            elif col_idx == 3:  # Harga Satuan
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                r = p.add_run(item[3])
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
            elif col_idx == 4:  # Total Harga
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                r = p.add_run(item[4])
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            elif col_idx == 5:  # Sumber / Link
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                src = item[5]
                if isinstance(src, tuple):
                    label, url = src
                    add_hyperlink(p, url, label, color="0056B3", underline=True)
                else:
                    r = p.add_run(src)
                    r.font.name = "Calibri"
                    r.font.size = Pt(8)
                    r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # Total Row
    tot_cells = table.rows[-1].cells
    tot_cells[0].merge(tot_cells[3])
    set_cell_background(tot_cells[0], "EAECEF")
    set_cell_background(tot_cells[4], "EAECEF")
    set_cell_background(tot_cells[5], "EAECEF")
    set_cell_margins(tot_cells[0], top=100, bottom=100, left=80, right=80)
    set_cell_margins(tot_cells[4], top=100, bottom=100, left=80, right=80)
    set_cell_margins(tot_cells[5], top=100, bottom=100, left=80, right=80)

    p_tot_label = tot_cells[0].paragraphs[0]
    p_tot_label.paragraph_format.space_before = Pt(0)
    p_tot_label.paragraph_format.space_after = Pt(0)
    p_tot_label.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tl = p_tot_label.add_run("TOTAL ESTIMASI BIAYA HARDWARE (ALL-IN):")
    r_tl.font.name = "Calibri"
    r_tl.font.size = Pt(9)
    r_tl.font.bold = True
    r_tl.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_tot_val = tot_cells[4].paragraphs[0]
    p_tot_val.paragraph_format.space_before = Pt(0)
    p_tot_val.paragraph_format.space_after = Pt(0)
    p_tot_val = tot_cells[4].paragraphs[0]
    p_tot_val.paragraph_format.space_before = Pt(0)
    p_tot_val.paragraph_format.space_after = Pt(0)
    p_tot_val.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tv = p_tot_val.add_run("Rp 6.791.145")
    r_tv.font.name = "Calibri"
    r_tv.font.size = Pt(9.5)
    r_tv.font.bold = True
    r_tv.font.color.rgb = RGBColor(0x1B, 0x7A, 0x3E)

    p_tot_sisa = tot_cells[5].paragraphs[0]
    p_tot_sisa.paragraph_format.space_before = Pt(0)
    p_tot_sisa.paragraph_format.space_after = Pt(0)
    p_tot_sisa.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_ts = p_tot_sisa.add_run("(Surplus: Rp 1.208.855)")
    r_ts.font.name = "Calibri"
    r_ts.font.size = Pt(8)
    r_ts.font.italic = True
    r_ts.font.color.rgb = RGBColor(0x1B, 0x7A, 0x3E)

    # Spacing before Synthesis
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # Synthesis & Technical Justification Section
    # -------------------------------------------------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("SINTESIS TEKNIS, METODOLOGI ALL-IN COST, & JUSTIFIKASI ANGGARAN")
    r_h1.font.name = "Calibri"
    r_h1.font.size = Pt(12.5)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    sections_content = [
        (
            "1. Metodologi Perhitungan Harga Satuan All-in (Landed Cost Method)",
            [
                ("Prinsip All-in Tanpa Kolom Terpisah: ", "Untuk menyajikan laporan keuangan yang rapi, ringkas, dan transparan, seluruh biaya pengiriman (shipping), biaya administrasi/layanan platform, bea masuk, pajak impor, dan biaya pelepasan tangan kurir tidak dicantumkan sebagai baris tersendiri, melainkan diakumulasikan langsung ke dalam harga unit masing-masing komponen. Rumus dasar: Harga Satuan All-in = (Subtotal Pesanan + Biaya Kirim + Biaya Layanan / Pajak - Diskon) / Jumlah Kuantitas."),
                ("Perhitungan Unit Impor Cytron (Raspberry Pi 3A+ & AI Camera): ", "Total faktur CIF dari Cytron sebesar $233.99 USD (kurs Rp 18.000 = Rp 4.211.820) ditambah Bea Masuk 7,5% (Rp 316.000), PPN Impor 11% (Rp 498.000), dan biaya pelepasan tangan FedEx (Rp 140.000), menghasilkan total pengeluaran bersih Rp 5.165.800. Beban ini dialokasikan secara proporsional sesuai nilai barang asal: Raspberry Pi AI Camera (porsi 73,68%) menjadi Rp 1.903.200/unit, dan Raspberry Pi 3A+ (porsi 26,32%) menjadi Rp 679.700/unit."),
                ("Efisiensi Ongkos Kirim Grosir Baterai RakkiPanda (4 Unit): ", "Tarif pengiriman reguler Shopee (Rp 13.000) dan biaya layanan (Rp 2.500) berbasis berat minimum 1 kg. Karena 4 keping baterai hanya berbobot total ~180 gram, seluruh 4 unit dikirim dalam satu paket yang sama tanpa penambahan ongkir. Biaya overhead Rp 15.500 dibagi rata ke 4 unit, sehingga harga per sel baterai menjadi sangat ekonomis: (4 x Rp 55.000 + Rp 15.500) / 4 = Rp 58.875/unit."),
                ("Komponen Shopee Lainnya: ", "MicroSD Samsung Ovation Extreme 64GB setelah diskon produk Rp 1.041.920 (Total Rp 569.500 / 2 = Rp 284.750/unit), Modul IP5310 (Total Rp 43.833 / 2 = Rp 21.917/unit), Holder Baterai Paralel (Total Rp 32.487 / 2 = Rp 16.244/unit), dan Tripod TaffSTUDIO NC-26 setelah diskon produk Rp 28.600 (Total Rp 64.025 / 2 = Rp 32.013/unit).")
            ]
        ),
        (
            "2. Analisis Efisiensi Kas terhadap Kesepakatan Anggaran Hardware (Rp 8.000.000)",
            [
                ("Alokasi Pagu Hardware: ", "Dalam kesepakatan anggaran proyek, pos belanja perangkat keras (Hardware & Enclosure) dialokasikan sebesar Rp 8.000.000 dari total nilai proyek Rp 18.000.000."),
                ("Realisasi All-in Riil: ", "Total keseluruhan realisasi pengadaan perangkat keras (termasuk estimasi casing 3D print 0.1mm Rp 600.000 dan baut/spacer Rp 50.000) adalah Rp 6.791.145."),
                ("Surplus Anggaran Terjaga: ", "Terjadi penghematan kas sebesar Rp 1.208.855 (surplus ~15,11% dari pagu hardware Rp 8 Juta). Hal ini memberikan bantalan likuiditas yang sangat aman, di mana pengadaan hardware tahap awal tertutup aman dari Termin 1 (DP 30% = Rp 5.400.000) dan sisanya dilunasi dengan sangat longgar pada pencairan Termin 2 (40% = Rp 7.200.000).")
            ]
        ),
        (
            "3. Justifikasi Teknis MicroSD (Samsung Ovation Extreme 64GB SDXC / A1 / U3 / V30)",
            [
                ("SDXC (Secure Digital Extra Capacity): ", "Menandakan kapasitas kartu memori 64 GB (standar 64 GB hingga 2 TB). Dengan sistem operasi headless Raspberry Pi OS dan script yang hanya mengonsumsi ~5 GB, tersisa ruang bebas sebesar ~59 GB untuk keleluasaan rotasi blok sel memori (wear-leveling) jangka panjang."),
                ("U3 (UHS Speed Class 3): ", "Menjamin kecepatan tulis minimum secara konstan tidak akan turun di bawah 30 MB/s. Sangat optimal untuk merekam dan mentransmisikan data video resolusi tinggi tanpa lag."),
                ("A1 (Application Performance Class 1): ", "Mengindikasikan optimasi kartu memori untuk membuka dan mengeksekusi file aplikasi sistem operasi secara lancar berkat pemrosesan Input-Output Access Per Second (IOPS) yang memadai."),
                ("V30 (Video Speed Class 30): ", "Menjamin kecepatan rekam video minimum yang stabil di angka 30 MB/s. Peringkat ini merupakan standar wajib untuk perekaman video tanpa ada bingkai yang terlewat (dropped frames)."),
                ("Kecepatan Baca Maksimum 160 MB/s: ", "Kecepatan baca hingga 160 MB/s memungkinkan pemindahan file besar (seperti video atau ratusan foto pengujian) dari kartu memori ke laptop atau komputer dalam waktu yang sangat singkat, sekaligus mempercepat proses boot sistem."),
                ("Efisiensi Pembelian Shopee: ", "Dengan memanfaatkan potongan diskon produk sebesar Rp 1.041.920, total harga bersih menjadi Rp 569.500 untuk 2 unit (Rp 284.750/unit all-in termasuk ongkir dan layanan).")
            ]
        ),
        (
            "4. Arsitektur Daya Mandiri & Keamanan Termal di Lapangan",
            [
                ("Beban Arus Rendah Baterai RakkiPanda (C-Rate 0.15C): ", "Kamera dan Pi 3A+ hanya mengonsumsi daya rata-rata ~3 Watt (0,6A @ 5V). Dalam konfigurasi 2 baterai paralel (2P 1S), beban per sel baterai hanya ~0,45 Ampere (rata-rata) dan ~0,9 Ampere (beban puncak). Angka ini jauh di bawah batas pelepasan maksimal baterai (10.5A / 3C), menjamin baterai tetap dingin dan tidak mengalami drop tegangan (voltage sag)."),
                ("Durasi Nyala 5,5 s/d 6,5 Jam Nonstop: ", "Dengan total energi efektif ~20 Watt-hour per kamera, unit mampu beroperasi penuh di atas tripod sepanjang sesi pengujian FIK tanpa kabel."),
                ("Fitur Pass-Through Charging (UPS Mode): ", "Modul IP5310 memungkinkan alat dicolok ke charger HP saat uji coba lab seharian penuh tanpa menguras baterai, dan langsung otomatis beralih ke baterai saat kabel dicabut tanpa memicu restart sistem."),
                ("Pendinginan Pasif Tanpa Kipas: ", "Inferensi pose AI dijalankan langsung pada chip NPU silikon Sony IMX500 (~0,7W), sehingga CPU Pi 3A+ tetap dingin dan cukup didinginkan menggunakan heatsink aluminium mini tanpa kipas aktif berisik.")
            ]
        )
    ]

    for title, points in sections_content:
        h2 = doc.add_paragraph()
        h2.paragraph_format.space_before = Pt(8)
        h2.paragraph_format.space_after = Pt(3)
        r_h2 = h2.add_run(title)
        r_h2.font.name = "Calibri"
        r_h2.font.size = Pt(10.5)
        r_h2.font.bold = True
        r_h2.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

        for p_label, p_desc in points:
            p_pt = doc.add_paragraph(style='List Bullet')
            p_pt.paragraph_format.space_before = Pt(1)
            p_pt.paragraph_format.space_after = Pt(2.5)
            r_bold = p_pt.add_run(p_label)
            r_bold.font.name = "Calibri"
            r_bold.font.size = Pt(9)
            r_bold.font.bold = True
            r_text = p_pt.add_run(p_desc)
            r_text.font.name = "Calibri"
            r_text.font.size = Pt(9)

    saved = False
    for ver in ["", "_v2", "_v3", "_v4", "_v5"]:
        target = output_path.replace(".docx", f"{ver}.docx") if ver else output_path
        try:
            doc.save(target)
            print(f"Document successfully created at: {target}")
            saved = True
            break
        except PermissionError:
            continue
    if not saved:
        print("Warning: Could not save, all versions are open.")

if __name__ == "__main__":
    out_file = r"d:\Aaa\Repo\Fitness-Tracking-Eye\docs\RAB_Pengadaan_Hardware_Fitness_Tracking_Eye.docx"
    create_rab_document(out_file)
