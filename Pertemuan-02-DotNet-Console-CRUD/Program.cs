using System;
using System.Collections.Generic;

namespace DotNetConsoleCRUD
{
    // Model data mahasiswa
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
            // Koleksi mahasiswa di memori
            List<Mahasiswa> daftarMahasiswa = new List<Mahasiswa>();

            // Data awal
            daftarMahasiswa.Add(new Mahasiswa("5025241264", "Muhammad Hilman Azhar", "Teknik Informatika", "PBKK C"));
            daftarMahasiswa.Add(new Mahasiswa("5025241001", "Ahmad Fauzi", "Teknik Informatika", "PBKK C"));

            bool berjalan = true;

            while (berjalan)
            {
                Console.WriteLine("\n============================================");
                Console.WriteLine("    APLIKASI CONSOLE CRUD DATA MAHASISWA");
                Console.WriteLine("          PBKK KELAS C - PERTEMUAN 2");
                Console.WriteLine("============================================");
                Console.WriteLine("1. Lihat Data Mahasiswa");
                Console.WriteLine("2. Tambah Data Mahasiswa");
                Console.WriteLine("3. Ubah Data Mahasiswa (Update)");
                Console.WriteLine("4. Hapus Data Mahasiswa (Delete)");
                Console.WriteLine("5. Keluar");
                Console.Write("Pilih menu (1-5): ");

                string pilihan = Console.ReadLine() ?? "";

                switch (pilihan.Trim())
                {
                    case "1":
                        TampilkanData(daftarMahasiswa);
                        break;

                    case "2":
                        TambahData(daftarMahasiswa);
                        break;

                    case "3":
                        UbahData(daftarMahasiswa);
                        break;

                    case "4":
                        HapusData(daftarMahasiswa);
                        break;

                    case "5":
                        Console.WriteLine("\nTerima kasih telah menggunakan aplikasi ini.");
                        berjalan = false;
                        break;

                    default:
                        Console.WriteLine("\n>> Pilihan tidak valid! Masukkan angka 1 sampai 5.");
                        break;
                }
            }
        }

        // 1. READ: Menampilkan daftar mahasiswa
        static void TampilkanData(List<Mahasiswa> list)
        {
            Console.WriteLine("\n--- Daftar Mahasiswa ---");
            if (list.Count == 0)
            {
                Console.WriteLine("Belum ada data mahasiswa yang tersimpan.");
                return;
            }

            Console.WriteLine("-----------------------------------------------------------------------------");
            Console.WriteLine(string.Format("{0,-4} | {1,-12} | {2,-24} | {3,-18} | {4,-8}", "No", "NRP", "Nama", "Jurusan", "Kelas"));
            Console.WriteLine("-----------------------------------------------------------------------------");
            for (int i = 0; i < list.Count; i++)
            {
                var m = list[i];
                Console.WriteLine(string.Format("{0,-4} | {1,-12} | {2,-24} | {3,-18} | {4,-8}", i + 1, m.NRP, m.Nama, m.Jurusan, m.Kelas));
            }
            Console.WriteLine("-----------------------------------------------------------------------------");
            Console.WriteLine($"Total Mahasiswa: {list.Count}");
        }

        // 2. CREATE: Menambahkan mahasiswa baru
        static void TambahData(List<Mahasiswa> list)
        {
            Console.WriteLine("\n--- Tambah Data Mahasiswa ---");
            Console.Write("Masukkan NRP     : ");
            string nrp = Console.ReadLine() ?? "";

            // Cek apakah NRP sudah terdaftar
            foreach (var mhs in list)
            {
                if (mhs.NRP.Equals(nrp.Trim(), StringComparison.OrdinalIgnoreCase))
                {
                    Console.WriteLine($">> Gagal: Mahasiswa dengan NRP '{nrp}' sudah terdaftar!");
                    return;
                }
            }

            Console.Write("Masukkan Nama    : ");
            string nama = Console.ReadLine() ?? "";

            Console.Write("Masukkan Jurusan : ");
            string jurusan = Console.ReadLine() ?? "";

            Console.Write("Masukkan Kelas   : ");
            string kelas = Console.ReadLine() ?? "";

            list.Add(new Mahasiswa(nrp.Trim(), nama.Trim(), jurusan.Trim(), kelas.Trim()));
            Console.WriteLine(">> Data mahasiswa berhasil ditambahkan.");
        }

        // 3. UPDATE: Mengubah data mahasiswa berdasarkan NRP
        static void UbahData(List<Mahasiswa> list)
        {
            Console.WriteLine("\n--- Ubah Data Mahasiswa ---");
            Console.Write("Masukkan NRP yang akan diubah: ");
            string targetNrp = Console.ReadLine() ?? "";

            Mahasiswa? target = null;
            foreach (var mhs in list)
            {
                if (mhs.NRP.Equals(targetNrp.Trim(), StringComparison.OrdinalIgnoreCase))
                {
                    target = mhs;
                    break;
                }
            }

            if (target == null)
            {
                Console.WriteLine($">> Mahasiswa dengan NRP '{targetNrp}' tidak ditemukan.");
                return;
            }

            Console.WriteLine($"\nData ditemukan: {target.NRP} - {target.Nama} ({target.Jurusan}, {target.Kelas})");
            Console.WriteLine("(Kosongkan / tekan Enter jika data tidak ingin diubah)");

            Console.Write($"Nama baru [{target.Nama}]: ");
            string namaBaru = Console.ReadLine() ?? "";
            if (!string.IsNullOrWhiteSpace(namaBaru))
            {
                target.Nama = namaBaru.Trim();
            }

            Console.Write($"Jurusan baru [{target.Jurusan}]: ");
            string jurusanBaru = Console.ReadLine() ?? "";
            if (!string.IsNullOrWhiteSpace(jurusanBaru))
            {
                target.Jurusan = jurusanBaru.Trim();
            }

            Console.Write($"Kelas baru [{target.Kelas}]: ");
            string kelasBaru = Console.ReadLine() ?? "";
            if (!string.IsNullOrWhiteSpace(kelasBaru))
            {
                target.Kelas = kelasBaru.Trim();
            }

            Console.WriteLine(">> Data mahasiswa berhasil diperbarui.");
        }

        // 4. DELETE: Menghapus data mahasiswa berdasarkan NRP
        static void HapusData(List<Mahasiswa> list)
        {
            Console.WriteLine("\n--- Hapus Data Mahasiswa ---");
            Console.Write("Masukkan NRP yang akan dihapus: ");
            string targetNrp = Console.ReadLine() ?? "";

            int indexHapus = -1;
            for (int i = 0; i < list.Count; i++)
            {
                if (list[i].NRP.Equals(targetNrp.Trim(), StringComparison.OrdinalIgnoreCase))
                {
                    indexHapus = i;
                    break;
                }
            }

            if (indexHapus == -1)
            {
                Console.WriteLine($">> Mahasiswa dengan NRP '{targetNrp}' tidak ditemukan.");
                return;
            }

            var dihapus = list[indexHapus];
            list.RemoveAt(indexHapus);
            Console.WriteLine($">> Mahasiswa '{dihapus.Nama}' (NRP: {dihapus.NRP}) berhasil dihapus dari daftar.");
        }
    }
}
