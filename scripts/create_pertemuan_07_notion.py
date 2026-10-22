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

def callout_block(text, emoji="📋", color="blue_background"):
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
    parent_id = "4009c072-0c5a-8133-8912-dd4d7e9c1525"
    
    print("1. Membuat subpage Pertemuan 7 di Notion...")
    page_data = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": [
                {
                    "type": "text",
                    "text": {"content": "Pertemuan 7 - Product Requirements Document (PRD) & Perancangan Proyek TutorMate"}
                }
            ]
        },
        "icon": {
            "type": "emoji",
            "emoji": "📋"
        }
    }
    
    new_page, err = make_request("pages", api_key, method="POST", data=page_data)
    if err:
        print("Gagal membuat halaman baru:", err)
        return
        
    page_id = new_page.get("id")
    page_url = new_page.get("url")
    print(f"Berhasil membuat halaman Pertemuan 7! ID: {page_id}")
    print(f"URL: {page_url}")
    
    # Siapkan konten blok
    blocks = []
    
    # Header Banner Callout
    blocks.append(callout_block(
        "TUGAS PERTEMUAN 07 - PEMROGRAMAN BERBASIS KERANGKA KERJA (PBKK C)\n"
        "Topik: Penyusunan Product Requirements Document (PRD) & Implementasi Awal Aplikasi Desktop TutorMate\n"
        "Kolaborasi Kelompok 8 PBKK C (WPF .NET 10, C# 13, ADO.NET SQL Server)",
        "🎓",
        "blue_background"
    ))
    
    # Identitas Pengembang Kelompok 8
    blocks.append(h_block("👥 Identitas Pengembang (Kelompok 8 - PBKK C)", 2))
    blocks.append(bullet_block("Muhammad Hilman Azhar (5025241264) - Ketua / Full-stack Developer", "1. Mahasiswa: "))
    blocks.append(bullet_block("A. Wildan Kevin Assyauqi (5025241265) - System Analyst & UI/UX", "2. Anggota Tim: "))
    blocks.append(bullet_block("Al Jad Kaukabudduri Hardianto (5025241248) - Database & Backend Developer", "3. Anggota Tim: "))
    blocks.append(bullet_block("Pemrograman Berbasis Kerangka Kerja C (Tahun 2026)", "• Kelas: "))
    blocks.append(bullet_block("Bapak Fajar Baskoro, S.Kom., M.T.", "• Dosen Pengampu: "))
    blocks.append(bullet_block("https://github.com/wildankev/PBKK/tree/main/W07", "• Repositori GitHub Tim (W07): "))
    blocks.append(bullet_block("https://github.com/milhan-z/PBKK-ETS-Desktop", "• Repositori GitHub Proyek Desktop ETS: "))
    blocks.append(bullet_block("PRD_TutorMate_Kelompok8_PBKK_C.pdf (23 Halaman Dokumen Formal)", "• Berkas PRD Resmi: "))
    
    blocks.append(divider_block())
    
    # Ringkasan Eksekutif & Latar Belakang
    blocks.append(h_block("📌 1. Ringkasan Eksekutif & Latar Belakang Proyek", 2))
    blocks.append(p_block(
        "TutorMate adalah aplikasi desktop berbasis Windows Presentation Foundation (WPF) dengan C# (.NET 10) "
        "yang dirancang untuk mengelola ekosistem layanan tutor akademik sebaya (peer tutoring) di lingkungan kampus. "
        "Aplikasi ini menyelesaikan masalah fragmentasi informasi tutor yang selama ini tersebar secara sporadis di grup chat, "
        "ketiadaan validasi kualifikasi nilai akademis yang terpercaya, serta kesulitan sinkronisasi jadwal antara mahasiswa dan tutor."
    ))
    blocks.append(bullet_block(
        "Menghubungkan mahasiswa yang membutuhkan bimbingan (Mentee/Peserta) dengan mahasiswa yang unggul pada mata kuliah tertentu (Mentor/Tutor).",
        "• Visi Utama: "
    ))
    blocks.append(bullet_block(
        "Memastikan tutor memiliki riwayat kompetensi terverifikasi (nilai minimal B, rekomendasi A/AB) untuk menjamin kualitas bimbingan.",
        "• Standar Kualifikasi: "
    ))
    blocks.append(bullet_block(
        "Menyediakan sistem desktop native dengan latensi mikrodetik dan akses basis data lokal yang reliabel tanpa kendala koneksi kampus.",
        "• Pendekatan Desktop Rich UI: "
    ))
    
    blocks.append(divider_block())
    
    # Analisis Pengguna & Matriks Hak Akses
    blocks.append(h_block("👤 2. Matriks Pengguna & Hak Akses (User Roles)", 2))
    blocks.append(bullet_block(
        "Memiliki hak akses penuh untuk mengelola katalog kurikulum mata kuliah (tambah/edit/nonaktifkan), memverifikasi pengajuan calon tutor, memantau seluruh request bimbingan, dan mengelola akun pengguna.",
        "A. Administrator: "
    ))
    blocks.append(bullet_block(
        "Mahasiswa yang telah lulus mata kuliah dengan nilai memuaskan. Berhak mendaftar sebagai tutor, mengisi jadwal ketersediaan bimbingan, menentukan topik keahlian khusus, dan menerima/menolak permohonan bimbingan.",
        "B. Mentor (Tutor Sebaya): "
    ))
    blocks.append(bullet_block(
        "Mahasiswa yang mencari bimbingan akademik. Berhak menjelajahi katalog mata kuliah, mencari tutor aktif, mengajukan sesi bimbingan belajar, dan memberikan rating/ulasan setelah sesi bimbingan selesai.",
        "C. Peserta (Mentee): "
    ))
    
    blocks.append(divider_block())
    
    # Kebutuhan Fungsional (FR) Inti
    blocks.append(h_block("⚙️ 3. Kebutuhan Fungsional Utama (Functional Requirements)", 2))
    blocks.append(bullet_block(
        "Pendaftaran akun baru dengan validasi keunikan NIM/NRP (10 digit numerik), validasi kecocokan password, serta login aman yang mengarahkan pengguna ke antarmuka sesuai perannya.",
        "• FR-01 & FR-02 (Autentikasi & Akun): "
    ))
    blocks.append(bullet_block(
        "Penyajian daftar mata kuliah dalam DataGrid interaktif lengkap dengan kode MK, nama mata kuliah, SKS, dan deskripsi silabus kompetensi.",
        "• FR-03 (Katalog Mata Kuliah): "
    ))
    blocks.append(bullet_block(
        "Antarmuka formulir bagi mahasiswa untuk mengajukan diri sebagai tutor dengan melampirkan riwayat nilai huruf (A, AB, B), hari jadwal bimbingan, dan topik spesifik.",
        "• FR-04 (Pendaftaran Tutor Sebaya): "
    ))
    blocks.append(bullet_block(
        "Tabel visual multi-kolom yang menyajikan seluruh tutor yang telah terdaftar dan terverifikasi untuk memudahkan pencarian oleh peserta bimbingan.",
        "• FR-05 (Daftar Tutor Aktif): "
    ))
    blocks.append(bullet_block(
        "Formulir khusus administrator untuk memperbarui dan menambah mata kuliah baru ke dalam basis data SQL Server secara persisten.",
        "• FR-06 (Manajemen Kurikulum Admin): "
    ))
    
    blocks.append(divider_block())
    
    # Perancangan Basis Data Relasional
    blocks.append(h_block("🗄️ 4. Perancangan Basis Data Relasional (TutorMateDB)", 2))
    blocks.append(p_block("Basis data dirancang menggunakan Microsoft SQL Server dengan 3 tabel utama pada rilis awal:", italic=True))
    
    blocks.append(bullet_block(
        "Menyimpan data akun dan peran pengguna (UserId PK, NIM UNIQUE, Nama, Password, Role). Role mencakup 'Admin', 'Mentor', dan 'Peserta'.",
        "1. Tabel Users: "
    ))
    blocks.append(bullet_block(
        "Menyimpan master data mata kuliah (SubjectId PK, KodeMK UNIQUE, NamaMataKuliah, Deskripsi).",
        "2. Tabel Subjects: "
    ))
    blocks.append(bullet_block(
        "Menyimpan relasi tutor dan mata kuliah yang diampu (ApplicationId PK, TutorId FK -> Users.UserId, SubjectId FK -> Subjects.SubjectId, NilaiHuruf, HariJadwal, TopikKeahlian).",
        "3. Tabel TutorApplications: "
    ))
    blocks.append(callout_block(
        "Integritas Relasional: Tabel TutorApplications menggunakan Foreign Key constraint yang merujuk pada Users(UserId) dan Subjects(SubjectId). Hal ini menjamin integritas referensial dan mencegah data tutor yatim (orphaned records).",
        "🛡️",
        "gray_background"
    ))
    
    blocks.append(divider_block())
    
    # Arsitektur Aplikasi Desktop WPF
    blocks.append(h_block("💻 5. Arsitektur Perangkat Lunak & Pola Desain (WPF Desktop)", 2))
    blocks.append(p_block("Aplikasi dibangun dengan memisahkan tanggung jawab kode (Separation of Concerns) secara ketat:", italic=True))
    blocks.append(bullet_block(
        "Mendefinisikan representasi entitas data murni (User.cs, Subject.cs, TutorApplication.cs).",
        "• Models: "
    ))
    blocks.append(bullet_block(
        "Mengisolasi seluruh perintah ADO.NET SQL Server (UserRepository.cs, TutorRepository.cs) dan dilengkapi kelas pembantu DatabaseConfig.cs dengan kapabilitas smart fallback (otomatis mendeteksi LocalDB maupun localhost).",
        "• Repositories (Data Access Layer): "
    ))
    blocks.append(bullet_block(
        "Antarmuka pengguna XAML modern (LoginWindow.xaml, RegisterWindow.xaml, MainWindow.xaml) dengan sidebar modern bertema dark navy (#2C3E50), aksen teal (#1ABC9C), dan DataGrid interaktif.",
        "• Views (User Interface): "
    ))
    blocks.append(bullet_block(
        "Menghubungkan aksi antarmuka dengan repositori data melalui implementasi RelayCommand.cs untuk navigasi responsif.",
        "• ViewModels & Commands: "
    ))
    
    blocks.append(divider_block())
    
    # Analisis Keselarasan PRD vs Implementasi Awal
    blocks.append(h_block("📊 6. Analisis Keselarasan PRD vs Implementasi Awal (Gap Analysis)", 2))
    blocks.append(p_block(
        "Sebagai bagian dari evaluasi tugas perancangan Pertemuan 7, dilakukan penelaahan terhadap tingkat ketercapaian "
        "implementasi awal (Sprint 1) dibandingkan dengan seluruh spesifikasi yang tercantum di PRD:",
        italic=True
    ))
    blocks.append(bullet_block(
        "Modul Autentikasi (Login/Register), Katalog Mata Kuliah, Pendaftaran Calon Tutor, DataGrid List Tutor Aktif, serta skema basis data inti SQL Server telah selesai 100% dan teruji berjalan stabil.",
        "✅ Capaian Implementasi Saat Ini (In-Scope W07): "
    ))
    blocks.append(bullet_block(
        "Alur permohonan sesi bimbingan belajar (TutorRequests) beserta riwayat statusnya (Menunggu, Diterima, Selesai) direncanakan pada sprint berikutnya setelah fase ETS.",
        "⏳ Rencana Modul Request Bimbingan: "
    ))
    blocks.append(bullet_block(
        "Fitur persetujuan/penolakan tutor oleh administrator dengan catatan verifikasi formal akan ditambahkan pada tabel TutorApplications.",
        "⏳ Rencana Verifikasi Admin: "
    ))
    blocks.append(bullet_block(
        "Pemberian skor bintang 1-5 dan testimoni ulasan (Reviews) setelah sesi bimbingan selesai.",
        "⏳ Rencana Modul Review & Rating: "
    ))
    blocks.append(bullet_block(
        "Peningkatan keamanan dengan enkripsi hashing (BCrypt / SHA-256) pada penyimpanan kata sandi tabel Users.",
        "🔒 Rekomendasi Peningkatan Keamanan: "
    ))
    
    blocks.append(divider_block())
    
    # Deliverables & Tautan Penting
    blocks.append(callout_block(
        "Tautan Berkas & Deliverables Resmi Pertemuan 07:\n"
        "• Repositori GitHub Tim (W07): https://github.com/wildankev/PBKK/tree/main/W07\n"
        "• Repositori GitHub Proyek Desktop ETS: https://github.com/milhan-z/PBKK-ETS-Desktop\n"
        "• Halaman Ujian ETS di Notion: https://app.notion.com/p/ETS-PBKK-4019c0720c5a800da87de47e82272510\n"
        "• Form Pengumpulan Tugas: https://docs.google.com/forms/d/e/1FAIpQLSesHiTZeZORmjc0G2PsvOjD_vNoZsJK3yfMPeVUelbAd7m9oA/viewform\n"
        "• Dashboard Evaluasi Looker Studio: https://lookerstudio.google.com/reporting/6b210206-b019-4eae-b642-90a3acabb008",
        "🔗",
        "gray_background"
    ))
    
    print(f"Mengirim {len(blocks)} blok konten laporan ke subpage Notion...")
    append_blocks_in_chunks(page_id, blocks, api_key)
    print("Selesai! Laporan Pertemuan 07 berhasil dibuat di Notion!")

if __name__ == "__main__":
    main()
