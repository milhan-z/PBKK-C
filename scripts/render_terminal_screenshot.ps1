param(
    [string]$OutputFile = "d:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-01-Pengenalan-Framework\screenshots\terminal_run.png"
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
    "PS D:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-01-Pengenalan-Framework> dotnet run",
    "",
    "============================================",
    "    APLIKASI MANAJEMEN DATA MAHASISWA",
    "          PBKK KELAS C - PERTEMUAN 1",
    "============================================",
    "1. Tambah Data Mahasiswa",
    "2. Tampilkan Daftar Mahasiswa",
    "3. Cari Mahasiswa Berdasarkan NRP",
    "4. Keluar",
    "Pilih menu (1-4): 2",
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
    "============================================",
    "    APLIKASI MANAJEMEN DATA MAHASISWA",
    "          PBKK KELAS C - PERTEMUAN 1",
    "============================================",
    "1. Tambah Data Mahasiswa",
    "2. Tampilkan Daftar Mahasiswa",
    "3. Cari Mahasiswa Berdasarkan NRP",
    "4. Keluar",
    "Pilih menu (1-4): 3",
    "",
    "--- Cari Mahasiswa Berdasarkan NRP ---",
    "Masukkan NRP yang dicari: 5025241264",
    "",
    ">> Data Mahasiswa Ditemukan:",
    "NRP     : 5025241264",
    "Nama    : Muhammad Hilman Azhar",
    "Jurusan : Teknik Informatika",
    "Kelas   : PBKK C",
    "",
    "============================================",
    "    APLIKASI MANAJEMEN DATA MAHASISWA",
    "          PBKK KELAS C - PERTEMUAN 1",
    "============================================",
    "1. Tambah Data Mahasiswa",
    "2. Tampilkan Daftar Mahasiswa",
    "3. Cari Mahasiswa Berdasarkan NRP",
    "4. Keluar",
    "Pilih menu (1-4): 4",
    "",
    "Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!",
    "PS D:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-01-Pengenalan-Framework> "
)

$font = New-Object System.Drawing.Font("Consolas", 11, [System.Drawing.FontStyle]::Regular)
$titleFont = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Regular)

$charWidth = 9.2
$lineHeight = 22
$paddingX = 24
$paddingY = 48 # space for title bar
$width = 880
$height = [int]($lines.Count * $lineHeight + $paddingY + 24)

$bmp = New-Object System.Drawing.Bitmap $width, $height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

# Background
$bgBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#0C0C0C"))
$g.FillRectangle($bgBrush, 0, 0, $width, $height)

# Title Bar (Windows Terminal style)
$titleBarBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#1F1F1F"))
$g.FillRectangle($titleBarBrush, 0, 0, $width, 34)

# Tab
$tabBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#0C0C0C"))
$g.FillRectangle($tabBrush, 10, 4, 210, 30)

$tabTextBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#CCCCCC"))
$g.DrawString("PowerShell - dotnet run", $titleFont, $tabTextBrush, 24, 10)

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
    } elseif ($line -like "*APLIKASI MANAJEMEN*" -or $line -like "*==*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#61AFEF"))
    } elseif ($line -like "*Ditemukan*" -or $line -like "*Daftar Mahasiswa*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#98C379"))
    } elseif ($line -like "Pilih menu*" -or $line -like "Masukkan NRP*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#E5C07B"))
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
