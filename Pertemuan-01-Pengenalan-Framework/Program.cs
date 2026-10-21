using System;
using System.Collections.Generic;

namespace ManajemenMahasiswa
{
    // Class model data mahasiswa
    class Mahasiswa
    {
        public string NRP { get; set; }
        public string Nama { get; set; }
        public string Jurusan { get; set; }
        public string Kelas { get; set; }

        public Mahasiswa(string nrp, string nama, string jurusan, string kelas)
        {
            NRP = nrp;
            Nama = nama;
            Jurusan = jurusan;
            Kelas = kelas;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // Inisialisasi daftar mahasiswa menggunakan List di memori
            List<Mahasiswa> daftarMahasiswa = new List<Mahasiswa>();

            // Data awal (dummy data)
            daftarMahasiswa.Add(new Mahasiswa("5025241264", "Muhammad Hilman Azhar", "Teknik Informatika", "PBKK C"));
            daftarMahasiswa.Add(new Mahasiswa("5025241001", "Ahmad Fauzi", "Teknik Informatika", "PBKK C"));

            bool berjalan = true;

            while (berjalan)
            {
                Console.WriteLine("\n============================================");
                Console.WriteLine("    APLIKASI MANAJEMEN DATA MAHASISWA");
                Console.WriteLine("          PBKK KELAS C - PERTEMUAN 1");
                Console.WriteLine("============================================");
                Console.WriteLine("1. Tambah Data Mahasiswa");
                Console.WriteLine("2. Tampilkan Daftar Mahasiswa");
                Console.WriteLine("3. Cari Mahasiswa Berdasarkan NRP");
                Console.WriteLine("4. Keluar");
                Console.Write("Pilih menu (1-4): ");

                string pilihan = Console.ReadLine() ?? "";

                switch (pilihan.Trim())
                {
                    case "1":
                        Console.WriteLine("\n--- Tambah Data Mahasiswa ---");
                        Console.Write("Masukkan NRP     : ");
                        string nrp = Console.ReadLine() ?? "";

                        Console.Write("Masukkan Nama    : ");
                        string nama = Console.ReadLine() ?? "";

                        Console.Write("Masukkan Jurusan : ");
                        string jurusan = Console.ReadLine() ?? "";

                        Console.Write("Masukkan Kelas   : ");
                        string kelas = Console.ReadLine() ?? "";

                        daftarMahasiswa.Add(new Mahasiswa(nrp, nama, jurusan, kelas));
                        Console.WriteLine(">> Data mahasiswa berhasil ditambahkan!");
                        break;

                    case "2":
                        Console.WriteLine("\n--- Daftar Mahasiswa ---");
                        if (daftarMahasiswa.Count == 0)
                        {
                            Console.WriteLine("Belum ada data mahasiswa yang tersimpan.");
                        }
                        else
                        {
                            int nomor = 1;
                            Console.WriteLine("-----------------------------------------------------------------------------");
                            Console.WriteLine(string.Format("{0,-4} | {1,-12} | {2,-24} | {3,-18} | {4,-8}", "No", "NRP", "Nama", "Jurusan", "Kelas"));
                            Console.WriteLine("-----------------------------------------------------------------------------");
                            foreach (var mhs in daftarMahasiswa)
                            {
                                Console.WriteLine(string.Format("{0,-4} | {1,-12} | {2,-24} | {3,-18} | {4,-8}", nomor, mhs.NRP, mhs.Nama, mhs.Jurusan, mhs.Kelas));
                                nomor++;
                            }
                            Console.WriteLine("-----------------------------------------------------------------------------");
                            Console.WriteLine($"Total Mahasiswa: {daftarMahasiswa.Count}");
                        }
                        break;

                    case "3":
                        Console.WriteLine("\n--- Cari Mahasiswa Berdasarkan NRP ---");
                        Console.Write("Masukkan NRP yang dicari: ");
                        string cariNrp = Console.ReadLine() ?? "";

                        bool ditemukan = false;
                        foreach (var mhs in daftarMahasiswa)
                        {
                            if (mhs.NRP.Equals(cariNrp.Trim(), StringComparison.OrdinalIgnoreCase))
                            {
                                Console.WriteLine("\n>> Data Mahasiswa Ditemukan:");
                                Console.WriteLine($"NRP     : {mhs.NRP}");
                                Console.WriteLine($"Nama    : {mhs.Nama}");
                                Console.WriteLine($"Jurusan : {mhs.Jurusan}");
                                Console.WriteLine($"Kelas   : {mhs.Kelas}");
                                ditemukan = true;
                                break;
                            }
                        }

                        if (!ditemukan)
                        {
                            Console.WriteLine($">> Mahasiswa dengan NRP '{cariNrp}' tidak ditemukan.");
                        }
                        break;

                    case "4":
                        Console.WriteLine("\nTerima kasih telah menggunakan aplikasi ini. Sampai jumpa!");
                        berjalan = false;
                        break;

                    default:
                        Console.WriteLine("\n>> Pilihan tidak valid! Silakan masukkan angka 1-4.");
                        break;
                }
            }
        }
    }
}
