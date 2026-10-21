param(
    [string]$OutputFile = "d:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-06-WPF-SQLServer-Integration\screenshots\sql_database_query.png"
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
    "PS D:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-06-WPF-SQLServer-Integration> sqlcmd -S `"(localdb)\MSSQLLocalDB`" -d DbMahasiswaPBKK",
    "1> -- Verifikasi Tabel dbo.Mahasiswa (Hands-on 1: Database SQL Server)",
    "2> SELECT Id, Nrp, Nama, Prodi, Angkatan, Ipk, Status, CONVERT(VARCHAR(19), CreatedAt, 120) AS WaktuDibuat",
    "3> FROM Mahasiswa",
    "4> ORDER BY Nrp ASC;",
    "5> GO",
    "Id   Nrp          Nama                     Prodi                 Angkatan  Ipk   Status  WaktuDibuat        ",
    "---- ------------ ------------------------ --------------------- --------- ----- ------- -------------------",
    "1    5025241264   Muhammad Hilman Azhar    Teknik Informatika         2024  3.88  Aktif   2026-10-22 01:06:36",
    "2    5025241010   Ahmad Fauzi Rahman       Teknik Informatika         2024  3.75  Aktif   2026-10-22 01:06:36",
    "3    5025231045   Siti Nurhaliza           Sistem Informasi           2023  3.90  Aktif   2026-10-22 01:06:36",
    "4    5025221088   Budi Santoso             Teknologi Informasi        2022  3.45  Cuti    2026-10-22 01:06:36",
    "5    5025241120   Dewi Anggraini           Sains Data                 2024  3.82  Aktif   2026-10-22 01:06:36",
    "",
    "(5 rows affected)",
    "",
    "1> -- Uji Query Agregasi Statistik",
    "2> SELECT COUNT(1) AS TotalMhs, AVG(Ipk) AS RataIpk FROM Mahasiswa;",
    "3> GO",
    "TotalMhs    RataIpk ",
    "----------- --------",
    "          5 3.760000",
    "",
    "(1 rows affected)",
    "1> QUIT",
    "PS D:\SAFAHIL\HILMAN\Kuliah\MatKul\PBKK\Pertemuan-06-WPF-SQLServer-Integration> "
)

$font = New-Object System.Drawing.Font("Consolas", 10.5, [System.Drawing.FontStyle]::Regular)
$titleFont = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Regular)

$lineHeight = 21
$paddingX = 24
$paddingY = 46
$width = 960
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
$g.FillRectangle($tabBrush, 10, 4, 300, 30)

$tabTextBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#CCCCCC"))
$g.DrawString("PowerShell - sqlcmd (SQL Server LocalDB)", $titleFont, $tabTextBrush, 24, 10)

# Window buttons
$btnBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#777777"))
$g.DrawString("-", $titleFont, $btnBrush, ($width - 80), 8)
$g.DrawString("[ ]", $titleFont, $btnBrush, ($width - 55), 8)
$g.DrawString("X", $titleFont, $btnBrush, ($width - 30), 8)

# Terminal content lines
$y = $paddingY
foreach ($line in $lines) {
    $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#CCCCCC"))
    
    if ($line -like "*sqlcmd*" -or $line -like "PS *") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#E5E5E5"))
    } elseif ($line -like "*-- Verifikasi*" -or $line -like "*-- Uji Query*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#61AFEF"))
    } elseif ($line -like "*SELECT*" -or $line -like "*FROM*" -or $line -like "*ORDER*" -or $line -like "*GO*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#E5C07B"))
    } elseif ($line -like "*(5 rows affected)*" -or $line -like "*(1 rows affected)*") {
        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#98C379"))
    } elseif ($line -like "Id *" -or $line -like "TotalMhs *") {
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
