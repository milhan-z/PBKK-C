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

def quote_block(text):
    return {
        "object": "block",
        "type": "quote",
        "quote": {
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
    page_id = "4019c072-0c5a-8177-9d82-cd70eceb63f0"
    
    print("1. Menghapus ikon emoji dan membersihkan blok lama...")
    make_request(f"pages/{page_id}", api_key, method="PATCH", data={"icon": None})
    
    # Hapus blok yang ada
    res, _ = make_request(f"blocks/{page_id}/children?page_size=100", api_key)
    old_blocks = res.get("results", [])
    print(f"Menghapus {len(old_blocks)} blok lama...")
    for b in old_blocks:
        make_request(f"blocks/{b['id']}", api_key, method="DELETE")
        
    print("2. Menyusun laporan formal Pertemuan 7 tanpa emoji dan tanpa referensi ETS...")
    blocks = []
    
    # Banner Ringkasan Formal (Quote Block)
    blocks.append(quote_block(
        "Tugas Pertemuan 07 - Pemrograman Berbasis Kerangka Kerja (PBKK C)\n"
        "Penyusunan Product Requirements Document (PRD) & Implementasi Awal Aplikasi Desktop TutorMate\n"
        "Pengembangan Kelompok 8 PBKK C (WPF .NET 10, C# 13, ADO.NET SQL Server)"
    ))
    
    # Identitas Pengembang
    blocks.append(h_block("Identitas Pengembang (Kelompok 8 - PBKK C)", 2))
    blocks.append(bullet_block("Muhammad Hilman Azhar (NRP 5025241264) - Ketua / Full-stack Developer", "1. Mahasiswa: "))
    blocks.append(bullet_block("A. Wildan Kevin Assyauqi (NRP 5025241265) - System Analyst & UI/UX", "2. Anggota Tim: "))
    blocks.append(bullet_block("Al Jad Kaukabudduri Hardianto (NRP 5025241248) - Database & Backend Developer", "3. Anggota Tim: "))
    blocks.append(bullet_block("Pemrograman Berbasis Kerangka Kerja C (Tahun 2026)", "Kelas: "))
    blocks.append(bullet_block("Fajar Baskoro, S.Kom., M.T.", "Dosen Pengampu: "))
    blocks.append(bullet_block("https://github.com/wildankev/PBKK/tree/main/W07", "Repositori GitHub Tugas (W07): "))
    blocks.append(bullet_block("PRD_TutorMate_Kelompok8_PBKK_C.pdf (Dokumen Formal 23 Halaman)", "Dokumen PRD Resmi: "))
    
    blocks.append(divider_block())
    
    # 1. Ringkasan Eksekutif & Latar Belakang Masalah
    blocks.append(h_block("1. Ringkasan Eksekutif & Latar Belakang Masalah", 2))
    blocks.append(p_block(
        "TutorMate adalah aplikasi desktop berbasis Windows Presentation Foundation (WPF) dengan C# (.NET 10) "
        "yang dirancang untuk mengelola ekosistem layanan tutor akademik sebaya (peer tutoring) di lingkungan kampus. "
        "Aplikasi ini menyelesaikan kendala fragmentasi informasi tutor yang selama ini tersebar secara sporadis di grup chat, "
        "ketiadaan validasi kualifikasi nilai akademis yang terpercaya, serta kesulitan sinkronisasi jadwal antara mahasiswa dan tutor."
    ))
    blocks.append(bullet_block(
        "Menghubungkan mahasiswa yang memerlukan bimbingan (Mentee/Peserta) dengan mahasiswa yang unggul pada mata kuliah tertentu (Mentor/Tutor).",
        "Visi Utama Produk: "
    ))
    blocks.append(bullet_block(
        "Memastikan tutor memiliki riwayat kompetensi terverifikasi (nilai minimal B, rekomendasi A atau AB) untuk menjaga kualitas bimbingan belajar.",
        "Standar Kualifikasi: "
    ))
    blocks.append(bullet_block(
        "Menyediakan sistem desktop native dengan latensi mikrodetik dan akses basis data lokal yang reliabel tanpa kendala koneksi kampus.",
        "Pendekatan Rich UI Desktop: "
    ))
    
    blocks.append(divider_block())
    
    # 2. Analisis Pengguna & Matriks Hak Akses
    blocks.append(h_block("2. Analisis Pengguna & Matriks Hak Akses (User Roles)", 2))
    blocks.append(bullet_block(
        "Memiliki wewenang mengelola katalog kurikulum mata kuliah (tambah, perbarui, nonaktifkan), memverifikasi berkas pengajuan calon tutor, memantau seluruh request bimbingan, dan mengelola akun pengguna.",
        "A. Administrator: "
    ))
    blocks.append(bullet_block(
        "Mahasiswa yang telah lulus mata kuliah dengan nilai memuaskan. Berwenang mendaftar sebagai tutor, mengisi jadwal ketersediaan bimbingan, menentukan topik keahlian khusus, dan menanggapi permohonan bimbingan.",
        "B. Mentor (Tutor Sebaya): "
    ))
    blocks.append(bullet_block(
        "Mahasiswa yang mencari bimbingan belajar. Berwenang menjelajahi katalog mata kuliah, mencari profil tutor aktif, mengajukan sesi bimbingan, dan memberikan penilaian performa setelah sesi bimbingan selesai.",
        "C. Peserta (Mentee): "
    ))
    
    blocks.append(divider_block())
    
    # 3. Kebutuhan Fungsional Utama
    blocks.append(h_block("3. Kebutuhan Fungsional Utama (Functional Requirements)", 2))
    blocks.append(bullet_block(
        "Pendaftaran akun baru dengan validasi keunikan NIM (10 digit numerik), validasi kecocokan kata sandi, serta login aman yang mengarahkan pengguna ke antarmuka sesuai perannya.",
        "FR-01 & FR-02 (Autentikasi & Akun): "
    ))
    blocks.append(bullet_block(
        "Penyajian daftar mata kuliah dalam DataGrid interaktif lengkap dengan kode mata kuliah, nama mata kuliah, dan silabus kompetensi.",
        "FR-03 (Katalog Mata Kuliah): "
    ))
    blocks.append(bullet_block(
        "Antarmuka formulir bagi mahasiswa untuk mengajukan diri sebagai tutor dengan melampirkan riwayat nilai huruf (A, AB, B), hari jadwal bimbingan, dan topik spesifik.",
        "FR-04 (Pendaftaran Tutor Sebaya): "
    ))
    blocks.append(bullet_block(
        "Tabel visual multi-kolom yang menyajikan seluruh tutor yang telah terdaftar untuk memudahkan pencarian oleh calon peserta bimbingan.",
        "FR-05 (Daftar Tutor Aktif): "
    ))
    blocks.append(bullet_block(
        "Formulir khusus administrator untuk memperbarui dan menambah kurikulum mata kuliah baru ke dalam basis data SQL Server secara persisten.",
        "FR-06 (Manajemen Kurikulum Admin): "
    ))
    
    blocks.append(divider_block())
    
    # 4. Perancangan Basis Data Relasional
    blocks.append(h_block("4. Perancangan Basis Data Relasional (TutorMateDB)", 2))
    blocks.append(p_block("Basis data dirancang menggunakan Microsoft SQL Server dengan 3 tabel utama pada rilis awal implementasi:", italic=True))
    
    blocks.append(bullet_block(
        "Menyimpan data akun dan peran pengguna (UserId sebagai Primary Key, NIM bersifat UNIQUE, Nama, Password, Role). Role mencakup 'Admin', 'Mentor', dan 'Peserta'.",
        "1. Tabel Users: "
    ))
    blocks.append(bullet_block(
        "Menyimpan master data mata kuliah (SubjectId sebagai Primary Key, KodeMK bersifat UNIQUE, NamaMataKuliah, Deskripsi).",
        "2. Tabel Subjects: "
    ))
    blocks.append(bullet_block(
        "Menyimpan relasi tutor dan mata kuliah yang diampu (ApplicationId sebagai Primary Key, TutorId sebagai Foreign Key ke Users.UserId, SubjectId sebagai Foreign Key ke Subjects.SubjectId, NilaiHuruf, HariJadwal, TopikKeahlian).",
        "3. Tabel TutorApplications: "
    ))
    blocks.append(quote_block(
        "Integritas Relasional: Tabel TutorApplications menerapkan Foreign Key constraint ke tabel Users(UserId) dan Subjects(SubjectId). "
        "Hal ini menjamin integritas referensial data serta mencegah timbulnya data tutor yatim (orphaned records)."
    ))
    
    blocks.append(divider_block())
    
    # 5. Arsitektur Perangkat Lunak WPF
    blocks.append(h_block("5. Arsitektur Perangkat Lunak & Pola Desain (WPF Desktop)", 2))
    blocks.append(p_block("Aplikasi dibangun dengan memisahkan tanggung jawab kode (Separation of Concerns) secara terstruktur:", italic=True))
    blocks.append(bullet_block(
        "Mendefinisikan representasi entitas data murni tanpa dependensi antarmuka (User.cs, Subject.cs, TutorApplication.cs).",
        "Models: "
    ))
    blocks.append(bullet_block(
        "Mengisolasi seluruh perintah ADO.NET SQL Server (UserRepository.cs, TutorRepository.cs) dan dilengkapi kelas pembantu DatabaseConfig.cs dengan kapabilitas deteksi otomatis server (LocalDB maupun localhost).",
        "Repositories (Data Access Layer): "
    ))
    blocks.append(bullet_block(
        "Antarmuka pengguna XAML modern (LoginWindow.xaml, RegisterWindow.xaml, MainWindow.xaml) dengan sidebar modern bertema navy (#2C3E50), aksen teal (#1ABC9C), dan DataGrid interaktif.",
        "Views (User Interface): "
    ))
    blocks.append(bullet_block(
        "Menghubungkan aksi antarmuka dengan logika bisnis melalui implementasi RelayCommand.cs untuk navigasi responsif.",
        "ViewModels & Commands: "
    ))
    
    blocks.append(divider_block())
    
    # 6. Analisis Ketercapaian Implementasi Awal
    blocks.append(h_block("6. Analisis Ketercapaian Implementasi Awal (Sprint 1)", 2))
    blocks.append(p_block(
        "Sebagai bagian dari evaluasi tugas perancangan Pertemuan 7, dilakukan penelaahan terhadap tingkat ketercapaian "
        "implementasi awal dibandingkan dengan rancangan spesifikasi pada dokumen PRD:",
        italic=True
    ))
    blocks.append(bullet_block(
        "Modul Autentikasi (Login dan Registrasi), Katalog Mata Kuliah, Formulir Pendaftaran Calon Tutor, DataGrid Daftar Tutor Aktif, serta skema basis data relasional SQL Server telah selesai dan teruji stabil.",
        "Capaian Implementasi Saat Ini (In-Scope Pertemuan 7): "
    ))
    blocks.append(bullet_block(
        "Alur permohonan sesi belajar (TutorRequests) beserta riwayat statusnya (Menunggu, Diterima, Selesai) direncanakan pada siklus pengembangan berikutnya.",
        "Rencana Modul Permohonan Bimbingan: "
    ))
    blocks.append(bullet_block(
        "Fitur persetujuan atau penolakan tutor oleh administrator dengan catatan verifikasi resmi akan ditambahkan pada tabel TutorApplications.",
        "Rencana Verifikasi Administrator: "
    ))
    blocks.append(bullet_block(
        "Pemberian skor penilaian 1 sampai 5 dan ulasan kualitatif (Reviews) setelah sesi bimbingan selesai diselenggarakan.",
        "Rencana Modul Ulasan & Rating: "
    ))
    blocks.append(bullet_block(
        "Peningkatan standar keamanan penyimpanan kata sandi menggunakan algoritma hashing (BCrypt atau SHA-256) pada tabel Users.",
        "Rekomendasi Peningkatan Keamanan: "
    ))
    
    blocks.append(divider_block())
    
    # 7. Tautan Berkas & Repositori
    blocks.append(h_block("7. Tautan Berkas & Deliverables Pertemuan 7", 2))
    blocks.append(bullet_block("https://github.com/wildankev/PBKK/tree/main/W07", "Repositori GitHub Tugas (W07): "))
    blocks.append(bullet_block("Tersedia di direktori W07 (PRD_TutorMate_Kelompok8_PBKK_C.pdf)", "Dokumen PRD Resmi: "))
    blocks.append(bullet_block("Tersedia di direktori W07 (TutorMate.sql)", "Skrip Basis Data: "))
    
    print(f"3. Mengirim {len(blocks)} blok konten laporan formal ke subpage Notion...")
    append_blocks_in_chunks(page_id, blocks, api_key)
    print("Selesai merevisi halaman Pertemuan 7 di Notion!")

if __name__ == "__main__":
    main()
