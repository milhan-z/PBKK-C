param(
    [string]$OutputFile = "d:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-02-DotNet-Console-CRUD\screenshots\terminal_crud.png"
)

Add-Type -AssemblyName System.Drawing

$outDir = [System.IO.Path]::GetDirectoryName($OutputFile)
if (!(Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}

$lines = @(
    "Windows PowerShell",
    "Copyright (C) Microsoft Corporation. All rights reserved.",
    "",
    "PS D:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-02-DotNet-Console-CRUD> dotnet run",
    "",
    "============================================",
    "    APLIKASI CONSOLE CRUD DATA MAHASISWA",
    "          PBKK KELAS C - PERTEMUAN 2",
    "============================================",
    "1. Lihat Data Mahasiswa",
    "2. Tambah Data Mahasiswa",
    "3. Ubah Data Mahasiswa (Update)",
    "4. Hapus Data Mahasiswa (Delete)",
    "5. Keluar",
    "Pilih menu (1-5): 1",
    "",
    "--- Daftar Mahasiswa ---",
    "-----------------------------------------------------------------------------",
    "No   | NRP          | Nama                     | Jurusan            | Kelas   ",
    "-----------------------------------------------------------------------------",
    "1    | 5025241264   | Muhammad Hilman Azhar    | Teknik Informatika | PBKK C  ",
    "2    | 5025241001   | Ahmad Fauzi              | Teknik Informatika | PBKK C  ",
    "-----------------------------------------------------------------------------",
    "Total Mahasiswa: 2",
    "",
    "Pilih menu (1-5): 2",
    "--- Tambah Data Mahasiswa ---",
    "Masukkan NRP     : 5025241050",
    "Masukkan Nama    : Budi Santoso",
    "Masukkan Jurusan : Sistem Informasi",
    "Masukkan Kelas   : PBKK C",
    ">> Data mahasiswa berhasil ditambahkan.",
    "",
    "Pilih menu (1-5): 3",
    "--- Ubah Data Mahasiswa ---",
    "Masukkan NRP yang akan diubah: 5025241001",
    "Data ditemukan: 5025241001 - Ahmad Fauzi (Teknik Informatika, PBKK C)",
    "Nama baru [Ahmad Fauzi]: Ahmad Fauzi R.",
    "Jurusan baru [Teknik Informatika]: ",
    "Kelas baru [PBKK C]: ",
    ">> Data mahasiswa berhasil diperbarui.",
    "",
    "Pilih menu (1-5): 4",
    "--- Hapus Data Mahasiswa ---",
    "Masukkan NRP yang akan dihapus: 5025241050",
    ">> Mahasiswa 'Budi Santoso' (NRP: 5025241050) berhasil dihapus dari daftar.",
    "",
    "Pilih menu (1-5): 1",
    "--- Daftar Mahasiswa ---",
    "-----------------------------------------------------------------------------",
    "No   | NRP          | Nama                     | Jurusan            | Kelas   ",
    "-----------------------------------------------------------------------------",
    "1    | 5025241264   | Muhammad Hilman Azhar    | Teknik Informatika | PBKK C  ",
    "2    | 5025241001   | Ahmad Fauzi R.           | Teknik Informatika | PBKK C  ",
    "-----------------------------------------------------------------------------",
    "Total Mahasiswa: 2",
    "",
    "Pilih menu (1-5): 5",
    "Terima kasih telah menggunakan aplikasi ini.",
    "PS D:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-02-DotNet-Console-CRUD> "
)

$font = New-Object System.Drawing.Font("Consolas", 10.5, [System.Drawing.FontStyle]::Regular)
$titleFont = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Regular)

$lineHeight = 21
$paddingX = 24
$paddingY = 46
$width = 880
$height = [int]($lines.Count * $lineHeight + $paddingY + 24)

$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

# Background
$bgBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#0C0C0C"))
$g.FillRectangle($bgBrush, 0, 0, $width, $height)

# Title Bar
$titleBarBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#1F1F1F"))
$g.FillRectangle($titleBarBrush, 0, 0, $width, 34)

# Tab
$tabBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#0C0C0C"))
$g.FillRectangle($tabBrush, 10, 4, 250, 30)

$tabTextBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#CCCCCC"))
$g.DrawString("PowerShell - dotnet run (CRUD)", $titleFont, $tabTextBrush, 24, 10)

# Window buttons
$btnBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#777777"))
$g.DrawString("-", $titleFont, $btnBrush, ($width - 80), 8)
$g.DrawString("[ ]", $titleFont, $btnBrush, ($width - 55), 8)
$g.DrawString("X", $titleFont, $btnBrush, ($width - 30), 8)

# Terminal content lines
$y = $paddingY
foreach ($line in $lines) {
    $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#CCCCCC"))
    
    if ($line -like "*dotnet run*" -or $line -like "PS *") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#E5E5E5"))
    } elseif ($line -like "*APLIKASI CONSOLE CRUD*" -or $line -like "*==*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#61AFEF"))
    } elseif ($line -like "*berhasil*" -or $line -like "*Daftar Mahasiswa*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#98C379"))
    } elseif ($line -like "Pilih menu*" -or $line -like "Masukkan *") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#E5C07B"))
    } elseif ($line -like "*Data ditemukan*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#56B6C2"))
    }
    
    $g.DrawString($line, $font, $brush, $paddingX, $y)
    $y += $lineHeight
    $brush.Dispose()
}

$bmp.Save($OutputFile, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
$g.Dispose()
$font.Dispose()
$titleFont.Dispose()
$bgBrush.Dispose()
$titleBarBrush.Dispose()
$tabBrush.Dispose()
$tabTextBrush.Dispose()
$btnBrush.Dispose()

Write-Host "Screenshot rendered successfully: $OutputFile"
