import json
import os
import re
from datetime import datetime, timezone, timedelta

def generate_raw_log():
    log_path = r'C:\Users\dharm\.gemini\antigravity-ide\brain\3c997ec9-fe07-406e-a6c1-dad6bc6587a0\.system_generated\logs\transcript_full.jsonl'
    
    records = []
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line))

    dialogue = []
    current_user = None
    current_model_responses = []
    current_tools = []

    for r in records:
        src = r.get('source')
        typ = r.get('type')
        if src == 'USER_EXPLICIT' and typ == 'USER_INPUT':
            if current_user:
                dialogue.append({
                    'user': current_user,
                    'model_responses': current_model_responses,
                    'tools': current_tools
                })
            current_user = r
            current_model_responses = []
            current_tools = []
        elif src == 'MODEL' and typ == 'PLANNER_RESPONSE':
            if r.get('content'):
                current_model_responses.append(r)
            if r.get('tool_calls'):
                for tc in r.get('tool_calls'):
                    current_tools.append(tc)
        elif src == 'MODEL' and typ in ('RUN_COMMAND', 'WRITE_TO_FILE', 'VIEW_FILE', 'SEARCH_WEB'):
            pass

    if current_user:
        dialogue.append({
            'user': current_user,
            'model_responses': current_model_responses,
            'tools': current_tools
        })

    wib = timezone(timedelta(hours=7))

    md_lines = []
    md_lines.append("# Riwayat Percakapan RAW (Verbatim Chat Log): Fitness Tracking Eye")
    md_lines.append("")
    md_lines.append("> [!IMPORTANT]")
    md_lines.append("> **DOKUMEN TRANSFER KONTEKS & MIGRASI DEVICE**  ")
    md_lines.append("> Dokumen ini dibuat khusus karena User akan berpindah device. Seluruh riwayat percakapan asli (*raw & verbatim*) antara User dan AI Assistant (Antigravity) disimpan secara lengkap di sini. Jika Anda adalah AI Agent di device baru, **baca dokumen ini untuk memahami seluruh latar belakang proyek, kesepakatan anggaran, komposisi tim, keputusan arsitektur, dan status kode terakhir.**")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 📌 Metadata & Ringkasan Konteks Proyek")
    md_lines.append("")
    md_lines.append("- **Nama Proyek:** Fitness Tracking Eye (Computer Vision & Sensor-based Gym/Fitness Form Tracker)")
    md_lines.append("- **Organisasi/Tim:** HowArts Technology, Padang (Oktober 2026)")
    md_lines.append("- **Komposisi Tim (5 Orang):**")
    md_lines.append("  - 2 Orang Teknisi / Hardware & Embedded Engineer")
    md_lines.append("  - 2 Orang Web Developer / Fullstack & Frontend/Backend")
    md_lines.append("  - 1 Orang Non-Teknis / Project Manager / Business & Client Relations")
    md_lines.append("- **Status Finansial & Anggaran yang Disepakati:**")
    md_lines.append("  - Modal bersih tim (*clean money*): **Rp 10.000.000** (Rp 10 Juta)")
    md_lines.append("  - Batas alokasi belanja hardware (*hardware cap*): **Rp 7.000.000 – Rp 8.000.000**")
    md_lines.append("  - Pembagian hasil (*profit/fee share*): Disepakati proporsional untuk 5 orang berdasarkan beban kerja teknis & manajemen")
    md_lines.append("- **Keputusan Arsitektur Kunci (v1 vs v2):**")
    md_lines.append("  - **Rancangan v1 (Proposal Asli):** 4 Kamera nirkabel (ESP32-CAM / WiFi 5GHz palsu / OV2640) streaming video mentah ke Main Device. Ditemukan kelemahan fatal: bandwidth tidak cukup, latensi tinggi, panas ekstrem, dan main device tidak ada di RAB.")
    md_lines.append("  - **Rancangan v2 (Temuan & Revisi Baru):** 2 Titik Kamera Edge AI (Raspberry Pi Zero 2W + Raspberry Pi AI Camera Sony IMX500 onboard NPU) yang mengekstrak koordinat sendi (MediaPipe/BlazePose keypoints) langsung di kamera dan hanya mengirim data koordinat (JSON kecil ~10KB/s) via WiFi ke Main Device. Skor evaluasi: v1 = 2.95/5 vs v2 = **4.15/5**.")
    md_lines.append("- **Status Kode & Prototipe Terakhir:**")
    md_lines.append("  - Library terpasang: `opencv-python`, `mediapipe`, `numpy`.")
    md_lines.append("  - Engine prototipe tahap 1 selesai dibuat dan di-commit di [src/prototype_webcam.py](file:///d:/Aaa/Fitness-Tracking-Eye/src/prototype_webcam.py): Deteksi Squat via webcam lokal, hitung sudut lutut kiri (hip-knee-ankle trigonometri), state machine UP/DOWN, dan counter repetisi.")
    md_lines.append("- **Dokumen Penting di Repositori:**")
    md_lines.append("  - Dokumen Proposal Asli: [docs/Proposal Fitness Tracking Eye.docx](file:///d:/Aaa/Fitness-Tracking-Eye/docs/Proposal%20Fitness%20Tracking%20Eye.docx)")
    md_lines.append("  - Ekstraksi Teks Proposal: [docs/extracted_proposal.md](file:///d:/Aaa/Fitness-Tracking-Eye/docs/extracted_proposal.md)")
    md_lines.append("  - Analisis Perbandingan Arsitektur: [docs/research/architectural_comparison_v1_vs_v2.md](file:///d:/Aaa/Fitness-Tracking-Eye/docs/research/architectural_comparison_v1_vs_v2.md)")
    md_lines.append("  - Dokumen Word Resmi Lampiran Teknis: [docs/Lampiran_Teknis_Perbandingan_Arsitektur_v1_vs_v2.docx](file:///d:/Aaa/Fitness-Tracking-Eye/docs/Lampiran_Teknis_Perbandingan_Arsitektur_v1_vs_v2.docx)")
    md_lines.append("  - Catatan RAB & Teknis Tambahan: [docs/research/catatan_rab_dan_teknis_tambahan.md](file:///d:/Aaa/Fitness-Tracking-Eye/docs/research/catatan_rab_dan_teknis_tambahan.md)")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 📑 Daftar Indeks Percakapan (29 Turn)")
    md_lines.append("")

    for i, item in enumerate(dialogue):
        u = item['user']
        u_raw = u.get('content', '')
        if '<USER_REQUEST>' in u_raw:
            u_text = u_raw.split('<USER_REQUEST>')[1].split('</USER_REQUEST>')[0].strip()
        else:
            u_text = u_raw.strip()
        
        # parse timestamp
        dt_str = u.get('created_at', '')
        if dt_str:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00')).astimezone(wib)
            time_fmt = dt.strftime('%d/%m/%Y %H:%M WIB')
        else:
            time_fmt = '-'
        
        short_prompt = u_text.replace('\n', ' ')
        if len(short_prompt) > 80:
            short_prompt = short_prompt[:80] + '...'
        
        md_lines.append(f"- [Turn #{i+1} ({time_fmt}): {short_prompt}](#turn-{i+1})")

    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 💬 Transkrip Lengkap Percakapan (RAW / Verbatim)")
    md_lines.append("")

    for i, item in enumerate(dialogue):
        u = item['user']
        m_list = item['model_responses']
        tools = item['tools']
        
        u_raw = u.get('content', '')
        if '<USER_REQUEST>' in u_raw:
            u_text = u_raw.split('<USER_REQUEST>')[1].split('</USER_REQUEST>')[0].strip()
        else:
            u_text = u_raw.strip()
            
        dt_str = u.get('created_at', '')
        if dt_str:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00')).astimezone(wib)
            time_fmt = dt.strftime('%A, %d %B %Y, %H:%M:%S WIB')
        else:
            time_fmt = '-'

        step_idx = u.get('step_index', '-')

        md_lines.append(f"<a id=\"turn-{i+1}\"></a>")
        md_lines.append(f"### 🗨️ Turn #{i+1} — {time_fmt} (Step {step_idx})")
        md_lines.append("")
        md_lines.append(f"#### 👤 **User:**")
        md_lines.append("```text")
        md_lines.append(u_text)
        md_lines.append("```")
        md_lines.append("")

        if tools:
            tool_names = list(dict.fromkeys([tc.get('name') for tc in tools if isinstance(tc, dict) and tc.get('name')]))
            if tool_names:
                md_lines.append(f"> ⚙️ *Tool Actions Dilakukan:* `{', '.join(tool_names)}`")
                md_lines.append("")

        if not m_list:
            md_lines.append("#### 🤖 **Assistant:**")
            md_lines.append("*(Pesan User ini diproses bersamaan dengan pesan berikutnya atau belum ada respon terpisah).*")
            md_lines.append("")
        else:
            for m_idx, m in enumerate(m_list):
                content = m.get('content', '').strip()
                if len(m_list) > 1:
                    md_lines.append(f"#### 🤖 **Assistant (Respon {m_idx+1}):**")
                else:
                    md_lines.append("#### 🤖 **Assistant:**")
                md_lines.append("")
                md_lines.append(content)
                md_lines.append("")

        md_lines.append("---")
        md_lines.append("")

    final_content = "\n".join(md_lines)
    
    out_path_1 = r'D:\Aaa\Fitness-Tracking-Eye\docs\riwayat_percakapan_raw.md'
    out_path_2 = r'D:\Aaa\Fitness-Tracking-Eye\docs\log_percakapan_pengembangan_engine.md'
    
    with open(out_path_1, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f'Wrote {len(final_content)} characters to {out_path_1}')
    
    with open(out_path_2, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f'Wrote {len(final_content)} characters to {out_path_2}')

if __name__ == '__main__':
    generate_raw_log()
