#requires -Version 5.1
<#
.SYNOPSIS
  Interaktiv meny för Buildr v2 — peka här eller kör: .\v2\run.ps1 från repo-roten.
#>

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

function Show-Header {
    Write-Host ""
    Write-Host "=== Buildr v2 — valmeny ===" -ForegroundColor Cyan
    Write-Host "Repo: $RepoRoot"
    Write-Host ""
}

function Invoke-PreflightValidate {
    $staging = Read-Host "Staging-katalog (t.ex. v2\.buildr\preflight\my-proj eller full sökväg)"
    if ([string]::IsNullOrWhiteSpace($staging)) {
        Write-Host "Avbrutet." -ForegroundColor Yellow
        return
    }
    $full = $staging
    if (-not [System.IO.Path]::IsPathRooted($staging)) {
        $rel = $staging.TrimStart([char[]]@([char]0x2F, [char]0x5C))
        $full = Join-Path $RepoRoot $rel
    }
    Write-Host "Kör: python -m engines.preflight_validate `"$full`"" -ForegroundColor Gray
    & python -m engines.preflight_validate $full
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Exit code: $LASTEXITCODE" -ForegroundColor Red
    }
}

function Copy-WorkspaceArchitectSkill {
    $src = Join-Path $RepoRoot "v2\skills\buildr-workspace-architect"
    $dst = Join-Path $RepoRoot "skills\buildr-workspace-architect"
    if (-not (Test-Path $src)) {
        Write-Host "Saknas: $src" -ForegroundColor Red
        return
    }
    if (Test-Path $dst) {
        $ok = Read-Host "Mappen finns redan: $dst — skriv OVERWRITE för att ersätta"
        if ($ok -ne 'OVERWRITE') {
            Write-Host "Avbrutet." -ForegroundColor Yellow
            return
        }
        Remove-Item -Recurse -Force $dst
    }
    Copy-Item -Recurse -Force $src $dst
    Write-Host "Kopierat till: $dst" -ForegroundColor Green
}

function Open-InEditor {
    param([string]$RelativePath)
    $p = Join-Path $RepoRoot $RelativePath
    if (-not (Test-Path $p)) {
        Write-Host "Saknas: $p" -ForegroundColor Red
        return
    }
    if (Get-Command code -ErrorAction SilentlyContinue) {
        & code $p
    }
    elseif (Get-Command cursor -ErrorAction SilentlyContinue) {
        & cursor $p
    }
    else {
        notepad $p
    }
}

Show-Header

$running = $true
while ($running) {
    Write-Host " 1) Öppna v2/ENTRY.md (nav)" -ForegroundColor White
    Write-Host " 2) Öppna docs/v2-overview.md" -ForegroundColor White
    Write-Host " 3) Öppna docs/BUILDR-purpose-and-layers.md" -ForegroundColor White
    Write-Host " 4) Öppna v2/start.md (författa v2)" -ForegroundColor White
    Write-Host " 5) Öppna v2/improve.md (backlog)" -ForegroundColor White
    Write-Host " 6) Öppna v2/prompts/buildr-advanced-operator.md" -ForegroundColor White
    Write-Host " 7) Kopiera buildr-workspace-architect -> skills/" -ForegroundColor White
    Write-Host " 8) Kör preflight_validate (staging-katalog)" -ForegroundColor White
    Write-Host " 9) pytest: bara test_preflight_validate" -ForegroundColor White
    Write-Host "10) pytest: hela suite" -ForegroundColor White
    Write-Host " 0) Avsluta" -ForegroundColor DarkGray
    Write-Host ""

    $choice = Read-Host "Välj nummer"

    switch ($choice) {
        '1'  { Open-InEditor "v2\ENTRY.md" }
        '2'  { Open-InEditor "docs\v2-overview.md" }
        '3'  { Open-InEditor "docs\BUILDR-purpose-and-layers.md" }
        '4'  { Open-InEditor "v2\start.md" }
        '5'  { Open-InEditor "v2\improve.md" }
        '6'  { Open-InEditor "v2\prompts\buildr-advanced-operator.md" }
        '7'  { Copy-WorkspaceArchitectSkill }
        '8'  { Invoke-PreflightValidate }
        '9'  {
                Write-Host "pytest tests\test_preflight_validate.py" -ForegroundColor Gray
                & pytest tests\test_preflight_validate.py
             }
        '10' {
                Write-Host "pytest" -ForegroundColor Gray
                & pytest
             }
        '0'  { $script:running = $false }
        default { Write-Host "Ogiltigt val. Försök igen." -ForegroundColor Yellow }
    }

    Write-Host ""
}

Write-Host "Hej då." -ForegroundColor DarkGray
