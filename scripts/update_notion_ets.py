import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.notion_helper import load_env, make_request

def create_text_block(text, b_type="paragraph", bold=False, italic=False, color="default"):
    return {
        "object": "block",
        "type": b_type,
        b_type: {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": text},
                    "annotations": {"bold": bold, "italic": italic, "color": color}
                }
            ]
        }
    }

def create_heading(text, level=2, color="default"):
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

def create_bullet(text, bold_prefix="", color="default"):
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

def create_callout(text, emoji="💡", color="blue_background"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }

def append_blocks_in_chunks(page_id, blocks, api_key):
    chunk_size = 50
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
    page_id = "4019c072-0c5a-800d-a87d-e47e82272510" # User's original ETS page
    
    print(f"Menyiapkan update konten ETS untuk halaman Notion {page_id}...")
    
    blocks = []
    
    # Callout Info Proyek Kelompok
    blocks.append(create_callout("Aplikasi Desktop ETS: TutorMate - Sistem Pendataan & Manajemen Tutor Akademik\nDikembangkan oleh Kelompok 8 PBKK C (WPF .NET 10, ADO.NET SQL Server)", "🎓", "blue_background"))
    
    # Identitas Anggota Kelompok 8
    blocks.append(create_heading("👥 Anggota Pengembang (Kelompok 8 - PBKK C)", 2))
    blocks.append(create_bullet("5025241264 (Ketua / Full-stack Developer)", "1. Muhammad Hilman Azhar: "))
    blocks.append(create_bullet("5025241265 (System Analyst & UI/UX)", "2. A. Wildan Kevin Assyauqi: "))
    blocks.append(create_bullet("5025241248 (Database & Backend Developer)", "3. Al Jad Kaukabudduri Hardianto: "))
    blocks.append(create_bullet("https://github.com/milhan-z/PBKK-ETS-Desktop", "🔗 Repositori GitHub Proyek: "))
    blocks.append(create_bullet("Tersedia di repositori (PRD_TutorMate_Kelompok8_PBKK_C.pdf)", "📄 Dokumen PRD: "))
    
    blocks.append({"object": "block", "type": "divider", "divider": {}})
    
    # SOAL 1
    blocks.append(create_heading("📌 Jawaban Soal 1: Perbedaan Aplikasi Desktop vs Aplikasi Lain & Urgensinya", 2))
    blocks.append(create_text_block("Aplikasi desktop memiliki karakteristik arsitektur dan eksekusi yang sangat berbeda secara fundamental dibandingkan aplikasi berbasis Web maupun Mobile:", italic=True))
    
    blocks.append(create_bullet(" Berjalan secara native langsung di atas sistem operasi (Windows/Linux/macOS) dengan akses penuh ke perangkat keras (CPU multi-core, GPU rendering hardware acceleration, memori lokal, sistem berkas lokal, dan driver perangkat I/O). Memiliki latensi komputasi mikrodetik (microsecond latency) serta kapabilitas offline-first penuh tanpa ketergantungan jaringan internet.", "1. Aplikasi Desktop (WPF / WinForms / .NET):"))
    blocks.append(create_bullet(" Berjalan di dalam lingkungan terisolasi (sandbox) peramban web yang dibatasi protokol stateless HTTP/HTTPS serta model keamanan browser. Sangat bergantung pada ketersediaan koneksi internet dan responsivitas server cloud, serta memiliki latensi jaringan yang dinamis.", "2. Aplikasi Web (SPA / SSR / Cloud):"))
    blocks.append(create_bullet(" Berjalan pada sistem operasi bergerak (Android/iOS) dengan fokus antarmuka layar sentuh ringkas. Dibatasi oleh konsumsi daya baterai, alokasi memori ketat, dan kebijakan pembatasan background thread agresif.", "3. Aplikasi Mobile:"))
    
    blocks.append(create_heading("Mengapa Aplikasi Desktop Masih Sangat Dibutuhkan di Era Modern?", 3))
    blocks.append(create_bullet(" Sistem krusial seperti kasir supermarket (POS), antrean bank, administrasi laboratorium kampus, dan gardu tol tidak boleh berhenti beroperasi (zero-downtime) saat jaringan internet putus.", "• Zero-Downtime & Offline Reliability: "))
    blocks.append(create_bullet(" Mampu merender dan memanipulasi puluhan ribu baris data pada DataGrid secara real-time dengan virtualisasi UI berbasis DirectX/GPU tanpa mengalami freeze atau memory leak.", "• High-Throughput & Real-time Visualization: "))
    blocks.append(create_bullet(" Terhubung langsung dengan periferal industri seperti printer thermal struk (ESC-POS), barcode scanner USB/Serial, kamera verifikasi ujian, dan smart card reader RFID tanpa hambatan protokol browser.", "• Direct Hardware Interfacing: "))
    blocks.append(create_bullet(" Data nilai, profil mahasiswa, dan transaksi rahasia tersimpan di server lokal (LocalDB / On-Premise) terproteksi tanpa risiko penyadapan atau kebocoran di jaringan publik.", "• Enterprise Data Privacy & Security: "))

    blocks.append({"object": "block", "type": "divider", "divider": {}})

    # SOAL 2
    blocks.append(create_heading("📌 Jawaban Soal 2: Problem Statement & Definisi Fitur TutorMate", 2))
    blocks.append(create_callout("Problem Statement: Berdasarkan observasi dan dokumen PRD Kelompok 8, mahasiswa seringkali kesulitan mencari tutor sebaya (peer tutoring) untuk mata kuliah pemodelan dan pemrograman karena informasi yang tersebar acak di grup chat, ketiadaan verifikasi kualifikasi nilai, serta bentrok jadwal bimbingan.", "⚠️", "yellow_background"))
    
    blocks.append(create_heading("Rincian Masalah yang Diselesaikan:", 3))
    blocks.append(create_bullet(" Informasi tutor sebaya tersebar secara sporadis di WhatsApp/Line tanpa repositori terpusat.", "1. Fragmentasi Informasi: "))
    blocks.append(create_bullet(" Mahasiswa calon peserta bimbingan ragu terhadap kemampuan tutor karena ketiadaan bukti kualifikasi nilai huruf (misal: syarat lulus nilai A/AB).", "2. Ketiadaan Validasi Kualifikasi: "))
    blocks.append(create_bullet(" Proses penyesuaian hari dan waktu bimbingan seringkali bentrok karena tidak ada data ketersediaan waktu yang pasti.", "3. Hambatan Penjadwalan: "))
    blocks.append(create_bullet(" Sistem pencatatan bimbingan di laboratorium kampus membutuhkan antarmuka yang cepat tanpa risiko server down saat trafik tinggi.", "4. Efisiensi Operasional Offline: "))
    
    blocks.append(create_heading("Definisi Fitur Solusi Aplikasi TutorMate:", 3))
    blocks.append(create_bullet(" Sistem login dan registrasi berbasis peran (Admin, Mentor/Tutor, dan Peserta) dengan validasi kredensial NIM unik.", "1. Multi-Role Authentication: "))
    blocks.append(create_bullet(" Tabel interaktif (DataGrid) yang menampilkan seluruh mata kuliah kurikulum, kode MK, dan silabus deskripsi.", "2. Katalog Mata Kuliah Interaktif: "))
    blocks.append(create_bullet(" Formulir khusus administrator untuk menambahkan mata kuliah baru yang langsung tersimpan persisten ke SQL Server.", "3. Form Manajemen Mata Kuliah (Admin): "))
    blocks.append(create_bullet(" Mahasiswa yang ingin menjadi tutor dapat mengajukan diri dengan memilih mata kuliah, memasukkan riwayat nilai huruf (A/AB), hari ketersediaan jadwal, dan topik keahlian.", "4. Formulir Pengajuan & Pendaftaran Tutor: "))
    blocks.append(create_bullet(" Tabel visual komprehensif bagi peserta untuk mencari tutor berdasarkan mata kuliah, rating nilai, ketersediaan hari bimbingan, dan topik spesifik.", "5. DataGrid Daftar Tutor Aktif: "))
    blocks.append(create_bullet(" Mekanisme koneksi ADO.NET cerdas yang mendeteksi dan menghubungkan database SQL Server baik pada LocalDB maupun localhost secara otomatis.", "6. Smart Multi-Server Fallback: "))
    blocks.append(create_bullet(" Implementasi arsitektur bersih yang memisahkan View (XAML), ViewModel (RelayCommand), Model entitas, dan Repository data access.", "7. Clean MVVM & Repository Pattern: "))

    blocks.append({"object": "block", "type": "divider", "divider": {}})

    # SOAL 3
    blocks.append(create_heading("📌 Jawaban Soal 3: Rancangan Desain Poster Infografis 1 Halaman", 2))
    blocks.append(create_callout("Catatan: Sesuai instruksi pengerjaan ETS, poster infografis dirancang dalam cetak biru (blueprint) 13 kotak terstruktur untuk dieksekusi secara visual pada Canva / Figma.", "🎨", "green_background"))

    blueprint_items = [
        ("Header Banner", "Logo TutorMate + Judul 'TutorMate: Rich Desktop Academic Tutor Management' + Identitas Lengkap Kelompok 8 PBKK C (NRP & Nama)."),
        ("Kotak 1: Problem & Solution", "Ringkasan problem kesulitan pencarian tutor sebaya dan solusi aplikasi desktop TutorMate yang terpusat, cepat, dan terverifikasi."),
        ("Kotak 2: Learning Goals", "Capaian pembelajaran: C# 13, .NET 10 WPF, XAML Data Binding, MVVM Pattern, dan ADO.NET SQL Server Integration."),
        ("Kotak 3: Tech Stack Badge", "Deretan badge teknologi: C#, .NET 10, WPF XAML, Microsoft SQL Server LocalDB, ADO.NET SqlClient, Visual Studio 2026, Git/GitHub."),
        ("Kotak 4: 4 Fitur Kunci", "Empat kartu fitur: Multi-Role Auth, Interactive Subject Catalog, Tutor Registration & Verification, Real-time Active Tutor DataGrid."),
        ("Kotak 5: Navigasi Sidebar", "Visual navigasi desktop: List Tutor, Katalog Mata Kuliah, Form Daftar Tutor, Tambah Mata Kuliah, Logout."),
        ("Kotak 6: Mockup Login Window", "Tangkapan layar jendela LoginWindow.xaml dengan input NIM, Password, tombol Login modern, dan link Registrasi."),
        ("Kotak 7: Mockup Form Pendaftaran Tutor", "Tangkapan layar formulir pendaftaran: ComboBox Mata Kuliah, TextBox Nilai Huruf, Hari Jadwal, Topik Keahlian, dan Tombol Submit."),
        ("Kotak 8: Mockup DataGrid List Tutor", "Tangkapan layar tabel DataGrid interaktif berisi data Nama Tutor, Mata Kuliah, Nilai Huruf, Hari Jadwal, dan Topik."),
        ("Kotak 9: Diagram Alur Pengguna (User Flow)", "Diagram flow: Mahasiswa Login ➔ Pilih Role ➔ Eksplorasi Katalog MK / Form Ajukan Tutor ➔ Data Tersimpan ke SQL Server ➔ Muncul di DataGrid."),
        ("Kotak 10: Struktur Solusi Proyek", "Struktur folder solusi Visual Studio: Models/, Views/, ViewModels/, Repositories/, Commands/, App.xaml, MainWindow.xaml."),
        ("Kotak 11: Matriks Skenario Pengujian", "Tabel hasil uji coba: Login Validasi (PASS), Dynamic Role Authorization (PASS), SQL Server Connection Fallback (PASS), Insert Tutor (PASS)."),
        ("Kotak 12 & 13: Deliverables & Repository", "Tautan Repositori GitHub publik (PBKK-ETS-Desktop), Dokumen PRD PDF Kelompok 8, dan Database Script DDL TutorMate.sql.")
    ]

    for title, desc in blueprint_items:
        blocks.append(create_bullet(f" {desc}", f"• {title}:"))

    blocks.append({"object": "block", "type": "divider", "divider": {}})
    
    # Submission Links Callout
    blocks.append(create_callout("Form Pengumpulan ETS: https://docs.google.com/forms/d/e/1FAIpQLSesHiTZeZORmjc0G2PsvOjD_vNoZsJK3yfMPeVUelbAd7m9oA/viewform\nDashboard Evaluasi: https://lookerstudio.google.com/reporting/6b210206-b019-4eae-b642-90a3acabb008", "🔗", "gray_background"))

    print(f"Mengirim {len(blocks)} blok konten ke Notion...")
    append_blocks_in_chunks(page_id, blocks, api_key)
    print("Selesai mengupdate halaman Notion ETS!")

if __name__ == "__main__":
    main()
