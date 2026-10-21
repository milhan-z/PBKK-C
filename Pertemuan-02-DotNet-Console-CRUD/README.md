# Pertemuan 02: .NET Framework & Aplikasi Console CRUD

Folder ini memuat implementasi aplikasi console untuk operasi CRUD (Create, Read, Update, Delete) data mahasiswa di memori menggunakan .NET SDK.

## Deskripsi Singkat
Program ini mengimplementasikan manipulasi data mahasiswa secara interaktif melalui antarmuka teks. Fitur yang disediakan meliputi penambahan data mahasiswa baru, penampilan seluruh daftar data, pembaruan atribut mahasiswa berdasarkan NRP, dan penghapusan data berdasarkan NRP.

## Struktur Berkas
- `Program.cs`: Berkas kode utama C# yang memuat class `Mahasiswa` dan fungsi CRUD (`TampilkanData`, `TambahData`, `UbahData`, `HapusData`).
- `Pertemuan-02-DotNet-Console-CRUD.csproj`: Berkas konfigurasi proyek .NET 10.0 Console.
- `screenshots/terminal_crud.png`: Tangkapan layar eksekusi program di terminal yang mendemonstrasikan seluruh alur CRUD.

## Cara Menjalankan
```bash
cd Pertemuan-02-DotNet-Console-CRUD
dotnet run
```

## Hasil Eksekusi
Tampilan output saat program dijalankan dan diuji melalui terminal:

![Hasil Eksekusi Terminal](./screenshots/terminal_crud.png)

## Dokumentasi Lengkap
Laporan lengkap mencakup arsitektur .NET Framework (komponen CLR dan BCL), analisis logika fungsi CRUD, dan hasil pengujian dapat diakses pada halaman Notion berikut:
👉 [Laporan Pertemuan 2 di Notion](https://app.notion.com/p/Pertemuan-2-NET-Framework-Latihan-Aplikasi-Console-CRUD-4009c0720c5a81e9b253db933f86e92b)
