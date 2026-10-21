param(
    [Parameter(Mandatory=$true)]
    [string]$Folder,
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    [string]$Description = ""
)

# Ambil token GitHub secara dinamis dari Git Credential Manager lokal
$credRaw = "protocol=https`nhost=github.com" | git credential fill
$token = ""
$username = "milhan-z"

foreach ($line in ($credRaw -split "`r?`n")) {
    if ($line.StartsWith("password=")) {
        $token = $line.Substring(9).Trim()
    }
    if ($line.StartsWith("username=")) {
        $username = $line.Substring(9).Trim()
    }
}

$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github+json"
    "User-Agent" = "AntigravityIDE"
}

# 1. Cek atau Buat Repository di GitHub
Write-Host "Memeriksa repositori $RepoName di GitHub..."
try {
    $existing = Invoke-RestMethod -Uri "https://api.github.com/repos/$username/$RepoName" -Method Get -Headers $headers -ErrorAction Stop
    Write-Host "Repositori $RepoName sudah ada: $($existing.html_url)"
} catch {
    Write-Host "Repositori belum ada, membuat repositori publik baru: $RepoName..."
    $body = @{
        name = $RepoName
        description = $Description
        private = $false
    } | ConvertTo-Json

    $newRepo = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "Repositori publik berhasil dibuat: $($newRepo.html_url)"
}

# 2. Setup Git di dalam Folder Pertemuan
$folderPath = Resolve-Path $Folder
Write-Host "Menyiapkan repositori git lokal di $folderPath..."

$localGitignore = Join-Path $folderPath ".gitignore"
if (!(Test-Path $localGitignore)) {
    @"
[Bb]in/
[Oo]bj/
.vs/
.vscode/
*.user
"@ | Set-Content -Path $localGitignore -Encoding utf8
}

Push-Location $folderPath
try {
    if (!(Test-Path ".git")) {
        git init -b main
    }

    $remoteUrl = "https://github.com/$username/$RepoName.git"
    $remotes = git remote
    if ($remotes -contains "origin") {
        git remote set-url origin $remoteUrl
    } else {
        git remote add origin $remoteUrl
    }

    git add .
    git commit -m "feat: inisialisasi source code dan bukti eksekusi $RepoName"
    
    Write-Host "Melakukan push ke $remoteUrl..."
    git push -u origin main --force
    Write-Host "Push berhasil untuk $RepoName!"
} finally {
    Pop-Location
}
