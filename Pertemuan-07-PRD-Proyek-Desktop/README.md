# Pertemuan 07: Product Requirement Document (PRD) & Perancangan Proyek ETS

## 👥 Kelompok 8 - PBKK C
1. **Muhammad Hilman Azhar** (5025241264)
2. **A. Wildan Kevin Assyauqi** (5025241265)
3. **Al Jad Kaukabudduri Hardianto** (5025241248)

---

## 📌 Deskripsi Singkat
Pertemuan ini berfokus pada tahapan perancangan sistem dan penyusunan dokumen **Product Requirement Document (PRD)** sebelum implementasi penuh aplikasi desktop untuk Evaluasi Tengah Semester (ETS). Kelompok 8 mengembangkan proyek **TutorMate**, sebuah sistem pendataan dan manajemen tutor akademik berbasis WPF (.NET 10) dan SQL Server.

Dokumen PRD resmi kelompok tersedia di:
- **Dokumen PRD:** [`PRD_TutorMate_Kelompok8_PBKK_C.pdf`](./PRD_TutorMate_Kelompok8_PBKK_C.pdf)
- **Draft Implementasi Aplikasi:** [`TutorMateApp-20261022T002353Z-1-001/`](./TutorMateApp-20261022T002353Z-1-001/)
- **Proyek ETS Utama:** [`../ETS-Proyek-Aplikasi-Desktop/`](../ETS-Proyek-Aplikasi-Desktop/)

---

## 🎯 Komponen Perancangan PRD TutorMate
1. **Latar Belakang & Masalah:** Mengatasi hambatan mahasiswa dalam menemukan tutor akademik sebaya (*peer tutoring*) yang terverifikasi dan sesuai jadwal.
2. **User Persona & Roles:**
   - *Admin:* Mengelola katalog mata kuliah dan memverifikasi aplikasi pendaftaran.
   - *Mentor (Tutor):* Mendaftarkan diri, mengunggah riwayat nilai, memilih hari jadwal, dan menentukan topik keahlian.
   - *Peserta:* Melihat katalog bimbingan dan menghubungi tutor sesuai preferensi mata kuliah.
3. **Arsitektur Sistem:**
   - Client: .NET 10 WPF (XAML UI)
   - Database: SQL Server (LocalDB / localhost `TutorMateDB`)
   - Data Access: ADO.NET (`Microsoft.Data.SqlClient`)
4. **Skema Basis Data (3 Entitas Utama):**
   - `Users` (UserId, NIM, Nama, Password, Role)
   - `Subjects` (SubjectId, KodeMK, NamaMataKuliah, Deskripsi)
   - `TutorApplications` (ApplicationId, TutorId, SubjectId, NilaiHuruf, HariJadwal, TopikKeahlian)
