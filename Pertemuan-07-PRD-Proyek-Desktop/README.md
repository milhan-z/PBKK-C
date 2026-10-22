# Pertemuan 07: Product Requirement Document (PRD) & Perancangan Proyek TutorMate

## Identitas Pengembang (Kelompok 8 - PBKK C)
1. Muhammad Hilman Azhar (5025241264) - Ketua / Full-stack Developer
2. A. Wildan Kevin Assyauqi (5025241265) - System Analyst & UI/UX
3. Al Jad Kaukabudduri Hardianto (5025241248) - Database & Backend Developer

---

## Deskripsi Singkat
Pertemuan ini berfokus pada tahapan perancangan sistem dan penyusunan dokumen Product Requirement Document (PRD) serta implementasi awal aplikasi desktop. Kelompok 8 mengembangkan proyek TutorMate, sebuah sistem pendataan dan manajemen tutor akademik berbasis WPF (.NET 10) dan basis data relasional SQL Server.

Dokumen dan kode sumber resmi kelompok tersedia di:
- Repositori GitHub Tugas: https://github.com/wildankev/PBKK/tree/main/W07
- Dokumen PRD Resmi: PRD_TutorMate_Kelompok8_PBKK_C.pdf
- Berkas Skrip Basis Data: TutorMate.sql
- Direktori Implementasi: TutorMateApp-20261022T002353Z-1-001/

---

## Komponen Perancangan PRD TutorMate
1. Latar Belakang & Masalah: Mengatasi kendala mahasiswa dalam menemukan tutor akademik sebaya (peer tutoring) yang kompeten, terverifikasi, dan sesuai ketersediaan jadwal.
2. User Persona & Roles:
   - Admin: Mengelola katalog mata kuliah dan memverifikasi permohonan bimbingan.
   - Mentor (Tutor): Mendaftarkan diri, mencatat riwayat nilai, memilih hari jadwal bimbingan, dan menentukan topik keahlian.
   - Peserta: Menjelajahi katalog bimbingan dan mencari tutor sesuai preferensi mata kuliah.
3. Arsitektur Perangkat Lunak:
   - Client: .NET 10 WPF (XAML UI)
   - Database: SQL Server (LocalDB / localhost TutorMateDB)
   - Data Access: ADO.NET (Microsoft.Data.SqlClient) dengan pola Repository
4. Skema Basis Data Relasional (3 Entitas Utama):
   - Users (UserId PK, NIM UNIQUE, Nama, Password, Role)
   - Subjects (SubjectId PK, KodeMK UNIQUE, NamaMataKuliah, Deskripsi)
   - TutorApplications (ApplicationId PK, TutorId FK, SubjectId FK, NilaiHuruf, HariJadwal, TopikKeahlian)
