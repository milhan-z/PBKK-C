import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.notion_helper import load_env, make_request

def p_block(text, bold=False, italic=False, color="default"):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": text},
                    "annotations": {"bold": bold, "italic": italic, "color": color}
                }
            ]
        }
    }

def h_block(text, level=2, color="default"):
    h_type = f"heading_{level}"
    return {
        "object": "block",
        "type": h_type,
        h_type: {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": text},
                    "annotations": {"bold": True, "color": color}
                }
            ]
        }
    }

def bullet_block(text, bold_prefix="", color="default"):
    rich_text = []
    if bold_prefix:
        rich_text.append({
            "type": "text",
            "text": {"content": bold_prefix},
            "annotations": {"bold": True}
        })
    rich_text.append({
        "type": "text",
        "text": {"content": text},
        "annotations": {"color": color}
    })
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text}
    }

def callout_block(text, emoji="💡", color="blue_background"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }

def divider_block():
    return {"object": "block", "type": "divider", "divider": {}}

def append_blocks_in_chunks(page_id, blocks, api_key):
    chunk_size = 40
    for i in range(0, len(blocks), chunk_size):
        chunk = blocks[i:i + chunk_size]
        data = {"children": chunk}
        res, err = make_request(f"blocks/{page_id}/children", api_key, method="PATCH", data=data)
        if err:
            print(f"Error appending chunk {i}: {err}")
        else:
            print(f"Success appending chunk {i}-{i+len(chunk)}")

def main():
    cfg = load_env()
    api_key = cfg.get("NOTION_API_KEY")
    page_id = "4019c072-0c5a-800d-a87d-e47e82272510"
    
    print(f"Membangun struktur konten lengkap di Notion page {page_id}...")
    
    blocks = []
    
    # 1. Header Banner Callout
    blocks.append(callout_block(
        "EVALUASI TENGAH SEMESTER (ETS) - PEMROGRAMAN BERBASIS KERANGKA KERJA (PBKK C)\n"
        "Studi Kasus Aplikasi Desktop Rich UI: TutorMate - Sistem Pendataan & Manajemen Tutor Akademik\n"
        "Dikembangkan oleh Kelompok 8 PBKK C (WPF .NET 10, C# 13, ADO.NET SQL Server)",
        "🎓",
        "blue_background"
    ))
    
    # 2. Identitas Mahasiswa & Kelompok
    blocks.append(h_block("👤 Identitas Pengembang (Kelompok 8 - PBKK C)", 2))
    blocks.append(bullet_block("Muhammad Hilman Azhar (5025241264) - Ketua & Full-stack Developer", "• Mahasiswa: "))
    blocks.append(bullet_block("A. Wildan Kevin Assyauqi (5025241265) - System Analyst & UI/UX", "• Anggota 1: "))
    blocks.append(bullet_block("Al Jad Kaukabudduri Hardianto (5025241248) - Database & Backend Developer", "• Anggota 2: "))
    blocks.append(bullet_block("Pemrograman Berbasis Kerangka Kerja C (Tahun 2026)", "• Kelas: "))
    blocks.append(bullet_block("Fajar Baskoro, S.Kom., M.T.", "• Dosen Pengampu: "))
    blocks.append(bullet_block("https://github.com/milhan-z/PBKK-ETS-Desktop", "• Repositori GitHub Proyek ETS: "))
    blocks.append(bullet_block("PRD_TutorMate_Kelompok8_PBKK_C.pdf (Tersedia di repositori)", "• Dokumen PRD Kelompok: "))
    
    blocks.append(divider_block())
    
    # 3. SOAL 1
    blocks.append(h_block("1. Jelaskan perbedaan aplikasi desktop dengan aplikasi lain? Mengapa masih dibutuhkan", 1))
    
    blocks.append(p_block("Berikut adalah perbandingan arsitektural dan karakteristik eksekusi antara Aplikasi Desktop, Aplikasi Web, dan Aplikasi Mobile:", italic=True))
    
    blocks.append(bullet_block(
        "Berjalan secara native langsung di atas sistem operasi (Windows/Linux/macOS) dengan akses penuh ke perangkat keras (CPU multi-core, GPU hardware rendering, memori lokal, sistem berkas OS, dan driver periferal). Memiliki latensi eksekusi sangat rendah (microsecond latency) serta beroperasi secara mandiri (offline-first) menggunakan database lokal seperti SQL Server LocalDB tanpa ketergantungan koneksi jaringan.",
        "A. Aplikasi Desktop (WPF / .NET / WinForms): "
    ))
    blocks.append(bullet_block(
        "Berjalan di dalam lingkungan terisolasi (sandbox) peramban web yang dibatasi oleh protokol stateless HTTP/HTTPS serta kebijakan keamanan browser (CORS, sandbox). Sangat bergantung pada ketersediaan koneksi internet dan keandalan server cloud, serta memiliki latensi jaringan (network latency) yang dinamis.",
        "B. Aplikasi Web (SPA / Web App): "
    ))
    blocks.append(bullet_block(
        "Berjalan pada sistem operasi perangkat bergerak (Android/iOS) yang dioptimasi untuk interaksi layar sentuh satu jendela. Dibatasi oleh konsumsi daya baterai, alokasi memori ketat, serta kebijakan pembatasan background thread yang agresif oleh OS.",
        "C. Aplikasi Mobile: "
    ))
    
    blocks.append(h_block("Mengapa Aplikasi Desktop Masih Sangat Dibutuhkan di Era Modern?", 3))
    blocks.append(bullet_block(
        "Sistem krusial seperti kasir supermarket (Point of Sales / POS), gardu tol, antrean rumah sakit, dan administrasi akademik laboratorium kampus tidak boleh terhenti (zero-downtime) saat koneksi internet kampus mengalami gangguan atau server down.",
        "1. Zero-Downtime & Offline Reliability: "
    ))
    blocks.append(bullet_block(
        "Aplikasi desktop WPF mampu merender dan memanipulasi puluhan ribu baris data pada DataGrid secara instan dengan virtualisasi UI berbasis akselerasi GPU (DirectX) tanpa mengalami browser freeze atau memory crash.",
        "2. High-Throughput & Real-time Visualization: "
    ))
    blocks.append(bullet_block(
        "Kemampuan berkomunikasi langsung dengan periferal fisik lokal seperti printer thermal struk (ESC-POS), pemindai barcode USB/Serial, smartcard RFID reader, dan webcam verifikasi ujian tanpa batasan sandbox browser.",
        "3. Direct Native Hardware Interfacing: "
    ))
    blocks.append(bullet_block(
        "Data akademik sensitif, profil mahasiswa, dan riwayat nilai tersimpan aman di jaringan internal kampus (LocalDB / on-premise server) tanpa risiko kebocoran data di cloud publik terbuka.",
        "4. Enterprise Data Privacy & Security: "
    ))
    
    blocks.append(divider_block())
    
    # 4. SOAL 2
    blocks.append(h_block("2. Tuliskan problem yang akan diselesaikan oleh aplikasi yang kamu buat? Definisikan fitur aplikasi yang merupakan solusi dari problem tersebut.", 1))
    
    blocks.append(callout_block(
        "Problem Statement Aplikasi TutorMate (Berdasarkan PRD Kelompok 8 PBKK C):\n"
        "Mahasiswa seringkali mengalami kesulitan mencari tutor akademik sebaya (peer tutoring) untuk mata kuliah tingkat lanjut karena informasi yang tersebar acak di grup chat WhatsApp/Line, ketiadaan verifikasi kualifikasi nilai resmi, serta seringnya terjadi bentrok jadwal bimbingan.",
        "⚠️",
        "yellow_background"
    ))
    
    blocks.append(h_block("Rincian Masalah yang Dihadapi Mahasiswa:", 3))
    blocks.append(bullet_block(
        "Informasi lowongan atau kesediaan menjadi tutor sebaya tersebar secara sporadis di berbagai grup chat tanpa adanya repositori pencarian terpusat.",
        "1. Fragmentasi Informasi: "
    ))
    blocks.append(bullet_block(
        "Calon peserta bimbingan ragu terhadap kemampuan tutor karena tidak ada bukti nilai huruf yang terverifikasi (misal: syarat nilai minimal A/AB pada mata kuliah terkait).",
        "2. Ketiadaan Validasi Kualifikasi Akademik: "
    ))
    blocks.append(bullet_block(
        "Penentuan jadwal bimbingan yang dilakukan manual lewat pesan pribadi seringkali bentrok dengan jadwal kuliah atau kegiatan lain, memicu pembatalan sepihak.",
        "3. Hambatan Sinkronisasi Jadwal: "
    ))
    blocks.append(bullet_block(
        "Pengelolaan pendaftaran bimbingan di laboratorium departemen membutuhkan sistem yang responsif dan dapat dioperasikan secara lokal tanpa terpengaruh kelambatan internet.",
        "4. Kebutuhan Operasional Mandiri: "
    ))
    
    blocks.append(h_block("Definisi Fitur Aplikasi TutorMate sebagai Solusi:", 3))
    blocks.append(bullet_block(
        "Sistem autentikasi berbasis peran (Admin, Mentor/Tutor, dan Peserta) dengan validasi kredensial NIM unik untuk membedakan hak akses menu dan fungsi antarmuka.",
        "1. Multi-Role Authentication (Login & Register): "
    ))
    blocks.append(bullet_block(
        "DataGrid interaktif multi-kolom yang menyajikan daftar lengkap mata kuliah kurikulum, kode MK, dan silabus deskripsi mata kuliah.",
        "2. Katalog Mata Kuliah Interaktif: "
    ))
    blocks.append(bullet_block(
        "Formulir khusus administrator untuk menambahkan kurikulum dan mata kuliah baru yang langsung tersimpan persisten ke SQL Server.",
        "3. Manajemen Penambahan Mata Kuliah (Admin): "
    ))
    blocks.append(bullet_block(
        "Formulir khusus bagi mahasiswa yang ingin menjadi tutor dengan memilih mata kuliah, melampirkan riwayat nilai huruf (A/AB), memilih hari ketersediaan jadwal, dan menentukan topik keahlian spesifik.",
        "4. Formulir Pendaftaran & Pengajuan Calon Tutor: "
    ))
    blocks.append(bullet_block(
        "Tabel visual komprehensif bagi peserta bimbingan untuk mencari tutor aktif berdasarkan mata kuliah, kualifikasi nilai, jadwal hari bimbingan, dan topik spesifik.",
        "5. DataGrid Daftar Tutor Aktif: "
    ))
    blocks.append(bullet_block(
        "Mekanisme ADO.NET cerdas yang secara otomatis mendeteksi dan menghubungkan basis data SQL Server baik pada LocalDB maupun localhost tanpa konfigurasi manual.",
        "6. Smart Multi-Server Connection Fallback: "
    ))
    blocks.append(bullet_block(
        "Pemisahan arsitektural yang bersih antara antarmuka (XAML Views), logika interaksi (ViewModels & RelayCommand), model data entitas (Models), dan query akses data (Repositories).",
        "7. Clean MVVM & Repository Pattern: "
    ))
    
    blocks.append(divider_block())
    
    # 5. SOAL 3
    blocks.append(h_block("3. Buat Poster Infografis aplikasi yang telah dibuat dalam 1 halaman.", 1))
    
    blocks.append(callout_block(
        "Rancangan Cetak Biru (Blueprint) Poster Infografis 1 Halaman:\n"
        "Sesuai arahan tugas ETS, bagian ini menyajikan rancangan terstruktur 13 kotak terstandarisasi (mengacu pada poster referensi Pak Fajar Baskoro), lengkap dengan layout grid, skema warna, dan teks copywriting yang siap dieksekusi secara visual pada Canva / Figma.",
        "🎨",
        "green_background"
    ))
    
    blocks.append(h_block("Spesifikasi Layout & Design System Poster:", 3))
    blocks.append(bullet_block("1 Halaman Portrait A4 / A3 (Rasio 2:3, rekomendasi kanvas 1024 × 1536 px, 300 DPI)", "• Format & Dimensi: "))
    blocks.append(bullet_block("Deep Navy (#2C3E50), Teal Accent (#1ABC9C), Vibrant Blue (#3498DB), Soft Canvas (#ECF0F1), White Card (#FFFFFF)", "• Skema Warna: "))
    blocks.append(bullet_block("Judul/Header: Montserrat / Poppins Bold; Isi Konten: Inter / Segoe UI Regular", "• Tipografi Rekomendasi: "))
    
    blocks.append(h_block("Struktur 13 Elemen Poster Siap Pakai di Canva / Figma:", 3))
    
    boxes = [
        ("Header Banner", "Logo TutorMate + Judul 'TUTORMATE: SISTEM PENDATAAN & MANAJEMEN TUTOR AKADEMIK' + Subjudul 'ETS PBKK C 2026 - Departemen Teknik Informatika ITS' + Identitas Kelompok 8 (Muhammad Hilman Azhar 5025241264, A. Wildan Kevin Assyauqi 5025241265, Al Jad Kaukabudduri Hardianto 5025241248)."),
        ("Kotak 1: Problem & Solution Statement", "Copywriting: 'Kesulitan mencari tutor sebaya yang kompeten dan terverifikasi? TutorMate hadir sebagai solusi desktop rich UI untuk menghubungkan mahasiswa dengan tutor akademik secara cepat, terstruktur, dan transparan.'"),
        ("Kotak 2: Learning Goals (Capaian Pembelajaran)", "Poin capaian: Penguasaan C# 13, .NET 10 WPF, XAML Data Binding, MVVM Pattern, dan integrasi database relasional ADO.NET SQL Server."),
        ("Kotak 3: Tech Stack Badges", "Ikon teknologi: C# 13, .NET 10, WPF XAML, Microsoft SQL Server LocalDB, ADO.NET SqlClient, Visual Studio 2026, Git/GitHub."),
        ("Kotak 4: 4 Fitur Kunci Aplikasi", "4 Kartu Fitur: 1) Multi-Role Auth (Admin, Mentor, Peserta), 2) Interactive Subject Catalog, 3) Tutor Registration & Grade Verification (A/AB), 4) Active Tutor DataGrid & Schedule Matching."),
        ("Kotak 5: Navigasi Sidebar Desktop", "Visual Sidebar desktop TutorMate: List Tutor, Katalog MK, Form Daftar Tutor, Tambah Matkul Baru, Tombol Logout."),
        ("Kotak 6: Mockup Login Window", "Tangkapan layar antarmuka LoginWindow.xaml: Card elevation, input NIM, input Password, validasi peran, dan tautan registrasi akun baru."),
        ("Kotak 7: Mockup Form Pendaftaran Tutor", "Tangkapan layar formulir registrasi: ComboBox pemilihan mata kuliah, input nilai huruf (A/AB), input ketersediaan hari bimbingan, input topik keahlian, dan tombol submit."),
        ("Kotak 8: Mockup DataGrid List Tutor", "Tangkapan layar tabel DataGrid interaktif: Kolom Nama Tutor, Mata Kuliah, Nilai Huruf, Jadwal Bimbingan, dan Topik Keahlian dengan zebra row styling."),
        ("Kotak 9: Diagram Alur Pengguna (User Flow)", "Diagram flowchart: Login ➔ Deteksi Peran (Admin/Mentor/Peserta) ➔ Akses Katalog MK / Form Ajukan Tutor ➔ Query ADO.NET ke SQL Server ➔ Tampil di DataGrid."),
        ("Kotak 10: Arsitektur Solusi Proyek", "Diagram hierarki solusi WPF: Models/ (User, Subject, TutorApplication), Views/ (Login, Register, Main), ViewModels/ (MainViewModel), Repositories/ (DatabaseConfig, UserRepository, TutorRepository), Commands/ (RelayCommand)."),
        ("Kotak 11: Matriks Skenario Pengujian", "Tabel verifikasi fitur: Login Valid (PASS), Dynamic Role Separation (PASS), SQL Server Connection Fallback (PASS), Insert Tutor & Binding (PASS)."),
        ("Kotak 12 & 13: Deliverables & Tautan Proyek", "QR Code & Link Repositori GitHub (milhan-z/PBKK-ETS-Desktop), Dokumen PRD PDF Kelompok 8, Database Script TutorMate.sql, dan Form Pengumpulan ETS.")
    ]
    
    for title, desc in boxes:
        blocks.append(bullet_block(f"{desc}", f"• {title}: "))
    
    blocks.append(divider_block())
    
    # 6. Callout Pengumpulan
    blocks.append(callout_block(
        "Tautan Pengumpulan Resmi ETS PBKK C:\n"
        "• Google Form Evaluasi: https://docs.google.com/forms/d/e/1FAIpQLSesHiTZeZORmjc0G2PsvOjD_vNoZsJK3yfMPeVUelbAd7m9oA/viewform\n"
        "• Dashboard Evaluasi Looker Studio: https://lookerstudio.google.com/reporting/6b210206-b019-4eae-b642-90a3acabb008\n"
        "• Repositori GitHub: https://github.com/milhan-z/PBKK-ETS-Desktop",
        "🔗",
        "gray_background"
    ))
    
    print(f"Mengirim {len(blocks)} blok konten baru ke Notion...")
    append_blocks_in_chunks(page_id, blocks, api_key)
    print("Selesai! Halaman ETS di Notion telah berhasil dibangun dengan sempurna!")

if __name__ == "__main__":
    main()
