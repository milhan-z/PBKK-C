using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Imaging;

namespace Pertemuan_04_WPF_Student_Registration;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        dpTanggalLahir.SelectedDate = new DateTime(2004, 8, 17);

        Loaded += MainWindow_Loaded;
    }

    private void MainWindow_Loaded(object sender, RoutedEventArgs e)
    {
        string[] args = Environment.GetCommandLineArgs();
        if (args.Contains("--screenshot"))
        {
            // Isi otomatis data contoh untuk bukti screenshot eksekusi
            txtNrp.Text = "5025241264";
            txtNama.Text = "Muhammad Hilman Azhar";
            txtEmail.Text = "5025241264@student.its.ac.id";
            rbLaki.IsChecked = true;
            cmbProdi.SelectedIndex = 0; // S1 Teknik Informatika
            cmbJalur.SelectedIndex = 0; // SNBP (Prestasi)
            dpTanggalLahir.SelectedDate = new DateTime(2004, 8, 17);
            chkWeb.IsChecked = true;
            chkMobile.IsChecked = false;
            chkAI.IsChecked = true;
            chkCyber.IsChecked = false;
            txtAlamat.Text = "Jl. Teknik Kimia, Kampus Sukolilo ITS, Keputih, Kec. Sukolilo, Surabaya, Jawa Timur 60111";

            // Jalankan simpan tanpa popup MessageBox
            ProsesSimpan(isSilent: true);

            // Tunggu layout ter-render sempurna
            Dispatcher.InvokeAsync(async () =>
            {
                await System.Threading.Tasks.Task.Delay(500);
                AmbilScreenshot();
                Application.Current.Shutdown();
            }, System.Windows.Threading.DispatcherPriority.ApplicationIdle);
        }
    }

    private void btnSimpan_Click(object sender, RoutedEventArgs e)
    {
        ProsesSimpan(isSilent: false);
    }

    private void ProsesSimpan(bool isSilent)
    {
        string nrp = txtNrp.Text.Trim();
        string nama = txtNama.Text.Trim();
        string email = txtEmail.Text.Trim();
        string alamat = txtAlamat.Text.Trim();

        // 1. Validasi NRP
        if (string.IsNullOrWhiteSpace(nrp) || !long.TryParse(nrp, out _))
        {
            if (!isSilent)
            {
                MessageBox.Show("NRP wajib diisi dan harus berupa angka numerik!", "Validasi Input", MessageBoxButton.OK, MessageBoxImage.Warning);
                txtNrp.Focus();
            }
            return;
        }

        // 2. Validasi Nama Lengkap
        if (string.IsNullOrWhiteSpace(nama) || nama.Length < 3)
        {
            if (!isSilent)
            {
                MessageBox.Show("Nama lengkap wajib diisi minimal 3 karakter!", "Validasi Input", MessageBoxButton.OK, MessageBoxImage.Warning);
                txtNama.Focus();
            }
            return;
        }

        // 3. Validasi Email
        if (string.IsNullOrWhiteSpace(email) || !email.Contains('@') || !email.Contains('.'))
        {
            if (!isSilent)
            {
                MessageBox.Show("Alamat email tidak valid! Pastikan menyertakan karakter '@' dan domain.", "Validasi Input", MessageBoxButton.OK, MessageBoxImage.Warning);
                txtEmail.Focus();
            }
            return;
        }

        // 4. Validasi Tanggal Lahir
        if (!dpTanggalLahir.SelectedDate.HasValue)
        {
            if (!isSilent)
            {
                MessageBox.Show("Tanggal lahir belum dipilih!", "Validasi Input", MessageBoxButton.OK, MessageBoxImage.Warning);
                dpTanggalLahir.Focus();
            }
            return;
        }

        // 5. Validasi Alamat
        if (string.IsNullOrWhiteSpace(alamat))
        {
            if (!isSilent)
            {
                MessageBox.Show("Alamat domisili wajib diisi!", "Validasi Input", MessageBoxButton.OK, MessageBoxImage.Warning);
                txtAlamat.Focus();
            }
            return;
        }

        // Ambil Data Lainnya
        string jenisKelamin = (rbLaki.IsChecked == true) ? "Laki-laki" : "Perempuan";
        string prodi = (cmbProdi.SelectedItem is ComboBoxItem itemProdi) ? itemProdi.Content.ToString() ?? "" : "";
        string jalur = (cmbJalur.SelectedItem is ComboBoxItem itemJalur) ? itemJalur.Content.ToString() ?? "" : "";
        DateTime tglLahir = dpTanggalLahir.SelectedDate.Value;

        // Kumpulkan Minat
        List<string> daftarMinat = new List<string>();
        if (chkWeb.IsChecked == true) daftarMinat.Add("Web Development");
        if (chkMobile.IsChecked == true) daftarMinat.Add("Mobile App");
        if (chkAI.IsChecked == true) daftarMinat.Add("AI & Data Science");
        if (chkCyber.IsChecked == true) daftarMinat.Add("Cyber Security");
        string minat = daftarMinat.Count > 0 ? string.Join(", ", daftarMinat) : "Tidak ada";

        // Perbarui Pratinjau
        lblPreviewNrp.Text = nrp;
        lblPreviewNama.Text = nama;
        lblPreviewEmail.Text = email;
        lblPreviewJK.Text = jenisKelamin;
        lblPreviewProdi.Text = prodi;
        lblPreviewJalur.Text = jalur;
        lblPreviewTglLahir.Text = tglLahir.ToString("dd MMMM yyyy");
        lblPreviewMinat.Text = minat;
        lblPreviewAlamat.Text = alamat;
        lblWaktuRegistrasi.Text = $"Waktu Registrasi: {DateTime.Now:dd/MM/yyyy HH:mm:ss} WIB";

        // Ubah Badge Status menjadi Berhasil (Hijau)
        badgeStatus.Background = new SolidColorBrush(Color.FromRgb(240, 253, 244));
        badgeStatus.BorderBrush = new SolidColorBrush(Color.FromRgb(134, 239, 172));
        txtStatus.Foreground = new SolidColorBrush(Color.FromRgb(22, 101, 52));
        txtStatus.Text = "● Status: Berhasil Terdaftar (Aktif)";

        if (!isSilent)
        {
            MessageBox.Show($"Pendaftaran atas nama {nama} (NRP: {nrp}) berhasil disimpan!", "Pendaftaran Sukses", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }

    private void btnReset_Click(object sender, RoutedEventArgs e)
    {
        txtNrp.Text = "";
        txtNama.Text = "";
        txtEmail.Text = "";
        rbLaki.IsChecked = true;
        cmbProdi.SelectedIndex = 0;
        cmbJalur.SelectedIndex = 0;
        dpTanggalLahir.SelectedDate = null;
        chkWeb.IsChecked = false;
        chkMobile.IsChecked = false;
        chkAI.IsChecked = false;
        chkCyber.IsChecked = false;
        txtAlamat.Text = "";

        // Reset Pratinjau
        lblPreviewNrp.Text = "-";
        lblPreviewNama.Text = "-";
        lblPreviewEmail.Text = "-";
        lblPreviewJK.Text = "-";
        lblPreviewProdi.Text = "-";
        lblPreviewJalur.Text = "-";
        lblPreviewTglLahir.Text = "-";
        lblPreviewMinat.Text = "-";
        lblPreviewAlamat.Text = "-";
        lblWaktuRegistrasi.Text = "Waktu Pendaftaran: -";

        // Reset Badge Status
        badgeStatus.Background = new SolidColorBrush(Color.FromRgb(254, 242, 242));
        badgeStatus.BorderBrush = new SolidColorBrush(Color.FromRgb(252, 165, 165));
        txtStatus.Foreground = new SolidColorBrush(Color.FromRgb(220, 38, 38));
        txtStatus.Text = "● Status: Belum Didaftarkan";

        txtNrp.Focus();
    }

    private void AmbilScreenshot()
    {
        try
        {
            int width = (int)ActualWidth;
            int height = (int)ActualHeight;

            if (width <= 0) width = 920;
            if (height <= 0) height = 780;

            RenderTargetBitmap renderBitmap = new RenderTargetBitmap(
                width, height, 96, 96, PixelFormats.Pbgra32);
            renderBitmap.Render(this);

            PngBitmapEncoder encoder = new PngBitmapEncoder();
            encoder.Frames.Add(BitmapFrame.Create(renderBitmap));

            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            // Ambil direktori proyek
            string dir = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", "screenshots"));
            Directory.CreateDirectory(dir);

            string file = Path.Combine(dir, "registration_gui.png");
            using (FileStream fs = new FileStream(file, FileMode.Create))
            {
                encoder.Save(fs);
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error screenshot: {ex.Message}");
        }
    }
}
